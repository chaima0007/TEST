from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MedicalNeutralityEntity:
    entity_id: str
    name: str
    country: str
    attacks_medical_facilities_score: float
    healthcare_workers_targeting_score: float
    medical_access_denial_score: float
    accountability_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_medical_neutrality_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.attacks_medical_facilities_score * 0.30
            + self.healthcare_workers_targeting_score * 0.25
            + self.medical_access_denial_score * 0.25
            + self.accountability_impunity_score * 0.20,
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
        self.estimated_medical_neutrality_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MedicalNeutralityEngineResult:
    agent: str = "Medical Neutrality Engine Agent"
    domain: str = "medical_neutrality"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_medical_neutrality_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MedicalNeutralityEntity] = field(default_factory=list)

def run_medical_neutrality_engine() -> MedicalNeutralityEngineResult:
    entities = [
        MedicalNeutralityEntity(
            entity_id="MN-001",
            name="Syrie — 600+ Hôpitaux Bombardés, Barrel Bombs Assad & Double-Tap sur Secouristes",
            country="Moyen-Orient",
            attacks_medical_facilities_score=92.0,
            healthcare_workers_targeting_score=90.0,
            medical_access_denial_score=95.0,
            accountability_impunity_score=88.0,
            primary_pattern="medical_access_denial",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-002",
            name="Gaza/Palestine — Hôpitaux Al-Shifa/Al-Ahli Détruits, Pénurie Médicale & Médecins Tués",
            country="Moyen-Orient",
            attacks_medical_facilities_score=90.0,
            healthcare_workers_targeting_score=85.0,
            medical_access_denial_score=92.0,
            accountability_impunity_score=88.0,
            primary_pattern="medical_access_denial",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-003",
            name="Yémen — Frappes Hôpitaux Coalition Saoudienne, Choléra & Blocus Médicaments",
            country="Moyen-Orient",
            attacks_medical_facilities_score=88.0,
            healthcare_workers_targeting_score=90.0,
            medical_access_denial_score=88.0,
            accountability_impunity_score=85.0,
            primary_pattern="healthcare_workers_targeting",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-004",
            name="Ukraine — Hôpitaux Marioupol/Kherson Bombardés, MSF Évacuations & Crimes de Guerre Russes",
            country="Europe de l'Est",
            attacks_medical_facilities_score=78.0,
            healthcare_workers_targeting_score=80.0,
            medical_access_denial_score=75.0,
            accountability_impunity_score=82.0,
            primary_pattern="accountability_impunity",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-005",
            name="Éthiopie/Tigré — Cliniques Pillées, Viol Personnel Médical & Famine Obstruction Aide",
            country="Afrique Sub-Saharienne",
            attacks_medical_facilities_score=52.0,
            healthcare_workers_targeting_score=58.0,
            medical_access_denial_score=55.0,
            accountability_impunity_score=50.0,
            primary_pattern="healthcare_workers_targeting",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-006",
            name="Myanmar — Raids Militaires Cliniques, Médecins Arrêtés & Soins Refusés Minorités",
            country="Asie du Sud-Est",
            attacks_medical_facilities_score=50.0,
            healthcare_workers_targeting_score=55.0,
            medical_access_denial_score=52.0,
            accountability_impunity_score=48.0,
            primary_pattern="attacks_medical_facilities",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-007",
            name="MSF/CICR — Reporting Violations, Safe Access Négociations & Plaidoyer Humanitaire",
            country="Global",
            attacks_medical_facilities_score=22.0,
            healthcare_workers_targeting_score=28.0,
            medical_access_denial_score=30.0,
            accountability_impunity_score=25.0,
            primary_pattern="attacks_medical_facilities",
        ),
        MedicalNeutralityEntity(
            entity_id="MN-008",
            name="ONU/OMS — Résolution WHA65.20, Monitoring SSA & Mécanisme Rapportage Attaques",
            country="Global",
            attacks_medical_facilities_score=4.0,
            healthcare_workers_targeting_score=5.0,
            medical_access_denial_score=3.0,
            accountability_impunity_score=6.0,
            primary_pattern="accountability_impunity",
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

    return MedicalNeutralityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_medical_neutrality_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "physicians_for_human_rights_attack_on_health_care_global_report",
            "msf_not_a_target_attacks_hospitals_healthcare_conflict_report",
            "who_ssa_surveillance_system_attacks_healthcare_database",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_medical_neutrality_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_medical_neutrality_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
