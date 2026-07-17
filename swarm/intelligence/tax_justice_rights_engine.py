from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0891b2"


@dataclass
class TaxJusticeRightsEntity:
    entity_id: str
    name: str
    country: str
    tax_haven_exploitation_score: float
    public_service_deprivation_score: float
    corporate_tax_evasion_score: float
    wealth_inequality_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_tax_justice_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.tax_haven_exploitation_score * 0.30
            + self.public_service_deprivation_score * 0.25
            + self.corporate_tax_evasion_score * 0.25
            + self.wealth_inequality_gap_score * 0.20,
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
        self.estimated_tax_justice_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class TaxJusticeRightsEngineResult:
    agent: str = "Tax Justice Rights Engine Agent"
    domain: str = "tax_justice_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_tax_justice_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[TaxJusticeRightsEntity] = field(default_factory=list)


def run_tax_justice_rights_engine() -> TaxJusticeRightsEngineResult:
    entities = [
        TaxJusticeRightsEntity(
            entity_id="TJR-001",
            name="Îles Caïmans — Paradis Fiscal #1 FSI, 0% Impôt Sociétés & 1600 Milliards USD Offshore",
            country="Îles Caïmans",
            tax_haven_exploitation_score=90.0,
            public_service_deprivation_score=87.0,
            corporate_tax_evasion_score=89.0,
            wealth_inequality_gap_score=86.0,
            primary_pattern="tax_haven_exploitation_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-002",
            name="Panama — Pandora Papers, 336k Sociétés Fantômes & Déprivation Services Publics Populations",
            country="Panama",
            tax_haven_exploitation_score=86.0,
            public_service_deprivation_score=84.0,
            corporate_tax_evasion_score=88.0,
            wealth_inequality_gap_score=83.0,
            primary_pattern="corporate_tax_evasion_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-003",
            name="Luxembourg — Double Irish Dutch Sandwich, Rulings Apple/Amazon & Manque à Gagner 120 Mds€ UE",
            country="Luxembourg",
            tax_haven_exploitation_score=84.0,
            public_service_deprivation_score=81.0,
            corporate_tax_evasion_score=86.0,
            wealth_inequality_gap_score=80.0,
            primary_pattern="corporate_tax_evasion_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-004",
            name="Nigeria — Évasion Fiscale 15 Mds USD/An Multinationales Pétrolières, Inégalités Extrêmes",
            country="Nigeria",
            tax_haven_exploitation_score=80.0,
            public_service_deprivation_score=83.0,
            corporate_tax_evasion_score=79.0,
            wealth_inequality_gap_score=82.0,
            primary_pattern="public_service_deprivation_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-005",
            name="USA — Déductions Fiscales Corporations, Gini 0.49 & Sous-Investissement Services Sociaux",
            country="USA",
            tax_haven_exploitation_score=54.0,
            public_service_deprivation_score=56.0,
            corporate_tax_evasion_score=58.0,
            wealth_inequality_gap_score=57.0,
            primary_pattern="corporate_tax_evasion_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-006",
            name="Pays-Bas — Boîtes aux Lettres Multinationales, 4500 Milliards Flux Passifs & BEPS Partiel",
            country="Pays-Bas",
            tax_haven_exploitation_score=49.0,
            public_service_deprivation_score=42.0,
            corporate_tax_evasion_score=51.0,
            wealth_inequality_gap_score=44.0,
            primary_pattern="corporate_tax_evasion_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-007",
            name="Brésil — Exemption Dividendes, Inégalité Fiscale Revenus Travail vs Capital & Réforme Partielle",
            country="Brésil",
            tax_haven_exploitation_score=33.0,
            public_service_deprivation_score=35.0,
            corporate_tax_evasion_score=31.0,
            wealth_inequality_gap_score=36.0,
            primary_pattern="wealth_inequality_gap_score",
        ),
        TaxJusticeRightsEntity(
            entity_id="TJR-008",
            name="Danemark — Taux Imposition Effectif Élevé, Transparence Registres & OCDE BEPS Conforme",
            country="Danemark",
            tax_haven_exploitation_score=12.0,
            public_service_deprivation_score=10.0,
            corporate_tax_evasion_score=11.0,
            wealth_inequality_gap_score=13.0,
            primary_pattern="tax_haven_exploitation_score",
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

    return TaxJusticeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_tax_justice_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "tax_justice_network_financial_secrecy_index_2024",
            "oxfam_inequality_report_corporate_tax_avoidance_2024",
            "un_special_rapporteur_extreme_poverty_tax_report",
            "oecd_beps_action_plan_implementation_report",
            "icij_pandora_papers_offshore_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_tax_justice_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
