from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SeafarersMaritimeLaborRightsEntity:
    entity_id: str
    name: str
    country: str
    ship_abandonment_wage_theft_severity_score: float
    flag_state_labor_standard_evasion_scale_score: float
    unsafe_working_conditions_fatality_risk_score: float
    repatriation_recruitment_fee_exploitation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_seafarers_maritime_labor_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.ship_abandonment_wage_theft_severity_score * 0.30
            + self.flag_state_labor_standard_evasion_scale_score * 0.25
            + self.unsafe_working_conditions_fatality_risk_score * 0.25
            + self.repatriation_recruitment_fee_exploitation_gap_score * 0.20,
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
        self.estimated_seafarers_maritime_labor_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SeafarersMaritimeLaborRightsEngineResult:
    agent: str = "Seafarers Maritime Labor Rights Engine Agent"
    domain: str = "seafarers_maritime_labor_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_seafarers_maritime_labor_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SeafarersMaritimeLaborRightsEntity] = field(default_factory=list)

def run_seafarers_maritime_labor_rights_engine() -> SeafarersMaritimeLaborRightsEngineResult:
    entities = [
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-001",
            name="Panama/Liberia Flag Convenience — 40% Flotte Mondiale Sous Standards ITF Non Respectés, Salaires Volés & Abandons en Mer",
            country="Panama/Liberia",
            ship_abandonment_wage_theft_severity_score=95.0,
            flag_state_labor_standard_evasion_scale_score=93.0,
            unsafe_working_conditions_fatality_risk_score=92.0,
            repatriation_recruitment_fee_exploitation_gap_score=91.0,
            primary_pattern="flag_state_labor_standard_evasion_scale",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-002",
            name="Golfe/Méditerranée — Marins Asiatiques Abandonnés Ports Grecs/Turcs, Passeports Confisqués & Frais Recrutement 15 000$",
            country="Méditerranée",
            ship_abandonment_wage_theft_severity_score=92.0,
            flag_state_labor_standard_evasion_scale_score=89.0,
            unsafe_working_conditions_fatality_risk_score=88.0,
            repatriation_recruitment_fee_exploitation_gap_score=90.0,
            primary_pattern="ship_abandonment_wage_theft_severity",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-003",
            name="Chine/Asie SE Chantiers — Conditions Mortelles Constructions Navales, 500+ Décès/An & Syndicats Interdits",
            country="Chine/Asie SE",
            ship_abandonment_wage_theft_severity_score=89.0,
            flag_state_labor_standard_evasion_scale_score=87.0,
            unsafe_working_conditions_fatality_risk_score=85.0,
            repatriation_recruitment_fee_exploitation_gap_score=86.0,
            primary_pattern="unsafe_working_conditions_fatality_risk",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-004",
            name="Méditerranée Migrants — Marins Forcés Transporter Migrants Sous Menace, Criminalisation Sauvetage & Abandons",
            country="Méditerranée",
            ship_abandonment_wage_theft_severity_score=86.0,
            flag_state_labor_standard_evasion_scale_score=83.0,
            unsafe_working_conditions_fatality_risk_score=82.0,
            repatriation_recruitment_fee_exploitation_gap_score=84.0,
            primary_pattern="ship_abandonment_wage_theft_severity",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-005",
            name="Philippines — 1/3 Marins Monde Filipino, Agences Recrutement Frais Illégaux, Contrats Substitués & Plaintes Ignorées",
            country="Philippines",
            ship_abandonment_wage_theft_severity_score=57.0,
            flag_state_labor_standard_evasion_scale_score=54.0,
            unsafe_working_conditions_fatality_risk_score=53.0,
            repatriation_recruitment_fee_exploitation_gap_score=55.0,
            primary_pattern="repatriation_recruitment_fee_exploitation_gap",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-006",
            name="Marins COVID — 400 000 Bloqués Bateaux 2020-21, Rotations Refusées, Santé Mentale & Suicides en Haute Mer",
            country="Global",
            ship_abandonment_wage_theft_severity_score=54.0,
            flag_state_labor_standard_evasion_scale_score=51.0,
            unsafe_working_conditions_fatality_risk_score=50.0,
            repatriation_recruitment_fee_exploitation_gap_score=52.0,
            primary_pattern="ship_abandonment_wage_theft_severity",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-007",
            name="ITF/International Transport Workers Federation — Campagnes Abandonment, Standards MLC 2006 & Fonds Secours Marins",
            country="Global",
            ship_abandonment_wage_theft_severity_score=28.0,
            flag_state_labor_standard_evasion_scale_score=26.0,
            unsafe_working_conditions_fatality_risk_score=27.0,
            repatriation_recruitment_fee_exploitation_gap_score=27.0,
            primary_pattern="flag_state_labor_standard_evasion_scale",
        ),
        SeafarersMaritimeLaborRightsEntity(
            entity_id="SML-008",
            name="OIT/MLC 2006 — Maritime Labour Convention 2006, Certificats Conformité & SDG 14 Océans Travail Décent",
            country="Global",
            ship_abandonment_wage_theft_severity_score=4.0,
            flag_state_labor_standard_evasion_scale_score=4.0,
            unsafe_working_conditions_fatality_risk_score=5.0,
            repatriation_recruitment_fee_exploitation_gap_score=4.0,
            primary_pattern="flag_state_labor_standard_evasion_scale",
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

    return SeafarersMaritimeLaborRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_seafarers_maritime_labor_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_maritime_labour_convention_mlc2006_reports",
            "itf_seafarers_abandonment_database",
            "imo_flag_state_compliance_audit_reports",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_seafarers_maritime_labor_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_seafarers_maritime_labor_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
