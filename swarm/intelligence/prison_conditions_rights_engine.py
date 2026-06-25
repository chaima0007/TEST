from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#64748b"


@dataclass
class PrisonConditionsRightsEntity:
    entity_id: str
    name: str
    country: str
    overcrowding_severity_score: float
    torture_ill_treatment_score: float
    healthcare_denial_score: float
    pretrial_detention_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_conditions_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.overcrowding_severity_score * 0.30
            + self.torture_ill_treatment_score * 0.25
            + self.healthcare_denial_score * 0.25
            + self.pretrial_detention_score * 0.20,
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
        self.estimated_prison_conditions_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PrisonConditionsRightsEngineResult:
    agent: str = "Prison Conditions Rights Engine Agent"
    domain: str = "prison_conditions_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_prison_conditions_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonConditionsRightsEntity] = field(default_factory=list)


def run_prison_conditions_rights_engine() -> PrisonConditionsRightsEngineResult:
    entities = [
        PrisonConditionsRightsEntity(
            entity_id="PCR-001",
            name="El Salvador",
            country="El Salvador",
            overcrowding_severity_score=99.0,
            torture_ill_treatment_score=96.0,
            healthcare_denial_score=97.0,
            pretrial_detention_score=95.0,
            primary_pattern="cecot_megaprison_world_record_incarceration",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-002",
            name="Venezuela",
            country="Venezuela",
            overcrowding_severity_score=94.0,
            torture_ill_treatment_score=92.0,
            healthcare_denial_score=89.0,
            pretrial_detention_score=90.0,
            primary_pattern="sebin_torture_400pct_overcrowding",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-003",
            name="Philippines",
            country="Philippines",
            overcrowding_severity_score=88.0,
            torture_ill_treatment_score=84.0,
            healthcare_denial_score=83.0,
            pretrial_detention_score=87.0,
            primary_pattern="war_on_drugs_500pct_capacity",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-004",
            name="Libye",
            country="Libye",
            overcrowding_severity_score=80.0,
            torture_ill_treatment_score=82.0,
            healthcare_denial_score=77.0,
            pretrial_detention_score=79.0,
            primary_pattern="informal_detention_centers_migrant_abuse",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-005",
            name="États-Unis",
            country="USA",
            overcrowding_severity_score=57.0,
            torture_ill_treatment_score=55.0,
            healthcare_denial_score=58.0,
            pretrial_detention_score=52.0,
            primary_pattern="solitary_confinement_private_healthcare",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-006",
            name="France",
            country="France",
            overcrowding_severity_score=49.0,
            torture_ill_treatment_score=44.0,
            healthcare_denial_score=46.0,
            pretrial_detention_score=47.0,
            primary_pattern="baumettes_145pct_occupation_cedh_condemned",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-007",
            name="Allemagne",
            country="Allemagne",
            overcrowding_severity_score=30.0,
            torture_ill_treatment_score=28.0,
            healthcare_denial_score=29.0,
            pretrial_detention_score=32.0,
            primary_pattern="9m2_standard_reinsertion_priority",
        ),
        PrisonConditionsRightsEntity(
            entity_id="PCR-008",
            name="Norvège",
            country="Norvège",
            overcrowding_severity_score=11.0,
            torture_ill_treatment_score=10.0,
            healthcare_denial_score=13.0,
            pretrial_detention_score=14.0,
            primary_pattern="halden_model_20pct_recidivism_rate",
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

    return PrisonConditionsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_conditions_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "hrw_prison_conditions_global_violations_2024",
            "icps_world_prison_population_list_2024",
            "amnesty_international_torture_detention_report",
            "un_subcommittee_prevention_torture_reports",
            "penal_reform_international_global_prison_trends",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_prison_conditions_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
