from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#818cf8"


@dataclass
class MentalHealthRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_psychiatry_score: float
    treatment_access_gap_score: float
    stigma_discrimination_score: float
    legal_capacity_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mental_health_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_psychiatry_score * 0.30
            + self.treatment_access_gap_score * 0.25
            + self.stigma_discrimination_score * 0.25
            + self.legal_capacity_denial_score * 0.20,
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
        self.estimated_mental_health_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class MentalHealthRightsEngineResult:
    agent: str = "Mental Health Rights Engine Agent"
    domain: str = "mental_health_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_mental_health_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MentalHealthRightsEntity] = field(default_factory=list)


def run_mental_health_rights_engine() -> MentalHealthRightsEngineResult:
    entities = [
        MentalHealthRightsEntity(
            entity_id="MHR-001",
            name="Chine — Ankang Psychiatrie Punitive Dissidents, 1,3M Lits Sans Recours Légal",
            country="Chine",
            forced_psychiatry_score=97.0,
            treatment_access_gap_score=94.0,
            stigma_discrimination_score=93.0,
            legal_capacity_denial_score=95.0,
            primary_pattern="forced_psychiatry",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-002",
            name="Russie — Psychiatrie Punitive Héritage Soviétique, Centre Serbsky & Dissidents Internés",
            country="Russie",
            forced_psychiatry_score=91.0,
            treatment_access_gap_score=87.0,
            stigma_discrimination_score=86.0,
            legal_capacity_denial_score=89.0,
            primary_pattern="forced_psychiatry",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-003",
            name="Inde — Mental Healthcare Act 2017 Non-Appliqué, 70% Soins Traditionnels & Chaînes",
            country="Inde",
            forced_psychiatry_score=85.0,
            treatment_access_gap_score=82.0,
            stigma_discrimination_score=81.0,
            legal_capacity_denial_score=79.0,
            primary_pattern="treatment_access_gap",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-004",
            name="Afrique Sub-Saharienne — 0,1 Psychiatre/100k Habitants, Médicaments Inaccessibles & Soins Nuls",
            country="Afrique Sub-Saharienne",
            forced_psychiatry_score=77.0,
            treatment_access_gap_score=79.0,
            stigma_discrimination_score=76.0,
            legal_capacity_denial_score=72.0,
            primary_pattern="treatment_access_gap",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-005",
            name="USA — Criminalisation Santé Mentale, 20% Détenus Trouble Psychiatrique Grave",
            country="USA",
            forced_psychiatry_score=57.0,
            treatment_access_gap_score=54.0,
            stigma_discrimination_score=53.0,
            legal_capacity_denial_score=52.0,
            primary_pattern="forced_psychiatry",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-006",
            name="Brésil — Réforme Psychiatrique Incomplète, CAPS Insuffisants & Hospitalisations Abusives",
            country="Brésil",
            forced_psychiatry_score=48.0,
            treatment_access_gap_score=45.0,
            stigma_discrimination_score=44.0,
            legal_capacity_denial_score=43.0,
            primary_pattern="treatment_access_gap",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-007",
            name="France — Isolement/Contention en Hausse, Contrôleur Général Alerte & Réforme Attendue",
            country="France",
            forced_psychiatry_score=32.0,
            treatment_access_gap_score=29.0,
            stigma_discrimination_score=28.0,
            legal_capacity_denial_score=28.0,
            primary_pattern="stigma_discrimination",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-008",
            name="Finlande/Pays-Bas — Open Dialogue, Care in Community & CRPD Art.12 Appliqué",
            country="Finlande/Pays-Bas",
            forced_psychiatry_score=10.0,
            treatment_access_gap_score=9.0,
            stigma_discrimination_score=9.0,
            legal_capacity_denial_score=11.0,
            primary_pattern="legal_capacity_denial",
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

    return MentalHealthRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_mental_health_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_mental_health_atlas_global_2023",
            "hrw_mental_health_rights_violations_global",
            "un_special_rapporteur_health_mental_health_2024",
            "crpd_committee_mental_health_legal_capacity",
            "global_mental_health_action_plan_2013_2030",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_mental_health_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
