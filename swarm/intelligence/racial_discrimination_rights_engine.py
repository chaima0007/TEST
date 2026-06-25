from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#1a0505"

@dataclass
class RacialDiscriminationRightsEntity:
    entity_id: str
    name: str
    country: str
    systemic_racism_score: float
    police_brutality_score: float
    economic_racial_exclusion_score: float
    institutional_discrimination_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_racial_discrimination_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.systemic_racism_score * 0.30
            + self.police_brutality_score * 0.25
            + self.economic_racial_exclusion_score * 0.25
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
        self.estimated_racial_discrimination_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class RacialDiscriminationRightsEngineResult:
    agent: str = "Racial Discrimination Rights Engine Agent"
    domain: str = "racial_discrimination_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_racial_discrimination_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RacialDiscriminationRightsEntity] = field(default_factory=list)


def run_racial_discrimination_rights_engine() -> RacialDiscriminationRightsEngineResult:
    entities = [
        RacialDiscriminationRightsEntity(
            entity_id="RDR-001",
            name="Myanmar — Génocide Rohingya, Apartheid de Facto Ethnique, Citoyenneté Refusée & Camps Internement Déplacés Internes",
            country="Myanmar",
            systemic_racism_score=97.0,
            police_brutality_score=94.0,
            economic_racial_exclusion_score=95.0,
            institutional_discrimination_score=96.0,
            primary_pattern="systemic_racism",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-002",
            name="Israël/Palestine — Apartheid Documenté Amnesty International, Ségrégation Territoriale, Restrictions Liberté Mouvement & Deux Systèmes Juridiques",
            country="Israël/Palestine",
            systemic_racism_score=90.0,
            police_brutality_score=88.0,
            economic_racial_exclusion_score=89.0,
            institutional_discrimination_score=91.0,
            primary_pattern="institutional_discrimination",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-003",
            name="USA — Racisme Systémique, Incarcération Masse Noire (13% Population/38% Détenus), Police Brutality & Ségrégation Scolaire Persistante",
            country="USA",
            systemic_racism_score=82.0,
            police_brutality_score=86.0,
            economic_racial_exclusion_score=80.0,
            institutional_discrimination_score=78.0,
            primary_pattern="police_brutality",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-004",
            name="Brésil — Violence Policière Contre Noirs, Inégalités Raciales Extrêmes, Favelas Militarisées & Racisme Structurel Non Reconnu",
            country="Brésil",
            systemic_racism_score=76.0,
            police_brutality_score=82.0,
            economic_racial_exclusion_score=78.0,
            institutional_discrimination_score=72.0,
            primary_pattern="police_brutality",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-005",
            name="France — Discrimination Banlieues, Violences Policières Jeunes Racisés, Contrôles Faciaux & Déni Officiel Racisme Systémique",
            country="France",
            systemic_racism_score=56.0,
            police_brutality_score=58.0,
            economic_racial_exclusion_score=54.0,
            institutional_discrimination_score=52.0,
            primary_pattern="police_brutality",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-006",
            name="UK — Windrush Scandal, Discrimination Institutionnelle, Disparités Santé COVID Racisés & Écart Salarial Ethnique",
            country="Royaume-Uni",
            systemic_racism_score=48.0,
            police_brutality_score=44.0,
            economic_racial_exclusion_score=50.0,
            institutional_discrimination_score=46.0,
            primary_pattern="economic_racial_exclusion",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-007",
            name="Afrique du Sud — Transformation Post-Apartheid Inégale, Inégalités Économiques Raciales Persistantes & Ségrégation Spatiale",
            country="Afrique du Sud",
            systemic_racism_score=32.0,
            police_brutality_score=28.0,
            economic_racial_exclusion_score=34.0,
            institutional_discrimination_score=30.0,
            primary_pattern="economic_racial_exclusion",
        ),
        RacialDiscriminationRightsEntity(
            entity_id="RDR-008",
            name="Nouvelle-Zélande — Te Tiriti o Waitangi Meilleure Pratique, Reconnaissance Droits Maoris, Tribunal Waitangi & Bilinguisme Officiel",
            country="Nouvelle-Zélande",
            systemic_racism_score=11.0,
            police_brutality_score=9.0,
            economic_racial_exclusion_score=12.0,
            institutional_discrimination_score=10.0,
            primary_pattern="systemic_racism",
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

    return RacialDiscriminationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_racial_discrimination_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_apartheid_report_israel_palestine_2022",
            "un_cerd_committee_racial_discrimination_reports",
            "hrw_racial_discrimination_global_documentation",
            "un_special_rapporteur_racism_annual_reports",
            "movement_for_black_lives_policing_data",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_racial_discrimination_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_racial_discrimination_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
