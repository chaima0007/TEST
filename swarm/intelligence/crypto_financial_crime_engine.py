"""
Crypto Financial Crime Intelligence Engine — Caelum Partners Swarm Module

Tracks crypto-asset financial crime: money laundering via crypto, sanctioned
entity transactions, darknet market flows, ransomware payments, DeFi protocol
exploits for laundering. Computes a composite crime score to identify high-risk
entities and trigger regulatory/law-enforcement actions.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage:
    from intelligence.crypto_financial_crime_engine import CryptoFinancialCrimeEngine
    engine = CryptoFinancialCrimeEngine()
    print(engine.summary())
    for entity in engine.entities:
        print(entity.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.crypto_financial_crime")


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class CryptoEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    laundering_risk_score: float       # 0–100
    sanctions_exposure_score: float    # 0–100
    darknet_flow_score: float          # 0–100
    traceability_gap_score: float      # 0–100
    primary_pattern: str
    key_signals: List[str]             # exactly 3 strings
    last_updated: str                  # ISO date string
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_crypto_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.estimated_crypto_index = round(self.composite_score / 100 * 10, 2)

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          laundering_risk_score    × 0.30
          sanctions_exposure_score × 0.25
          darknet_flow_score       × 0.25
          traceability_gap_score   × 0.20
        """
        score = (
            self.laundering_risk_score    * 0.30
            + self.sanctions_exposure_score * 0.25
            + self.darknet_flow_score       * 0.25
            + self.traceability_gap_score   * 0.20
        )
        return round(score, 2)

    def _compute_risk_level(self) -> str:
        if self.composite_score >= 60:
            return "critique"
        if self.composite_score >= 40:
            return "élevé"
        if self.composite_score >= 20:
            return "modéré"
        return "faible"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id":                self.entity_id,
            "name":                     self.name,
            "country":                  self.country,
            "sector":                   self.sector,
            "composite_score":          self.composite_score,
            "laundering_risk_score":    self.laundering_risk_score,
            "sanctions_exposure_score": self.sanctions_exposure_score,
            "darknet_flow_score":       self.darknet_flow_score,
            "traceability_gap_score":   self.traceability_gap_score,
            "risk_level":               self.risk_level,
            "primary_pattern":          self.primary_pattern,
            "key_signals":              self.key_signals,
            "estimated_crypto_index":   self.estimated_crypto_index,
            "last_updated":             self.last_updated,
            "watchlist_flag":           self.risk_level in ("critique", "élevé"),
        }


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name":        "Blanchiment Crypto Structuré",
        "severity_fr": "critique",
        "action_fr":   "Signalement immédiat TRACFIN et gel des avoirs crypto",
        "signal_fr":   "laundering_risk_score > 80",
    },
    {
        "name":        "Transaction Entité Sanctionnée",
        "severity_fr": "critique",
        "action_fr":   "Blocage transaction et notification autorités OFAC/UE",
        "signal_fr":   "sanctions_exposure_score > 75",
    },
    {
        "name":        "Flux Marché Darknet",
        "severity_fr": "élevé",
        "action_fr":   "Analyse blockchain forensique et coopération Europol",
        "signal_fr":   "darknet_flow_score > 65",
    },
    {
        "name":        "Opacité Mixer Crypto",
        "severity_fr": "élevé",
        "action_fr":   "Due diligence renforcée et rapport AML automatisé",
        "signal_fr":   "traceability_gap_score > 60",
    },
    {
        "name":        "Paiement Ransomware Détecté",
        "severity_fr": "modéré",
        "action_fr":   "Identification portefeuille et signalement CERT/ANSSI",
        "signal_fr":   "darknet_flow_score between 40-65",
    },
]


# ── Engine ────────────────────────────────────────────────────────────────────

