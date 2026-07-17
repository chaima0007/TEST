"""Caelum Partners — Refugee Integration Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.refugee_integration")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "integration_failure",
        "severity_fr": "Échec d'Intégration Systémique",
        "action_fr": "Programme d'intégration d'urgence multidimensionnel",
        "signal_fr": "Barrières d'intégration sociales critiques détectées",
    },
    {
        "name": "economic_exclusion",
        "severity_fr": "Exclusion Économique Sévère",
        "action_fr": "Insertion professionnelle prioritaire et formation linguistique",
        "signal_fr": "Exclusion économique systématique identifiée",
    },
    {
        "name": "legal_precarity",
        "severity_fr": "Précarité Juridique Critique",
        "action_fr": "Assistance juridique d'urgence et accompagnement administratif",
        "signal_fr": "Vulnérabilité juridique et administrative élevée",
    },
    {
        "name": "mental_health_crisis",
        "severity_fr": "Crise de Santé Mentale",
        "action_fr": "Soutien psychologique immédiat et réseaux communautaires",
        "signal_fr": "Détresse psychologique et traumatisme sévère",
    },
    {
        "name": "successful_integration",
        "severity_fr": "Intégration Réussie",
        "action_fr": "Renforcement des programmes de réussite et partage des meilleures pratiques",
        "signal_fr": "Trajectoire d'intégration positive",
    },
]

_PATTERN_MAP: Dict[str, Dict[str, str]] = {p["name"]: p for p in PATTERNS}


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class EntityRecord:
    entity_id: str
    name: str
    country: str
    sector: str
    social_integration_barrier_score: float   # 0–100, weight 0.30
    economic_exclusion_score: float            # 0–100, weight 0.25
    legal_vulnerability_score: float           # 0–100, weight 0.25
    mental_health_crisis_score: float          # 0–100, weight 0.20
    key_signals: List[str]
    confidence_level: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          social_integration_barrier_score × 0.30
          + economic_exclusion_score × 0.25
          + legal_vulnerability_score × 0.25
          + mental_health_crisis_score × 0.20
        """
        return round(
            self.social_integration_barrier_score * 0.30
            + self.economic_exclusion_score * 0.25
            + self.legal_vulnerability_score * 0.25
            + self.mental_health_crisis_score * 0.20,
            2,
        )

    def _compute_risk_level(self) -> str:
        if self.composite_score >= 60:
            return "critique"
        if self.composite_score >= 40:
            return "élevé"
        if self.composite_score >= 20:
            return "modéré"
        return "faible"

    def _compute_primary_pattern(self) -> str:
        if self.social_integration_barrier_score >= 70:
            return "integration_failure"
        if self.economic_exclusion_score >= 70:
            return "economic_exclusion"
        if self.legal_vulnerability_score >= 70:
            return "legal_precarity"
        if self.mental_health_crisis_score >= 70:
            return "mental_health_crisis"
        return "successful_integration"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        primary_pattern = self._compute_primary_pattern()
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "social_integration_barrier_score": self.social_integration_barrier_score,
            "economic_exclusion_score": self.economic_exclusion_score,
            "legal_vulnerability_score": self.legal_vulnerability_score,
            "mental_health_crisis_score": self.mental_health_crisis_score,
            "risk_level": self.risk_level,
            "primary_pattern": primary_pattern,
            "key_signals": self.key_signals,
            "estimated_refugee_index": round(self.composite_score / 100 * 10, 2),
            "last_updated": "2026-06-20",
            "confidence_level": self.confidence_level,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class RefugeeIntegrationEngine:
    """
    Swarm Intelligence module for refugee integration tracking.

    Computes composite vulnerability scores, detects integration patterns,
    and surfaces actionable insights for the Caelum Partners humanitarian platform.
    """

    def __init__(self) -> None:
        self.entities: List[EntityRecord] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "RefugeeIntegrationEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[EntityRecord]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Composite formula verification:
          REF-001: 82*0.30 + 65*0.25 + 60*0.25 + 68*0.20
                 = 24.60 + 16.25 + 15.00 + 13.60 = 69.45  → critique ✓ (integration_failure, sib>=70)
          REF-002: 65*0.30 + 60*0.25 + 78*0.25 + 62*0.20
                 = 19.50 + 15.00 + 19.50 + 12.40 = 66.40  → critique ✓ (legal_precarity, lv>=70)
          REF-003: 60*0.30 + 55*0.25 + 58*0.25 + 75*0.20
                 = 18.00 + 13.75 + 14.50 + 15.00 = 61.25  → critique ✓ (mental_health_crisis, mh>=70)
          REF-004: 55*0.30 + 72*0.25 + 45*0.25 + 30*0.20
                 = 16.50 + 18.00 + 11.25 +  6.00 = 51.75  → élevé ✓  (economic_exclusion, ee>=70)
          REF-005: 78*0.30 + 42*0.25 + 38*0.25 + 25*0.20
                 = 23.40 + 10.50 +  9.50 +  5.00 = 48.40  → élevé ✓  (integration_failure, sib>=70)
          REF-006: 35*0.30 + 30*0.25 + 28*0.25 + 22*0.20
                 = 10.50 +  7.50 +  7.00 +  4.40 = 29.40  → modéré ✓ (successful_integration)
          REF-007: 15*0.30 + 12*0.25 + 18*0.25 + 14*0.20
                 =  4.50 +  3.00 +  4.50 +  2.80 = 14.80  → faible ✓  (successful_integration)
          REF-008: 10*0.30 +  8*0.25 + 12*0.25 + 10*0.20
                 =  3.00 +  2.00 +  3.00 +  2.00 = 10.00  → faible ✓  (successful_integration)
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # integration_failure (sib >= 70)
            {
                "entity_id": "REF-001",
                "name": "Programme d'Accueil Berlin",
                "country": "Syria",
                "sector": "Germany",
                "social_integration_barrier_score": 82.0,
                "economic_exclusion_score": 65.0,
                "legal_vulnerability_score": 60.0,
                "mental_health_crisis_score": 68.0,
                "key_signals": [
                    "Isolement linguistique et culturel sévère détecté",
                    "Accès limité aux services d'intégration communautaire",
                    "Discrimination systémique sur le marché du logement",
                ],
                "confidence_level": 0.83,
            },
            # legal_precarity (lv >= 70)
            {
                "entity_id": "REF-002",
                "name": "Centre d'Intégration Paris",
                "country": "Afghanistan",
                "sector": "France",
                "social_integration_barrier_score": 65.0,
                "economic_exclusion_score": 60.0,
                "legal_vulnerability_score": 78.0,
                "mental_health_crisis_score": 62.0,
                "key_signals": [
                    "Statut juridique précaire et procédures d'asile bloquées",
                    "Risque élevé d'expulsion et absence de protection temporaire",
                    "Accès restreint aux droits sociaux fondamentaux",
                ],
                "confidence_level": 0.79,
            },
            # mental_health_crisis (mh >= 70)
            {
                "entity_id": "REF-003",
                "name": "Foyer d'Accueil Bruxelles",
                "country": "Sudan",
                "sector": "Belgium",
                "social_integration_barrier_score": 60.0,
                "economic_exclusion_score": 55.0,
                "legal_vulnerability_score": 58.0,
                "mental_health_crisis_score": 75.0,
                "key_signals": [
                    "Traumatismes post-conflictuels non traités et détresse sévère",
                    "Absence de soutien psychologique spécialisé disponible",
                    "Rupture des liens familiaux et isolement social profond",
                ],
                "confidence_level": 0.85,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # economic_exclusion (ee >= 70)
            {
                "entity_id": "REF-004",
                "name": "Centre Varsovie",
                "country": "Ukraine",
                "sector": "Poland",
                "social_integration_barrier_score": 55.0,
                "economic_exclusion_score": 72.0,
                "legal_vulnerability_score": 45.0,
                "mental_health_crisis_score": 30.0,
                "key_signals": [
                    "Exclusion du marché du travail malgré qualifications reconnues",
                    "Barrières linguistiques bloquant l'insertion professionnelle",
                    "Dépendance aux aides sociales faute d'accès à l'emploi",
                ],
                "confidence_level": 0.81,
            },
            # integration_failure (sib >= 70)
            {
                "entity_id": "REF-005",
                "name": "Programme Rome",
                "country": "Ethiopia",
                "sector": "Italy",
                "social_integration_barrier_score": 78.0,
                "economic_exclusion_score": 42.0,
                "legal_vulnerability_score": 38.0,
                "mental_health_crisis_score": 25.0,
                "key_signals": [
                    "Fragmentation communautaire et absence de réseaux de soutien",
                    "Difficultés majeures d'accès aux services locaux d'intégration",
                    "Rejet social et marginalisation dans les quartiers d'accueil",
                ],
                "confidence_level": 0.77,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # successful_integration (no sub-score >= 70)
            {
                "entity_id": "REF-006",
                "name": "Accueil Madrid",
                "country": "Venezuela",
                "sector": "Spain",
                "social_integration_barrier_score": 35.0,
                "economic_exclusion_score": 30.0,
                "legal_vulnerability_score": 28.0,
                "mental_health_crisis_score": 22.0,
                "key_signals": [
                    "Intégration partielle avec quelques obstacles résiduels",
                    "Accès aux services de base en cours de consolidation",
                    "Liens communautaires en développement progressif",
                ],
                "confidence_level": 0.88,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # successful_integration
            {
                "entity_id": "REF-007",
                "name": "Centre Amsterdam",
                "country": "Colombia",
                "sector": "Netherlands",
                "social_integration_barrier_score": 15.0,
                "economic_exclusion_score": 12.0,
                "legal_vulnerability_score": 18.0,
                "mental_health_crisis_score": 14.0,
                "key_signals": [
                    "Intégration socio-économique réussie et autonomie établie",
                    "Statut légal sécurisé et accès complet aux droits sociaux",
                    "Réseau communautaire solide et participation civique active",
                ],
                "confidence_level": 0.91,
            },
            # successful_integration
            {
                "entity_id": "REF-008",
                "name": "Programme Genève",
                "country": "Morocco",
                "sector": "Switzerland",
                "social_integration_barrier_score": 10.0,
                "economic_exclusion_score": 8.0,
                "legal_vulnerability_score": 12.0,
                "mental_health_crisis_score": 10.0,
                "key_signals": [
                    "Modèle d'intégration exemplaire à fort potentiel de réplication",
                    "Insertion professionnelle complète avec progression de carrière",
                    "Bien-être psychologique et cohésion sociale remarquables",
                ],
                "confidence_level": 0.93,
            },
        ]

        return [EntityRecord(**d) for d in raw]  # type: ignore[arg-type]

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)
        avg_confidence = round(sum(e.confidence_level for e in self.entities) / n, 2)

        risk_distribution = {
            "critique": sum(1 for e in self.entities if e.risk_level == "critique"),
            "élevé": sum(1 for e in self.entities if e.risk_level == "élevé"),
            "modéré": sum(1 for e in self.entities if e.risk_level == "modéré"),
            "faible": sum(1 for e in self.entities if e.risk_level == "faible"),
        }

        pattern_distribution: Dict[str, int] = {p["name"]: 0 for p in PATTERNS}
        for e in self.entities:
            pattern_distribution[e.to_dict()["primary_pattern"]] += 1

        top_3 = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:3]
        top_risk_entities = [e.name for e in top_3]
        critical_alerts = [e.name for e in self.entities if e.risk_level == "critique"]

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20T00:00:00Z",
            "engine_version": "1.0.0",
            "domain": "refugee",
            "confidence_score": avg_confidence,
            "data_sources": [
                "UNHCR Integration Reports",
                "EU Asylum Statistics",
                "IOM Migration Data",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_refugee_index": round(avg_composite / 100 * 10, 2),
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[EntityRecord]:
        return [e for e in self.entities if e.risk_level == risk_level]


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_refugee() -> dict:
    return RefugeeIntegrationEngine().summary()
