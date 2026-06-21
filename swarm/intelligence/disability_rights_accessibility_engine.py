from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DisabilityRightsAccessibilityEntity:
    entity_id: str
    name: str
    country: str
    institutional_segregation_forced_treatment_severity_score: float
    employment_education_exclusion_scale_score: float
    physical_infrastructure_accessibility_barrier_score: float
    crpd_legal_capacity_recognition_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_accessibility_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.institutional_segregation_forced_treatment_severity_score * 0.30
            + self.employment_education_exclusion_scale_score * 0.25
            + self.physical_infrastructure_accessibility_barrier_score * 0.25
            + self.crpd_legal_capacity_recognition_deficit_gap_score * 0.20,
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
        self.estimated_disability_rights_accessibility_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DisabilityRightsAccessibilityEngineResult:
    agent: str = "Disability Rights Accessibility Engine Agent"
    domain: str = "disability_rights_accessibility"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_disability_rights_accessibility_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DisabilityRightsAccessibilityEntity] = field(default_factory=list)


def run_disability_rights_accessibility_engine() -> DisabilityRightsAccessibilityEngineResult:
    entities = [
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-001",
            name="Russie/Internats Psychiatriques — Handicapés Isolés Institutions, Traitement Forcé Soviétique & Tutelle Totale Abus",
            country="Russie",
            institutional_segregation_forced_treatment_severity_score=94.0,
            employment_education_exclusion_scale_score=91.0,
            physical_infrastructure_accessibility_barrier_score=90.0,
            crpd_legal_capacity_recognition_deficit_gap_score=93.0,
            primary_pattern="institutional_segregation_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-002",
            name="Inde/Lépreux Colonies — Exclus Société Villages Séparés, Mendier Autorisé Légalement & Discrimination Systémique",
            country="Inde",
            institutional_segregation_forced_treatment_severity_score=91.0,
            employment_education_exclusion_scale_score=89.0,
            physical_infrastructure_accessibility_barrier_score=88.0,
            crpd_legal_capacity_recognition_deficit_gap_score=90.0,
            primary_pattern="institutional_segregation_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-003",
            name="Chine/Handicapés Mentaux — Institutions Abus Documentés, Loi 2008 Non-Appliquée & Travail Forcé Ateliers",
            country="Chine",
            institutional_segregation_forced_treatment_severity_score=88.0,
            employment_education_exclusion_scale_score=86.0,
            physical_infrastructure_accessibility_barrier_score=85.0,
            crpd_legal_capacity_recognition_deficit_gap_score=87.0,
            primary_pattern="crpd_legal_capacity_recognition_deficit_gap",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-004",
            name="Brésil/Manicômios — Réforme Psychiatrique Incomplète, 30 000 Internés Institutions & Violence Documentée HRW",
            country="Brésil",
            institutional_segregation_forced_treatment_severity_score=85.0,
            employment_education_exclusion_scale_score=83.0,
            physical_infrastructure_accessibility_barrier_score=82.0,
            crpd_legal_capacity_recognition_deficit_gap_score=84.0,
            primary_pattern="institutional_segregation_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-005",
            name="USA/Institutions Psychiatriques — Olmstead Non-Appliqué Intégralement, ADA Gaps & Criminalisation Handicap Mental",
            country="USA",
            institutional_segregation_forced_treatment_severity_score=55.0,
            employment_education_exclusion_scale_score=53.0,
            physical_infrastructure_accessibility_barrier_score=52.0,
            crpd_legal_capacity_recognition_deficit_gap_score=58.0,
            primary_pattern="crpd_legal_capacity_recognition_deficit_gap",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-006",
            name="Afrique Sub-Saharienne — Handicap Exclusion Emploi 90%, Infrastructures Inaccessibles & Sorcellerie Stigma Handicap",
            country="Afrique Sub-Saharienne",
            institutional_segregation_forced_treatment_severity_score=52.0,
            employment_education_exclusion_scale_score=58.0,
            physical_infrastructure_accessibility_barrier_score=57.0,
            crpd_legal_capacity_recognition_deficit_gap_score=54.0,
            primary_pattern="employment_education_exclusion_scale",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-007",
            name="DPO/IDA Alliance Internationale — Handicapés Organisations, CRPD Monitoring & Inclusion Advocacy Global",
            country="Global",
            institutional_segregation_forced_treatment_severity_score=27.0,
            employment_education_exclusion_scale_score=25.0,
            physical_infrastructure_accessibility_barrier_score=26.0,
            crpd_legal_capacity_recognition_deficit_gap_score=28.0,
            primary_pattern="crpd_legal_capacity_recognition_deficit_gap",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-008",
            name="ONU/CRPD 2006 — Convention Droits Personnes Handicapées, Comité CRPD Examen États & Art.12 Capacité Juridique",
            country="Global",
            institutional_segregation_forced_treatment_severity_score=5.0,
            employment_education_exclusion_scale_score=5.0,
            physical_infrastructure_accessibility_barrier_score=4.0,
            crpd_legal_capacity_recognition_deficit_gap_score=5.0,
            primary_pattern="crpd_legal_capacity_recognition_deficit_gap",
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

    return DisabilityRightsAccessibilityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disability_rights_accessibility_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_crpd_committee_concluding_observations",
            "hrw_disability_rights_violations_documentation",
            "ida_international_disability_alliance_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_disability_rights_accessibility_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_disability_rights_accessibility_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
