from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#f59e0b"


@dataclass
class CollectiveBargainingRightsEntity:
    entity_id: str
    name: str
    country: str
    union_suppression_score: float
    strike_criminalization_score: float
    collective_agreement_refusal_score: float
    worker_representative_persecution_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_collective_bargaining_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.union_suppression_score * 0.30
            + self.strike_criminalization_score * 0.25
            + self.collective_agreement_refusal_score * 0.25
            + self.worker_representative_persecution_score * 0.20,
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
        self.estimated_collective_bargaining_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class CollectiveBargainingRightsEngineResult:
    agent: str = "Collective Bargaining Rights Engine Agent"
    domain: str = "collective_bargaining_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_collective_bargaining_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CollectiveBargainingRightsEntity] = field(default_factory=list)


def run_collective_bargaining_rights_engine() -> CollectiveBargainingRightsEngineResult:
    entities = [
        CollectiveBargainingRightsEntity(
            entity_id="CBR-001",
            name="Chine — Syndicats Indépendants Bannis, ACFTU Contrôlé État & Militants Arrêtés Systématiquement",
            country="Chine",
            union_suppression_score=91.0,
            strike_criminalization_score=89.0,
            collective_agreement_refusal_score=88.0,
            worker_representative_persecution_score=90.0,
            primary_pattern="union_suppression_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-002",
            name="Arabie Saoudite — Syndicats Totalement Interdits, Kafala System & Travailleurs Migrants Sans Droits",
            country="Arabie Saoudite",
            union_suppression_score=90.0,
            strike_criminalization_score=88.0,
            collective_agreement_refusal_score=87.0,
            worker_representative_persecution_score=89.0,
            primary_pattern="union_suppression_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-003",
            name="Bangladesh — Zones Export Syndicats Réprimés Violemment, Meurtres Organisateurs & Usines Rana Plaza",
            country="Bangladesh",
            union_suppression_score=85.0,
            strike_criminalization_score=84.0,
            collective_agreement_refusal_score=82.0,
            worker_representative_persecution_score=86.0,
            primary_pattern="worker_representative_persecution_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-004",
            name="Pakistan — Syndicats Persécutés Zones Franches, Lois Anti-Grève & Représailles Patronales Impunies",
            country="Pakistan",
            union_suppression_score=82.0,
            strike_criminalization_score=81.0,
            collective_agreement_refusal_score=80.0,
            worker_representative_persecution_score=83.0,
            primary_pattern="worker_representative_persecution_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-005",
            name="Cambodge — Dissolution Syndicats Garment Workers, Loi Syndicats 2016 Restrictive & Meurtres Impunis",
            country="Cambodge",
            union_suppression_score=54.0,
            strike_criminalization_score=52.0,
            collective_agreement_refusal_score=50.0,
            worker_representative_persecution_score=55.0,
            primary_pattern="worker_representative_persecution_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-006",
            name="Colombie — 150+ Syndicalistes Assassinés/An Historique, Impunité 97% & Paramilitaires Anti-Syndicaux",
            country="Colombie",
            union_suppression_score=46.0,
            strike_criminalization_score=44.0,
            collective_agreement_refusal_score=43.0,
            worker_representative_persecution_score=48.0,
            primary_pattern="worker_representative_persecution_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-007",
            name="USA — Taft-Hartley Restrictions, Amazon & Starbucks Union-Busting & Droit de Grève Limité",
            country="USA",
            union_suppression_score=30.0,
            strike_criminalization_score=29.0,
            collective_agreement_refusal_score=31.0,
            worker_representative_persecution_score=28.0,
            primary_pattern="collective_agreement_refusal_score",
        ),
        CollectiveBargainingRightsEntity(
            entity_id="CBR-008",
            name="Danemark — Syndicalisation 67%, Négociation Collective Référence Nordique & Grèves Légales Protégées",
            country="Danemark",
            union_suppression_score=10.0,
            strike_criminalization_score=9.0,
            collective_agreement_refusal_score=8.0,
            worker_representative_persecution_score=10.0,
            primary_pattern="union_suppression_score",
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

    return CollectiveBargainingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_collective_bargaining_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_report_freedom_association_collective_bargaining",
            "ituc_global_rights_index_2024",
            "hrw_labour_rights_freedom_association_documentation",
            "ilo_committee_freedom_association_cases",
            "uni_global_union_persecution_tracker",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_collective_bargaining_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
