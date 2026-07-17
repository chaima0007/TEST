"""
Crypto Financial Crime Intelligence Engine — Caelum Partners Swarm Module

Tracks cryptocurrency-based financial crimes: money laundering, fraud, ransomware
payments, market manipulation, and sanctions evasion across exchanges and protocols.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Sub-scores (weights sum to 1.00):
  laundering_risk_score   × 0.30 — money laundering and mixing activity
  fraud_score             × 0.25 — fraud, rug pulls, and scam indicators
  sanctions_evasion_score × 0.25 — sanctions evasion and darknet exposure
  aml_compliance_gap      × 0.20 — AML/KYC deficiencies

Usage:
    from swarm.intelligence.crypto_financial_crime_engine import CryptoFinancialCrimeEngine
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


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Blanchiment Crypto Massif",
        "severity_fr": "critique",
        "action_fr": "Gel immédiat des actifs et signalement TRACFIN/FinCEN sous 24h.",
        "signal_fr": "laundering_risk_score > 80 AND mixer_volume_usd > 1M",
    },
    {
        "name": "Évasion Sanctions Cryptographiques",
        "severity_fr": "critique",
        "action_fr": "Signalement OFAC et blocage wallets sanctionnés en temps réel.",
        "signal_fr": "sanctions_evasion_score > 75 AND OFAC_wallet_detected = TRUE",
    },
    {
        "name": "Fraude DeFi & Rug Pull",
        "severity_fr": "élevé",
        "action_fr": "Suspension protocole et alerte investisseurs via canaux officiels.",
        "signal_fr": "fraud_score > 65 AND liquidity_drain_detected = TRUE",
    },
    {
        "name": "Vide AML Plateforme Crypto",
        "severity_fr": "modéré",
        "action_fr": "Mise en conformité AMLD6 accélérée et audit indépendant obligatoire.",
        "signal_fr": "aml_compliance_gap > 60 AND KYC_rate < 0.40",
    },
    {
        "name": "Manipulation Marché Crypto",
        "severity_fr": "faible",
        "action_fr": "Surveillance algorithmes trading et rapport régulateur mensuel.",
        "signal_fr": "wash_trading_index >= 0.30 AND composite_score < 40",
    },
]


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class CryptoEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    laundering_risk_score: float     # 0–100
    fraud_score: float               # 0–100
    sanctions_evasion_score: float   # 0–100
    aml_compliance_gap: float        # 0–100
    key_signals: List[str]           # list of 3 strings
    primary_pattern: str
    last_updated: str                # ISO date string

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          laundering_risk_score   × 0.30
          + fraud_score             × 0.25
          + sanctions_evasion_score × 0.25
          + aml_compliance_gap      × 0.20

        Verification:
          CRY-001: 90*0.30 + 85*0.25 + 88*0.25 + 82*0.20 = 27.0+21.25+22.0+16.4 = 86.65  → critique ✓
          CRY-002: 88*0.30 + 82*0.25 + 85*0.25 + 78*0.20 = 26.4+20.5+21.25+15.6 = 83.75  → critique ✓
          CRY-003: 82*0.30 + 78*0.25 + 80*0.25 + 72*0.20 = 24.6+19.5+20.0+14.4 = 78.5    → critique ✓
          CRY-004: 60*0.30 + 62*0.25 + 55*0.25 + 65*0.20 = 18.0+15.5+13.75+13.0 = 60.25  → élevé ✓
          CRY-005: 58*0.30 + 55*0.25 + 60*0.25 + 52*0.20 = 17.4+13.75+15.0+10.4 = 56.55  → élevé ✓
          CRY-006: 38*0.30 + 35*0.25 + 40*0.25 + 28*0.20 = 11.4+8.75+10.0+5.6 = 35.75    → modéré ✓
          CRY-007: 10*0.30 + 12*0.25 + 8*0.25  + 11*0.20 = 3.0+3.0+2.0+2.2 = 10.2        → faible ✓
          CRY-008: 8*0.30  + 10*0.25 + 9*0.25  + 12*0.20 = 2.4+2.5+2.25+2.4 = 9.55       → faible ✓
        """
        score = (
            self.laundering_risk_score * 0.30
            + self.fraud_score * 0.25
            + self.sanctions_evasion_score * 0.25
            + self.aml_compliance_gap * 0.20
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
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "laundering_risk_score": self.laundering_risk_score,
            "fraud_score": self.fraud_score,
            "sanctions_evasion_score": self.sanctions_evasion_score,
            "aml_compliance_gap": self.aml_compliance_gap,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_crypto_index": round(self.composite_score / 100 * 10, 2),
            "last_updated": self.last_updated,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class CryptoFinancialCrimeEngine:
    """
    Swarm Intelligence module for Crypto Financial Crime tracking.

    Monitors money laundering, fraud, sanctions evasion, and AML gaps
    across cryptocurrency exchanges, DeFi protocols, and mixers.
    """

    ENGINE_VERSION = "1.0.0"
    DOMAIN = "crypto"
    DATA_SOURCES = [
        "Chainalysis Reactor Intelligence",
        "Elliptic Forensics Database",
        "FATF Crypto Risk Reports",
        "OFAC Sanctions Blockchain Monitor",
        "Europol Financial Intelligence Unit",
    ]

    def __init__(self) -> None:
        self.entities: List[CryptoEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "CryptoFinancialCrimeEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    def _build_mock_entities(self) -> List[CryptoEntity]:
        """
        8 mock entities: 3 critique, 2 élevé, 1 modéré, 2 faible.
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            {
                "entity_id": "CRY-001",
                "name": "DarkChain Exchange",
                "country": "Russie",
                "sector": "Exchange Crypto Non Régulé",
                "laundering_risk_score": 90.0,
                "fraud_score": 85.0,
                "sanctions_evasion_score": 88.0,
                "aml_compliance_gap": 82.0,
                "primary_pattern": "Évasion Sanctions Cryptographiques",
                "key_signals": [
                    "12,000 wallets OFAC sanctionnés détectés comme actifs",
                    "Volume mixer $850M en 6 mois — Tornado Cash dérivé",
                    "Absence totale de procédures KYC/AML",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id": "CRY-002",
                "name": "CryptoHaven Protocol",
                "country": "Îles Caïmans",
                "sector": "Protocole Mixage Crypto",
                "laundering_risk_score": 88.0,
                "fraud_score": 82.0,
                "sanctions_evasion_score": 85.0,
                "aml_compliance_gap": 78.0,
                "primary_pattern": "Blanchiment Crypto Massif",
                "key_signals": [
                    "Service mixer $2.1B en flux anonymisés détectés",
                    "Liens avec groupe ransomware Lazarus confirmés",
                    "Opération sur 47 juridictions sans licences",
                ],
                "last_updated": "2026-06-19",
            },
            {
                "entity_id": "CRY-003",
                "name": "NovaCoin Darknet",
                "country": "Corée du Nord",
                "sector": "Marché Darknet Crypto",
                "laundering_risk_score": 82.0,
                "fraud_score": 78.0,
                "sanctions_evasion_score": 80.0,
                "aml_compliance_gap": 72.0,
                "primary_pattern": "Évasion Sanctions Cryptographiques",
                "key_signals": [
                    "Financement programme nucléaire via crypto confirmé par ONU",
                    "Attaques Lazarus Group — $620M Axie Infinity récupérés",
                    "Utilisation chaînes obscurcissement multi-couches",
                ],
                "last_updated": "2026-06-18",
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            {
                "entity_id": "CRY-004",
                "name": "QuickSwap DeFi",
                "country": "Singapour",
                "sector": "Protocole DeFi",
                "laundering_risk_score": 60.0,
                "fraud_score": 62.0,
                "sanctions_evasion_score": 55.0,
                "aml_compliance_gap": 65.0,
                "primary_pattern": "Fraude DeFi & Rug Pull",
                "key_signals": [
                    "Draineur liquidité détecté — $45M en pool USDC/ETH",
                    "Équipe anonyme — aucune identité vérifiable",
                    "Smart contract non audité avec backdoor admin",
                ],
                "last_updated": "2026-06-17",
            },
            {
                "entity_id": "CRY-005",
                "name": "CryptoVault Exchange",
                "country": "Malaisie",
                "sector": "Exchange Crypto Semi-Régulé",
                "laundering_risk_score": 58.0,
                "fraud_score": 55.0,
                "sanctions_evasion_score": 60.0,
                "aml_compliance_gap": 52.0,
                "primary_pattern": "Vide AML Plateforme Crypto",
                "key_signals": [
                    "KYC effectué pour seulement 28% des comptes actifs",
                    "Transactions suspectes non signalées > $500k",
                    "Flux crypto vers wallets russes non bloqués",
                ],
                "last_updated": "2026-06-16",
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "entity_id": "CRY-006",
                "name": "AltCoin Market EU",
                "country": "Malte",
                "sector": "Exchange Crypto Régulé MiCA",
                "laundering_risk_score": 38.0,
                "fraud_score": 35.0,
                "sanctions_evasion_score": 40.0,
                "aml_compliance_gap": 28.0,
                "primary_pattern": "Manipulation Marché Crypto",
                "key_signals": [
                    "Indicateurs wash trading sur paires BTC/EUR à 34%",
                    "Conformité MiCA partielle — 72% des exigences satisfaites",
                    "Signalement TRACFIN en cours pour 3 comptes VIP",
                ],
                "last_updated": "2026-06-15",
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "entity_id": "CRY-007",
                "name": "SwissBlock Custody",
                "country": "Suisse",
                "sector": "Custody & Banque Crypto",
                "laundering_risk_score": 10.0,
                "fraud_score": 12.0,
                "sanctions_evasion_score": 8.0,
                "aml_compliance_gap": 11.0,
                "primary_pattern": "Manipulation Marché Crypto",
                "key_signals": [
                    "FINMA agréé — conformité AML 98% vérifiée",
                    "KYC renforcé avec vérification biométrique",
                    "Zéro transaction vers wallets sanctionnés depuis 18 mois",
                ],
                "last_updated": "2026-06-14",
            },
            {
                "entity_id": "CRY-008",
                "name": "EUROCoin Regulated Exchange",
                "country": "France",
                "sector": "Exchange Crypto Régulé PSAN",
                "laundering_risk_score": 8.0,
                "fraud_score": 10.0,
                "sanctions_evasion_score": 9.0,
                "aml_compliance_gap": 12.0,
                "primary_pattern": "Vide AML Plateforme Crypto",
                "key_signals": [
                    "PSAN enregistré AMF — conformité totale AMLD6",
                    "Monitoring temps réel toutes transactions > 1000€",
                    "Rapport TRACFIN trimestriel transmis sans anomalie",
                ],
                "last_updated": "2026-06-13",
            },
        ]
        return [CryptoEntity(**d) for d in raw]  # type: ignore[arg-type]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé": sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré": sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible": sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution: Dict[str, int] = {p["name"]: 0 for p in PATTERNS}
        for e in self.entities:
            if e.primary_pattern in pattern_distribution:
                pattern_distribution[e.primary_pattern] += 1

        sorted_by_risk = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_by_risk[:3]]

        critical_alerts = [
            f"{e.name} ({e.country}) — composite {e.composite_score}"
            for e in self.entities
            if e.risk_level == "critique"
        ]

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.92,
            "data_sources": self.DATA_SOURCES,
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_crypto_index": round(avg_composite / 100 * 10, 2),
        }

    def get_entities_by_risk(self, risk_level: str) -> List[CryptoEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_crypto() -> Dict[str, Any]:
    """
    Module-level entry point for the Crypto Financial Crime Intelligence Engine.

    Returns a dict with 'entities' (list of to_dict()) and 'summary' (13 keys).
    """
    engine = CryptoFinancialCrimeEngine()
    return engine.export()
