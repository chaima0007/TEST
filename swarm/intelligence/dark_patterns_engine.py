"""
Dark Patterns Intelligence Engine — Caelum Partners Swarm Module

Tracks deceptive UX/UI dark patterns used by digital platforms:
forced continuity, roach motels, disguised ads, hidden costs,
confirmshaming, trick questions, privacy zuckering.

Computes a composite risk score from 4 sub-scores to identify
high-risk platforms and trigger regulatory/compliance actions.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage:
    from intelligence.dark_patterns_engine import DarkPatternsEngine
    engine = DarkPatternsEngine()
    print(engine.summary())
    for entity in engine.entities:
        print(entity.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.dark_patterns")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Manipulation Consentement Forcé",
        "severity_fr": "critique",
        "action_fr": "Mise en demeure CNIL/DPA immédiate et audit UX obligatoire",
        "signal_fr": "consent_violation_score > 80",
    },
    {
        "name": "Piège Abonnement Caché",
        "severity_fr": "critique",
        "action_fr": "Remboursement automatique utilisateurs et rectification interface",
        "signal_fr": "financial_harm_score > 75",
    },
    {
        "name": "Déceptivité Interface Systémique",
        "severity_fr": "élevé",
        "action_fr": "Redesign UX supervisé par autorité régulation numérique",
        "signal_fr": "manipulation_score > 65",
    },
    {
        "name": "Violation DSA Répétée",
        "severity_fr": "élevé",
        "action_fr": "Plan de conformité DSA accéléré avec deadline 90 jours",
        "signal_fr": "regulatory_risk_score > 60",
    },
    {
        "name": "Monétisation Données Occulte",
        "severity_fr": "modéré",
        "action_fr": "Transparence politique de données et opt-out simplifié",
        "signal_fr": "consent_violation_score between 40-80",
    },
]

# Map pattern name → action for convenience
_PATTERN_ACTIONS: Dict[str, str] = {p["name"]: p["action_fr"] for p in PATTERNS}


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class EntityRecord:
    entity_id: str
    name: str
    country: str
    sector: str
    manipulation_score: float        # 0–100
    consent_violation_score: float   # 0–100
    financial_harm_score: float      # 0–100
    regulatory_risk_score: float     # 0–100
    primary_pattern: str
    key_signals: List[str]           # exactly 3 strings
    last_updated: str                # ISO date string
    # computed
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_darkpattern_index: float = field(init=False)
    recommended_action: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.estimated_darkpattern_index = round(self.composite_score / 100 * 10, 2)
        self.recommended_action = _PATTERN_ACTIONS.get(
            self.primary_pattern, "Audit UX complémentaire requis"
        )

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          manipulation_score      × 0.30
          consent_violation_score × 0.25
          financial_harm_score    × 0.25
          regulatory_risk_score   × 0.20
        """
        score = (
            self.manipulation_score * 0.30
            + self.consent_violation_score * 0.25
            + self.financial_harm_score * 0.25
            + self.regulatory_risk_score * 0.20
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
            "manipulation_score": self.manipulation_score,
            "consent_violation_score": self.consent_violation_score,
            "financial_harm_score": self.financial_harm_score,
            "regulatory_risk_score": self.regulatory_risk_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_darkpattern_index": self.estimated_darkpattern_index,
            "recommended_action": self.recommended_action,
            "last_updated": self.last_updated,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class DarkPatternsEngine:
    """
    Swarm Intelligence module for dark pattern detection and UX deception tracking.

    Monitors deceptive UX/UI practices (forced continuity, roach motels,
    disguised ads, hidden costs, confirmshaming, trick questions, privacy
    zuckering), computes composite risk scores, and surfaces regulatory actions
    for the Caelum Partners compliance intelligence platform.
    """

    VERSION = "1.0.0"
    DOMAIN = "darkpattern"
    DATA_SOURCES = [
        "DSA Compliance Reports",
        "CNIL/DPA Enforcement Database",
        "UX Audit Intelligence Feed",
        "GDPR Violation Registry",
        "Consumer Protection Agency Data",
    ]

    def __init__(self) -> None:
        self.entities: List[EntityRecord] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "DarkPatternsEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[EntityRecord]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: 3 critique, 2 élevé, 1 modéré, 2 faible.

        Composite formula verification (manipulation*0.30 + consent*0.25 + financial*0.25 + regulatory*0.20):
          DKP-001: 90*0.30 + 88*0.25 + 85*0.25 + 82*0.20
                 = 27.0 + 22.0 + 21.25 + 16.4 = 86.65  → critique ✓
          DKP-002: 85*0.30 + 80*0.25 + 88*0.25 + 78*0.20
                 = 25.5 + 20.0 + 22.0 + 15.6 = 83.1   → critique ✓
          DKP-003: 82*0.30 + 78*0.25 + 80*0.25 + 75*0.20
                 = 24.6 + 19.5 + 20.0 + 15.0 = 79.1   → critique ✓
          DKP-004: 55*0.30 + 52*0.25 + 58*0.25 + 50*0.20
                 = 16.5 + 13.0 + 14.5 + 10.0 = 54.0   → élevé ✓
          DKP-005: 50*0.30 + 58*0.25 + 45*0.25 + 55*0.20
                 = 15.0 + 14.5 + 11.25 + 11.0 = 51.75 → élevé ✓
          DKP-006: 42*0.30 + 38*0.25 + 40*0.25 + 35*0.20
                 = 12.6 + 9.5 + 10.0 + 7.0 = 39.1    → modéré ✓
          DKP-007: 8*0.30  + 10*0.25 + 6*0.25  + 12*0.20
                 = 2.4 + 2.5 + 1.5 + 2.4 = 8.8       → faible ✓
          DKP-008: 6*0.30  + 8*0.25  + 5*0.25  + 10*0.20
                 = 1.8 + 2.0 + 1.25 + 2.0 = 7.05     → faible ✓
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # Manipulation Consentement Forcé: consent_violation_score > 80
            {
                "entity_id": "DKP-001",
                "name": "DarkClick Media",
                "country": "USA",
                "sector": "Publicité Numérique",
                "manipulation_score": 90.0,
                "consent_violation_score": 88.0,
                "financial_harm_score": 85.0,
                "regulatory_risk_score": 82.0,
                "primary_pattern": "Manipulation Consentement Forcé",
                "key_signals": [
                    "Opt-out impossible conçu délibérément",
                    "Publicités déguisées en contenu éditorial",
                    "Données vendues 47 courtiers sans consentement",
                ],
                "last_updated": "2026-06-20",
            },
            # Piège Abonnement Caché: financial_harm_score > 75
            {
                "entity_id": "DKP-002",
                "name": "SubTrap Platform",
                "country": "Irlande",
                "sector": "SaaS & Abonnements",
                "manipulation_score": 85.0,
                "consent_violation_score": 80.0,
                "financial_harm_score": 88.0,
                "regulatory_risk_score": 78.0,
                "primary_pattern": "Piège Abonnement Caché",
                "key_signals": [
                    "Renouvellement auto sans alerte",
                    "Annulation 17 étapes requises",
                    "Frais cachés découverts post-souscription",
                ],
                "last_updated": "2026-06-20",
            },
            # Déceptivité Interface Systémique: manipulation_score > 65
            {
                "entity_id": "DKP-003",
                "name": "ConfirmShame App",
                "country": "Royaume-Uni",
                "sector": "Applications Mobile",
                "manipulation_score": 82.0,
                "consent_violation_score": 78.0,
                "financial_harm_score": 80.0,
                "regulatory_risk_score": 75.0,
                "primary_pattern": "Déceptivité Interface Systémique",
                "key_signals": [
                    "Bouton refus labellisé négativement",
                    "Interface de désabonnement introuvable",
                    "Pop-up consentement pré-coché systématique",
                ],
                "last_updated": "2026-06-20",
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # Violation DSA Répétée: regulatory_risk_score > 60
            {
                "entity_id": "DKP-004",
                "name": "HiddenFee Commerce",
                "country": "Allemagne",
                "sector": "E-commerce",
                "manipulation_score": 55.0,
                "consent_violation_score": 52.0,
                "financial_harm_score": 58.0,
                "regulatory_risk_score": 50.0,
                "primary_pattern": "Violation DSA Répétée",
                "key_signals": [
                    "Frais livraison ajoutés au checkout",
                    "Prix barré fictif systématique",
                    "Injonction DSA reçue mars 2026",
                ],
                "last_updated": "2026-06-20",
            },
            # Monétisation Données Occulte: consent_violation_score between 40-80
            {
                "entity_id": "DKP-005",
                "name": "DataHarvest Social",
                "country": "Luxembourg",
                "sector": "Réseaux Sociaux",
                "manipulation_score": 50.0,
                "consent_violation_score": 58.0,
                "financial_harm_score": 45.0,
                "regulatory_risk_score": 55.0,
                "primary_pattern": "Monétisation Données Occulte",
                "key_signals": [
                    "Paramètres vie privée enfouis",
                    "Consentement bundlé illégalement",
                    "Revente données santé non déclarée",
                ],
                "last_updated": "2026-06-20",
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # Monétisation Données Occulte: consent_violation_score between 40-80
            {
                "entity_id": "DKP-006",
                "name": "GrayUX Solutions",
                "country": "France",
                "sector": "Design UX/UI",
                "manipulation_score": 42.0,
                "consent_violation_score": 38.0,
                "financial_harm_score": 40.0,
                "regulatory_risk_score": 35.0,
                "primary_pattern": "Monétisation Données Occulte",
                "key_signals": [
                    "Patterns ambigus partiellement corrigés",
                    "CNIL en dialogue",
                    "Conformité RGPD en cours",
                ],
                "last_updated": "2026-06-20",
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # Ethically compliant — minor DSA signal
            {
                "entity_id": "DKP-007",
                "name": "EthicalUX Collective",
                "country": "Suède",
                "sector": "Design Éthique",
                "manipulation_score": 8.0,
                "consent_violation_score": 10.0,
                "financial_harm_score": 6.0,
                "regulatory_risk_score": 12.0,
                "primary_pattern": "Violation DSA Répétée",
                "key_signals": [
                    "Certifié conforme DSA",
                    "Interface transparence primée",
                    "Open source patterns éthiques",
                ],
                "last_updated": "2026-06-20",
            },
            # Excellent compliance, subscription clarity model
            {
                "entity_id": "DKP-008",
                "name": "TrustFirst Digital",
                "country": "Danemark",
                "sector": "Services Numériques",
                "manipulation_score": 6.0,
                "consent_violation_score": 8.0,
                "financial_harm_score": 5.0,
                "regulatory_risk_score": 10.0,
                "primary_pattern": "Piège Abonnement Caché",
                "key_signals": [
                    "Annulation en un clic",
                    "Alerte renouvellement J-30",
                    "Prix tout inclus garantis",
                ],
                "last_updated": "2026-06-20",
            },
        ]

        return [EntityRecord(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(
            sum(e.composite_score for e in self.entities) / n, 2
        )

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

        sorted_by_risk = sorted(
            self.entities, key=lambda e: e.composite_score, reverse=True
        )
        top_risk_entities = [e.name for e in sorted_by_risk[:3]]

        critical_alerts = risk_distribution["critique"]
        avg_darkpattern_index = round(avg_composite / 100 * 10, 2)

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
            "avg_estimated_darkpattern_index": avg_darkpattern_index,
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[EntityRecord]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def get_pattern_action(self, pattern_name: str) -> str:
        return _PATTERN_ACTIONS.get(pattern_name, "Audit UX complémentaire requis")

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_darkpattern(
    entity_id: str,
    name: str,
    country: str,
    sector: str,
    manipulation_score: float,
    consent_violation_score: float,
    financial_harm_score: float,
    regulatory_risk_score: float,
    primary_pattern: str = "",
    key_signals: List[str] | None = None,
    last_updated: str = "2026-06-20",
) -> Dict[str, Any]:
    """
    Analyse a single entity for dark pattern risk.

    Returns a dict with 15 keys matching EntityRecord.to_dict().

    Example:
        result = analyze_darkpattern(
            entity_id="DKP-999",
            name="Example Platform",
            country="France",
            sector="E-commerce",
            manipulation_score=72.0,
            consent_violation_score=68.0,
            financial_harm_score=60.0,
            regulatory_risk_score=55.0,
        )
    """
    if key_signals is None:
        key_signals = ["Signal non renseigné", "Audit en attente", "Données insuffisantes"]

    # Auto-detect primary_pattern if not provided
    if not primary_pattern:
        if consent_violation_score > 80:
            primary_pattern = "Manipulation Consentement Forcé"
        elif financial_harm_score > 75:
            primary_pattern = "Piège Abonnement Caché"
        elif manipulation_score > 65:
            primary_pattern = "Déceptivité Interface Systémique"
        elif regulatory_risk_score > 60:
            primary_pattern = "Violation DSA Répétée"
        else:
            primary_pattern = "Monétisation Données Occulte"

    record = EntityRecord(
        entity_id=entity_id,
        name=name,
        country=country,
        sector=sector,
        manipulation_score=manipulation_score,
        consent_violation_score=consent_violation_score,
        financial_harm_score=financial_harm_score,
        regulatory_risk_score=regulatory_risk_score,
        primary_pattern=primary_pattern,
        key_signals=key_signals,
        last_updated=last_updated,
    )
    return record.to_dict()
