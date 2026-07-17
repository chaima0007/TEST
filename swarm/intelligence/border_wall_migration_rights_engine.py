from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class BorderWallMigrationRightsEntity:
    entity_id: str
    name: str
    country: str
    physical_barrier_pushback_violence_score: float
    detention_deportation_rights_violations_score: float
    asylum_process_obstruction_scale_score: float
    family_separation_unaccompanied_minors_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_border_wall_migration_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.physical_barrier_pushback_violence_score * 0.30
            + self.detention_deportation_rights_violations_score * 0.25
            + self.asylum_process_obstruction_scale_score * 0.25
            + self.family_separation_unaccompanied_minors_score * 0.20,
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
        self.estimated_border_wall_migration_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class BorderWallMigrationRightsEngineResult:
    agent: str = "Border Wall Migration Rights Engine Agent"
    domain: str = "border_wall_migration_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_border_wall_migration_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BorderWallMigrationRightsEntity] = field(default_factory=list)


def run_border_wall_migration_rights_engine() -> BorderWallMigrationRightsEngineResult:
    entities = [
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-001",
            name="USA/Mexique — Mur 700km Trump, Title 42 Expulsions, Cage Children Tornillo, 853 Morts Rio Grande 2022",
            country="USA/Mexique",
            physical_barrier_pushback_violence_score=88.0,
            detention_deportation_rights_violations_score=85.0,
            asylum_process_obstruction_scale_score=87.0,
            family_separation_unaccompanied_minors_score=83.0,
            primary_pattern="physical_barrier_pushback_violence",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-002",
            name="UE/Balkans — Pushbacks Croatie-Grèce Documentés, Frontex Complicité, Moria Incendie 2020, Accord Turquie 6Md€",
            country="Union Européenne",
            physical_barrier_pushback_violence_score=86.0,
            detention_deportation_rights_violations_score=83.0,
            asylum_process_obstruction_scale_score=85.0,
            family_separation_unaccompanied_minors_score=81.0,
            primary_pattern="asylum_process_obstruction_scale",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-003",
            name="Libye/EU Deal — Garde-Côtes Financés Europe, Renvois Centres Torture, Esclavage Documenté CNN 2017",
            country="Libye",
            physical_barrier_pushback_violence_score=90.0,
            detention_deportation_rights_violations_score=88.0,
            asylum_process_obstruction_scale_score=85.0,
            family_separation_unaccompanied_minors_score=86.0,
            primary_pattern="detention_deportation_rights_violations",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-004",
            name="Australie/Offshore — Manus-Nauru Détention Offshore 2013-2019, Torture PTSD, Assange Parallèle, Médecins Bâillonnés",
            country="Australie",
            physical_barrier_pushback_violence_score=84.0,
            detention_deportation_rights_violations_score=82.0,
            asylum_process_obstruction_scale_score=80.0,
            family_separation_unaccompanied_minors_score=78.0,
            primary_pattern="detention_deportation_rights_violations",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-005",
            name="Pologne/Belarus — Crise Instrumentalisée Loukachenko 2021, Pushbacks Legalisés, Hypothermie Morts Forêt Bialowieza",
            country="Pologne/Belarus",
            physical_barrier_pushback_violence_score=55.0,
            detention_deportation_rights_violations_score=53.0,
            asylum_process_obstruction_scale_score=52.0,
            family_separation_unaccompanied_minors_score=50.0,
            primary_pattern="physical_barrier_pushback_violence",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-006",
            name="Tunisie/Libye — Accord UE-Tunisie 2023, Migrants Subsahariens Abandonnés Désert, Violences Documentées HRW",
            country="Tunisie/Libye",
            physical_barrier_pushback_violence_score=51.0,
            detention_deportation_rights_violations_score=49.0,
            asylum_process_obstruction_scale_score=48.0,
            family_separation_unaccompanied_minors_score=46.0,
            primary_pattern="physical_barrier_pushback_violence",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-007",
            name="HCR/Pacte Mondial — Cadre Gouvernance Migration 2018, Standard Droits Migrants, États Souverains Résistent",
            country="Global",
            physical_barrier_pushback_violence_score=27.0,
            detention_deportation_rights_violations_score=26.0,
            asylum_process_obstruction_scale_score=25.0,
            family_separation_unaccompanied_minors_score=23.0,
            primary_pattern="asylum_process_obstruction_scale",
        ),
        BorderWallMigrationRightsEntity(
            entity_id="BWMR-008",
            name="Canada/IRCC — Systèmes Parrainage Réfugiés, Accueil Ukrainiens 2022, Taux Acceptation 60%, Modèle Relatif",
            country="Canada",
            physical_barrier_pushback_violence_score=6.0,
            detention_deportation_rights_violations_score=5.0,
            asylum_process_obstruction_scale_score=5.0,
            family_separation_unaccompanied_minors_score=4.0,
            primary_pattern="family_separation_unaccompanied_minors",
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

    return BorderWallMigrationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_border_wall_migration_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_trends_forced_displacement_report",
            "hrw_border_violence_pushback_documentation",
            "amnesty_international_migration_detention_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_border_wall_migration_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_border_wall_migration_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
