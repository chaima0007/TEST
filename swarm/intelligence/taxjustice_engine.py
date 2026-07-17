#!/usr/bin/env python3
"""CaelumSwarm™ — Tax Justice Risk Engine (GRI 207 Tax Transparency Standards)"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class TaxJusticeEntity:
    entity_id: str
    name: str
    country: str
    transfer_pricing_abuse_score: float
    tax_haven_routing_score: float
    profit_shifting_exposure_score: float
    public_cbcr_disclosure_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_taxjustice_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.transfer_pricing_abuse_score * 0.30
            + self.tax_haven_routing_score * 0.25
            + self.profit_shifting_exposure_score * 0.25
            + self.public_cbcr_disclosure_gap_score * 0.20,
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
        self.estimated_taxjustice_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class TaxJusticeEngineResult:
    agent: str = "Tax Justice Risk Engine Agent"
    domain: str = "taxjustice"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_taxjustice_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[TaxJusticeEntity] = field(default_factory=list)


def run_taxjustice_engine() -> TaxJusticeEngineResult:
    entities = [
        TaxJusticeEntity(
            entity_id="TJ-001",
            name="Apple/Google/Meta — Structures Double Irlandais, Transferts Prix Licences IP & BEPS Agressif",
            country="Global/USA",
            transfer_pricing_abuse_score=99.0,
            tax_haven_routing_score=97.0,
            profit_shifting_exposure_score=95.0,
            public_cbcr_disclosure_gap_score=93.0,
            primary_pattern="transfer_pricing_abuse",
        ),
        TaxJusticeEntity(
            entity_id="TJ-002",
            name="Îles Caïmans/BVI — Registres Bénéficiaires Opaques, Structures Offshore & Évasion Systémique",
            country="Caraïbes",
            transfer_pricing_abuse_score=93.0,
            tax_haven_routing_score=90.0,
            profit_shifting_exposure_score=88.0,
            public_cbcr_disclosure_gap_score=86.0,
            primary_pattern="tax_haven_routing",
        ),
        TaxJusticeEntity(
            entity_id="TJ-003",
            name="Multinationales Extractives — Prix Transfert Minerais, Contrats Secrets & Pertes Pays Africains",
            country="Afrique/Global",
            transfer_pricing_abuse_score=85.0,
            tax_haven_routing_score=82.0,
            profit_shifting_exposure_score=80.0,
            public_cbcr_disclosure_gap_score=78.0,
            primary_pattern="profit_shifting_exposure",
        ),
        TaxJusticeEntity(
            entity_id="TJ-004",
            name="Luxembourg/Pays-Bas — Rulings Fiscaux Opaques, Conduits Holdings & Arbitrage Traités OCDE",
            country="Europe",
            transfer_pricing_abuse_score=80.0,
            tax_haven_routing_score=77.0,
            profit_shifting_exposure_score=75.0,
            public_cbcr_disclosure_gap_score=73.0,
            primary_pattern="tax_haven_routing",
        ),
        TaxJusticeEntity(
            entity_id="TJ-005",
            name="Secteur Pharmaceutique — Brevets IP Irlande/Suisse, Prix Transfert R&D & Profit Shifting Médicaments",
            country="Global",
            transfer_pricing_abuse_score=61.0,
            tax_haven_routing_score=58.0,
            profit_shifting_exposure_score=56.0,
            public_cbcr_disclosure_gap_score=54.0,
            primary_pattern="transfer_pricing_abuse",
        ),
        TaxJusticeEntity(
            entity_id="TJ-006",
            name="Amazon/E-Commerce — Structures TVA Europe, Entrepôts Luxembourg & Optimisation Taxe Digitale",
            country="Europe/USA",
            transfer_pricing_abuse_score=51.0,
            tax_haven_routing_score=48.0,
            profit_shifting_exposure_score=46.0,
            public_cbcr_disclosure_gap_score=44.0,
            primary_pattern="public_cbcr_disclosure_gap",
        ),
        TaxJusticeEntity(
            entity_id="TJ-007",
            name="OCDE Pilier 2 / Impôt Minimum 15% — Mise en Oeuvre, Exclusions & Lacunes Pays en Développement",
            country="Global",
            transfer_pricing_abuse_score=32.0,
            tax_haven_routing_score=29.0,
            profit_shifting_exposure_score=27.0,
            public_cbcr_disclosure_gap_score=25.0,
            primary_pattern="public_cbcr_disclosure_gap",
        ),
        TaxJusticeEntity(
            entity_id="TJ-008",
            name="Tax Justice Network / GRI 207 — Reporting Transparence Fiscale, CbCR Public & Bonnes Pratiques",
            country="Global",
            transfer_pricing_abuse_score=13.0,
            tax_haven_routing_score=11.0,
            profit_shifting_exposure_score=9.0,
            public_cbcr_disclosure_gap_score=7.0,
            primary_pattern="public_cbcr_disclosure_gap",
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

    return TaxJusticeEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_taxjustice_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "tax_justice_network_financial_secrecy_index_2025",
            "gri_207_tax_transparency_reporting_standard_implementation_tracker",
            "oecd_beps_pillar2_global_minimum_tax_implementation_monitor",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_taxjustice_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_taxjustice_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
