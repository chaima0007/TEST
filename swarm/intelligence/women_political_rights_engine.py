from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#ec4899"


@dataclass
class WomenPoliticalRightsEntity:
    entity_id: str
    name: str
    country: str
    political_exclusion_score: float
    electoral_violence_score: float
    legal_barriers_participation_score: float
    institutional_discrimination_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_women_political_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.political_exclusion_score * 0.30
            + self.electoral_violence_score * 0.25
            + self.legal_barriers_participation_score * 0.25
            + self.institutional_discrimination_score * 0.20,
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
        self.estimated_women_political_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class WomenPoliticalRightsEngineResult:
    agent: str = "Women Political Rights Engine Agent"
    domain: str = "women_political_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_women_political_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WomenPoliticalRightsEntity] = field(default_factory=list)


def run_women_political_rights_engine() -> WomenPoliticalRightsEngineResult:
    entities = [
        WomenPoliticalRightsEntity(
            entity_id="WPR-001",
            name="Arabie Saoudite — Premières Élections Municipales 2015, Quota 0% Shura Avant Réforme & Tutelle Masculine Permanente",
            country="Arabie Saoudite",
            political_exclusion_score=92.0,
            electoral_violence_score=88.0,
            legal_barriers_participation_score=90.0,
            institutional_discrimination_score=91.0,
            primary_pattern="political_exclusion_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-002",
            name="Afghanistan — Femmes Bannies Totalement de la Politique par les Taliban, Zéro Représentation Institutionnelle",
            country="Afghanistan",
            political_exclusion_score=95.0,
            electoral_violence_score=90.0,
            legal_barriers_participation_score=95.0,
            institutional_discrimination_score=93.0,
            primary_pattern="legal_barriers_participation_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-003",
            name="Yémen — Guerre Civile, Femmes Marginalisées des Négociations de Paix & Représentation Inférieure à 1%",
            country="Yémen",
            political_exclusion_score=88.0,
            electoral_violence_score=87.0,
            legal_barriers_participation_score=85.0,
            institutional_discrimination_score=89.0,
            primary_pattern="electoral_violence_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-004",
            name="Iran — Candidates Présidentielles Filtrées par le Conseil des Gardiens, Femmes Exclues des Postes Suprêmes",
            country="Iran",
            political_exclusion_score=85.0,
            electoral_violence_score=82.0,
            legal_barriers_participation_score=86.0,
            institutional_discrimination_score=84.0,
            primary_pattern="legal_barriers_participation_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-005",
            name="Pakistan — Violence Systématique Contre les Candidates Femmes, Blasphème Utilisé Comme Outil de Suppression Politique",
            country="Pakistan",
            political_exclusion_score=52.0,
            electoral_violence_score=55.0,
            legal_barriers_participation_score=48.0,
            institutional_discrimination_score=50.0,
            primary_pattern="electoral_violence_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-006",
            name="Égypte — Restrictions Légales Encadrant les Femmes en Politique, Normes Sociales Limitant la Participation Électorale",
            country="Égypte",
            political_exclusion_score=48.0,
            electoral_violence_score=45.0,
            legal_barriers_participation_score=50.0,
            institutional_discrimination_score=47.0,
            primary_pattern="legal_barriers_participation_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-007",
            name="Brésil — Quota 30% Respecté en Surface mais Violence Politique Contre les Femmes Élues en Hausse Documentée",
            country="Brésil",
            political_exclusion_score=30.0,
            electoral_violence_score=32.0,
            legal_barriers_participation_score=26.0,
            institutional_discrimination_score=28.0,
            primary_pattern="electoral_violence_score",
        ),
        WomenPoliticalRightsEntity(
            entity_id="WPR-008",
            name="Islande — Plus de 50% de Femmes au Parlement, Parité Gouvernementale & Première Présidente Élue au Monde",
            country="Islande",
            political_exclusion_score=10.0,
            electoral_violence_score=9.0,
            legal_barriers_participation_score=8.0,
            institutional_discrimination_score=11.0,
            primary_pattern="political_exclusion_score",
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

    return WomenPoliticalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_women_political_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ipu_women_in_parliament_global_report_2024",
            "un_women_political_participation_data_2024",
            "eiu_democracy_index_gender_2024",
            "hrw_women_political_rights_violations",
            "v_dem_electoral_gender_equality_index",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_women_political_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
