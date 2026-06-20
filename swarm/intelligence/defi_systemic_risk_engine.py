"""
DeFi Systemic Risk Intelligence Engine — Caelum Partners Swarm Module

Tracks systemic risks in decentralized finance (DeFi): protocol exploits,
liquidity crises, oracle manipulation, contagion risks, stablecoin depegs,
governance attacks.

Composite score = protocol_risk_score*0.30 + liquidity_risk_score*0.25
                + contagion_risk_score*0.25 + governance_risk_score*0.20

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage:
    from intelligence.defi_systemic_risk_engine import DeFiSystemicRiskEngine
    engine = DeFiSystemicRiskEngine()
    print(engine.summary())
    for entity in engine.entities:
        print(entity.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.defi_systemic_risk")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Exploit Protocole Critique",
        "severity_fr": "critique",
        "action_fr": "Pause protocole immédiate et activation war room sécurité",
        "signal_fr": "protocol_risk_score > 80",
    },
    {
        "name": "Crise Liquidité Systémique",
        "severity_fr": "critique",
        "action_fr": "Injection liquidité d'urgence et coordination market makers",
        "signal_fr": "liquidity_risk_score > 75",
    },
    {
        "name": "Contagion Inter-Protocoles",
        "severity_fr": "élevé",
        "action_fr": "Isolation exposition contagion et audit dépendances croisées",
        "signal_fr": "contagion_risk_score > 65",
    },
    {
        "name": "Attaque Gouvernance DAO",
        "severity_fr": "élevé",
        "action_fr": "Veto proposition et révision mécanisme gouvernance",
        "signal_fr": "governance_risk_score > 60",
    },
    {
        "name": "Dépeg Stablecoin Partiel",
        "severity_fr": "modéré",
        "action_fr": "Surveillance maintien ancrage et réserves collatéral vérifiées",
        "signal_fr": "liquidity_risk_score between 40-75",
    },
]


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class DeFiEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    protocol_risk_score: float    # 0–100
    liquidity_risk_score: float   # 0–100
    contagion_risk_score: float   # 0–100
    governance_risk_score: float  # 0–100
    key_signals: List[str]        # exactly 3 strings
    last_updated: str             # ISO date string
    _primary_pattern_override: str = field(default="", repr=False)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    estimated_defi_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.primary_pattern = (
            self._primary_pattern_override
            if self._primary_pattern_override
            else self._compute_primary_pattern()
        )
        self.estimated_defi_index = round(self.composite_score / 100 * 10, 2)

    def _compute_composite(self) -> float:
        """
        Weighted composite score (weights sum to 1.00):
          protocol_risk_score   × 0.30
          liquidity_risk_score  × 0.25
          contagion_risk_score  × 0.25
          governance_risk_score × 0.20
        """
        score = (
            self.protocol_risk_score * 0.30
            + self.liquidity_risk_score * 0.25
            + self.contagion_risk_score * 0.25
            + self.governance_risk_score * 0.20
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

    def _compute_primary_pattern(self) -> str:
        if self.protocol_risk_score > 80:
            return "Exploit Protocole Critique"
        if self.liquidity_risk_score > 75:
            return "Crise Liquidité Systémique"
        if self.contagion_risk_score > 65:
            return "Contagion Inter-Protocoles"
        if self.governance_risk_score > 60:
            return "Attaque Gouvernance DAO"
        if 40 <= self.liquidity_risk_score <= 75:
            return "Dépeg Stablecoin Partiel"
        return "Exploit Protocole Critique"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys:
        entity_id, name, country, sector, composite_score,
        protocol_risk_score, liquidity_risk_score, contagion_risk_score, governance_risk_score,
        risk_level, primary_pattern, key_signals, estimated_defi_index, last_updated,
        domain
        """
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "protocol_risk_score": self.protocol_risk_score,
            "liquidity_risk_score": self.liquidity_risk_score,
            "contagion_risk_score": self.contagion_risk_score,
            "governance_risk_score": self.governance_risk_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_defi_index": self.estimated_defi_index,
            "last_updated": self.last_updated,
            "domain": "defi",
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class DeFiSystemicRiskEngine:
    """
    Swarm Intelligence module for DeFi systemic risk tracking.

    Computes composite risk scores across protocol, liquidity, contagion and
    governance dimensions to detect critical DeFi risks for Caelum Partners.
    """

    VERSION = "1.0.0"
    DOMAIN = "defi"
    DATA_SOURCES = [
        "DeFiLlama Protocol Data",
        "Chainalysis On-Chain Analytics",
        "OpenZeppelin Security Audits",
        "Dune Analytics DeFi Metrics",
        "CoinGecko Market Data",
        "DAO Governance Snapshot",
        "Certik Audit Reports",
        "Nansen Wallet Intelligence",
    ]

    def __init__(self) -> None:
        self.entities: List[DeFiEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "DeFiSystemicRiskEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[DeFiEntity]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: 3 critique, 2 élevé, 1 modéré, 2 faible.

        Composite formula verification:
          DFI-001: 92.0*0.30 + 85.0*0.25 + 88.0*0.25 + 80.0*0.20
                 = 27.6 + 21.25 + 22.0 + 16.0 = 86.85   → critique ✓
          DFI-002: 82.0*0.30 + 90.0*0.25 + 85.0*0.25 + 75.0*0.20
                 = 24.6 + 22.5 + 21.25 + 15.0 = 83.35   → critique ✓
          DFI-003: 78.0*0.30 + 72.0*0.25 + 80.0*0.25 + 88.0*0.20
                 = 23.4 + 18.0 + 20.0 + 17.6 = 79.0     → critique ✓
          DFI-004: 35.0*0.30 + 45.0*0.25 + 68.0*0.25 + 40.0*0.20
                 = 10.5 + 11.25 + 17.0 + 8.0 = 46.75    → élevé ✓
          DFI-005: 45.0*0.30 + 55.0*0.25 + 42.0*0.25 + 38.0*0.20
                 = 13.5 + 13.75 + 10.5 + 7.6 = 45.35    → élevé ✓
          DFI-006: 42.0*0.30 + 38.0*0.25 + 40.0*0.25 + 35.0*0.20
                 = 12.6 + 9.5 + 10.0 + 7.0 = 39.1       → modéré ✓
          DFI-007: 12.0*0.30 + 10.0*0.25 + 8.0*0.25 + 15.0*0.20
                 = 3.6 + 2.5 + 2.0 + 3.0 = 11.1         → faible ✓
          DFI-008: 8.0*0.30 + 6.0*0.25 + 10.0*0.25 + 12.0*0.20
                 = 2.4 + 1.5 + 2.5 + 2.4 = 8.8          → faible ✓
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # Exploit Protocole Critique — protocol_risk > 80
            {
                "entity_id": "DFI-001",
                "name": "VulnSwap Protocol",
                "country": "Anonyme",
                "sector": "DEX / AMM",
                "protocol_risk_score": 92.0,
                "liquidity_risk_score": 85.0,
                "contagion_risk_score": 88.0,
                "governance_risk_score": 80.0,
                "key_signals": [
                    "Reentrancy bug confirmé audit",
                    "$450M TVL à risque immédiat",
                    "Dépendances 12 protocoles connectés",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Exploit Protocole Critique",
            },
            # Crise Liquidité Systémique — liquidity_risk > 75
            {
                "entity_id": "DFI-002",
                "name": "TerraClone Finance",
                "country": "Corée du Sud",
                "sector": "Stablecoin Algorithmique",
                "protocol_risk_score": 82.0,
                "liquidity_risk_score": 90.0,
                "contagion_risk_score": 85.0,
                "governance_risk_score": 75.0,
                "key_signals": [
                    "Mécanisme ancrage similaire Terra-LUNA",
                    "Réserves insuffisantes run bancaire",
                    "Contagion pools Curve/Balancer",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Crise Liquidité Systémique",
            },
            # Attaque Gouvernance DAO — governance_risk 88 > 60
            {
                "entity_id": "DFI-003",
                "name": "WhaleDAO Governance",
                "country": "Îles Caïmans",
                "sector": "Protocole Gouvernance",
                "protocol_risk_score": 78.0,
                "liquidity_risk_score": 72.0,
                "contagion_risk_score": 80.0,
                "governance_risk_score": 88.0,
                "key_signals": [
                    "3 baleines = 67% votes",
                    "Proposition hostile soumise",
                    "Quorum aisément manipulable",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Attaque Gouvernance DAO",
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # Contagion Inter-Protocoles — contagion_risk 68 > 65, composite 46.75 → élevé
            {
                "entity_id": "DFI-004",
                "name": "CrossChain Bridge Alpha",
                "country": "Singapour",
                "sector": "Bridge Inter-Chaînes",
                "protocol_risk_score": 35.0,
                "liquidity_risk_score": 45.0,
                "contagion_risk_score": 68.0,
                "governance_risk_score": 40.0,
                "key_signals": [
                    "Bridge historiquement exploité",
                    "Validateurs centralisés 5 nœuds",
                    "$1.2B locked sans assurance",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Contagion Inter-Protocoles",
            },
            # Dépeg Stablecoin Partiel — liquidity 55 between 40-75, composite 45.35 → élevé
            {
                "entity_id": "DFI-005",
                "name": "LeverageFarm Ultra",
                "country": "Îles Vierges Britanniques",
                "sector": "Yield Farming Levieré",
                "protocol_risk_score": 45.0,
                "liquidity_risk_score": 55.0,
                "contagion_risk_score": 42.0,
                "governance_risk_score": 38.0,
                "key_signals": [
                    "Levier 20x positions ouvertes",
                    "Oracle Chainlink mono-source",
                    "Liquidations en cascade risque",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Dépeg Stablecoin Partiel",
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # Dépeg Stablecoin Partiel — liquidity 38, but closest pattern for moderate
            {
                "entity_id": "DFI-006",
                "name": "StableYield Moderate",
                "country": "Suisse",
                "sector": "Lending Protocol",
                "protocol_risk_score": 42.0,
                "liquidity_risk_score": 38.0,
                "contagion_risk_score": 40.0,
                "governance_risk_score": 35.0,
                "key_signals": [
                    "Collatéral excédentaire 150%",
                    "Audit Certik récent",
                    "Gouvernance multi-sig 5/9",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Dépeg Stablecoin Partiel",
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # Exploit Protocole Critique pattern (low risk, well audited)
            {
                "entity_id": "DFI-007",
                "name": "Aave Secure V4",
                "country": "Royaume-Uni",
                "sector": "Lending Régulé",
                "protocol_risk_score": 12.0,
                "liquidity_risk_score": 10.0,
                "contagion_risk_score": 8.0,
                "governance_risk_score": 15.0,
                "key_signals": [
                    "3 audits majeurs annuels",
                    "Circuit breaker automatique",
                    "Gouvernance décentralisée réelle",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Exploit Protocole Critique",
            },
            # Attaque Gouvernance DAO pattern (low risk, healthy governance)
            {
                "entity_id": "DFI-008",
                "name": "Uniswap Foundation",
                "country": "USA",
                "sector": "DEX Mature",
                "protocol_risk_score": 8.0,
                "liquidity_risk_score": 6.0,
                "contagion_risk_score": 10.0,
                "governance_risk_score": 12.0,
                "key_signals": [
                    "Liquidité $5B+ dispersée",
                    "Contrats immutables vérifiés",
                    "Gouvernance UNI 300k+ holders",
                ],
                "last_updated": "2026-06-20",
                "_primary_pattern_override": "Attaque Gouvernance DAO",
            },
        ]

        return [DeFiEntity(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

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

        pattern_distribution: Dict[str, int] = {}
        for e in self.entities:
            pattern_distribution[e.primary_pattern] = (
                pattern_distribution.get(e.primary_pattern, 0) + 1
            )

        top_risk_entities = [
            e.name
            for e in sorted(self.entities, key=lambda x: x.composite_score, reverse=True)[:3]
        ]

        critical_alerts = risk_distribution["critique"]
        avg_estimated_defi_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": self.VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.91,
            "data_sources": self.DATA_SOURCES,
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_defi_index": avg_estimated_defi_index,
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[DeFiEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def get_entity_patterns(self, entity: DeFiEntity) -> List[Dict[str, str]]:
        """Return the list of pattern dicts triggered for a given entity."""
        matched = []
        if entity.protocol_risk_score > 80:
            matched.append(PATTERNS[0])
        if entity.liquidity_risk_score > 75:
            matched.append(PATTERNS[1])
        if entity.contagion_risk_score > 65:
            matched.append(PATTERNS[2])
        if entity.governance_risk_score > 60:
            matched.append(PATTERNS[3])
        if 40 <= entity.liquidity_risk_score <= 75:
            matched.append(PATTERNS[4])
        return matched

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_defi() -> Dict[str, Any]:
    """
    Module-level entry point for the DeFi Systemic Risk Engine.

    Returns a dict with 'entities' (list of to_dict()), 'summary' (13 keys),
    and 'patterns' (list of 5 pattern dicts).
    """
    engine = DeFiSystemicRiskEngine()
    return engine.export()
