from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MigrationAsylumSeekersRightsEntity:
    entity_id: str
    name: str
    country: str
    asylum_detention_pushback_severity_score: float
    refugee_determination_unfair_process_scale_score: float
    family_separation_unaccompanied_minors_score: float
    statelessness_documentation_access_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_migration_asylum_seekers_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.asylum_detention_pushback_severity_score * 0.30
            + self.refugee_determination_unfair_process_scale_score * 0.25
            + self.family_separation_unaccompanied_minors_score * 0.25
            + self.statelessness_documentation_access_deficit_gap_score * 0.20,
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
        self.estimated_migration_asylum_seekers_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MigrationAsylumSeekersRightsEngineResult:
    agent: str = "Migration Asylum Seekers Rights Engine Agent"
    domain: str = "migration_asylum_seekers_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_migration_asylum_seekers_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MigrationAsylumSeekersRightsEntity] = field(default_factory=list)


def run_migration_asylum_seekers_rights_engine() -> MigrationAsylumSeekersRightsEngineResult:
    entities = [
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-001",
            name="UE/Grèce Pushbacks Mer Égée Morts — 27 000 Refoulements Documentés ECRE, Noyades Frontex Complicité & Violence Frontières Systémique",
            country="UE/Grèce",
            asylum_detention_pushback_severity_score=94.0,
            refugee_determination_unfair_process_scale_score=90.0,
            family_separation_unaccompanied_minors_score=88.0,
            statelessness_documentation_access_deficit_gap_score=86.0,
            primary_pattern="asylum_detention_pushback_severity",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-002",
            name="Libye/Centres Détention Torture Migrants — Esclavage Documenté CNN 2017, Torture Rançonnage & Retours Forcés UE-Garde Côtes Libyenne",
            country="Libye",
            asylum_detention_pushback_severity_score=93.0,
            refugee_determination_unfair_process_scale_score=91.0,
            family_separation_unaccompanied_minors_score=90.0,
            statelessness_documentation_access_deficit_gap_score=89.0,
            primary_pattern="asylum_detention_pushback_severity",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-003",
            name="USA/Politique Tolérance Zéro Séparation Familles — 5 500 Enfants Séparés Parents 2018, Cages Détention & Rétention ICE Conditions Dégradantes",
            country="USA",
            asylum_detention_pushback_severity_score=89.0,
            refugee_determination_unfair_process_scale_score=87.0,
            family_separation_unaccompanied_minors_score=93.0,
            statelessness_documentation_access_deficit_gap_score=84.0,
            primary_pattern="family_separation_unaccompanied_minors",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-004",
            name="Australie/Détention Offshore Manus Nauru — 12 Ans Détention Indéfinie, Suicides Documentés, Interdiction Réinstallation & Pacific Solution",
            country="Australie",
            asylum_detention_pushback_severity_score=87.0,
            refugee_determination_unfair_process_scale_score=86.0,
            family_separation_unaccompanied_minors_score=82.0,
            statelessness_documentation_access_deficit_gap_score=85.0,
            primary_pattern="refugee_determination_unfair_process_scale",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-005",
            name="Biélorussie/Instrumentalisation Migrants Frontière Pologne — Arme Hybride Migration 2021, Migrants Piégés Forêts & Refoulements Violents Pologne",
            country="Biélorussie",
            asylum_detention_pushback_severity_score=57.0,
            refugee_determination_unfair_process_scale_score=55.0,
            family_separation_unaccompanied_minors_score=54.0,
            statelessness_documentation_access_deficit_gap_score=56.0,
            primary_pattern="asylum_detention_pushback_severity",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-006",
            name="Tunisie/Refoulements Désert Migrants Sub-Sahariens — Abandon Désert Documenté HRW, Violences Racistes & Complicité Tacite Accord UE-Tunisie",
            country="Tunisie",
            asylum_detention_pushback_severity_score=54.0,
            refugee_determination_unfair_process_scale_score=52.0,
            family_separation_unaccompanied_minors_score=50.0,
            statelessness_documentation_access_deficit_gap_score=53.0,
            primary_pattern="asylum_detention_pushback_severity",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-007",
            name="UNHCR/IOM Normes Protection Demandeurs Asile — Standards Détermination Statut Réfugié, Assistance Humanitaire & Plaidoyer Non-Refoulement",
            country="Global",
            asylum_detention_pushback_severity_score=28.0,
            refugee_determination_unfair_process_scale_score=27.0,
            family_separation_unaccompanied_minors_score=26.0,
            statelessness_documentation_access_deficit_gap_score=25.0,
            primary_pattern="refugee_determination_unfair_process_scale",
        ),
        MigrationAsylumSeekersRightsEntity(
            entity_id="MAS-008",
            name="ONU/Convention Réfugiés 1951 & Protocole 1967 — Droit Asile International, Non-Refoulement Principe & Cadre Normatif Protection Globale",
            country="Global",
            asylum_detention_pushback_severity_score=6.0,
            refugee_determination_unfair_process_scale_score=5.0,
            family_separation_unaccompanied_minors_score=5.0,
            statelessness_documentation_access_deficit_gap_score=6.0,
            primary_pattern="statelessness_documentation_access_deficit_gap",
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

    return MigrationAsylumSeekersRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_migration_asylum_seekers_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_trends_forced_displacement_report",
            "ecre_asylum_statistics_europe_quarterly",
            "hrw_migrant_detention_conditions_global",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_migration_asylum_seekers_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_migration_asylum_seekers_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
