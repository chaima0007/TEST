from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EmergencyPowersAbuseEntity:
    entity_id: str
    name: str
    country: str
    democratic_oversight_suspension_score: float
    rights_derogation_breadth_score: float
    duration_proportionality_violation_score: float
    accountability_mechanism_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_emergency_powers_abuse_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.democratic_oversight_suspension_score * 0.30
            + self.rights_derogation_breadth_score * 0.25
            + self.duration_proportionality_violation_score * 0.25
            + self.accountability_mechanism_absence_score * 0.20,
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
        self.estimated_emergency_powers_abuse_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EmergencyPowersAbuseEngineResult:
    agent: str = "Emergency Powers Abuse Engine Agent"
    domain: str = "emergency_powers_abuse"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_emergency_powers_abuse_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EmergencyPowersAbuseEntity] = field(default_factory=list)

def run_emergency_powers_abuse_engine() -> EmergencyPowersAbuseEngineResult:
    entities = [
        EmergencyPowersAbuseEntity(
            entity_id="EP-001",
            name="Thaïlande — État Urgence 3 Ans Post-Coup, Art.44 Pouvoir Absolu & Lèse-Majesté",
            country="Asie du Sud-Est",
            democratic_oversight_suspension_score=95.0,
            rights_derogation_breadth_score=92.0,
            duration_proportionality_violation_score=95.0,
            accountability_mechanism_absence_score=90.0,
            primary_pattern="democratic_oversight_suspension",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-002",
            name="Turquie/Erdogan — État Urgence 2016-18, 150K Arrêtés, 150 Médias Fermés & Décrets",
            country="Moyen-Orient",
            democratic_oversight_suspension_score=92.0,
            rights_derogation_breadth_score=88.0,
            duration_proportionality_violation_score=90.0,
            accountability_mechanism_absence_score=88.0,
            primary_pattern="rights_derogation_breadth",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-003",
            name="Égypte/Sissi — État Urgence 4 Ans Continu 2017-21, 60K Prisonniers Pol. & Tribunaux Militaires",
            country="Afrique du Nord",
            democratic_oversight_suspension_score=88.0,
            rights_derogation_breadth_score=90.0,
            duration_proportionality_violation_score=88.0,
            accountability_mechanism_absence_score=88.0,
            primary_pattern="rights_derogation_breadth",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-004",
            name="Biélorussie/Loukachenko — Loi Extrémisme 2020, 35K Arrêtés & Répression Totale Manifestants",
            country="Europe de l'Est",
            democratic_oversight_suspension_score=85.0,
            rights_derogation_breadth_score=85.0,
            duration_proportionality_violation_score=88.0,
            accountability_mechanism_absence_score=82.0,
            primary_pattern="duration_proportionality_violation",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-005",
            name="Inde/AFSPA — Loi Pouvoirs Spéciaux Armée 60+ Ans Cachemire & Impunité Militaire",
            country="Asie du Sud",
            democratic_oversight_suspension_score=52.0,
            rights_derogation_breadth_score=55.0,
            duration_proportionality_violation_score=58.0,
            accountability_mechanism_absence_score=52.0,
            primary_pattern="duration_proportionality_violation",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-006",
            name="UE/Covid — Pouvoirs d'Urgence Pandémie, Hongrie Orban Sans Limite & Abus Droits",
            country="Europe",
            democratic_oversight_suspension_score=48.0,
            rights_derogation_breadth_score=52.0,
            duration_proportionality_violation_score=50.0,
            accountability_mechanism_absence_score=48.0,
            primary_pattern="rights_derogation_breadth",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-007",
            name="ICNL/Commission de Venise — Monitoring Pouvoirs Urgence & Standards Dérogations Légales",
            country="Global",
            democratic_oversight_suspension_score=22.0,
            rights_derogation_breadth_score=25.0,
            duration_proportionality_violation_score=28.0,
            accountability_mechanism_absence_score=30.0,
            primary_pattern="accountability_mechanism_absence",
        ),
        EmergencyPowersAbuseEntity(
            entity_id="EP-008",
            name="ONU/CCPR — Art.4 PIDCP Dérogations, Proportionnalité & Droits Non-Dérogeables",
            country="Global",
            democratic_oversight_suspension_score=4.0,
            rights_derogation_breadth_score=5.0,
            duration_proportionality_violation_score=3.0,
            accountability_mechanism_absence_score=6.0,
            primary_pattern="accountability_mechanism_absence",
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

    return EmergencyPowersAbuseEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_emergency_powers_abuse_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icnl_civic_freedom_monitor_emergency_powers_tracker",
            "venice_commission_emergency_legislation_standards",
            "human_rights_watch_covid_emergency_powers_abuse_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_emergency_powers_abuse_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_emergency_powers_abuse_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
