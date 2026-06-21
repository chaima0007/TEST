from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StatelessnessRightsEntity:
    entity_id: str
    name: str
    country: str
    statelessness_documentation_deprivation_severity_score: float
    birth_registration_absence_exclusion_scale_score: float
    nationality_acquisition_barrier_score: float
    social_service_access_stateless_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_statelessness_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.statelessness_documentation_deprivation_severity_score * 0.30
            + self.birth_registration_absence_exclusion_scale_score * 0.25
            + self.nationality_acquisition_barrier_score * 0.25
            + self.social_service_access_stateless_gap_score * 0.20,
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
        self.estimated_statelessness_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class StatelessnessRightsEngineResult:
    agent: str = "Statelessness Rights Engine Agent"
    domain: str = "statelessness_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_statelessness_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessnessRightsEntity] = field(default_factory=list)

def run_statelessness_rights_engine() -> StatelessnessRightsEngineResult:
    entities = [
        StatelessnessRightsEntity(
            entity_id="STR-001",
            name="Myanmar/Rohingyas — 600 000 Apatrides, Loi Citoyenneté 1982 Exclusion Ethnique & Déni Documents Génération",
            country="Myanmar",
            statelessness_documentation_deprivation_severity_score=97.0,
            birth_registration_absence_exclusion_scale_score=93.0,
            nationality_acquisition_barrier_score=93.0,
            social_service_access_stateless_gap_score=91.0,
            primary_pattern="statelessness_documentation_deprivation_severity",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-002",
            name="Côte d'Ivoire — 700 000 Apatrides Post-Guerre Civile, Enregistrement Naissances Rural Absent & Discrimination Dioula",
            country="Côte d'Ivoire",
            statelessness_documentation_deprivation_severity_score=93.0,
            birth_registration_absence_exclusion_scale_score=89.0,
            nationality_acquisition_barrier_score=88.0,
            social_service_access_stateless_gap_score=88.0,
            primary_pattern="birth_registration_absence_exclusion_scale",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-003",
            name="Thaïlande/Peuples Collines — 480 000 Highland Peoples Sans Nationalité, Restriction Mobilité & Exclusion Éducation",
            country="Thaïlande",
            statelessness_documentation_deprivation_severity_score=91.0,
            birth_registration_absence_exclusion_scale_score=87.0,
            nationality_acquisition_barrier_score=87.0,
            social_service_access_stateless_gap_score=86.0,
            primary_pattern="nationality_acquisition_barrier",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-004",
            name="Koweït/Bidoun — 100 000 Bidoun Apatrides, Accès Emploi Public Interdit & Passeports Voyageurs Refusés",
            country="Koweït",
            statelessness_documentation_deprivation_severity_score=89.0,
            birth_registration_absence_exclusion_scale_score=85.0,
            nationality_acquisition_barrier_score=86.0,
            social_service_access_stateless_gap_score=85.0,
            primary_pattern="social_service_access_stateless_gap",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-005",
            name="Europe/Roms — 46 000 Roms Apatrides UE, Non-Enregistrement Naissances Itinérants & Discrimination Administrative",
            country="Europe",
            statelessness_documentation_deprivation_severity_score=56.0,
            birth_registration_absence_exclusion_scale_score=52.0,
            nationality_acquisition_barrier_score=53.0,
            social_service_access_stateless_gap_score=51.0,
            primary_pattern="birth_registration_absence_exclusion_scale",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-006",
            name="République Dominicaine — Arrêt TC 168-13 Déchéance Rétroactive, 133 000 Dominicains Haïtiens Apatrides",
            country="République Dominicaine",
            statelessness_documentation_deprivation_severity_score=54.0,
            birth_registration_absence_exclusion_scale_score=51.0,
            nationality_acquisition_barrier_score=52.0,
            social_service_access_stateless_gap_score=48.0,
            primary_pattern="nationality_acquisition_barrier",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-007",
            name="UNHCR/ISI — Campagne #IBelong Fin Apatridie 2024, Cartographie Globale & Plaidoyer Convention 1954",
            country="Global",
            statelessness_documentation_deprivation_severity_score=24.0,
            birth_registration_absence_exclusion_scale_score=28.0,
            nationality_acquisition_barrier_score=26.0,
            social_service_access_stateless_gap_score=26.0,
            primary_pattern="statelessness_documentation_deprivation_severity",
        ),
        StatelessnessRightsEntity(
            entity_id="STR-008",
            name="ONU/Convention 1954 — Statut Apatrides, Convention 1961 Réduction Apatridie & SDG 16.9 Identité Légale",
            country="Global",
            statelessness_documentation_deprivation_severity_score=4.0,
            birth_registration_absence_exclusion_scale_score=5.0,
            nationality_acquisition_barrier_score=4.0,
            social_service_access_stateless_gap_score=5.0,
            primary_pattern="birth_registration_absence_exclusion_scale",
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

    return StatelessnessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_statelessness_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_ibelong_campaign_statelessness_global_trends_report",
            "institute_statelessness_inclusion_global_statelessness_report",
            "human_rights_watch_statelessness_nationality_discrimination_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_statelessness_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_statelessness_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
