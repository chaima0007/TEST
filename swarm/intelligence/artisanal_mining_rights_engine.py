from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ArtisanalMiningRightsEntity:
    entity_id: str
    name: str
    country: str
    child_labor_exploitation_scale_score: float
    mercury_toxic_exposure_severity_score: float
    legal_formalization_absence_score: float
    armed_group_coercion_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_artisanal_mining_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.child_labor_exploitation_scale_score * 0.30
            + self.mercury_toxic_exposure_severity_score * 0.25
            + self.legal_formalization_absence_score * 0.25
            + self.armed_group_coercion_pattern_score * 0.20,
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
        self.estimated_artisanal_mining_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ArtisanalMiningRightsEngineResult:
    agent: str = "Artisanal Mining Rights Engine Agent"
    domain: str = "artisanal_mining_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_artisanal_mining_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArtisanalMiningRightsEntity] = field(default_factory=list)

def run_artisanal_mining_rights_engine() -> ArtisanalMiningRightsEngineResult:
    entities = [
        ArtisanalMiningRightsEntity(
            entity_id="AM-001",
            name="RDC — 150K Enfants Mines Cobalt Katanga, Travail Forcé, Accidents & Chaîne EV Non Tracée",
            country="Afrique Centrale",
            child_labor_exploitation_scale_score=95.0,
            mercury_toxic_exposure_severity_score=88.0,
            legal_formalization_absence_score=92.0,
            armed_group_coercion_pattern_score=95.0,
            primary_pattern="child_labor_exploitation_scale",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-002",
            name="Burkina Faso/Mali — Mines Or Artisanales, Groupes Armés Taxent Creuseurs & Enfants Recrutés",
            country="Afrique de l'Ouest",
            child_labor_exploitation_scale_score=88.0,
            mercury_toxic_exposure_severity_score=90.0,
            legal_formalization_absence_score=88.0,
            armed_group_coercion_pattern_score=92.0,
            primary_pattern="armed_group_coercion_pattern",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-003",
            name="Pérou — 70K Mineurs Or Madre de Dios, Mercure Contamination Amazonie & Déforestation 100K Ha",
            country="Amérique Latine",
            child_labor_exploitation_scale_score=82.0,
            mercury_toxic_exposure_severity_score=95.0,
            legal_formalization_absence_score=88.0,
            armed_group_coercion_pattern_score=78.0,
            primary_pattern="mercury_toxic_exposure_severity",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-004",
            name="Philippines — 200K Mineurs Or Mercure, Accidents Effondrements & Typhons Inondent Sites",
            country="Asie du Sud-Est",
            child_labor_exploitation_scale_score=85.0,
            mercury_toxic_exposure_severity_score=88.0,
            legal_formalization_absence_score=88.0,
            armed_group_coercion_pattern_score=75.0,
            primary_pattern="legal_formalization_absence",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-005",
            name="Tanzanie — Mines Tanzanite/Or, Travail Enfant, Effondrements & Absence Protection Travailleurs",
            country="Afrique de l'Est",
            child_labor_exploitation_scale_score=52.0,
            mercury_toxic_exposure_severity_score=55.0,
            legal_formalization_absence_score=55.0,
            armed_group_coercion_pattern_score=50.0,
            primary_pattern="child_labor_exploitation_scale",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-006",
            name="Colombie — Orpaillage Illégal, FARC Dissidents Contrôlent Zones, Déplacement & Mercure",
            country="Amérique Latine",
            child_labor_exploitation_scale_score=50.0,
            mercury_toxic_exposure_severity_score=48.0,
            legal_formalization_absence_score=52.0,
            armed_group_coercion_pattern_score=55.0,
            primary_pattern="armed_group_coercion_pattern",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-007",
            name="Alliance for Responsible Mining/ASM — Certification Fairtrade Or, Formalisation & Traçabilité",
            country="Global",
            child_labor_exploitation_scale_score=22.0,
            mercury_toxic_exposure_severity_score=28.0,
            legal_formalization_absence_score=25.0,
            armed_group_coercion_pattern_score=30.0,
            primary_pattern="legal_formalization_absence",
        ),
        ArtisanalMiningRightsEntity(
            entity_id="AM-008",
            name="OIT/Convention 176 Sécurité Mines — Protection ASM, SDG 8.7 Travail Enfant & ASGM Minamata",
            country="Global",
            child_labor_exploitation_scale_score=4.0,
            mercury_toxic_exposure_severity_score=5.0,
            legal_formalization_absence_score=3.0,
            armed_group_coercion_pattern_score=6.0,
            primary_pattern="mercury_toxic_exposure_severity",
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

    return ArtisanalMiningRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_artisanal_mining_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "alliance_responsible_mining_asm_global_mercury_child_labor_report",
            "pact_responsible_artisanal_mining_due_diligence_framework",
            "ilo_convention_176_mine_safety_artisanal_small_scale_mining",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_artisanal_mining_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_artisanal_mining_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
