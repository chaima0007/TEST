from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LandRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_scale_score: float
    indigenous_territorial_dispossession_score: float
    agroindustry_land_grab_score: float
    legal_remedy_access_failure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_scale_score * 0.30
            + self.indigenous_territorial_dispossession_score * 0.25
            + self.agroindustry_land_grab_score * 0.25
            + self.legal_remedy_access_failure_score * 0.20,
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
        self.estimated_land_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class LandRightsEngineResult:
    agent: str = "Land Rights Engine Agent"
    domain: str = "land_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_land_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LandRightsEntity] = field(default_factory=list)

def run_land_rights_engine() -> LandRightsEngineResult:
    entities = [
        LandRightsEntity(
            entity_id="LR-001",
            name="Brésil/Amazonie — Déforestation Terres Autochtones, Garimpeiros & Assassinats Défenseurs Fonciers",
            country="Amérique Latine",
            forced_eviction_scale_score=92.0,
            indigenous_territorial_dispossession_score=95.0,
            agroindustry_land_grab_score=90.0,
            legal_remedy_access_failure_score=88.0,
            primary_pattern="indigenous_territorial_dispossession",
        ),
        LandRightsEntity(
            entity_id="LR-002",
            name="Cambodge — Concessions Économiques ELC, Expulsions Forcées Villages & Impunité Investisseurs",
            country="Asie du Sud-Est",
            forced_eviction_scale_score=88.0,
            indigenous_territorial_dispossession_score=85.0,
            agroindustry_land_grab_score=88.0,
            legal_remedy_access_failure_score=85.0,
            primary_pattern="forced_eviction_scale",
        ),
        LandRightsEntity(
            entity_id="LR-003",
            name="Éthiopie — Expulsions Oromia/Gambela, Investisseurs Étrangers Terres & Déplacés Internes",
            country="Afrique de l'Est",
            forced_eviction_scale_score=85.0,
            indigenous_territorial_dispossession_score=82.0,
            agroindustry_land_grab_score=85.0,
            legal_remedy_access_failure_score=82.0,
            primary_pattern="agroindustry_land_grab",
        ),
        LandRightsEntity(
            entity_id="LR-004",
            name="Philippines — Conflits Ancestral Domain Mindanao, Militarisation Terres Autochtones & NPA",
            country="Asie du Sud-Est",
            forced_eviction_scale_score=80.0,
            indigenous_territorial_dispossession_score=82.0,
            agroindustry_land_grab_score=78.0,
            legal_remedy_access_failure_score=80.0,
            primary_pattern="indigenous_territorial_dispossession",
        ),
        LandRightsEntity(
            entity_id="LR-005",
            name="Colombie — Restitution Terres Loi 1448, Paramilitaires & Retards Justice Post-Conflit",
            country="Amérique Latine",
            forced_eviction_scale_score=52.0,
            indigenous_territorial_dispossession_score=55.0,
            agroindustry_land_grab_score=50.0,
            legal_remedy_access_failure_score=58.0,
            primary_pattern="legal_remedy_access_failure",
        ),
        LandRightsEntity(
            entity_id="LR-006",
            name="Kenya — Expulsions Maasai Loliondo, Tourisme Safari & Accès Terres Ancestrales Bloqué",
            country="Afrique de l'Est",
            forced_eviction_scale_score=48.0,
            indigenous_territorial_dispossession_score=55.0,
            agroindustry_land_grab_score=48.0,
            legal_remedy_access_failure_score=52.0,
            primary_pattern="indigenous_territorial_dispossession",
        ),
        LandRightsEntity(
            entity_id="LR-007",
            name="Land Watch/FIAN — Rapport Accaparement Terres, Directives Volontaires FAO & Réformes Foncières",
            country="Global",
            forced_eviction_scale_score=22.0,
            indigenous_territorial_dispossession_score=25.0,
            agroindustry_land_grab_score=28.0,
            legal_remedy_access_failure_score=30.0,
            primary_pattern="agroindustry_land_grab",
        ),
        LandRightsEntity(
            entity_id="LR-008",
            name="ONU/CESCR — Droit Logement Adéquat, Directives Expulsions & Rapporteur Spécial Logement",
            country="Global",
            forced_eviction_scale_score=4.0,
            indigenous_territorial_dispossession_score=5.0,
            agroindustry_land_grab_score=3.0,
            legal_remedy_access_failure_score=6.0,
            primary_pattern="legal_remedy_access_failure",
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

    return LandRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_land_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_land_defenders_killings_annual_report",
            "land_matrix_initiative_global_land_deal_database",
            "fao_voluntary_guidelines_responsible_governance_tenure_implementation_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_land_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_land_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
