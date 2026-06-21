from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IndigenousCulturalGenocideAssimilationEntity:
    entity_id: str
    name: str
    country: str
    forced_assimilation_child_removal_severity_score: float
    language_cultural_suppression_scale_score: float
    territorial_dispossession_violence_score: float
    state_accountability_reparations_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_cultural_genocide_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_assimilation_child_removal_severity_score * 0.30
            + self.language_cultural_suppression_scale_score * 0.25
            + self.territorial_dispossession_violence_score * 0.25
            + self.state_accountability_reparations_gap_score * 0.20,
            2,
        )
        if self.composite_score >= 65:
            self.risk_level = "critique"
        elif self.composite_score >= 45:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_indigenous_cultural_genocide_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class IndigenousCulturalGenocideAssimilationEngineResult:
    agent: str = "Indigenous Cultural Genocide Assimilation Engine Agent"
    domain: str = "indigenous_cultural_genocide_assimilation"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_cultural_genocide_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousCulturalGenocideAssimilationEntity] = field(default_factory=list)


def run_indigenous_cultural_genocide_assimilation_engine() -> IndigenousCulturalGenocideAssimilationEngineResult:
    entities = [
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-001",
            name="Canada/Pensionnats 150 000 Enfants Arrachés — Politique Assimilation 1831-1996, 3213 Décès Confirmés Tombes",
            country="Canada",
            forced_assimilation_child_removal_severity_score=93.0,
            language_cultural_suppression_scale_score=91.0,
            territorial_dispossession_violence_score=88.0,
            state_accountability_reparations_gap_score=72.0,
            primary_pattern="forced_assimilation_child_removal_severity",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-002",
            name="Australie/Stolen Generation Politique Assimilation — 100 000 Enfants Mêlés Retirés 1910-1970, Dommages Générationnels",
            country="Australie",
            forced_assimilation_child_removal_severity_score=91.0,
            language_cultural_suppression_scale_score=89.0,
            territorial_dispossession_violence_score=90.0,
            state_accountability_reparations_gap_score=68.0,
            primary_pattern="forced_assimilation_child_removal_severity",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-003",
            name="USA/Boarding Schools 50 000 Enfants Autochtones — Kill Indian Save Man, 50+ Écoles Fédérales, Abus Systémiques",
            country="USA",
            forced_assimilation_child_removal_severity_score=89.0,
            language_cultural_suppression_scale_score=87.0,
            territorial_dispossession_violence_score=85.0,
            state_accountability_reparations_gap_score=83.0,
            primary_pattern="forced_assimilation_child_removal_severity",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-004",
            name="Chine/Internats Tibétains Séparation Familles — 800 000+ Enfants Tibétains Retirés 2019-2024, Sinisation Forcée",
            country="Chine",
            forced_assimilation_child_removal_severity_score=95.0,
            language_cultural_suppression_scale_score=96.0,
            territorial_dispossession_violence_score=92.0,
            state_accountability_reparations_gap_score=97.0,
            primary_pattern="state_accountability_reparations_gap",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-005",
            name="Brésil/Amazonie Garimpeiros Yanomami — Orpaillage Illégal Mercure, 570 Morts 2021-2023, Terres Envahies",
            country="Brésil",
            forced_assimilation_child_removal_severity_score=48.0,
            language_cultural_suppression_scale_score=52.0,
            territorial_dispossession_violence_score=60.0,
            state_accountability_reparations_gap_score=55.0,
            primary_pattern="territorial_dispossession_violence",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-006",
            name="Colombie/Peuples Isolés FARC Territoires — Dissidences FARC ELN Envahissent Terres Sacrées, 100+ Peuples Menacés",
            country="Colombie",
            forced_assimilation_child_removal_severity_score=52.0,
            language_cultural_suppression_scale_score=58.0,
            territorial_dispossession_violence_score=68.0,
            state_accountability_reparations_gap_score=62.0,
            primary_pattern="territorial_dispossession_violence",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-007",
            name="Bolivie/Droits Constitutionnels Modèle — 36 Peuples Reconnus Constitution 2009, Terres Collectives Garanties",
            country="Bolivie",
            forced_assimilation_child_removal_severity_score=22.0,
            language_cultural_suppression_scale_score=18.0,
            territorial_dispossession_violence_score=25.0,
            state_accountability_reparations_gap_score=20.0,
            primary_pattern="forced_assimilation_child_removal_severity",
        ),
        IndigenousCulturalGenocideAssimilationEntity(
            entity_id="ICG-008",
            name="Nouvelle-Zélande/Traité Waitangi Modèle — Maori Co-Gouvernance 1840, Revitalisation Langue Te Reo, Tribunaux Actifs",
            country="Nouvelle-Zélande",
            forced_assimilation_child_removal_severity_score=8.0,
            language_cultural_suppression_scale_score=6.0,
            territorial_dispossession_violence_score=7.0,
            state_accountability_reparations_gap_score=5.0,
            primary_pattern="forced_assimilation_child_removal_severity",
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

    dist = {"critique": risk_dist.get("critique", 0), "élevé": risk_dist.get("élevé", 0),
            "modéré": risk_dist.get("modéré", 0), "faible": risk_dist.get("faible", 0)}
    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"

    return IndigenousCulturalGenocideAssimilationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_cultural_genocide_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "nctr_canada_final_report_truth_reconciliation_commission",
            "bring_them_home_report_australia_stolen_generation_1997",
            "un_special_rapporteur_indigenous_peoples_cultural_genocide",
            "human_rights_watch_china_tibet_boarding_schools_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_indigenous_cultural_genocide_assimilation_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_indigenous_cultural_genocide_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
