from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DisabilityRightsAccessibilityEntity:
    entity_id: str
    name: str
    country: str
    institutionalization_forced_treatment_severity_score: float
    physical_accessibility_exclusion_scale_score: float
    disability_employment_discrimination_score: float
    crpd_legal_capacity_guardianship_reform_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_accessibility_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.institutionalization_forced_treatment_severity_score * 0.30
            + self.physical_accessibility_exclusion_scale_score * 0.25
            + self.disability_employment_discrimination_score * 0.25
            + self.crpd_legal_capacity_guardianship_reform_deficit_gap_score * 0.20,
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
            name="Chine — Institutions Psychiatriques Dissidents, Xiebi Internement Forcé, Eugénisme Stérilisation & Travail Forcé Handicapés",
            country="Chine",
            institutionalization_forced_treatment_severity_score=95.0,
            physical_accessibility_exclusion_scale_score=93.0,
            disability_employment_discrimination_score=92.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=91.0,
            primary_pattern="institutionalization_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-002",
            name="Russie — Internats Psychiatriques Punição Politique, Psychiatrie Punitive Retour & Handicapés Institutionnalisés 150 000",
            country="Russie",
            institutionalization_forced_treatment_severity_score=92.0,
            physical_accessibility_exclusion_scale_score=90.0,
            disability_employment_discrimination_score=89.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=88.0,
            primary_pattern="institutionalization_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-003",
            name="Afrique Sub-Saharienne — Sorcellerie Handicaps Infantiles, Exclusion Scolaire, Albinos Mutilations & Sans Protection CRPD",
            country="Afrique Sub-Saharienne",
            institutionalization_forced_treatment_severity_score=89.0,
            physical_accessibility_exclusion_scale_score=87.0,
            disability_employment_discrimination_score=86.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=85.0,
            primary_pattern="physical_accessibility_exclusion_scale",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-004",
            name="Inde — Personnes Handicapées Mental Internées, Loi Santé Mentale 2017 Inappliquée, Accessibilité Zéro Ruraux & Discrimination Castes",
            country="Inde",
            institutionalization_forced_treatment_severity_score=86.0,
            physical_accessibility_exclusion_scale_score=84.0,
            disability_employment_discrimination_score=83.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=82.0,
            primary_pattern="crpd_legal_capacity_guardianship_reform_deficit_gap",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-005",
            name="USA/Europe — Olmstead Inappliqué Partiellement, Guardianship Abusif, ADA/ADAEU Lacunes & Électrochocs Sans Consentement",
            country="USA/Europe",
            institutionalization_forced_treatment_severity_score=57.0,
            physical_accessibility_exclusion_scale_score=55.0,
            disability_employment_discrimination_score=54.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=53.0,
            primary_pattern="institutionalization_forced_treatment_severity",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-006",
            name="MENA — Stigmatisation Handicap Mental, Loi Tutelle Totale, Femmes Handicapées Double Discrimination & Accessibilité Absente",
            country="MENA",
            institutionalization_forced_treatment_severity_score=54.0,
            physical_accessibility_exclusion_scale_score=52.0,
            disability_employment_discrimination_score=51.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=50.0,
            primary_pattern="disability_employment_discrimination",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-007",
            name="IDA/DPO Global — Disabled Peoples Organisations, CRPD Advocacy, Monitoring Mise en Œuvre & Standards Accessibilité",
            country="Global",
            institutionalization_forced_treatment_severity_score=27.0,
            physical_accessibility_exclusion_scale_score=26.0,
            disability_employment_discrimination_score=25.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=25.0,
            primary_pattern="crpd_legal_capacity_guardianship_reform_deficit_gap",
        ),
        DisabilityRightsAccessibilityEntity(
            entity_id="DRA-008",
            name="ONU/CRPD — Convention Droits Personnes Handicapées 2006, Comité CRPD & SDG 10.2 Inclusion",
            country="Global",
            institutionalization_forced_treatment_severity_score=5.0,
            physical_accessibility_exclusion_scale_score=4.0,
            disability_employment_discrimination_score=4.0,
            crpd_legal_capacity_guardianship_reform_deficit_gap_score=4.0,
            primary_pattern="physical_accessibility_exclusion_scale",
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
            "who_disability_world_report_global_data",
            "mental_disability_rights_international_monitoring",
            "crpd_committee_concluding_observations_database",
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
