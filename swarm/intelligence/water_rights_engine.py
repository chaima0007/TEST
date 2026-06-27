from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WaterRightsEntity:
    entity_id: str
    name: str
    country: str
    access_denial_scale_score: float
    privatization_commodification_score: float
    pollution_industrial_contamination_score: float
    transboundary_conflict_governance_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_water_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.access_denial_scale_score * 0.30
            + self.privatization_commodification_score * 0.25
            + self.pollution_industrial_contamination_score * 0.25
            + self.transboundary_conflict_governance_score * 0.20,
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
        self.estimated_water_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class WaterRightsEngineResult:
    agent: str = "Water Rights Engine Agent"
    domain: str = "water_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_water_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WaterRightsEntity] = field(default_factory=list)

def run_water_rights_engine() -> WaterRightsEngineResult:
    entities = [
        WaterRightsEntity(
            entity_id="WR-001",
            name="Gaza/Palestine — Blocus Eau, Infrastructures Détruites, 90% Eau Non Potable & Déshydratation",
            country="Moyen-Orient",
            access_denial_scale_score=95.0,
            privatization_commodification_score=82.0,
            pollution_industrial_contamination_score=92.0,
            transboundary_conflict_governance_score=95.0,
            primary_pattern="access_denial_scale",
        ),
        WaterRightsEntity(
            entity_id="WR-002",
            name="Yémen — Guerre Infrastructures Eau, Choléra 2.5M Cas & Puits Bombardés",
            country="Moyen-Orient",
            access_denial_scale_score=92.0,
            privatization_commodification_score=78.0,
            pollution_industrial_contamination_score=88.0,
            transboundary_conflict_governance_score=90.0,
            primary_pattern="access_denial_scale",
        ),
        WaterRightsEntity(
            entity_id="WR-003",
            name="Afrique Sub-Saharienne — 400M Sans Eau Potable, Marche 6h/jour & Maladies Hydriques",
            country="Afrique Sub-Saharienne",
            access_denial_scale_score=88.0,
            privatization_commodification_score=85.0,
            pollution_industrial_contamination_score=82.0,
            transboundary_conflict_governance_score=80.0,
            primary_pattern="privatization_commodification",
        ),
        WaterRightsEntity(
            entity_id="WR-004",
            name="Bolivie/Cochabamba — Privatisation Suez, Guerre de l'Eau 2000 & Multinationales Ressources",
            country="Amérique Latine",
            access_denial_scale_score=80.0,
            privatization_commodification_score=88.0,
            pollution_industrial_contamination_score=75.0,
            transboundary_conflict_governance_score=78.0,
            primary_pattern="privatization_commodification",
        ),
        WaterRightsEntity(
            entity_id="WR-005",
            name="Inde/Gange — Pollution Industrielle, Sécheresses Agricoles & Tensions Inter-États",
            country="Asie du Sud",
            access_denial_scale_score=52.0,
            privatization_commodification_score=50.0,
            pollution_industrial_contamination_score=58.0,
            transboundary_conflict_governance_score=52.0,
            primary_pattern="pollution_industrial_contamination",
        ),
        WaterRightsEntity(
            entity_id="WR-006",
            name="Nil/Barrage GERD — Éthiopie vs Égypte/Soudan, Traités Obsolètes & Crise Hydropolitique",
            country="Afrique du Nord-Est",
            access_denial_scale_score=48.0,
            privatization_commodification_score=45.0,
            pollution_industrial_contamination_score=50.0,
            transboundary_conflict_governance_score=58.0,
            primary_pattern="transboundary_conflict_governance",
        ),
        WaterRightsEntity(
            entity_id="WR-007",
            name="Water Justice Movement — Coalition Mondiale, Déprivatisation & Droit Constitutionnel Eau",
            country="Global",
            access_denial_scale_score=22.0,
            privatization_commodification_score=28.0,
            pollution_industrial_contamination_score=25.0,
            transboundary_conflict_governance_score=30.0,
            primary_pattern="access_denial_scale",
        ),
        WaterRightsEntity(
            entity_id="WR-008",
            name="ONU/Résolution 64/292 — Droit Humain à l'Eau 2010, Rapporteur Spécial & Mécanismes Suivi",
            country="Global",
            access_denial_scale_score=4.0,
            privatization_commodification_score=5.0,
            pollution_industrial_contamination_score=3.0,
            transboundary_conflict_governance_score=6.0,
            primary_pattern="transboundary_conflict_governance",
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

    return WaterRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_water_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_water_sanitation_annual_reports",
            "water_justice_coalition_global_privatization_audit",
            "who_unicef_jmp_water_sanitation_hygiene_progress_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_water_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_water_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
