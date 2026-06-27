from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ConscientiousObjectorRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_prosecution_scale_score: float
    alternative_service_availability_score: float
    legal_recognition_gap_score: float
    persecution_harassment_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_conscientious_objector_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_prosecution_scale_score * 0.30
            + self.alternative_service_availability_score * 0.25
            + self.legal_recognition_gap_score * 0.25
            + self.persecution_harassment_pattern_score * 0.20,
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
        self.estimated_conscientious_objector_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ConscientiousObjectorRightsEngineResult:
    agent: str = "Conscientious Objector Rights Engine Agent"
    domain: str = "conscientious_objector_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_conscientious_objector_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ConscientiousObjectorRightsEntity] = field(default_factory=list)

def run_conscientious_objector_rights_engine() -> ConscientiousObjectorRightsEngineResult:
    entities = [
        ConscientiousObjectorRightsEntity(
            entity_id="CO-001",
            name="Russie — Objecteurs Ukraine Emprisonnés, Mobilisation Forcée 300K & Torture Rapportée",
            country="Europe de l'Est",
            criminalization_prosecution_scale_score=95.0,
            alternative_service_availability_score=92.0,
            legal_recognition_gap_score=95.0,
            persecution_harassment_pattern_score=92.0,
            primary_pattern="legal_recognition_gap",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-002",
            name="Corée du Sud — 600+ Emprisonnements/An Témoins Jéhovah & CDH ONU Condamné 18 Fois",
            country="Asie de l'Est",
            criminalization_prosecution_scale_score=90.0,
            alternative_service_availability_score=88.0,
            legal_recognition_gap_score=92.0,
            persecution_harassment_pattern_score=90.0,
            primary_pattern="criminalization_prosecution_scale",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-003",
            name="Érythrée — Conscription à Vie, Objecteurs Camp Sawa Torturés & Fuite Massive vers Europe",
            country="Afrique de l'Est",
            criminalization_prosecution_scale_score=88.0,
            alternative_service_availability_score=90.0,
            legal_recognition_gap_score=88.0,
            persecution_harassment_pattern_score=88.0,
            primary_pattern="alternative_service_availability",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-004",
            name="Turquie — Aucune Loi OC Reconnue, Poursuites Répétées Büyükanıt & CEDH Condamné 15x",
            country="Moyen-Orient",
            criminalization_prosecution_scale_score=85.0,
            alternative_service_availability_score=85.0,
            legal_recognition_gap_score=88.0,
            persecution_harassment_pattern_score=85.0,
            primary_pattern="legal_recognition_gap",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-005",
            name="Israël — OC Partiel, Prisonniers Conscience Femmes Bédouines & Traitement Discriminatoire",
            country="Moyen-Orient",
            criminalization_prosecution_scale_score=55.0,
            alternative_service_availability_score=52.0,
            legal_recognition_gap_score=55.0,
            persecution_harassment_pattern_score=52.0,
            primary_pattern="persecution_harassment_pattern",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-006",
            name="Grèce — Service Civil Punitif 2x Militaire, Réforme 2019 Incomplète & Discrimination Persist.",
            country="Europe",
            alternative_service_availability_score=48.0,
            criminalization_prosecution_scale_score=50.0,
            legal_recognition_gap_score=50.0,
            persecution_harassment_pattern_score=50.0,
            primary_pattern="alternative_service_availability",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-007",
            name="War Resisters International/Amnesty — Monitoring OC Global, Prisonniers Conscience & Plaidoyer",
            country="Global",
            criminalization_prosecution_scale_score=22.0,
            alternative_service_availability_score=28.0,
            legal_recognition_gap_score=25.0,
            persecution_harassment_pattern_score=30.0,
            primary_pattern="persecution_harassment_pattern",
        ),
        ConscientiousObjectorRightsEntity(
            entity_id="CO-008",
            name="ONU/CDH — Résolution 1998/77 Objection Conscience, CCPR Art.18 & Comité Droits Humains",
            country="Global",
            criminalization_prosecution_scale_score=4.0,
            alternative_service_availability_score=5.0,
            legal_recognition_gap_score=3.0,
            persecution_harassment_pattern_score=6.0,
            primary_pattern="legal_recognition_gap",
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

    return ConscientiousObjectorRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_conscientious_objector_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "war_resisters_international_conscientious_objection_country_report",
            "amnesty_international_prisoners_of_conscience_conscription_report",
            "un_commission_human_rights_resolution_conscientious_objection",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_conscientious_objector_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_conscientious_objector_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