class CryptoFinancialCrimeEngine:
    """
    Swarm Intelligence module for crypto-asset financial crime surveillance.

    Computes composite crime scores, detects laundering/darknet/sanctions
    patterns, and surfaces actionable intelligence for Caelum Partners.
    """

    def __init__(self) -> None:
        self.entities: List[CryptoEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "CryptoFinancialCrimeEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[CryptoEntity]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: 3 critique, 2 élevé, 1 modéré, 2 faible.

        Composite formula verification:
          CRP-001: 92*0.30 + 88*0.25 + 85*0.25 + 80*0.20
                 = 27.6 + 22.0 + 21.25 + 16.0 = 86.85  → critique ✓
          CRP-002: 85*0.30 + 82*0.25 + 78*0.25 + 75*0.20
                 = 25.5 + 20.5 + 19.5 + 15.0 = 80.5    → critique ✓
          CRP-003: 78*0.30 + 72*0.25 + 88*0.25 + 82*0.20
                 = 23.4 + 18.0 + 22.0 + 16.4 = 79.8    → critique ✓
          CRP-004: 55*0.30 + 48*0.25 + 52*0.25 + 58*0.20
                 = 16.5 + 12.0 + 13.0 + 11.6 = 53.1    → élevé ✓
          CRP-005: 58*0.30 + 50*0.25 + 55*0.25 + 62*0.20
                 = 17.4 + 12.5 + 13.75 + 12.4 = 56.05  → élevé ✓
          CRP-006: 42*0.30 + 35*0.25 + 38*0.25 + 40*0.20
                 = 12.6 + 8.75 + 9.5 + 8.0 = 38.85     → modéré ✓
          CRP-007: 10*0.30 + 8*0.25 + 5*0.25 + 12*0.20
                 = 3.0 + 2.0 + 1.25 + 2.4 = 8.65       → faible ✓
          CRP-008: 8*0.30 + 6*0.25 + 4*0.25 + 10*0.20
                 = 2.4 + 1.5 + 1.0 + 2.0 = 6.9         → faible ✓
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            {
                "entity_id":                "CRP-001",
                "name":                     "DarkChain Exchange",
                "country":                  "Russie",
                "sector":                   "Exchange Crypto",
                "laundering_risk_score":    92.0,
                "sanctions_exposure_score": 88.0,
                "darknet_flow_score":       85.0,
                "traceability_gap_score":   80.0,
                "primary_pattern":          "Blanchiment Crypto Structuré",
                "key_signals": [
                    "$2.3B transactions sanctionnées OFAC",
                    "Mixing automatique tous fonds",
                    "Adresses Hydra Market liées",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id":                "CRP-002",
                "name":                     "NovaCoin Broker",
                "country":                  "Émirats Arabes Unis",
                "sector":                   "OTC Crypto",
                "laundering_risk_score":    85.0,
                "sanctions_exposure_score": 82.0,
                "darknet_flow_score":       78.0,
                "traceability_gap_score":   75.0,
                "primary_pattern":          "Transaction Entité Sanctionnée",
                "key_signals": [
                    "Transactions directes entités IRGC",
                    "KYC minimal contourné",
                    "Portefeuilles multisig opaques",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id":                "CRP-003",
                "name":                     "TorSwap Protocol",
                "country":                  "Anonyme",
                "sector":                   "DEX Anonyme",
                "laundering_risk_score":    78.0,
                "sanctions_exposure_score": 72.0,
                "darknet_flow_score":       88.0,
                "traceability_gap_score":   82.0,
                "primary_pattern":          "Flux Marché Darknet",
                "key_signals": [
                    "Interface Tor exclusive",
                    "80% flux darknet tracés",
                    "Absence totale AML",
                ],
                "last_updated": "2026-06-20",
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            {
                "entity_id":                "CRP-004",
                "name":                     "MixMaster Finance",
                "country":                  "Pays-Bas",
                "sector":                   "Mixing Service",
                "laundering_risk_score":    55.0,
                "sanctions_exposure_score": 48.0,
                "darknet_flow_score":       52.0,
                "traceability_gap_score":   58.0,
                "primary_pattern":          "Opacité Mixer Crypto",
                "key_signals": [
                    "Service tumbling Bitcoin",
                    "CoinJoin automatisé",
                    "Utilisateurs VPN masqués",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id":                "CRP-005",
                "name":                     "RansomTrack Wallet",
                "country":                  "Ukraine",
                "sector":                   "Portefeuille Crypto",
                "laundering_risk_score":    58.0,
                "sanctions_exposure_score": 50.0,
                "darknet_flow_score":       55.0,
                "traceability_gap_score":   62.0,
                "primary_pattern":          "Paiement Ransomware Détecté",
                "key_signals": [
                    "Paiements REvil confirmés",
                    "Conversion rapide USDT",
                    "Dispersion multi-wallets",
                ],
                "last_updated": "2026-06-20",
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "entity_id":                "CRP-006",
                "name":                     "GreyZone Trading",
                "country":                  "Malte",
                "sector":                   "Trading Crypto",
                "laundering_risk_score":    42.0,
                "sanctions_exposure_score": 35.0,
                "darknet_flow_score":       38.0,
                "traceability_gap_score":   40.0,
                "primary_pattern":          "Opacité Mixer Crypto",
                "key_signals": [
                    "KYC partiel implémenté",
                    "Transactions suspectes modérées",
                    "Conformité AML en cours",
                ],
                "last_updated": "2026-06-20",
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "entity_id":                "CRP-007",
                "name":                     "Coinbase Institutional",
                "country":                  "USA",
                "sector":                   "Exchange Régulé",
                "laundering_risk_score":    10.0,
                "sanctions_exposure_score":  8.0,
                "darknet_flow_score":        5.0,
                "traceability_gap_score":   12.0,
                "primary_pattern":          "Blanchiment Crypto Structuré",
                "key_signals": [
                    "Licence BitLicense NY",
                    "OFAC screening temps réel",
                    "Chainalysis intégré",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id":                "CRP-008",
                "name":                     "Kraken Europe MiCA",
                "country":                  "Irlande",
                "sector":                   "Exchange Régulé",
                "laundering_risk_score":     8.0,
                "sanctions_exposure_score":  6.0,
                "darknet_flow_score":        4.0,
                "traceability_gap_score":   10.0,
                "primary_pattern":          "Transaction Entité Sanctionnée",
                "key_signals": [
                    "Conformité MiCA certifiée",
                    "AML niveau bancaire",
                    "Reporting automatique AMLA",
                ],
                "last_updated": "2026-06-20",
            },
        ]

        return [CryptoEntity(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé":    sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré":   sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible":   sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution: Dict[str, int] = {}
        for e in self.entities:
            pattern_distribution[e.primary_pattern] = (
                pattern_distribution.get(e.primary_pattern, 0) + 1
            )

        sorted_by_score = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_by_score[:3]]
        critical_alerts = risk_distribution["critique"]
        avg_estimated_crypto_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities":             n,
            "avg_composite":              avg_composite,
            "risk_distribution":          risk_distribution,
            "pattern_distribution":       pattern_distribution,
            "top_risk_entities":          top_risk_entities,
            "critical_alerts":            critical_alerts,
            "last_analysis":              "2026-06-20",
            "engine_version":             "1.0.0",
            "domain":                     "crypto",
            "confidence_score":           0.91,
            "data_sources": [
                "OFAC SDN List",
                "Chainalysis Reactor",
                "Europol EC3 Darknet Reports",
                "TRACFIN Intelligence",
                "CipherTrace AML",
            ],
            "entities":                   [e.to_dict() for e in self.entities],
            "avg_estimated_crypto_index": avg_estimated_crypto_index,
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[CryptoEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def get_entity_patterns(self, entity: CryptoEntity) -> List[Dict[str, str]]:
        """Return the list of pattern dicts matching the entity's primary pattern."""
        return [p for p in PATTERNS if p["name"] == entity.primary_pattern]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary":  self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level convenience function ─────────────────────────────────────────

def analyze_crypto() -> Dict[str, Any]:
    """
    Module-level entry point for the Caelum Partners Swarm orchestrator.

    Returns the full engine export (entities + summary + patterns).
    """
    engine = CryptoFinancialCrimeEngine()
    return engine.export()
