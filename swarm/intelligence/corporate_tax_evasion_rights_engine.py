"""
Caelum Partners — Corporate Tax Evasion Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Évasion fiscale des entreprises et impact sur les droits humains (exploitation des paradis
fiscaux, transfert de bénéfices, désinvestissement services publics, arbitrage réglementaire).

L'évasion fiscale agressive des multinationales prive les États de ressources essentielles
au financement des droits économiques et sociaux. Selon l'OCDE, les pratiques BEPS
(Base Erosion and Profit Shifting) font perdre aux gouvernements entre 100 et 240
milliards USD annuellement. Des entreprises comme Apple ont accumulé 60 milliards USD
dans des paradis fiscaux irlandais/jersiais ; Google a exploité le "Double Irish/Dutch
Sandwich" pour transférer 23 milliards offshore. Ces pratiques constituent une violation
indirecte des droits humains en désinvestissant la santé, l'éducation et la protection
sociale des populations les plus vulnérables.

Risk levels (paradis fiscaux, transfert bénéfices, désinvestissement, arbitrage réglementaire) :
  critique  -> composite >= 60  (évasion systémique — milliards offshore, condamnation EU/OCDE)
  élevé     -> composite >= 40  (optimisation agressive — structures opaques, pertes fiscales majeures)
  modéré    -> composite >= 20  (cadre partiel — BEPS mise en œuvre incomplète, lacunes)
  faible    -> composite < 20   (meilleure pratique — transparence CBCR, taux effectif équitable)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class CorporateTaxEvasionRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    tax_haven_exploitation_score: float
    profit_shifting_score: float
    public_services_defunding_score: float
    regulatory_arbitrage_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_corporate_tax_evasion_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.tax_haven_exploitation_score * 0.30
            + self.profit_shifting_score * 0.25
            + self.public_services_defunding_score * 0.25
            + self.regulatory_arbitrage_score * 0.20,
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
        self.estimated_corporate_tax_evasion_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "tax_haven_exploitation_score": self.tax_haven_exploitation_score,
            "profit_shifting_score": self.profit_shifting_score,
            "public_services_defunding_score": self.public_services_defunding_score,
            "regulatory_arbitrage_score": self.regulatory_arbitrage_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_corporate_tax_evasion_rights_index": self.estimated_corporate_tax_evasion_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class CorporateTaxEvasionRightsEngineResult:
    agent: str = "Corporate Tax Evasion Rights Engine Agent"
    domain: str = "corporate_tax_evasion_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_corporate_tax_evasion_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CorporateTaxEvasionRightsEntity] = field(default_factory=list)


def run_corporate_tax_evasion_rights_engine() -> CorporateTaxEvasionRightsEngineResult:
    entities = [
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-001",
            name="Apple Inc. — 60 Mds$ Paradis Fiscaux Irlande/Jersey, Condamné EU 13 Mds€ & Profit Shifting Systémique",
            country="USA/Irlande",
            sector="Tech — Optimisation Fiscale Agressive",
            tax_haven_exploitation_score=92.0,
            profit_shifting_score=91.0,
            public_services_defunding_score=90.0,
            regulatory_arbitrage_score=91.0,
            primary_pattern="tax_haven_exploitation",
            key_signals=[
                "60 milliards USD accumulation paradis fiscaux Irlande/Jersey",
                "EU Commission condamne 13 milliards€ aide d'État illégale 2016",
                "taux effectif imposition 0.005% revenus irlandais documenté",
                "profit shifting déplace bénéfices pays à fiscalité nulle",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-002",
            name="Google/Alphabet — Double Irish Dutch Sandwich, 23 Mds$ Offshore & Sanction EU Abus Marché Fiscal",
            country="USA/Pays-Bas/Irlande",
            sector="Tech — Structures Optimisation Fiscale Offshore",
            tax_haven_exploitation_score=90.0,
            profit_shifting_score=91.0,
            public_services_defunding_score=89.0,
            regulatory_arbitrage_score=90.0,
            primary_pattern="profit_shifting",
            key_signals=[
                "Double Irish Dutch Sandwich — 23 milliards USD offshore",
                "transfert droits propriété intellectuelle paradis fiscaux",
                "taux effectif imposition < 5% revenus hors USA",
                "sanction EU abus de position dominante — impacts fiscalité",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-003",
            name="Amazon — Luxembourg Shell Companies, 0% Impôts Certaines Années & Condamné EU State Aid Illégale",
            country="USA/Luxembourg",
            sector="E-commerce — Optimisation Fiscale Structurelle",
            tax_haven_exploitation_score=89.0,
            profit_shifting_score=88.0,
            public_services_defunding_score=89.0,
            regulatory_arbitrage_score=88.0,
            primary_pattern="tax_haven_exploitation",
            key_signals=[
                "Luxembourg sociétés holding — impôts fédéraux USA 0% 2017-2018",
                "EU Commission — accord fiscal Luxembourg aide illégale 250M€",
                "transfert bénéfices via redevances propriété intellectuelle",
                "désinvestissement fiscal — services publics pays opérations",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-004",
            name="Shell/BP — Paradis Fiscaux Cayman/Bermudes, Sous-Déclaration Revenus Pétroliers & Subsidies Cachés",
            country="UK/Pays-Bas",
            sector="Énergie — Extractivisme & Optimisation Fiscale",
            tax_haven_exploitation_score=87.0,
            profit_shifting_score=86.0,
            public_services_defunding_score=88.0,
            regulatory_arbitrage_score=87.0,
            primary_pattern="public_services_defunding",
            key_signals=[
                "filiales Cayman/Bermudes — optimisation paiements royalties",
                "sous-déclaration revenus extraction pays en développement",
                "subsidies fossiles estimés 55 milliards USD annuels implicites",
                "pays africains d'extraction perdent milliards fiscalité due",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-005",
            name="Luxembourg / Cayman Islands — Hubs Tax Haven Facilitant Évasion Globale & Opacité Structurelle",
            country="Luxembourg/Cayman Islands",
            sector="Juridictions Offshore & Facilitateurs Évasion",
            tax_haven_exploitation_score=54.0,
            profit_shifting_score=55.0,
            public_services_defunding_score=53.0,
            regulatory_arbitrage_score=56.0,
            primary_pattern="regulatory_arbitrage",
            key_signals=[
                "4 000+ fonds investissement enregistrés Cayman Islands",
                "Luxembourg — 147 accords fiscaux secrets LuxLeaks révélés",
                "facilitation légale structures évitement impôt multinational",
                "opacité bénéficiaire effectif — registres non publics",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-006",
            name="Big 4 Accounting (Deloitte/EY/KPMG/PwC) — Architectes Optimisation Fiscale Agressive Mondiale",
            country="International",
            sector="Services Audit & Conseil Fiscal",
            tax_haven_exploitation_score=51.0,
            profit_shifting_score=52.0,
            public_services_defunding_score=50.0,
            regulatory_arbitrage_score=53.0,
            primary_pattern="regulatory_arbitrage",
            key_signals=[
                "conception et vente schémas optimisation fiscale agressive",
                "LuxLeaks — PwC créateur 548 accords secrets Luxembourg",
                "conflits intérêts audit-conseil — même client opacité",
                "KPMG Panama Papers connexions structures offshore documentées",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-007",
            name="BEPS OCDE Framework — Pilier 15% Minimum Global, Application Partielle 2024 & Lacunes Persistantes",
            country="International",
            sector="Régulation Internationale Fiscale",
            tax_haven_exploitation_score=28.0,
            profit_shifting_score=29.0,
            public_services_defunding_score=27.0,
            regulatory_arbitrage_score=30.0,
            primary_pattern="public_services_defunding",
            key_signals=[
                "Pilier 2 — taux minimum 15% grandes multinationales adopté",
                "application incomplète — USA non ratifié, pays tiers résistants",
                "lacunes substance économique — jurisdictions contournement",
                "estimations pertes BEPS réduites 30% seulement avec nouvelles règles",
            ],
        ),
        CorporateTaxEvasionRightsEntity(
            entity_id="CTE-008",
            name="EU Tax Transparency / CBCR — Reporting Pays par Pays, Meilleure Pratique Registres Bénéficiaires",
            country="Union Européenne",
            sector="Régulation & Transparence Fiscale",
            tax_haven_exploitation_score=6.0,
            profit_shifting_score=5.0,
            public_services_defunding_score=6.0,
            regulatory_arbitrage_score=5.0,
            primary_pattern="tax_haven_exploitation",
            key_signals=[
                "CBCR public — reporting pays par pays grandes entreprises EU",
                "registres bénéficiaires effectifs — 5ème directive anti-blanchiment",
                "liste noire EU juridictions non coopératives actualisée",
                "échange automatique d'informations fiscales 90+ États OCDE",
            ],
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

    return CorporateTaxEvasionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_corporate_tax_evasion_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "oecd_beps_action_plan_implementation_report_2024",
            "tax_justice_network_financial_secrecy_index_2024",
            "eu_commission_state_aid_investigations_database",
            "icij_panama_papers_offshore_leaks_database",
            "oxfam_tax_dodging_multinational_corporations_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_corporate_tax_evasion_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_corporate_tax_evasion_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
