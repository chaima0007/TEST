from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IndigenousRightsEntity:
    entity_id: str
    name: str
    country: str
    territorial_dispossession_score: float
    fpic_violation_scale_score: float
    cultural_linguistic_erasure_score: float
    undrip_implementation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.territorial_dispossession_score * 0.30
            + self.fpic_violation_scale_score * 0.25
            + self.cultural_linguistic_erasure_score * 0.25
            + self.undrip_implementation_gap_score * 0.20,
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
        self.estimated_indigenous_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class IndigenousRightsEngineResult:
    agent: str = "Indigenous Rights Engine Agent"
    domain: str = "indigenous_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousRightsEntity] = field(default_factory=list)

def run_indigenous_rights_engine() -> IndigenousRightsEngineResult:
    entities = [
        IndigenousRightsEntity(
            entity_id="IR-001",
            name="Brésil/Amazonie — Garimpeiros Invasions, Yanomami Génocide Lent & Démantèlement FUNAI",
            country="Amérique Latine",
            territorial_dispossession_score=95.0,
            fpic_violation_scale_score=92.0,
            cultural_linguistic_erasure_score=88.0,
            undrip_implementation_gap_score=92.0,
            primary_pattern="territorial_dispossession",
        ),
        IndigenousRightsEntity(
            entity_id="IR-002",
            name="Canada — Pensionnats Génocide Culturel, 215 Enfants Kamloops & MMIWG Non Résolus",
            country="Amérique du Nord",
            territorial_dispossession_score=88.0,
            fpic_violation_scale_score=85.0,
            cultural_linguistic_erasure_score=92.0,
            undrip_implementation_gap_score=88.0,
            primary_pattern="cultural_linguistic_erasure",
        ),
        IndigenousRightsEntity(
            entity_id="IR-003",
            name="Australie — Uluru Statement Ignoré, Surincarcération Aborigène & Terres Non Restituées",
            country="Océanie",
            territorial_dispossession_score=85.0,
            fpic_violation_scale_score=82.0,
            cultural_linguistic_erasure_score=85.0,
            undrip_implementation_gap_score=85.0,
            primary_pattern="territorial_dispossession",
        ),
        IndigenousRightsEntity(
            entity_id="IR-004",
            name="Philippines — Projets Miniers FPIC Bafoués, Défenseurs Terres Assassinés & Militarisation",
            country="Asie du Sud-Est",
            territorial_dispossession_score=82.0,
            fpic_violation_scale_score=88.0,
            cultural_linguistic_erasure_score=78.0,
            undrip_implementation_gap_score=82.0,
            primary_pattern="fpic_violation_scale",
        ),
        IndigenousRightsEntity(
            entity_id="IR-005",
            name="USA — Dakota Access Pipeline, Standing Rock Répression & Réserves Sous-financées",
            country="Amérique du Nord",
            territorial_dispossession_score=55.0,
            fpic_violation_scale_score=58.0,
            cultural_linguistic_erasure_score=52.0,
            undrip_implementation_gap_score=50.0,
            primary_pattern="fpic_violation_scale",
        ),
        IndigenousRightsEntity(
            entity_id="IR-006",
            name="Norvège/Sápmi — Éoliennes Fosen FPIC Non Respecté, Jeûne Sami & Arrêt Cour Non Appliqué",
            country="Europe du Nord",
            territorial_dispossession_score=48.0,
            fpic_violation_scale_score=55.0,
            cultural_linguistic_erasure_score=48.0,
            undrip_implementation_gap_score=52.0,
            primary_pattern="fpic_violation_scale",
        ),
        IndigenousRightsEntity(
            entity_id="IR-007",
            name="IWGIA/Forest Peoples Programme — Réseau Mondial, Documentation & Plaidoyer UNDRIP",
            country="Global",
            territorial_dispossession_score=22.0,
            fpic_violation_scale_score=25.0,
            cultural_linguistic_erasure_score=28.0,
            undrip_implementation_gap_score=30.0,
            primary_pattern="territorial_dispossession",
        ),
        IndigenousRightsEntity(
            entity_id="IR-008",
            name="ONU/UNDRIP — Déclaration Droits Peuples Autochtones 2007, Instance Permanente & Rapporteur",
            country="Global",
            territorial_dispossession_score=4.0,
            fpic_violation_scale_score=5.0,
            cultural_linguistic_erasure_score=3.0,
            undrip_implementation_gap_score=6.0,
            primary_pattern="undrip_implementation_gap",
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

    return IndigenousRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "iwgia_indigenous_world_annual_report",
            "un_special_rapporteur_indigenous_peoples_country_visits_reports",
            "forest_peoples_programme_fpic_violations_global_tracker",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_indigenous_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_indigenous_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
