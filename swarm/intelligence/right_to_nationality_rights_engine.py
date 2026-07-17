from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0369a1"


@dataclass
class RightToNationalityRightsEntity:
    entity_id: str
    name: str
    country: str
    nationality_deprivation_score: float
    discriminatory_nationality_law_score: float
    stateless_adult_population_score: float
    naturalization_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_nationality_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.nationality_deprivation_score * 0.30
            + self.discriminatory_nationality_law_score * 0.25
            + self.stateless_adult_population_score * 0.25
            + self.naturalization_barrier_score * 0.20,
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
        self.estimated_right_to_nationality_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToNationalityRightsEngineResult:
    agent: str = "Right To Nationality Rights Engine Agent"
    domain: str = "right_to_nationality_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_nationality_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToNationalityRightsEntity] = field(default_factory=list)


def run_right_to_nationality_rights_engine() -> RightToNationalityRightsEngineResult:
    entities = [
        RightToNationalityRightsEntity(
            entity_id="RTN-001",
            name="Myanmar — Rohingyas Dénationalisés Loi 1982, 800k Apatrides, Expulsion Complète Système Citoyenneté",
            country="Myanmar",
            nationality_deprivation_score=97.0,
            discriminatory_nationality_law_score=98.0,
            stateless_adult_population_score=96.0,
            naturalization_barrier_score=97.0,
            primary_pattern="discriminatory_nationality_law_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-002",
            name="Kuwait/Émirats — Bidun, 100k+ Adultes Apatrides 2e Génération, Aucune Solution Légale Offerte",
            country="Kuwait/Émirats",
            nationality_deprivation_score=90.0,
            discriminatory_nationality_law_score=88.0,
            stateless_adult_population_score=92.0,
            naturalization_barrier_score=94.0,
            primary_pattern="naturalization_barrier_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-003",
            name="République Dominicaine — Dénationalisation Rétroactive 200k Haïtiens, Arrêt TC 168-13, Apatridie de Masse",
            country="République Dominicaine",
            nationality_deprivation_score=88.0,
            discriminatory_nationality_law_score=85.0,
            stateless_adult_population_score=84.0,
            naturalization_barrier_score=82.0,
            primary_pattern="nationality_deprivation_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-004",
            name="Arabie Saoudite — Lois Nationalité Discriminatoires Femmes, Enfants Mère Non-Transmissibles, Patrilinéarité Absolue",
            country="Arabie Saoudite",
            nationality_deprivation_score=78.0,
            discriminatory_nationality_law_score=90.0,
            stateless_adult_population_score=70.0,
            naturalization_barrier_score=74.0,
            primary_pattern="discriminatory_nationality_law_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-005",
            name="Liban — Lois Nationalité Patrilinéaires, 80k Apatrides Femmes Mariées Étrangers, Transmission Bloquée",
            country="Liban",
            nationality_deprivation_score=52.0,
            discriminatory_nationality_law_score=58.0,
            stateless_adult_population_score=48.0,
            naturalization_barrier_score=54.0,
            primary_pattern="discriminatory_nationality_law_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-006",
            name="Népal — Citoyenneté Lignée Paternelle Obligatoire, Discrimination Systémique Femmes, Enfants Pères Inconnus",
            country="Népal",
            nationality_deprivation_score=46.0,
            discriminatory_nationality_law_score=52.0,
            stateless_adult_population_score=42.0,
            naturalization_barrier_score=48.0,
            primary_pattern="discriminatory_nationality_law_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-007",
            name="Allemagne — Jus Soli Récent 2000, Naturalisations Longues, Inégalités Persistantes Communautés Immigrées",
            country="Allemagne",
            nationality_deprivation_score=22.0,
            discriminatory_nationality_law_score=20.0,
            stateless_adult_population_score=24.0,
            naturalization_barrier_score=30.0,
            primary_pattern="naturalization_barrier_score",
        ),
        RightToNationalityRightsEntity(
            entity_id="RTN-008",
            name="Irlande — Jus Soli Historique Réformé, Meilleure Pratique Inclusion, Procédure Naturalisation Accessible",
            country="Irlande",
            nationality_deprivation_score=7.0,
            discriminatory_nationality_law_score=6.0,
            stateless_adult_population_score=5.0,
            naturalization_barrier_score=8.0,
            primary_pattern="naturalization_barrier_score",
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

    return RightToNationalityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_nationality_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_action_plan_statelessness_2024",
            "un_convention_reduction_statelessness_1961",
            "global_campaign_equal_nationality_rights_report",
            "institute_statelessness_inclusion_global_report_2024",
            "un_special_rapporteur_migrants_nationality_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_nationality_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
