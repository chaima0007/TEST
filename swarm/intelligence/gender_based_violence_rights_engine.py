from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#be185d"


@dataclass
class GenderBasedViolenceRightsEntity:
    entity_id: str
    name: str
    country: str
    femicide_score: float
    domestic_violence_impunity_score: float
    institutional_revictimization_score: float
    access_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_gender_based_violence_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.femicide_score * 0.30
            + self.domestic_violence_impunity_score * 0.25
            + self.institutional_revictimization_score * 0.25
            + self.access_protection_gap_score * 0.20,
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
        self.estimated_gender_based_violence_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class GenderBasedViolenceRightsEngineResult:
    agent: str = "Gender Based Violence Rights Engine Agent"
    domain: str = "gender_based_violence_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_gender_based_violence_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[GenderBasedViolenceRightsEntity] = field(default_factory=list)


def run_gender_based_violence_rights_engine() -> GenderBasedViolenceRightsEngineResult:
    entities = [
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-001",
            name="Honduras — Taux Féminicide Parmi les Plus Élevés Monde, Impunité 95% & Gangs MS-13",
            country="Honduras",
            femicide_score=90.0,
            domestic_violence_impunity_score=88.0,
            institutional_revictimization_score=87.0,
            access_protection_gap_score=86.0,
            primary_pattern="femicide_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-002",
            name="RD Congo — Viols de Guerre Systématiques, Arme de Guerre Documentée ONU & Impunité Totale",
            country="RD Congo",
            femicide_score=88.0,
            domestic_violence_impunity_score=86.0,
            institutional_revictimization_score=85.0,
            access_protection_gap_score=84.0,
            primary_pattern="domestic_violence_impunity_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-003",
            name="Afghanistan — Abolition Droits Femmes Talibans, Violences Domestiques Légalisées & Zéro Recours",
            country="Afghanistan",
            femicide_score=87.0,
            domestic_violence_impunity_score=85.0,
            institutional_revictimization_score=88.0,
            access_protection_gap_score=86.0,
            primary_pattern="institutional_revictimization_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-004",
            name="Mexique — 10 Femicides/Jour, Alerte Genre 21 États & Défaillance Systémique Ministerio Público",
            country="Mexique",
            femicide_score=82.0,
            domestic_violence_impunity_score=80.0,
            institutional_revictimization_score=78.0,
            access_protection_gap_score=77.0,
            primary_pattern="femicide_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-005",
            name="Inde — Violence Conjugale 30% Femmes, Barrières Culturelles Dépôt Plainte & Justice Lente",
            country="Inde",
            femicide_score=55.0,
            domestic_violence_impunity_score=57.0,
            institutional_revictimization_score=53.0,
            access_protection_gap_score=56.0,
            primary_pattern="domestic_violence_impunity_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-006",
            name="Turquie — Retrait Convention Istanbul 2021, Hausse Féminicides & Résistances Institutionnelles",
            country="Turquie",
            femicide_score=49.0,
            domestic_violence_impunity_score=51.0,
            institutional_revictimization_score=50.0,
            access_protection_gap_score=48.0,
            primary_pattern="institutional_revictimization_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-007",
            name="Brésil — Loi Maria da Penha Partiellement Appliquée, Lacunes Refuges & Violences Rurales",
            country="Brésil",
            femicide_score=32.0,
            domestic_violence_impunity_score=30.0,
            institutional_revictimization_score=28.0,
            access_protection_gap_score=31.0,
            primary_pattern="access_protection_gap_score",
        ),
        GenderBasedViolenceRightsEntity(
            entity_id="GBV-008",
            name="Islande — Cadre Légal Fort Convention Istanbul, Réseau Refuges Complet & Taux Condamnation Élevé",
            country="Islande",
            femicide_score=12.0,
            domestic_violence_impunity_score=11.0,
            institutional_revictimization_score=10.0,
            access_protection_gap_score=13.0,
            primary_pattern="access_protection_gap_score",
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

    return GenderBasedViolenceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_gender_based_violence_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_women_global_femicide_database_2024",
            "who_violence_against_women_global_estimates",
            "hrw_gender_based_violence_country_reports",
            "un_special_rapporteur_violence_against_women_annual_report",
            "amnesty_international_gender_rights_violations",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_gender_based_violence_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
