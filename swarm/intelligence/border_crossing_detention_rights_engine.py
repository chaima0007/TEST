from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class BorderCrossingDetentionRightsEntity:
    entity_id: str
    name: str
    country: str
    border_violence_pushback_death_severity_score: float
    immigration_detention_conditions_duration_scale_score: float
    family_separation_unaccompanied_minors_score: float
    stateless_person_documentation_legal_aid_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_border_crossing_detention_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.border_violence_pushback_death_severity_score * 0.30
            + self.immigration_detention_conditions_duration_scale_score * 0.25
            + self.family_separation_unaccompanied_minors_score * 0.25
            + self.stateless_person_documentation_legal_aid_deficit_gap_score * 0.20,
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
        self.estimated_border_crossing_detention_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class BorderCrossingDetentionRightsEngineResult:
    agent: str = "Border Crossing Detention Rights Engine Agent"
    domain: str = "border_crossing_detention_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_border_crossing_detention_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BorderCrossingDetentionRightsEntity] = field(default_factory=list)


def run_border_crossing_detention_rights_engine() -> BorderCrossingDetentionRightsEngineResult:
    entities = [
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-001",
            name="USA/Mexique — 853 Morts Frontière 2022, Titre 42 Expulsions, Séparation Familles 5 000+, CBP Violence & Razor Wire Texas",
            country="USA/Mexique",
            border_violence_pushback_death_severity_score=95.0,
            immigration_detention_conditions_duration_scale_score=93.0,
            family_separation_unaccompanied_minors_score=92.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=91.0,
            primary_pattern="family_separation_unaccompanied_minors",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-002",
            name="UE/Méditerranée — 30 000 Morts Depuis 1993, Pushbacks Croatie/Grèce Documentés, Frontex Complicité & Lampedusa Crise",
            country="UE/Méditerranée",
            border_violence_pushback_death_severity_score=92.0,
            immigration_detention_conditions_duration_scale_score=90.0,
            family_separation_unaccompanied_minors_score=89.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=88.0,
            primary_pattern="border_violence_pushback_death_severity",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-003",
            name="Libye — Centres Détention Torture ONU Documentée, Coast Guard Financement EU, Retours Forcés & Conditions Dégradantes",
            country="Libye",
            border_violence_pushback_death_severity_score=89.0,
            immigration_detention_conditions_duration_scale_score=87.0,
            family_separation_unaccompanied_minors_score=86.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=85.0,
            primary_pattern="immigration_detention_conditions_duration_scale",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-004",
            name="Australie — Nauru Détention Offshore Indéfinie, Manus Island Fermé Tard, Suicides Détenus & Medical Transfers Refusés",
            country="Australie",
            border_violence_pushback_death_severity_score=86.0,
            immigration_detention_conditions_duration_scale_score=84.0,
            family_separation_unaccompanied_minors_score=83.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=82.0,
            primary_pattern="immigration_detention_conditions_duration_scale",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-005",
            name="UK/France — Channel Deaths 2022 Record 46, Pushbacks Illégaux Dunkerque, Rwanda Plan & Small Boats Act 2023",
            country="UK/France",
            border_violence_pushback_death_severity_score=57.0,
            immigration_detention_conditions_duration_scale_score=55.0,
            family_separation_unaccompanied_minors_score=54.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=53.0,
            primary_pattern="border_violence_pushback_death_severity",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-006",
            name="Turquie/Balkans — Route Bosnie Violences, Détention Sans Limite Légale, Mineurs Non-Accompagnés Perdus & Corruption Gardes",
            country="Turquie/Balkans",
            border_violence_pushback_death_severity_score=54.0,
            immigration_detention_conditions_duration_scale_score=52.0,
            family_separation_unaccompanied_minors_score=51.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=50.0,
            primary_pattern="stateless_person_documentation_legal_aid_deficit_gap",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-007",
            name="UNHCR/MSF — Monitoring Frontières, Sauvetages Méditerranée, Dossiers Décès & Advocacy Standards Détention",
            country="Global",
            border_violence_pushback_death_severity_score=27.0,
            immigration_detention_conditions_duration_scale_score=26.0,
            family_separation_unaccompanied_minors_score=25.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=25.0,
            primary_pattern="border_violence_pushback_death_severity",
        ),
        BorderCrossingDetentionRightsEntity(
            entity_id="BCD-008",
            name="ONU/Convention 1951 Art.31 — Non-Pénalisation Entrée Irrégulière, Standards Détention UNHCR & SDG 10.7 Migration",
            country="Global",
            border_violence_pushback_death_severity_score=5.0,
            immigration_detention_conditions_duration_scale_score=4.0,
            family_separation_unaccompanied_minors_score=4.0,
            stateless_person_documentation_legal_aid_deficit_gap_score=4.0,
            primary_pattern="stateless_person_documentation_legal_aid_deficit_gap",
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

    return BorderCrossingDetentionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_border_crossing_detention_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_mediterranean_sea_crossing_deaths_database",
            "border_violence_monitoring_network_report",
            "human_rights_watch_immigration_detention_conditions",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_border_crossing_detention_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_border_crossing_detention_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
