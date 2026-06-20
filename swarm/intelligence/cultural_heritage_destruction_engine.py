from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CulturalHeritageDestructionEntity:
    entity_id: str
    name: str
    country: str
    deliberate_destruction_scale_score: float
    looting_trafficking_score: float
    cultural_identity_erasure_score: float
    impunity_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_cultural_heritage_destruction_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.deliberate_destruction_scale_score * 0.30
            + self.looting_trafficking_score * 0.25
            + self.cultural_identity_erasure_score * 0.25
            + self.impunity_accountability_gap_score * 0.20,
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
        self.estimated_cultural_heritage_destruction_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CulturalHeritageDestructionEngineResult:
    agent: str = "Cultural Heritage Destruction Engine Agent"
    domain: str = "cultural_heritage_destruction"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.82
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_cultural_heritage_destruction_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CulturalHeritageDestructionEntity] = field(default_factory=list)

def run_cultural_heritage_destruction_engine() -> CulturalHeritageDestructionEngineResult:
    entities = [
        CulturalHeritageDestructionEntity(
            entity_id="CHD-001",
            name="Irak/Syrie/Daech — Palmyre, Nimroud, Bibliothèque Mossoul & Destruction Systématique",
            country="Moyen-Orient",
            deliberate_destruction_scale_score=95.0,
            looting_trafficking_score=90.0,
            cultural_identity_erasure_score=92.0,
            impunity_accountability_gap_score=88.0,
            primary_pattern="deliberate_destruction_scale",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-002",
            name="Chine/Tibet/Ouïghours — Mosquées Rasées, Monastères Détruits & Sinisation Culturelle",
            country="Asie du Nord-Est",
            deliberate_destruction_scale_score=85.0,
            looting_trafficking_score=72.0,
            cultural_identity_erasure_score=92.0,
            impunity_accountability_gap_score=80.0,
            primary_pattern="cultural_identity_erasure",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-003",
            name="Mali/Tombouctou — Mausolées UNESCO, Manuscrits Brûlés & Destruction Ansar Dine",
            country="Afrique Sub-Saharienne",
            deliberate_destruction_scale_score=82.0,
            looting_trafficking_score=85.0,
            cultural_identity_erasure_score=88.0,
            impunity_accountability_gap_score=90.0,
            primary_pattern="impunity_accountability_gap",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-004",
            name="Yémen — Patrimoine Millénaire, Bombardements Sana'a, Marib Pillés & Guerre Coalition",
            country="Moyen-Orient",
            deliberate_destruction_scale_score=80.0,
            looting_trafficking_score=78.0,
            cultural_identity_erasure_score=82.0,
            impunity_accountability_gap_score=85.0,
            primary_pattern="looting_trafficking",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-005",
            name="Ukraine — Patrimoine Détruit par Russie, Monuments Volés & Effacement Identité",
            country="Europe de l'Est",
            deliberate_destruction_scale_score=55.0,
            looting_trafficking_score=58.0,
            cultural_identity_erasure_score=52.0,
            impunity_accountability_gap_score=50.0,
            primary_pattern="deliberate_destruction_scale",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-006",
            name="Afghanistan/Bamiyan — Bouddhas Détruits Taliban, Trafic Antiquités & Insécurité Totale",
            country="Asie Centrale",
            deliberate_destruction_scale_score=52.0,
            looting_trafficking_score=60.0,
            cultural_identity_erasure_score=50.0,
            impunity_accountability_gap_score=55.0,
            primary_pattern="looting_trafficking",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-007",
            name="Musées Occident — Restitution Coloniale, Bronzes Bénin, Elgin Marbles & Blocage Légal",
            country="Europe/Amérique du Nord",
            deliberate_destruction_scale_score=22.0,
            looting_trafficking_score=35.0,
            cultural_identity_erasure_score=30.0,
            impunity_accountability_gap_score=28.0,
            primary_pattern="cultural_identity_erasure",
        ),
        CulturalHeritageDestructionEntity(
            entity_id="CHD-008",
            name="UNESCO/INTERPOL/CPI — Convention 1954, Résolution Al-Mahdi, ALIPH & Bouclier Bleu",
            country="Global",
            deliberate_destruction_scale_score=4.0,
            looting_trafficking_score=5.0,
            cultural_identity_erasure_score=3.0,
            impunity_accountability_gap_score=6.0,
            primary_pattern="deliberate_destruction_scale",
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

    return CulturalHeritageDestructionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_cultural_heritage_destruction_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unesco_report_on_illicit_trafficking_cultural_property_annual",
            "interpol_works_of_art_unit_stolen_cultural_property_global_report",
            "aliph_international_alliance_protection_heritage_conflict_areas_annual",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_cultural_heritage_destruction_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_cultural_heritage_destruction_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
