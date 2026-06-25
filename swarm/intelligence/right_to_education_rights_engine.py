from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0284c7"


@dataclass
class RightToEducationRightsEntity:
    entity_id: str
    name: str
    country: str
    out_of_school_score: float
    gender_education_gap_score: float
    education_quality_gap_score: float
    attacks_on_education_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_education_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.out_of_school_score * 0.30
            + self.gender_education_gap_score * 0.25
            + self.education_quality_gap_score * 0.25
            + self.attacks_on_education_score * 0.20,
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
        self.estimated_right_to_education_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class RightToEducationRightsEngineResult:
    agent: str = "RightToEducationRights Engine Agent"
    domain: str = "right_to_education_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_education_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToEducationRightsEntity] = field(default_factory=list)


def run_right_to_education_rights_engine() -> RightToEducationRightsEngineResult:
    entities = [
        # --- 4 CRITIQUE (>=60) ---
        RightToEducationRightsEntity(
            entity_id="RTE-001",
            name="Niger — 45% scolarisation, 3M hors école, Boko Haram 800 écoles",
            country="Niger",
            out_of_school_score=97.0,
            gender_education_gap_score=95.0,
            education_quality_gap_score=94.0,
            attacks_on_education_score=96.0,
            primary_pattern="Jihadist school closures & extreme gender exclusion",
        ),
        RightToEducationRightsEntity(
            entity_id="RTE-002",
            name="Afghanistan — 1.4M filles exclues lycées, enseignantes congédiées",
            country="Afghanistan",
            out_of_school_score=90.0,
            gender_education_gap_score=98.0,
            education_quality_gap_score=82.0,
            attacks_on_education_score=88.0,
            primary_pattern="Taliban gender apartheid in education system",
        ),
        RightToEducationRightsEntity(
            entity_id="RTE-003",
            name="Mali — 800+ écoles fermées, 400k enfants déscolarisés",
            country="Mali",
            out_of_school_score=84.0,
            gender_education_gap_score=80.0,
            education_quality_gap_score=78.0,
            attacks_on_education_score=92.0,
            primary_pattern="Armed group attacks on schools & teachers",
        ),
        RightToEducationRightsEntity(
            entity_id="RTE-004",
            name="Yémen — 2M déscolarisés, 2 500 écoles détruites, enseignants non payés",
            country="Yémen",
            out_of_school_score=80.0,
            gender_education_gap_score=74.0,
            education_quality_gap_score=76.0,
            attacks_on_education_score=88.0,
            primary_pattern="Conflict-destroyed education infrastructure",
        ),
        # --- 2 ÉLEVÉ (40-59) ---
        RightToEducationRightsEntity(
            entity_id="RTE-005",
            name="Pakistan — 22M hors école, madrasas insuffisantes, inégalités urbain/rural",
            country="Pakistan",
            out_of_school_score=58.0,
            gender_education_gap_score=60.0,
            education_quality_gap_score=52.0,
            attacks_on_education_score=46.0,
            primary_pattern="Massive out-of-school crisis with gender gap",
        ),
        RightToEducationRightsEntity(
            entity_id="RTE-006",
            name="Nigeria — 10M déscolarisés #1 Afrique, Boko Haram 1 500 écoles",
            country="Nigeria",
            out_of_school_score=50.0,
            gender_education_gap_score=46.0,
            education_quality_gap_score=44.0,
            attacks_on_education_score=52.0,
            primary_pattern="Boko Haram attacks & North-South education divide",
        ),
        # --- 1 MODÉRÉ (20-39) ---
        RightToEducationRightsEntity(
            entity_id="RTE-007",
            name="Inde — RTE Act lacunes, 35M OOS, discrimination castes",
            country="Inde",
            out_of_school_score=32.0,
            gender_education_gap_score=30.0,
            education_quality_gap_score=34.0,
            attacks_on_education_score=22.0,
            primary_pattern="Caste discrimination & quality gap in public education",
        ),
        # --- 1 FAIBLE (<20) ---
        RightToEducationRightsEntity(
            entity_id="RTE-008",
            name="Finlande/Corée du Sud — PISA top, éducation gratuite universelle",
            country="Finlande/Corée du Sud",
            out_of_school_score=5.0,
            gender_education_gap_score=6.0,
            education_quality_gap_score=4.0,
            attacks_on_education_score=2.0,
            primary_pattern="Universal free education, teacher excellence model",
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

    return RightToEducationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_education_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "unesco_global_education_monitoring_report_2024",
            "unicef_out_of_school_children_global_2024",
            "hrw_attacks_on_education_documentation",
            "right_to_education_initiative_global_violations",
            "safe_schools_declaration_implementation_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_education_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
