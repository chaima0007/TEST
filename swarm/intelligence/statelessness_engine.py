from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StatelessnessEntity:
    entity_id: str
    name: str
    country: str
    population_scale_denial_score: float
    documentation_access_failure_score: float
    generational_transmission_score: float
    protection_legal_framework_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_statelessness_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.population_scale_denial_score * 0.30
            + self.documentation_access_failure_score * 0.25
            + self.generational_transmission_score * 0.25
            + self.protection_legal_framework_gap_score * 0.20,
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
        self.estimated_statelessness_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class StatelessnessEngineResult:
    agent: str = "Statelessness Engine Agent"
    domain: str = "statelessness"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_statelessness_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessnessEntity] = field(default_factory=list)

def run_statelessness_engine() -> StatelessnessEngineResult:
    entities = [
        StatelessnessEntity(
            entity_id="SL-001",
            name="Myanmar/Rohingya — 1M Apatrides, Génocide & Déni Citoyenneté Depuis 1982",
            country="Asie du Sud-Est",
            population_scale_denial_score=95.0,
            documentation_access_failure_score=92.0,
            generational_transmission_score=90.0,
            protection_legal_framework_gap_score=88.0,
            primary_pattern="population_scale_denial",
        ),
        StatelessnessEntity(
            entity_id="SL-002",
            name="Koweït/Bidun — 100K Apatrides, Interdits Éducation/Soins & Traitement Kafala Abusif",
            country="Moyen-Orient",
            population_scale_denial_score=88.0,
            documentation_access_failure_score=85.0,
            generational_transmission_score=88.0,
            protection_legal_framework_gap_score=85.0,
            primary_pattern="generational_transmission",
        ),
        StatelessnessEntity(
            entity_id="SL-003",
            name="Thaïlande — 480K Apatrides Collines, Enfants Sans Acte Naissance & Traite Favorisée",
            country="Asie du Sud-Est",
            population_scale_denial_score=82.0,
            documentation_access_failure_score=85.0,
            generational_transmission_score=80.0,
            protection_legal_framework_gap_score=82.0,
            primary_pattern="documentation_access_failure",
        ),
        StatelessnessEntity(
            entity_id="SL-004",
            name="Côte d'Ivoire — 700K Apatrides Post-Guerre Civile, Enfants Migrants Sans Docs & Exclusion",
            country="Afrique de l'Ouest",
            population_scale_denial_score=80.0,
            documentation_access_failure_score=82.0,
            generational_transmission_score=78.0,
            protection_legal_framework_gap_score=80.0,
            primary_pattern="documentation_access_failure",
        ),
        StatelessnessEntity(
            entity_id="SL-005",
            name="Europe/Ex-URSS — Apatrides Baltes Soviétiques, Russophones Latvia/Estonie & Naturalisation Restrictive",
            country="Europe de l'Est",
            population_scale_denial_score=52.0,
            documentation_access_failure_score=50.0,
            generational_transmission_score=55.0,
            protection_legal_framework_gap_score=48.0,
            primary_pattern="generational_transmission",
        ),
        StatelessnessEntity(
            entity_id="SL-006",
            name="République Dominicaine — Dénationalisation Haïtiens, Arrêt TC168/13 & Apatridie Générationnelle",
            country="Caraïbes",
            population_scale_denial_score=48.0,
            documentation_access_failure_score=52.0,
            generational_transmission_score=55.0,
            protection_legal_framework_gap_score=50.0,
            primary_pattern="protection_legal_framework_gap",
        ),
        StatelessnessEntity(
            entity_id="SL-007",
            name="HCR/#IBelong — Campagne Fin Apatridie 2024, Réformes Législatives & Enregistrements Naissances",
            country="Global",
            population_scale_denial_score=22.0,
            documentation_access_failure_score=28.0,
            generational_transmission_score=25.0,
            protection_legal_framework_gap_score=30.0,
            primary_pattern="population_scale_denial",
        ),
        StatelessnessEntity(
            entity_id="SL-008",
            name="ONU/Convention 1954-1961 — Statut Apatrides, Réduction Apatridie & Cadre Protection Global",
            country="Global",
            population_scale_denial_score=4.0,
            documentation_access_failure_score=5.0,
            generational_transmission_score=3.0,
            protection_legal_framework_gap_score=6.0,
            primary_pattern="protection_legal_framework_gap",
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

    return StatelessnessEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_statelessness_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_ibelong_campaign_global_statelessness_report_2024",
            "institute_statelessness_inclusion_global_statelessness_report",
            "open_society_foundations_statelessness_documentation_access_study",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_statelessness_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_statelessness_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
