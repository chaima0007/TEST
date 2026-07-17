from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ColonialReparationsEntity:
    entity_id: str
    name: str
    country: str
    economic_extraction_scale_score: float
    cultural_artifact_restitution_gap_score: float
    structural_inequality_persistence_score: float
    political_acknowledgment_refusal_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_colonial_reparations_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.economic_extraction_scale_score * 0.30
            + self.cultural_artifact_restitution_gap_score * 0.25
            + self.structural_inequality_persistence_score * 0.25
            + self.political_acknowledgment_refusal_score * 0.20,
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
        self.estimated_colonial_reparations_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ColonialReparationsEngineResult:
    agent: str = "Colonial Reparations Engine Agent"
    domain: str = "colonial_reparations"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_colonial_reparations_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ColonialReparationsEntity] = field(default_factory=list)

def run_colonial_reparations_engine() -> ColonialReparationsEngineResult:
    entities = [
        ColonialReparationsEntity(
            entity_id="CR-001",
            name="Congo/Belgique — Extraction Caoutchouc/Minéraux, 10M Morts & Déni Réparations Léopold II",
            country="Afrique Centrale",
            economic_extraction_scale_score=95.0,
            cultural_artifact_restitution_gap_score=88.0,
            structural_inequality_persistence_score=92.0,
            political_acknowledgment_refusal_score=90.0,
            primary_pattern="economic_extraction_scale",
        ),
        ColonialReparationsEntity(
            entity_id="CR-002",
            name="Inde/UK — Pillage East India Company, Famine Bengal & Refus Reconnaissance Dette Coloniale",
            country="Asie du Sud",
            economic_extraction_scale_score=92.0,
            cultural_artifact_restitution_gap_score=90.0,
            structural_inequality_persistence_score=88.0,
            political_acknowledgment_refusal_score=88.0,
            primary_pattern="cultural_artifact_restitution_gap",
        ),
        ColonialReparationsEntity(
            entity_id="CR-003",
            name="Caraïbes/France — Esclavage 250 Ans, Dette Haïti 1825 & Silence Officiel Réparations",
            country="Caraïbes",
            economic_extraction_scale_score=88.0,
            cultural_artifact_restitution_gap_score=82.0,
            structural_inequality_persistence_score=90.0,
            political_acknowledgment_refusal_score=85.0,
            primary_pattern="structural_inequality_persistence",
        ),
        ColonialReparationsEntity(
            entity_id="CR-004",
            name="Afrique Ouest/France — CFA Franc Néocolonial, Ressources Extractées & Ingérence Politique",
            country="Afrique de l'Ouest",
            economic_extraction_scale_score=82.0,
            cultural_artifact_restitution_gap_score=78.0,
            structural_inequality_persistence_score=88.0,
            political_acknowledgment_refusal_score=82.0,
            primary_pattern="structural_inequality_persistence",
        ),
        ColonialReparationsEntity(
            entity_id="CR-005",
            name="USA — Esclavage/Jim Crow, Réparations HR40 Bloquées & Inégalités Raciales Persistantes",
            country="Amérique du Nord",
            economic_extraction_scale_score=52.0,
            cultural_artifact_restitution_gap_score=50.0,
            structural_inequality_persistence_score=58.0,
            political_acknowledgment_refusal_score=55.0,
            primary_pattern="political_acknowledgment_refusal",
        ),
        ColonialReparationsEntity(
            entity_id="CR-006",
            name="Allemagne/Namibie — Génocide Herero 1904, Accord 2021 Insuffisant & Descendants Exclus",
            country="Afrique Australe",
            economic_extraction_scale_score=48.0,
            cultural_artifact_restitution_gap_score=52.0,
            structural_inequality_persistence_score=50.0,
            political_acknowledgment_refusal_score=55.0,
            primary_pattern="political_acknowledgment_refusal",
        ),
        ColonialReparationsEntity(
            entity_id="CR-007",
            name="CARICOM — Alliance 14 Nations, Plan Réparations 10 Points & Plaidoyer ONU",
            country="Global",
            economic_extraction_scale_score=22.0,
            cultural_artifact_restitution_gap_score=28.0,
            structural_inequality_persistence_score=25.0,
            political_acknowledgment_refusal_score=30.0,
            primary_pattern="economic_extraction_scale",
        ),
        ColonialReparationsEntity(
            entity_id="CR-008",
            name="ONU/Déclaration Durban — Conférence Anti-Racisme 2001, Suivi & Mécanismes Révision",
            country="Global",
            economic_extraction_scale_score=4.0,
            cultural_artifact_restitution_gap_score=5.0,
            structural_inequality_persistence_score=3.0,
            political_acknowledgment_refusal_score=6.0,
            primary_pattern="cultural_artifact_restitution_gap",
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

    return ColonialReparationsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_colonial_reparations_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_durban_declaration_programme_action_reparations_review",
            "caricom_reparations_commission_ten_point_plan_report",
            "colonial_crimes_accountability_coalition_global_audit",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_colonial_reparations_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_colonial_reparations_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
