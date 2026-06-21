from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class CasteDiscriminationUntouchabilityEntity:
    entity_id: str
    name: str
    country: str
    caste_based_violence_atrocity_severity_score: float
    untouchability_practice_occupation_segregation_scale_score: float
    intercaste_marriage_honor_violence_score: float
    caste_affirmative_action_legal_protection_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_caste_discrimination_untouchability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.caste_based_violence_atrocity_severity_score * 0.30
            + self.untouchability_practice_occupation_segregation_scale_score * 0.25
            + self.intercaste_marriage_honor_violence_score * 0.25
            + self.caste_affirmative_action_legal_protection_deficit_gap_score * 0.20,
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
    confidence_score: float = 0.85
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
            name="Inde/Dalits — 165M Dalits Discrimination Systémique, 50 000 Atrocités/An PoA, Femmes Dalits 4× Viol & Manuels Scolaires Caste",
            country="Inde",
            caste_based_violence_atrocity_severity_score=95.0,
            untouchability_practice_occupation_segregation_scale_score=93.0,
            intercaste_marriage_honor_violence_score=92.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=94.0,
            primary_pattern="caste_based_violence_atrocity_severity",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-002",
            name="Népal/Dalit — Untouchability 1963 Formellement Aboli, Mariage Intercaste Violence 2000+ Cas/An, Caste Publique Affichée & Dalits Temples Interdits",
            country="Népal",
            caste_based_violence_atrocity_severity_score=91.0,
            untouchability_practice_occupation_segregation_scale_score=92.0,
            intercaste_marriage_honor_violence_score=88.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=90.0,
            primary_pattern="untouchability_practice_occupation_segregation_scale",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-003",
            name="Pakistan/Scheduled — Chrétiens-Hindous Sanitation Forcés, Travail Bonded 57% SC, Blasphème Dalits Ciblés & Mariages Forcés Minorités",
            country="Pakistan",
            caste_based_violence_atrocity_severity_score=87.0,
            untouchability_practice_occupation_segregation_scale_score=85.0,
            intercaste_marriage_honor_violence_score=88.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=86.0,
            primary_pattern="caste_based_violence_atrocity_severity",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-004",
            name="Sri Lanka/Rodiya — Castes Inférieures Rodiya Marginalisation, Système Jati Bouddhisme, Discrimination Emploi & Intermariage Violence",
            country="Sri Lanka",
            caste_based_violence_atrocity_severity_score=83.0,
            untouchability_practice_occupation_segregation_scale_score=82.0,
            intercaste_marriage_honor_violence_score=84.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=81.0,
            primary_pattern="intercaste_marriage_honor_violence",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-005",
            name="Japon/Burakumin — 1M Burakumin Discrimination Cachée, Bases Données Illégales Vente, Quartiers Évités & Mariage Refusé Enquêteurs",
            country="Japon",
            caste_based_violence_atrocity_severity_score=56.0,
            untouchability_practice_occupation_segregation_scale_score=54.0,
            intercaste_marriage_honor_violence_score=55.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=57.0,
            primary_pattern="untouchability_practice_occupation_segregation_scale",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-006",
            name="Afrique/Ostracisés — Osu Igbo Nigeria, Sab Somalie, Castes Wolof & Mande Discrimination Subsaharienne",
            country="Afrique",
            caste_based_violence_atrocity_severity_score=52.0,
            untouchability_practice_occupation_segregation_scale_score=51.0,
            intercaste_marriage_honor_violence_score=54.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=53.0,
            primary_pattern="caste_affirmative_action_legal_protection_deficit_gap",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-007",
            name="IDSN/NACDOR — International Dalit Solidarity Network, National Campaign Dalit HR, Résolution HRC & Principes Discrimination Caste ONU",
            country="Global",
            caste_based_violence_atrocity_severity_score=27.0,
            untouchability_practice_occupation_segregation_scale_score=25.0,
            intercaste_marriage_honor_violence_score=28.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=26.0,
            primary_pattern="caste_affirmative_action_legal_protection_deficit_gap",
        ),
        CasteDiscriminationUntouchabilityEntity(
            entity_id="CDU-008",
            name="ONU/CERD Caste — CERD Recommandation Générale 29 Caste 2002, HCDH Rapport Discrimination Ascendance & SDG 10 Inégalités",
            country="Global",
            caste_based_violence_atrocity_severity_score=4.0,
            untouchability_practice_occupation_segregation_scale_score=4.0,
            intercaste_marriage_honor_violence_score=4.0,
            caste_affirmative_action_legal_protection_deficit_gap_score=4.0,
            primary_pattern="caste_based_violence_atrocity_severity",
        ),
    ]

    return CasteDiscriminationUntouchabilityEngineResult(
        agent="Caste Discrimination Untouchability Engine Agent",
        domain="caste_discrimination_untouchability",
        entities=entities,
        data_sources=[
            "international_dalit_solidarity_network_report",
            "human_rights_watch_caste_discrimination_report",
            "un_cerd_descent_discrimination_report",
        ],
    )


if __name__ == "__main__":
    result = run_caste_discrimination_untouchability_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_caste_discrimination_untouchability_index}")
    print(f"Distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
