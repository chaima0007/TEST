from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0f766e"


@dataclass
class MedicalExperimentationRightsEntity:
    entity_id: str
    name: str
    country: str
    non_consensual_experimentation_score: float
    vulnerable_population_targeting_score: float
    regulatory_oversight_gap_score: float
    accountability_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_medical_experimentation_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.non_consensual_experimentation_score * 0.30
            + self.vulnerable_population_targeting_score * 0.25
            + self.regulatory_oversight_gap_score * 0.25
            + self.accountability_impunity_score * 0.20,
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
        self.estimated_medical_experimentation_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class MedicalExperimentationRightsEngineResult:
    agent: str = "Medical Experimentation Rights Engine Agent"
    domain: str = "medical_experimentation_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_medical_experimentation_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MedicalExperimentationRightsEntity] = field(default_factory=list)


def run_medical_experimentation_rights_engine() -> MedicalExperimentationRightsEngineResult:
    entities = [
        MedicalExperimentationRightsEntity(
            entity_id="MER-001",
            name="Guatemala — Expériences Syphilis USA 1940s, 1 300 Prisonniers Non-Consentis, Découverte 2010 Susan Reverby",
            country="Guatemala",
            non_consensual_experimentation_score=96.0,
            vulnerable_population_targeting_score=94.0,
            regulatory_oversight_gap_score=92.0,
            accountability_impunity_score=90.0,
            primary_pattern="non_consensual_experimentation_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-002",
            name="USA Tuskegee Héritage — Continuation Expériences Non-Consenties Populations Noires, 40 Ans Silence Médical",
            country="USA",
            non_consensual_experimentation_score=90.0,
            vulnerable_population_targeting_score=92.0,
            regulatory_oversight_gap_score=85.0,
            accountability_impunity_score=88.0,
            primary_pattern="vulnerable_population_targeting_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-003",
            name="Chine — Expériences Organes Prisonniers Falun Gong, Documentation 2019 Tribunal Londres, Protocoles Forcés",
            country="Chine",
            non_consensual_experimentation_score=89.0,
            vulnerable_population_targeting_score=88.0,
            regulatory_oversight_gap_score=91.0,
            accountability_impunity_score=93.0,
            primary_pattern="accountability_impunity_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-004",
            name="Afrique Sub-Saharienne — Essais VIH/Ebola Sans Consentement Éclairé, CROs Pression Financière, Décès Non Signalés",
            country="Afrique Sub-Saharienne",
            non_consensual_experimentation_score=74.0,
            vulnerable_population_targeting_score=78.0,
            regulatory_oversight_gap_score=80.0,
            accountability_impunity_score=76.0,
            primary_pattern="regulatory_oversight_gap_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-005",
            name="Inde — Essais Cliniques Pauvres Ruraux, Décès Non Signalés, Compensation Nulle, Consentement Biaisé",
            country="Inde",
            non_consensual_experimentation_score=56.0,
            vulnerable_population_targeting_score=58.0,
            regulatory_oversight_gap_score=54.0,
            accountability_impunity_score=52.0,
            primary_pattern="vulnerable_population_targeting_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-006",
            name="Brésil — Expériences Non-Consenties Populations Autochtones Isolées, Amazonie, Pression Laboratoires",
            country="Brésil",
            non_consensual_experimentation_score=48.0,
            vulnerable_population_targeting_score=52.0,
            regulatory_oversight_gap_score=46.0,
            accountability_impunity_score=44.0,
            primary_pattern="vulnerable_population_targeting_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-007",
            name="USA — Prisonniers Études Pharmacologiques, Paiement Sous Pression, Comité Belmont 1979 Post-Tuskegee",
            country="USA",
            non_consensual_experimentation_score=30.0,
            vulnerable_population_targeting_score=28.0,
            regulatory_oversight_gap_score=24.0,
            accountability_impunity_score=26.0,
            primary_pattern="non_consensual_experimentation_score",
        ),
        MedicalExperimentationRightsEntity(
            entity_id="MER-008",
            name="Norvège — Standards Éthiques OCDE, Consentement Éclairé Exemplaire, NENT Comité National Éthique",
            country="Norvège",
            non_consensual_experimentation_score=6.0,
            vulnerable_population_targeting_score=5.0,
            regulatory_oversight_gap_score=4.0,
            accountability_impunity_score=7.0,
            primary_pattern="non_consensual_experimentation_score",
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

    return MedicalExperimentationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_medical_experimentation_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "declaration_of_helsinki_compliance_2024",
            "who_research_ethics_review_committee_standards",
            "hrw_medical_experimentation_prisoners_documentation",
            "un_special_rapporteur_health_research_ethics_report",
            "nuffield_council_bioethics_global_research_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_medical_experimentation_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
