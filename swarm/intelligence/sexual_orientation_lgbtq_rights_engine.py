from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SexualOrientationLgbtqRightsEntity:
    entity_id: str
    name: str
    country: str
    lgbtq_criminalization_imprisonment_severity_score: float
    lgbtq_violence_hate_crime_impunity_scale_score: float
    same_sex_partnership_legal_recognition_absence_score: float
    lgbtq_asylum_protection_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sexual_orientation_lgbtq_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.lgbtq_criminalization_imprisonment_severity_score * 0.30
            + self.lgbtq_violence_hate_crime_impunity_scale_score * 0.25
            + self.same_sex_partnership_legal_recognition_absence_score * 0.25
            + self.lgbtq_asylum_protection_deficit_gap_score * 0.20,
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
        self.estimated_sexual_orientation_lgbtq_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SexualOrientationLgbtqRightsEngineResult:
    agent: str = "Sexual Orientation LGBTQ Rights Engine Agent"
    domain: str = "sexual_orientation_lgbtq_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sexual_orientation_lgbtq_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexualOrientationLgbtqRightsEntity] = field(default_factory=list)

def run_sexual_orientation_lgbtq_rights_engine() -> SexualOrientationLgbtqRightsEngineResult:
    entities = [
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-001",
            name="Ouganda — Anti-Homosexualité Loi Peine Mort 2023, Refuges LGBT Fermés, Journalistes Outés & Familles Reniement",
            country="Ouganda",
            lgbtq_criminalization_imprisonment_severity_score=96.0,
            lgbtq_violence_hate_crime_impunity_scale_score=93.0,
            same_sex_partnership_legal_recognition_absence_score=95.0,
            lgbtq_asylum_protection_deficit_gap_score=92.0,
            primary_pattern="lgbtq_criminalization_imprisonment_severity",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-002",
            name="Iran/Arabie Saoudite — Homosexualité Mort/Flagellation, Exécutions Publiques, Transgenres Forcés Opération & Arrestations Systématiques",
            country="Iran/Arabie Saoudite",
            lgbtq_criminalization_imprisonment_severity_score=93.0,
            lgbtq_violence_hate_crime_impunity_scale_score=91.0,
            same_sex_partnership_legal_recognition_absence_score=92.0,
            lgbtq_asylum_protection_deficit_gap_score=90.0,
            primary_pattern="lgbtq_criminalization_imprisonment_severity",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-003",
            name="Russie — Loi Propagande LGBT+ Totale, Organisations Liquidées, Chechen Camps Concentration & Arrestations Pride",
            country="Russie",
            lgbtq_criminalization_imprisonment_severity_score=89.0,
            lgbtq_violence_hate_crime_impunity_scale_score=87.0,
            same_sex_partnership_legal_recognition_absence_score=88.0,
            lgbtq_asylum_protection_deficit_gap_score=86.0,
            primary_pattern="lgbtq_violence_hate_crime_impunity_scale",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-004",
            name="Chine — Dépathologisation Sans Droits, Applications Gay Bloquées, Transgenres Hôpitaux Psychiatriques & Organizations Fermées",
            country="Chine",
            lgbtq_criminalization_imprisonment_severity_score=86.0,
            lgbtq_violence_hate_crime_impunity_scale_score=83.0,
            same_sex_partnership_legal_recognition_absence_score=85.0,
            lgbtq_asylum_protection_deficit_gap_score=84.0,
            primary_pattern="same_sex_partnership_legal_recognition_absence",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-005",
            name="Pologne/Hongrie — Zones LGBT-Free, Adoption Interdite Couples Même Sexe, Propaganda Laws & Pride Bâton Pologne",
            country="Pologne/Hongrie",
            lgbtq_criminalization_imprisonment_severity_score=57.0,
            lgbtq_violence_hate_crime_impunity_scale_score=55.0,
            same_sex_partnership_legal_recognition_absence_score=56.0,
            lgbtq_asylum_protection_deficit_gap_score=54.0,
            primary_pattern="same_sex_partnership_legal_recognition_absence",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-006",
            name="USA/Brésil — State-Level Bans 20 États Trans Mineurs, Violences Anti-Trans Record, Bolsonaro Héritage & Felony Drag",
            country="USA/Brésil",
            lgbtq_criminalization_imprisonment_severity_score=54.0,
            lgbtq_violence_hate_crime_impunity_scale_score=53.0,
            same_sex_partnership_legal_recognition_absence_score=52.0,
            lgbtq_asylum_protection_deficit_gap_score=51.0,
            primary_pattern="lgbtq_violence_hate_crime_impunity_scale",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-007",
            name="ILGA World/Rainbow Europe — Cartographie Droits LGBTI, Criminalisation Map, Standards Protection & Rapports Annuels",
            country="Global",
            lgbtq_criminalization_imprisonment_severity_score=24.0,
            lgbtq_violence_hate_crime_impunity_scale_score=28.0,
            same_sex_partnership_legal_recognition_absence_score=26.0,
            lgbtq_asylum_protection_deficit_gap_score=27.0,
            primary_pattern="lgbtq_violence_hate_crime_impunity_scale",
        ),
        SexualOrientationLgbtqRightsEntity(
            entity_id="SOL-008",
            name="ONU/Principes Yogyakarta — Principes Orientation Sexuelle Identité Genre, Résolution CDHONU & SDG 10 Inégalités",
            country="Global",
            lgbtq_criminalization_imprisonment_severity_score=4.0,
            lgbtq_violence_hate_crime_impunity_scale_score=5.0,
            same_sex_partnership_legal_recognition_absence_score=4.0,
            lgbtq_asylum_protection_deficit_gap_score=5.0,
            primary_pattern="lgbtq_criminalization_imprisonment_severity",
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

    return SexualOrientationLgbtqRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sexual_orientation_lgbtq_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilga_world_state_sponsored_homophobia_report",
            "rainbow_europe_lgbti_rights_annual_index",
            "human_rights_watch_lgbtq_violence_documentation",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_sexual_orientation_lgbtq_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sexual_orientation_lgbtq_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
