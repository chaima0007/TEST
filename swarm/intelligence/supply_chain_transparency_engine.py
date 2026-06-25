from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SupplyChainTransparencyEntity:
    entity_id: str
    name: str
    country: str
    sub1_traceability_gap: float
    sub2_audit_independence: float
    sub3_whistleblower_protection: float
    sub4_csddd_compliance: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_supply_chain_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sub1_traceability_gap * 0.30
            + self.sub2_audit_independence * 0.25
            + self.sub3_whistleblower_protection * 0.25
            + self.sub4_csddd_compliance * 0.20,
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
        self.estimated_supply_chain_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SupplyChainTransparencyEngineResult:
    agent: str = "Supply Chain Transparency Engine Agent"
    domain: str = "supply_chain_transparency"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_supply_chain_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SupplyChainTransparencyEntity] = field(default_factory=list)


def run_supply_chain_transparency_engine() -> SupplyChainTransparencyEngineResult:
    entities = [
        SupplyChainTransparencyEntity(
            entity_id="SCT-001",
            name="Fast Fashion Bangladesh/Ethiopie — Rana Plaza Legacy, Sous-Traitants Invisibles, Audits Falsifies & Salaires Misere",
            country="Bangladesh/Ethiopie",
            sub1_traceability_gap=91.0,
            sub2_audit_independence=89.0,
            sub3_whistleblower_protection=87.0,
            sub4_csddd_compliance=83.0,
            primary_pattern="sub1_traceability_gap",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-002",
            name="Cobalt RDC — EVs Smartphones Mines Artisanales, Enfants Creuseurs, Negociants Intermediaires & Due Diligence Absente",
            country="RDC",
            sub1_traceability_gap=95.0,
            sub2_audit_independence=93.0,
            sub3_whistleblower_protection=91.0,
            sub4_csddd_compliance=89.0,
            primary_pattern="sub1_traceability_gap",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-003",
            name="Cacao Cote d'Ivoire — Child Labor Systemique, Certification Faible, Farmgate Prices Exploiteurs & Barry Callebaut",
            country="Cote d'Ivoire",
            sub1_traceability_gap=85.0,
            sub2_audit_independence=83.0,
            sub3_whistleblower_protection=81.0,
            sub4_csddd_compliance=78.0,
            primary_pattern="sub2_audit_independence",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-004",
            name="Peche Thaïlandaise — Travail Force Bateaux, Travailleurs Migrants, IUU Fishing & Seafood Watch Alertes",
            country="Thaïlande",
            sub1_traceability_gap=79.0,
            sub2_audit_independence=77.0,
            sub3_whistleblower_protection=75.0,
            sub4_csddd_compliance=72.0,
            primary_pattern="sub3_whistleblower_protection",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-005",
            name="Agroalimentaire Bresil — Deforestation Amazonie, Soja Tracabilite Lacunaire, Beef Moratorium Partiel & Cerrado",
            country="Bresil",
            sub1_traceability_gap=60.0,
            sub2_audit_independence=58.0,
            sub3_whistleblower_protection=56.0,
            sub4_csddd_compliance=52.0,
            primary_pattern="sub1_traceability_gap",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-006",
            name="Construction Qatar — Kafala System, Travailleurs Migrants Coupe du Monde, Passeports Confisques & Heat Stress",
            country="Qatar",
            sub1_traceability_gap=52.0,
            sub2_audit_independence=50.0,
            sub3_whistleblower_protection=47.0,
            sub4_csddd_compliance=44.0,
            primary_pattern="sub2_audit_independence",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-007",
            name="Textile Turquie — CSDDD Partiel, Refugies Syriens Non-Declares, Marques EU Fournisseurs & Progres Reel Mitige",
            country="Turquie",
            sub1_traceability_gap=34.0,
            sub2_audit_independence=32.0,
            sub3_whistleblower_protection=30.0,
            sub4_csddd_compliance=27.0,
            primary_pattern="sub4_csddd_compliance",
        ),
        SupplyChainTransparencyEntity(
            entity_id="SCT-008",
            name="Electronique Pays-Bas Fairphone — Full Traceability, Conflict Minerals Audit, Reparation Droit & B Corp",
            country="Pays-Bas",
            sub1_traceability_gap=13.0,
            sub2_audit_independence=12.0,
            sub3_whistleblower_protection=11.0,
            sub4_csddd_compliance=11.0,
            primary_pattern="sub2_audit_independence",
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

    return SupplyChainTransparencyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_supply_chain_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "know_the_chain_benchmark_supply_chain",
            "corporate_human_rights_benchmark_chrb",
            "csddd_eu_due_diligence_directive_tracker",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_supply_chain_transparency_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_supply_chain_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")

    assert result.risk_distribution.get("critique", 0) == 4, f"Expected 4 critique, got {result.risk_distribution.get('critique', 0)}"
    assert result.risk_distribution.get("elevé", 0) == 2 or result.risk_distribution.get("élevé", 0) == 2, f"Expected 2 élevé, got {result.risk_distribution}"
    assert result.risk_distribution.get("modéré", 0) == 1, f"Expected 1 modéré, got {result.risk_distribution.get('modéré', 0)}"
    assert result.risk_distribution.get("faible", 0) == 1, f"Expected 1 faible, got {result.risk_distribution.get('faible', 0)}"
    print("Distribution assertion: PASSED 4/2/1/1")

    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
