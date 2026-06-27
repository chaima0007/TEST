from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0891b2"


@dataclass
class JuvenileJusticeRightsEntity:
    entity_id: str
    name: str
    country: str
    child_incarceration_score: float
    adult_prosecution_minors_score: float
    detention_conditions_minors_score: float
    rehabilitation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_juvenile_justice_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.child_incarceration_score * 0.30
            + self.adult_prosecution_minors_score * 0.25
            + self.detention_conditions_minors_score * 0.25
            + self.rehabilitation_gap_score * 0.20,
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
        self.estimated_juvenile_justice_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class JuvenileJusticeRightsEngineResult:
    agent: str = "Juvenile Justice Rights Engine Agent"
    domain: str = "juvenile_justice_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_juvenile_justice_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[JuvenileJusticeRightsEntity] = field(default_factory=list)


def run_juvenile_justice_rights_engine() -> JuvenileJusticeRightsEngineResult:
    entities = [
        JuvenileJusticeRightsEntity(
            entity_id="JJR-001",
            name="Pakistan — Peine de Mort Mineurs, 1 500 Enfants dans Prisons Adultes",
            country="Pakistan",
            child_incarceration_score=97.0,
            adult_prosecution_minors_score=96.0,
            detention_conditions_minors_score=95.0,
            rehabilitation_gap_score=94.0,
            primary_pattern="adult_prosecution_minors",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-002",
            name="Iran — Exécutions Mineurs, 90 Condamnés à Mort Ex-Mineurs, CRC Non-Respectée",
            country="Iran",
            child_incarceration_score=92.0,
            adult_prosecution_minors_score=94.0,
            detention_conditions_minors_score=90.0,
            rehabilitation_gap_score=91.0,
            primary_pattern="adult_prosecution_minors",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-003",
            name="Nigéria — Almajiri/Enfants Rues Incarcérés, Prisons Adultes, Torture",
            country="Nigéria",
            child_incarceration_score=85.0,
            adult_prosecution_minors_score=83.0,
            detention_conditions_minors_score=87.0,
            rehabilitation_gap_score=82.0,
            primary_pattern="detention_conditions_minors",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-004",
            name="USA — JLWOP (Juvenile Life Without Parole), 44 000 Mineurs Incarcérés, Solitary",
            country="USA",
            child_incarceration_score=76.0,
            adult_prosecution_minors_score=78.0,
            detention_conditions_minors_score=74.0,
            rehabilitation_gap_score=72.0,
            primary_pattern="child_incarceration",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-005",
            name="Brésil — FUNABEM Héritage, 24 000 Mineurs FEBEM, Violence Systémique",
            country="Brésil",
            child_incarceration_score=56.0,
            adult_prosecution_minors_score=52.0,
            detention_conditions_minors_score=58.0,
            rehabilitation_gap_score=54.0,
            primary_pattern="detention_conditions_minors",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-006",
            name="Indonésie — Age Responsabilité 8 Ans, 3 000 Mineurs Prisons Adultes",
            country="Indonésie",
            child_incarceration_score=46.0,
            adult_prosecution_minors_score=48.0,
            detention_conditions_minors_score=44.0,
            rehabilitation_gap_score=42.0,
            primary_pattern="adult_prosecution_minors",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-007",
            name="UK — Age Responsabilité 10 Ans (Plus Bas UE), Rainsbrook STC Fermeture Tardive",
            country="UK",
            child_incarceration_score=28.0,
            adult_prosecution_minors_score=30.0,
            detention_conditions_minors_score=26.0,
            rehabilitation_gap_score=24.0,
            primary_pattern="child_incarceration",
        ),
        JuvenileJusticeRightsEntity(
            entity_id="JJR-008",
            name="Norvège/Belgique — Justice Restauratrice, Âge 15+, Centres Ouverts Réhabilitation",
            country="Norvège/Belgique",
            child_incarceration_score=6.0,
            adult_prosecution_minors_score=7.0,
            detention_conditions_minors_score=5.0,
            rehabilitation_gap_score=8.0,
            primary_pattern="rehabilitation_gap",
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

    return JuvenileJusticeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_juvenile_justice_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_juvenile_justice_global_report_2024",
            "hrw_children_adult_prisons_documentation",
            "un_crc_committee_juvenile_justice_2024",
            "penal_reform_international_youth_detention",
            "defense_for_children_international_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_juvenile_justice_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
