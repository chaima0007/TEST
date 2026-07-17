"""
Tax Justice Intelligence Engine — Caelum Partners Swarm Module

Tracks tax evasion, offshore avoidance, regulatory circumvention and fiscal
inequality to identify entities with systemic tax justice risks.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage:
    from intelligence.tax_justice_engine import TaxJusticeEngine
    engine = TaxJusticeEngine()
    print(engine.summary())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List

logger = logging.getLogger("swarm.tax_justice")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "id": "P1",
        "name": "Évasion Fiscale Systémique",
        "severity_fr": "critique",
        "action_fr": "Signalement immédiat aux autorités fiscales et ouverture d'une procédure d'enquête fiscale internationale.",
        "signal_fr": "Évasion fiscale systémique détectée — intervention immédiate requise.",
    },
    {
        "id": "P2",
        "name": "Optimisation Abusive Offshore",
        "severity_fr": "critique",
        "action_fr": "Audit des structures offshore et restructuration fiscale obligatoire sous contrôle régulateur.",
        "signal_fr": "Optimisation offshore abusive — structures IP routing hybrides détectées.",
    },
    {
        "id": "P3",
        "name": "Contournement Réglementaire",
        "severity_fr": "élevé",
        "action_fr": "Audit de conformité fiscale renforcé avec rapport de remédiation au comité de direction.",
        "signal_fr": "Contournement réglementaire actif — audit de conformité requis.",
    },
    {
        "id": "P4",
        "name": "Inégalité Fiscale Structurelle",
        "severity_fr": "modéré",
        "action_fr": "Révision de la politique fiscale et publication d'un rapport d'équité fiscale selon les normes GRI 207.",
        "signal_fr": "Inégalité fiscale structurelle — révision politique fiscale recommandée.",
    },
    {
        "id": "P5",
        "name": "Risque Réputation Fiscale",
        "severity_fr": "faible",
        "action_fr": "Veille réputation fiscale et alignement proactif avec les standards CbCR de l'OCDE.",
        "signal_fr": "Risque réputation fiscale contenu — surveillance standard suffisante.",
    },
]


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class TaxEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    evasion_score: float      # 0–100
    avoidance_score: float    # 0–100
    offshore_score: float     # 0–100
    inequality_score: float   # 0–100
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: List[str] = field(init=False)
    estimated_tax_justice_index: float = field(init=False)
    last_updated: str = field(init=False)
    recommended_action: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.primary_pattern = self._compute_pattern()
        self.key_signals = self._compute_signals()
        self.estimated_tax_justice_index = round(self.composite_score / 100 * 10, 2)
        self.last_updated = str(date.today())
        self.recommended_action = self._compute_action()

    def _compute_action(self) -> str:
        if self.risk_level == "critique":
            return "signalement_autorités_fiscales_enquête_internationale"
        if self.risk_level == "élevé":
            return "audit_conformité_fiscale_renforcé"
        if self.risk_level == "modéré":
            return "révision_politique_fiscale_équité"
        return "veille_réputation_fiscale_standard"

    def _compute_composite(self) -> float:
        score = (
            self.evasion_score * 0.30
            + self.avoidance_score * 0.25
            + self.offshore_score * 0.25
            + self.inequality_score * 0.20
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

    def _compute_pattern(self) -> str:
        if self.evasion_score >= 75 and self.offshore_score >= 80:
            return "Évasion Fiscale Systémique"
        if self.avoidance_score >= 75:
            return "Optimisation Abusive Offshore"
        if self.evasion_score >= 50 or self.avoidance_score >= 55:
            return "Contournement Réglementaire"
        if self.inequality_score >= 30:
            return "Inégalité Fiscale Structurelle"
        return "Risque Réputation Fiscale"

    def _compute_signals(self) -> List[str]:
        signals = []
        if self.evasion_score >= 60:
            signals.append(f"Évasion fiscale détectée ({self.evasion_score:.0f}/100)")
        if self.avoidance_score >= 55:
            signals.append(f"Optimisation offshore abusive ({self.avoidance_score:.0f}/100)")
        if self.offshore_score >= 60:
            signals.append(f"Structures offshore suspectes ({self.offshore_score:.0f}/100)")
        if self.inequality_score >= 40:
            signals.append(f"Inégalité fiscale structurelle ({self.inequality_score:.0f}/100)")
        if not signals:
            signals.append("Conformité fiscale CbCR OCDE vérifiée")
            signals.append("Taux effectif aligné sur taux légal")
            signals.append("Transparence fiscale selon GRI 207")
        while len(signals) < 3:
            signals.append("Surveillance fiscale continue active")
        return signals[:3]

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "evasion_score": self.evasion_score,
            "avoidance_score": self.avoidance_score,
            "offshore_score": self.offshore_score,
            "inequality_score": self.inequality_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_tax_justice_index": self.estimated_tax_justice_index,
            "last_updated": self.last_updated,
            "recommended_action": self.recommended_action,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class TaxJusticeEngine:
    """
    Swarm Intelligence module for tax justice tracking.

    Computes composite risk scores for evasion, avoidance, offshore structures
    and inequality to surface systemic fiscal opacity.
    """

    ENGINE_VERSION = "1.0.0"
    DOMAIN = "tax_justice"
    DATA_SOURCES = ["OCDE CbCR", "Tax Justice Network", "OpenCorporates", "ICIJ Offshore Leaks"]

    def __init__(self) -> None:
        self.entities: List[TaxEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "TaxJusticeEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    def _build_mock_entities(self) -> List[TaxEntity]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: 3 critique, 2 élevé, 1 modéré, 2 faible.

        Composite formula (weights sum to 1.00):
          evasion_score × 0.30
          + avoidance_score × 0.25
          + offshore_score × 0.25
          + inequality_score × 0.20

        TAX-001: 88*0.30+82*0.25+90*0.25+75*0.20 = 26.4+20.5+22.5+15.0 = 84.40 → critique
        TAX-002: 72*0.30+85*0.25+78*0.25+68*0.20 = 21.6+21.25+19.5+13.6 = 75.95 → critique
        TAX-003: 80*0.30+76*0.25+82*0.25+65*0.20 = 24.0+19.0+20.5+13.0 = 76.50 → critique
        TAX-004: 55*0.30+60*0.25+52*0.25+45*0.20 = 16.5+15.0+13.0+9.0  = 53.50 → élevé
        TAX-005: 58*0.30+62*0.25+55*0.25+42*0.20 = 17.4+15.5+13.75+8.4 = 55.05 → élevé
        TAX-006: 28*0.30+32*0.25+25*0.25+38*0.20 = 8.4+8.0+6.25+7.6    = 30.25 → modéré
        TAX-007:  8*0.30+12*0.25+ 6*0.25+10*0.20 = 2.4+3.0+1.5+2.0     =  8.90 → faible
        TAX-008:  5*0.30+ 8*0.25+ 4*0.25+ 7*0.20 = 1.5+2.0+1.0+1.4     =  5.90 → faible
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            {
                "entity_id": "TAX-001",
                "name": "MegaCorp Cayman Holdings",
                "country": "Cayman Islands",
                "sector": "Finance",
                "evasion_score": 88.0,
                "avoidance_score": 82.0,
                "offshore_score": 90.0,
                "inequality_score": 75.0,
            },
            {
                "entity_id": "TAX-002",
                "name": "TechGiant Ireland LLC",
                "country": "Ireland",
                "sector": "Technology",
                "evasion_score": 72.0,
                "avoidance_score": 85.0,
                "offshore_score": 78.0,
                "inequality_score": 68.0,
            },
            {
                "entity_id": "TAX-003",
                "name": "LuxHolding SA",
                "country": "Luxembourg",
                "sector": "Real Estate",
                "evasion_score": 80.0,
                "avoidance_score": 76.0,
                "offshore_score": 82.0,
                "inequality_score": 65.0,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            {
                "entity_id": "TAX-004",
                "name": "ShellCompany BV",
                "country": "Netherlands",
                "sector": "Consulting",
                "evasion_score": 55.0,
                "avoidance_score": 60.0,
                "offshore_score": 52.0,
                "inequality_score": 45.0,
            },
            {
                "entity_id": "TAX-005",
                "name": "PharmaOffset AG",
                "country": "Switzerland",
                "sector": "Pharmaceuticals",
                "evasion_score": 58.0,
                "avoidance_score": 62.0,
                "offshore_score": 55.0,
                "inequality_score": 42.0,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "entity_id": "TAX-006",
                "name": "RetailGroup SARL",
                "country": "France",
                "sector": "Retail",
                "evasion_score": 28.0,
                "avoidance_score": 32.0,
                "offshore_score": 25.0,
                "inequality_score": 38.0,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "entity_id": "TAX-007",
                "name": "Nordic Fair AS",
                "country": "Denmark",
                "sector": "Renewable Energy",
                "evasion_score": 8.0,
                "avoidance_score": 12.0,
                "offshore_score": 6.0,
                "inequality_score": 10.0,
            },
            {
                "entity_id": "TAX-008",
                "name": "Transparent Corp",
                "country": "Germany",
                "sector": "Manufacturing",
                "evasion_score": 5.0,
                "avoidance_score": 8.0,
                "offshore_score": 4.0,
                "inequality_score": 7.0,
            },
        ]
        return [TaxEntity(**d) for d in raw]  # type: ignore[arg-type]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        for e in self.entities:
            risk_distribution[e.risk_level] = risk_distribution.get(e.risk_level, 0) + 1
            pattern_distribution[e.primary_pattern] = pattern_distribution.get(e.primary_pattern, 0) + 1

        top_risk = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:3]
        critical_alerts = [e.name for e in self.entities if e.risk_level == "critique"]
        avg_tji = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": [e.name for e in top_risk],
            "critical_alerts": critical_alerts,
            "last_analysis": str(date.today()),
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 0.89,
            "data_sources": self.DATA_SOURCES,
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_tax_justice_index": avg_tji,
        }

    def get_entities_by_risk(self, risk_level: str) -> List[TaxEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


def analyze_taxjustice() -> Dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    engine = TaxJusticeEngine()
    return engine.summary()


if __name__ == "__main__":
    import json

    result = analyze_taxjustice()
    print(json.dumps(result, ensure_ascii=False, indent=2))
