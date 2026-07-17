"""Caste Discrimination Untouchability Engine — Pratiques d'intouchabilité, ségrégation caste, violence intersectionnelle Dalit."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class CasteDiscriminationUntouchabilityEntity:
    entity_id: str
    name: str
    country: str
    untouchability_practice_violence_score: float
    caste_based_segregation_exclusion_score: float
    dalit_women_intersectional_violence_score: float
    caste_legal_protection_enforcement_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_caste_discrimination_untouchability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.untouchability_practice_violence_score * 0.30
            + self.caste_based_segregation_exclusion_score * 0.25
            + self.dalit_women_intersectional_violence_score * 0.25
            + self.caste_legal_protection_enforcement_deficit_score * 0.20,
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
        self.estimated_caste_discrimination_untouchability_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class CasteDiscriminationUntouchabilityEngineResult:
    agent: str
    domain: str
    entities: List[CasteDiscriminationUntouchabilityEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_caste_discrimination_untouchability_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.87
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_caste_discrimination_untouchability_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_caste_discrimination_untouchability_engine() -> CasteDiscriminationUntouchabilityEngineResult:
    entities = [
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-001",
            name="Inde/Dalits 200M — 50 000 Atrocités/An PoA, Femmes Dalits 4× Viol, Ségrégation Villages & Manuels Scolaires Caste",
            country="Inde",
            untouchability_practice_violence_score=92.0,
            caste_based_segregation_exclusion_score=90.0,
            dalit_women_intersectional_violence_score=88.0,
            caste_legal_protection_enforcement_deficit_score=85.0,
            primary_pattern="untouchability_practice_violence",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-002",
            name="Népal/Castes Impures — Untouchability Formellement Aboli 1963, Mariages Intercaste Violence 2000+ Cas/An & Temples Interdits",
            country="Népal",
            untouchability_practice_violence_score=85.0,
            caste_based_segregation_exclusion_score=82.0,
            dalit_women_intersectional_violence_score=88.0,
            caste_legal_protection_enforcement_deficit_score=80.0,
            primary_pattern="dalit_women_intersectional_violence",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-003",
            name="Pakistan/Scheduled Castes — Chrétiens-Hindous Sanitation Forcés, Travail Bonded 57% SC, Blasphème Ciblé & Mariages Forcés",
            country="Pakistan",
            untouchability_practice_violence_score=80.0,
            caste_based_segregation_exclusion_score=78.0,
            dalit_women_intersectional_violence_score=82.0,
            caste_legal_protection_enforcement_deficit_score=75.0,
            primary_pattern="caste_based_segregation_exclusion",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-004",
            name="Sri Lanka/Rodiya Castes — Castes Inférieures Rodiya Marginalisation, Système Jati Bouddhisme & Discrimination Emploi Persistante",
            country="Sri Lanka",
            untouchability_practice_violence_score=75.0,
            caste_based_segregation_exclusion_score=72.0,
            dalit_women_intersectional_violence_score=78.0,
            caste_legal_protection_enforcement_deficit_score=70.0,
            primary_pattern="untouchability_practice_violence",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-005",
            name="Bangladesh/Namasudra — Castes Inférieures Discrimination Persistante, Violences Électorales, Exode Hindous & Justice Limitée",
            country="Bangladesh",
            untouchability_practice_violence_score=55.0,
            caste_based_segregation_exclusion_score=52.0,
            dalit_women_intersectional_violence_score=58.0,
            caste_legal_protection_enforcement_deficit_score=50.0,
            primary_pattern="dalit_women_intersectional_violence",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-006",
            name="Japon/Burakumin — 1M Burakumin Discrimination Cachée, Bases Données Illégales Vente, Quartiers Évités & Mariages Refusés",
            country="Japon",
            untouchability_practice_violence_score=45.0,
            caste_based_segregation_exclusion_score=48.0,
            dalit_women_intersectional_violence_score=42.0,
            caste_legal_protection_enforcement_deficit_score=50.0,
            primary_pattern="caste_based_segregation_exclusion",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-007",
            name="USA/Discrimination Caste Diaspora — Communautés Sud-Asiatiques, Plaintes EEOC, Lois Californie & Documentation Equality Labs",
            country="USA",
            untouchability_practice_violence_score=25.0,
            caste_based_segregation_exclusion_score=28.0,
            dalit_women_intersectional_violence_score=22.0,
            caste_legal_protection_enforcement_deficit_score=30.0,
            primary_pattern="caste_legal_protection_enforcement_deficit",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-008",
            name="Royaume-Uni/Loi Égalité Caste 2010 — Protection Juridique Adoptée, Jurisprudence Établie & Modèle Législatif Diaspora",
            country="Royaume-Uni",
            untouchability_practice_violence_score=5.0,
            caste_based_segregation_exclusion_score=6.0,
            dalit_women_intersectional_violence_score=4.0,
            caste_legal_protection_enforcement_deficit_score=8.0,
            primary_pattern="caste_legal_protection_enforcement_deficit",
        ),
    ]

    return CasteDiscriminationUntouchabilityEngineResult(
        agent="Caste Discrimination Untouchability Engine Agent",
        domain="caste_discrimination_untouchability",
        entities=entities,
        data_sources=[
            "human_rights_watch_caste_discrimination_2023",
            "equality_labs_caste_report_2023",
            "international_dalit_solidarity_network_2023",
            "un_special_rapporteur_minority_rights_caste_2023",
        ],
    )


if __name__ == "__main__":
    result = run_caste_discrimination_untouchability_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_caste_discrimination_untouchability_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
