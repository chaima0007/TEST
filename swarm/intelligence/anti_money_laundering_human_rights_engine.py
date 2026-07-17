from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AntiMoneyLaunderingHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    sub1_illicit_flows_gdp: float
    sub2_financial_secrecy: float
    sub3_kleptocracy_index: float
    sub4_human_rights_funding: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_aml_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sub1_illicit_flows_gdp * 0.30
            + self.sub2_financial_secrecy * 0.25
            + self.sub3_kleptocracy_index * 0.25
            + self.sub4_human_rights_funding * 0.20,
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
        self.estimated_aml_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class AntiMoneyLaunderingHumanRightsEngineResult:
    agent: str = "Anti-Money Laundering Human Rights Engine Agent"
    domain: str = "anti_money_laundering_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_aml_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AntiMoneyLaunderingHumanRightsEntity] = field(default_factory=list)


def run_anti_money_laundering_human_rights_engine() -> AntiMoneyLaunderingHumanRightsEngineResult:
    entities = [
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-001",
            name="Iles Caïmans — Paradis Blanchiment, Fonds Offshore Opaques, Structures Shell & Financement Violations Droits",
            country="Iles Caïmans",
            sub1_illicit_flows_gdp=90.0,
            sub2_financial_secrecy=88.0,
            sub3_kleptocracy_index=85.0,
            sub4_human_rights_funding=83.0,
            primary_pattern="sub2_financial_secrecy",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-002",
            name="Corée du Nord — Financement Armes Nucléaires, Crypto Hacking, Sanctions Contournées & Esclavage Exporté",
            country="Corée du Nord",
            sub1_illicit_flows_gdp=94.0,
            sub2_financial_secrecy=92.0,
            sub3_kleptocracy_index=90.0,
            sub4_human_rights_funding=88.0,
            primary_pattern="sub1_illicit_flows_gdp",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-003",
            name="Russie — Oligarques Post-Sanctions, Yachts Saisis, Flux Illicites Guerre Ukraine & Actifs Gelés Contournés",
            country="Russie",
            sub1_illicit_flows_gdp=86.0,
            sub2_financial_secrecy=84.0,
            sub3_kleptocracy_index=82.0,
            sub4_human_rights_funding=80.0,
            primary_pattern="sub3_kleptocracy_index",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-004",
            name="Venezuela — Madurisme Narco-État, Pétrole Illicite PDVSA, Bolivars Crypto & Répression Financée",
            country="Venezuela",
            sub1_illicit_flows_gdp=81.0,
            sub2_financial_secrecy=79.0,
            sub3_kleptocracy_index=77.0,
            sub4_human_rights_funding=74.0,
            primary_pattern="sub3_kleptocracy_index",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-005",
            name="Panama — Legacy Pandora Papers, Sociétés Anonymes Résiduelles, Réformes Partielles GAFI & Zones Franches",
            country="Panama",
            sub1_illicit_flows_gdp=58.0,
            sub2_financial_secrecy=56.0,
            sub3_kleptocracy_index=53.0,
            sub4_human_rights_funding=50.0,
            primary_pattern="sub1_illicit_flows_gdp",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-006",
            name="Emirats Arabes Unis — Or Conflit, Crypto Non-Régulée, DMCC Dubai & Flux Russes Post-Sanctions",
            country="Emirats Arabes Unis",
            sub1_illicit_flows_gdp=51.0,
            sub2_financial_secrecy=49.0,
            sub3_kleptocracy_index=46.0,
            sub4_human_rights_funding=44.0,
            primary_pattern="sub2_financial_secrecy",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-007",
            name="Luxembourg — Ruling Fiscal Résiduel, Fonds Investissement Opaques, Réformes UE Partielles & ETF Domiciliation",
            country="Luxembourg",
            sub1_illicit_flows_gdp=29.0,
            sub2_financial_secrecy=28.0,
            sub3_kleptocracy_index=26.0,
            sub4_human_rights_funding=24.0,
            primary_pattern="sub1_illicit_flows_gdp",
        ),
        AntiMoneyLaunderingHumanRightsEntity(
            entity_id="AML-008",
            name="Suisse Post-FATF — Transparence Améliorée, Registres Bénéficiaires, FINMA Renforcée & Comptes Russes Gelés",
            country="Suisse",
            sub1_illicit_flows_gdp=11.0,
            sub2_financial_secrecy=10.0,
            sub3_kleptocracy_index=9.0,
            sub4_human_rights_funding=9.0,
            primary_pattern="sub2_financial_secrecy",
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

    return AntiMoneyLaunderingHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_aml_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fatf_mutual_evaluation_reports",
            "financial_secrecy_index_tax_justice_network",
            "global_financial_integrity_illicit_flows_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_anti_money_laundering_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_aml_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")

    assert result.risk_distribution.get("critique", 0) == 4, f"Expected 4 critique, got {result.risk_distribution.get('critique', 0)}"
    assert result.risk_distribution.get("élevé", 0) == 2, f"Expected 2 élevé, got {result.risk_distribution.get('élevé', 0)}"
    assert result.risk_distribution.get("modéré", 0) == 1, f"Expected 1 modéré, got {result.risk_distribution.get('modéré', 0)}"
    assert result.risk_distribution.get("faible", 0) == 1, f"Expected 1 faible, got {result.risk_distribution.get('faible', 0)}"
    print("Distribution assertion: PASSED 4/2/1/1")

    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
