from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PatentEntity:
    entity_id: str
    name: str
    invention_code: str
    market_size_potential: float
    competitive_moat: float
    filing_urgency: float
    licensing_revenue_potential: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_patent_revenue_prioritization_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.market_size_potential * 0.30
            + self.competitive_moat * 0.25
            + self.filing_urgency * 0.25
            + self.licensing_revenue_potential * 0.20,
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
        self.estimated_patent_revenue_prioritization_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PatentRevenuePrioritizationEngineResult:
    agent: str = "Patent Revenue Prioritization Engine Agent"
    domain: str = "patent_revenue_prioritization"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.94
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_patent_revenue_prioritization_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    revenue_forecast: dict = field(default_factory=dict)
    entities: List[PatentEntity] = field(default_factory=list)


def run_patent_revenue_prioritization_engine() -> PatentRevenuePrioritizationEngineResult:
    entities = [
        # ---- CRITIQUE / PRIORITÉ MAX (4) ----
        PatentEntity(
            entity_id="PAT-001",
            name="CAE-INV-005 — ESG CSDDD Compliance Engine (50 000 entreprises EU obligées 2026)",
            invention_code="CAE-INV-005",
            market_size_potential=98.0,
            competitive_moat=92.0,
            filing_urgency=95.0,
            licensing_revenue_potential=95.0,
            primary_pattern="filing_urgency",
        ),
        PatentEntity(
            entity_id="PAT-002",
            name="CAE-INV-006 — Risque Conflit Armé & Analyse Géopolitique IA (Défense/Gouvernements)",
            invention_code="CAE-INV-006",
            market_size_potential=88.0,
            competitive_moat=95.0,
            filing_urgency=90.0,
            licensing_revenue_potential=92.0,
            primary_pattern="competitive_moat",
        ),
        PatentEntity(
            entity_id="PAT-003",
            name="CAE-INV-004 — Blockchain Preuves Droits Humains (Legal Tech & Justice Internationale)",
            invention_code="CAE-INV-004",
            market_size_potential=85.0,
            competitive_moat=90.0,
            filing_urgency=88.0,
            licensing_revenue_potential=88.0,
            primary_pattern="competitive_moat",
        ),
        PatentEntity(
            entity_id="PAT-004",
            name="CAE-INV-007 — AI Scoring V2 Droits Humains Gen4 (Prochaine Génération Moteurs)",
            invention_code="CAE-INV-007",
            market_size_potential=82.0,
            competitive_moat=88.0,
            filing_urgency=85.0,
            licensing_revenue_potential=80.0,
            primary_pattern="competitive_moat",
        ),
        # ---- ÉLEVÉ (2) ----
        PatentEntity(
            entity_id="PAT-005",
            name="CAE-INV-003 — Federated Learning Données Sensibles (Privacy-Preserving AI Analytics)",
            invention_code="CAE-INV-003",
            market_size_potential=52.0,
            competitive_moat=55.0,
            filing_urgency=48.0,
            licensing_revenue_potential=50.0,
            primary_pattern="competitive_moat",
        ),
        PatentEntity(
            entity_id="PAT-006",
            name="CAE-INV-008 — ESG Reporting Automatisé Gen4 (CSRD/GRI/SASB Multi-Framework)",
            invention_code="CAE-INV-008",
            market_size_potential=58.0,
            competitive_moat=45.0,
            filing_urgency=52.0,
            licensing_revenue_potential=48.0,
            primary_pattern="market_size_potential",
        ),
        # ---- MODÉRÉ (1) ----
        PatentEntity(
            entity_id="PAT-007",
            name="CAE-INV-002 — Détection Crises Humanitaires Précoce (Early Warning System)",
            invention_code="CAE-INV-002",
            market_size_potential=35.0,
            competitive_moat=28.0,
            filing_urgency=22.0,
            licensing_revenue_potential=30.0,
            primary_pattern="market_size_potential",
        ),
        # ---- FAIBLE (1) ----
        PatentEntity(
            entity_id="PAT-008",
            name="CAE-INV-001 — Scoring IA Droits Humains V1 (Protection En Cours — Dépôt Initial)",
            invention_code="CAE-INV-001",
            market_size_potential=12.0,
            competitive_moat=10.0,
            filing_urgency=8.0,
            licensing_revenue_potential=15.0,
            primary_pattern="licensing_revenue_potential",
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
        f"{e.invention_code}: {e.primary_pattern} — EPO FILING URGENT"
        for e in sorted_entities[:4]
    ]

    revenue_forecast = {
        "CAE-INV-005": {
            "market": "EU CSDDD compliance",
            "target_companies": 50000,
            "license_fee_eur": 15000,
            "annual_potential": "750M EUR",
        },
        "CAE-INV-006": {
            "market": "Defense/Government",
            "target_contracts": 50,
            "license_fee_eur": 500000,
            "annual_potential": "25M EUR",
        },
        "CAE-INV-004": {
            "market": "Legal Tech",
            "target_companies": 5000,
            "license_fee_eur": 20000,
            "annual_potential": "100M EUR",
        },
        "CAE-INV-007": {
            "market": "AI Platform SaaS",
            "target_companies": 10000,
            "license_fee_eur": 8000,
            "annual_potential": "80M EUR",
        },
        "CAE-INV-003": {
            "market": "FinTech / HealthTech Privacy",
            "target_companies": 3000,
            "license_fee_eur": 25000,
            "annual_potential": "75M EUR",
        },
        "CAE-INV-008": {
            "market": "ESG SaaS",
            "target_companies": 20000,
            "license_fee_eur": 5000,
            "annual_potential": "100M EUR",
        },
    }

    return PatentRevenuePrioritizationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_patent_revenue_prioritization_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "epo_patent_analytics_2026",
            "caelum_market_analysis_2026",
            "eu_csddd_implementation_tracker_2026",
            "un_sdg_technology_licensing_2025",
        ],
        revenue_forecast=revenue_forecast,
        entities=entities,
    )


