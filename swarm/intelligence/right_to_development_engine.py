from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RightToDevelopmentEntity:
    entity_id: str
    name: str
    country: str
    development_finance_neocolonial_conditionality_score: float
    technology_knowledge_transfer_exclusion_scale_score: float
    debt_trap_sovereignty_undermining_score: float
    sdg_implementation_inequality_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_development_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.development_finance_neocolonial_conditionality_score * 0.30
            + self.technology_knowledge_transfer_exclusion_scale_score * 0.25
            + self.debt_trap_sovereignty_undermining_score * 0.25
            + self.sdg_implementation_inequality_gap_score * 0.20,
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
        self.estimated_right_to_development_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RightToDevelopmentEngineResult:
    agent: str = "Right to Development Engine Agent"
    domain: str = "right_to_development"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_development_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToDevelopmentEntity] = field(default_factory=list)

def run_right_to_development_engine() -> RightToDevelopmentEngineResult:
    entities = [
        RightToDevelopmentEntity(
            entity_id="RTD-001",
            name="Afrique Sub-Saharienne/FMI — Conditionnalités Austérité Coupes Santé/Éducation, Dette 70% PIB & Souveraineté Économique Réduite",
            country="Afrique Sub-Saharienne",
            development_finance_neocolonial_conditionality_score=96.0,
            technology_knowledge_transfer_exclusion_scale_score=91.0,
            debt_trap_sovereignty_undermining_score=93.0,
            sdg_implementation_inequality_gap_score=94.0,
            primary_pattern="development_finance_neocolonial_conditionality",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-002",
            name="Sri Lanka/Zambie — Surendettement Ceinture Route Chine, Ports Loués 99 Ans & Défaut Paiement Sans Restructuration",
            country="Sri Lanka/Zambie",
            development_finance_neocolonial_conditionality_score=92.0,
            technology_knowledge_transfer_exclusion_scale_score=87.0,
            debt_trap_sovereignty_undermining_score=95.0,
            sdg_implementation_inequality_gap_score=88.0,
            primary_pattern="debt_trap_sovereignty_undermining",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-003",
            name="Haïti — Ingérence FMI/Banque Mondiale 30 Ans, Corruption Induite Aide & Dépendance Structurelle Humanitaire",
            country="Haïti",
            development_finance_neocolonial_conditionality_score=89.0,
            technology_knowledge_transfer_exclusion_scale_score=85.0,
            debt_trap_sovereignty_undermining_score=87.0,
            sdg_implementation_inequality_gap_score=87.0,
            primary_pattern="development_finance_neocolonial_conditionality",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-004",
            name="Sahel — Accords EPA UE Bloquant Industrialisation, Dumping Agricole & Marché Fermé Produits Locaux",
            country="Sahel",
            development_finance_neocolonial_conditionality_score=86.0,
            technology_knowledge_transfer_exclusion_scale_score=83.0,
            debt_trap_sovereignty_undermining_score=82.0,
            sdg_implementation_inequality_gap_score=85.0,
            primary_pattern="development_finance_neocolonial_conditionality",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-005",
            name="Asie du Sud/Bangladesh — Propriété Intellectuelle TRIPS Médicaments Génériques, Semences Brevets & Transfert Technologie Refusé",
            country="Asie du Sud",
            development_finance_neocolonial_conditionality_score=52.0,
            technology_knowledge_transfer_exclusion_scale_score=58.0,
            debt_trap_sovereignty_undermining_score=50.0,
            sdg_implementation_inequality_gap_score=54.0,
            primary_pattern="technology_knowledge_transfer_exclusion_scale",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-006",
            name="Amérique Latine — Traités Investissement ISDS vs Politiques Publiques, Nationalisations Pénalisées & Souveraineté Normative",
            country="Amérique Latine",
            development_finance_neocolonial_conditionality_score=50.0,
            technology_knowledge_transfer_exclusion_scale_score=48.0,
            debt_trap_sovereignty_undermining_score=55.0,
            sdg_implementation_inequality_gap_score=52.0,
            primary_pattern="debt_trap_sovereignty_undermining",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-007",
            name="G77/UNCTAD — Coalition Sud Global, Commerce Équitable, Réforme Institutions Bretton Woods & Standards NIEO",
            country="Global",
            development_finance_neocolonial_conditionality_score=26.0,
            technology_knowledge_transfer_exclusion_scale_score=28.0,
            debt_trap_sovereignty_undermining_score=25.0,
            sdg_implementation_inequality_gap_score=26.0,
            primary_pattern="technology_knowledge_transfer_exclusion_scale",
        ),
        RightToDevelopmentEntity(
            entity_id="RTD-008",
            name="ONU/Déclaration 1986 — Déclaration Droit Développement, Résolution 41/128 & SDG 17 Partenariats",
            country="Global",
            development_finance_neocolonial_conditionality_score=4.0,
            technology_knowledge_transfer_exclusion_scale_score=4.0,
            debt_trap_sovereignty_undermining_score=4.0,
            sdg_implementation_inequality_gap_score=5.0,
            primary_pattern="sdg_implementation_inequality_gap",
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

    return RightToDevelopmentEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_development_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_declaration_right_to_development_1986_resolution_41_128",
            "unctad_trade_development_report",
            "oxfam_imf_austerity_conditionality_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_right_to_development_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_right_to_development_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
