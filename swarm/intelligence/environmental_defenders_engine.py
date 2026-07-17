from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EnvironmentalDefendersEntity:
    entity_id: str
    name: str
    country: str
    killings_disappearances_score: float
    criminalization_prosecution_score: float
    corporate_state_collusion_score: float
    impunity_justice_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_defenders_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.killings_disappearances_score * 0.30
            + self.criminalization_prosecution_score * 0.25
            + self.corporate_state_collusion_score * 0.25
            + self.impunity_justice_denial_score * 0.20,
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
        self.estimated_environmental_defenders_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EnvironmentalDefendersEngineResult:
    agent: str = "Environmental Defenders Engine Agent"
    domain: str = "environmental_defenders"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_defenders_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalDefendersEntity] = field(default_factory=list)

def run_environmental_defenders_engine() -> EnvironmentalDefendersEngineResult:
    entities = [
        EnvironmentalDefendersEntity(
            entity_id="ED-001",
            name="Honduras/Amérique Centrale — Berta Cáceres, 200 Défenseurs Tués/An & Impunité Totale",
            country="Amérique Latine",
            killings_disappearances_score=95.0,
            criminalization_prosecution_score=88.0,
            corporate_state_collusion_score=92.0,
            impunity_justice_denial_score=90.0,
            primary_pattern="killings_disappearances",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-002",
            name="Philippines — 200 Défenseurs Tués, Proclamation 32 & Criminalisation Activisme",
            country="Asie du Sud-Est",
            killings_disappearances_score=88.0,
            criminalization_prosecution_score=92.0,
            corporate_state_collusion_score=85.0,
            impunity_justice_denial_score=88.0,
            primary_pattern="criminalization_prosecution",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-003",
            name="Brésil/Amazonie — Dom Phillips, Bruno Araújo & Déforestation Industrie Agro",
            country="Amérique Latine",
            killings_disappearances_score=85.0,
            criminalization_prosecution_score=78.0,
            corporate_state_collusion_score=90.0,
            impunity_justice_denial_score=88.0,
            primary_pattern="corporate_state_collusion",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-004",
            name="RDC/Congo — Défenseurs Forêts, Parc Virunga & Industrie Extractive Violente",
            country="Afrique Sub-Saharienne",
            killings_disappearances_score=78.0,
            criminalization_prosecution_score=72.0,
            corporate_state_collusion_score=82.0,
            impunity_justice_denial_score=80.0,
            primary_pattern="impunity_justice_denial",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-005",
            name="Inde — Défenseurs Adivasi, UAPA & Criminalisation Protestataires Environnement",
            country="Asie du Sud",
            killings_disappearances_score=52.0,
            criminalization_prosecution_score=58.0,
            corporate_state_collusion_score=55.0,
            impunity_justice_denial_score=60.0,
            primary_pattern="criminalization_prosecution",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-006",
            name="Indonésie — Papouasie, Défenseurs Forêts & Loi Minière Extractiviste",
            country="Asie du Sud-Est",
            killings_disappearances_score=50.0,
            criminalization_prosecution_score=55.0,
            corporate_state_collusion_score=58.0,
            impunity_justice_denial_score=52.0,
            primary_pattern="corporate_state_collusion",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-007",
            name="Europe/SLAPP — Poursuites-Bâillons Anti-Environnement, Directive Anti-SLAPP UE",
            country="Europe",
            killings_disappearances_score=20.0,
            criminalization_prosecution_score=32.0,
            corporate_state_collusion_score=28.0,
            impunity_justice_denial_score=30.0,
            primary_pattern="criminalization_prosecution",
        ),
        EnvironmentalDefendersEntity(
            entity_id="ED-008",
            name="ONU/Global Witness/OHCHR — Rapporteur Défenseurs & Déclaration ONU Droits",
            country="Global",
            killings_disappearances_score=4.0,
            criminalization_prosecution_score=5.0,
            corporate_state_collusion_score=3.0,
            impunity_justice_denial_score=6.0,
            primary_pattern="killings_disappearances",
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

    return EnvironmentalDefendersEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_defenders_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_defending_tomorrow_annual_report_environmental_defenders",
            "front_line_defenders_global_analysis_human_rights_defenders_at_risk",
            "un_special_rapporteur_environmental_defenders_annual_report_ohchr",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_environmental_defenders_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_defenders_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