if __name__ == "__main__":
    result = run_patent_revenue_prioritization_engine()
    print(f"Agent: {result.agent}")
    print(f"Domain: {result.domain}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"avg_estimated_patent_revenue_prioritization_index: {result.avg_estimated_patent_revenue_prioritization_index}")
    print(f"Confidence: {result.confidence_score}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Top risk entities: {result.top_risk_entities}")
    print(f"Critical alerts: {result.critical_alerts}")
    print("\n--- Entities ---")
    for e in result.entities:
        print(f"  {e.entity_id} [{e.invention_code}]: score={e.composite_score} [{e.risk_level}] | index={e.estimated_patent_revenue_prioritization_index}")
    print("\n--- Revenue Forecast ---")
    print(json.dumps(result.revenue_forecast, ensure_ascii=False, indent=2))
    print("\n--- Full JSON Output ---")
    output = {
        "agent": result.agent,
        "domain": result.domain,
        "total_entities": result.total_entities,
        "avg_composite": result.avg_composite,
        "confidence_score": result.confidence_score,
        "avg_estimated_patent_revenue_prioritization_index": result.avg_estimated_patent_revenue_prioritization_index,
        "risk_distribution": result.risk_distribution,
        "pattern_distribution": result.pattern_distribution,
        "top_risk_entities": result.top_risk_entities,
        "critical_alerts": result.critical_alerts,
        "last_analysis": result.last_analysis,
        "engine_version": result.engine_version,
        "data_sources": result.data_sources,
        "revenue_forecast": result.revenue_forecast,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "invention_code": e.invention_code,
                "market_size_potential": e.market_size_potential,
                "competitive_moat": e.competitive_moat,
                "filing_urgency": e.filing_urgency,
                "licensing_revenue_potential": e.licensing_revenue_potential,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_patent_revenue_prioritization_index": e.estimated_patent_revenue_prioritization_index,
                "last_updated": e.last_updated,
            }
            for e in result.entities
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
