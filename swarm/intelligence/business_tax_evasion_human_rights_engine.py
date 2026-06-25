"""Business Tax Evasion Human Rights Engine — Paradis fiscaux, évasion fiscale, droits sociaux volés aux États."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class BusinessTaxEvasionHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    tax_haven_secrecy_opacity_score: float
    corporate_profit_shifting_scale_score: float
    social_rights_funding_deprivation_score: float
    regulatory_enforcement_failure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_business_tax_evasion_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.tax_haven_secrecy_opacity_score * 0.30
            + self.corporate_profit_shifting_scale_score * 0.25
            + self.social_rights_funding_deprivation_score * 0.25
            + self.regulatory_enforcement_failure_score * 0.20,
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
        self.estimated_business_tax_evasion_human_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class BusinessTaxEvasionHumanRightsEngineResult:
    agent: str
    domain: str
    entities: List[BusinessTaxEvasionHumanRightsEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_business_tax_evasion_human_rights_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.87
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_business_tax_evasion_human_rights_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_business_tax_evasion_human_rights_engine() -> BusinessTaxEvasionHumanRightsEngineResult:
    entities = [
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-001",
            name="Panama/Îles Caïmans — Panama Papers 11.5M Documents, Fuites Historiques ICIJ, Droits Sociaux Volés & Financement Dictatures",
            country="Panama/Îles Caïmans",
            tax_haven_secrecy_opacity_score=92.0,
            corporate_profit_shifting_scale_score=90.0,
            social_rights_funding_deprivation_score=88.0,
            regulatory_enforcement_failure_score=85.0,
            primary_pattern="tax_haven_secrecy_opacity",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-002",
            name="Suisse/Secret Bancaire — Dépôts Dictateurs, UBS Deutsche Bank Sanctions, Fortunes Oligarques & Blanchiment Capitaux Élites",
            country="Suisse",
            tax_haven_secrecy_opacity_score=88.0,
            corporate_profit_shifting_scale_score=85.0,
            social_rights_funding_deprivation_score=82.0,
            regulatory_enforcement_failure_score=80.0,
            primary_pattern="tax_haven_secrecy_opacity",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-003",
            name="Luxembourg/LuxLeaks — Rulings Fiscaux Apple Amazon ICIJ, Tax Rulings Secrets, ATAD Contourné & Optimisation Agressive UE",
            country="Luxembourg",
            tax_haven_secrecy_opacity_score=82.0,
            corporate_profit_shifting_scale_score=88.0,
            social_rights_funding_deprivation_score=80.0,
            regulatory_enforcement_failure_score=78.0,
            primary_pattern="corporate_profit_shifting_scale",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-004",
            name="Pays-Bas/Boîtes Aux Lettres — Multinationales Holdings Vides, ATAD Contournement, Flux Royalties & Structures Double Irish Dutch Sandwich",
            country="Pays-Bas",
            tax_haven_secrecy_opacity_score=78.0,
            corporate_profit_shifting_scale_score=82.0,
            social_rights_funding_deprivation_score=76.0,
            regulatory_enforcement_failure_score=72.0,
            primary_pattern="corporate_profit_shifting_scale",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-005",
            name="Delaware/USA — Paradis Fiscal Interne 1M Sociétés Anonymes, LLC Fantômes, Bénéficiaires Cachés & Blanchiment Immobilier",
            country="USA/Delaware",
            tax_haven_secrecy_opacity_score=58.0,
            corporate_profit_shifting_scale_score=55.0,
            social_rights_funding_deprivation_score=52.0,
            regulatory_enforcement_failure_score=50.0,
            primary_pattern="tax_haven_secrecy_opacity",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-006",
            name="Singapour/Hub Asie — Optimisation Fiscale Agressive Firmes Tech, Traités Double Imposition, IP Box Régimes & Profits Asie-Pacifique",
            country="Singapour",
            tax_haven_secrecy_opacity_score=55.0,
            corporate_profit_shifting_scale_score=58.0,
            social_rights_funding_deprivation_score=48.0,
            regulatory_enforcement_failure_score=52.0,
            primary_pattern="corporate_profit_shifting_scale",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-007",
            name="Irlande/Taux 12.5% — Accord OCDE BEPS Partiel, Apple 14.3Md€ Récupérés CJUE, Transition Pilier 2 & Résistances Lobbying",
            country="Irlande",
            tax_haven_secrecy_opacity_score=28.0,
            corporate_profit_shifting_scale_score=32.0,
            social_rights_funding_deprivation_score=25.0,
            regulatory_enforcement_failure_score=22.0,
            primary_pattern="regulatory_enforcement_failure",
        ),
        BusinessTaxEvasionHumanRightsEntity(
            entity_id="BTEHR-008",
            name="OCDE/Pilier 2 — Taux Minimum 15% Accord 136 Pays 2021, Règles UTPR QDMTT, Mise en Oeuvre Progressive & Standard Mondial",
            country="OCDE/International",
            tax_haven_secrecy_opacity_score=8.0,
            corporate_profit_shifting_scale_score=10.0,
            social_rights_funding_deprivation_score=6.0,
            regulatory_enforcement_failure_score=12.0,
            primary_pattern="regulatory_enforcement_failure",
        ),
    ]

    return BusinessTaxEvasionHumanRightsEngineResult(
        agent="Business Tax Evasion Human Rights Engine Agent",
        domain="business_tax_evasion_human_rights",
        entities=entities,
        data_sources=[
            "icij_panama_papers_2016_ongoing",
            "tax_justice_network_fsi_2023",
            "oxfam_tax_havens_report_2023",
            "oecd_beps_implementation_2023",
        ],
    )


if __name__ == "__main__":
    result = run_business_tax_evasion_human_rights_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_business_tax_evasion_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
