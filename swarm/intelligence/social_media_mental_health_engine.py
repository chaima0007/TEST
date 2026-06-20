"""Caelum Partners — Social Media Mental Health Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.social_media_mental_health")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "algorithmic_radicalization",
        "severity_fr": "Radicalisation Algorithmique",
        "action_fr": "Audit algorithmique indépendant et refonte des systèmes de recommandation",
        "signal_fr": "Amplification algorithmique de contenus nocifs détectée",
    },
    {
        "name": "youth_mental_crisis",
        "severity_fr": "Crise Santé Mentale Jeunes",
        "action_fr": "Restrictions d'accès mineurs et protocoles de protection renforcés",
        "signal_fr": "Exposition massive des jeunes à des contenus préjudiciables",
    },
    {
        "name": "depression_anxiety_nexus",
        "severity_fr": "Nexus Dépression-Anxiété",
        "action_fr": "Partenariat clinique et intégration d'outils de bien-être numérique",
        "signal_fr": "Corrélation forte entre usage plateforme et troubles mentaux",
    },
    {
        "name": "platform_negligence",
        "severity_fr": "Négligence Platforme",
        "action_fr": "Cadre de responsabilité réglementaire et sanctions plateformes",
        "signal_fr": "Déficit critique de responsabilité plateforme",
    },
    {
        "name": "platform_responsible",
        "severity_fr": "Plateforme Responsable",
        "action_fr": "Maintien et amplification des bonnes pratiques bien-être numérique",
        "signal_fr": "Pratiques de protection de la santé mentale conformes",
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
    # Sub-score inputs (0–100)
    algorithmic_harm_amplification_score: float    # weight 0.30
    youth_vulnerability_exposure_score: float      # weight 0.25
    mental_disorder_correlation_score: float       # weight 0.25
    platform_accountability_deficit_score: float   # weight 0.20
    # Computed fields
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          algorithmic_harm_amplification_score × 0.30
          + youth_vulnerability_exposure_score  × 0.25
          + mental_disorder_correlation_score   × 0.25
          + platform_accountability_deficit_score × 0.20
        """
        score = (
            self.algorithmic_harm_amplification_score * 0.30
            + self.youth_vulnerability_exposure_score * 0.25
            + self.mental_disorder_correlation_score * 0.25
            + self.platform_accountability_deficit_score * 0.20
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

    def _primary_pattern(self) -> str:
        if self.algorithmic_harm_amplification_score >= 70:
            return "algorithmic_radicalization"
        if self.youth_vulnerability_exposure_score >= 70:
            return "youth_mental_crisis"
        if self.mental_disorder_correlation_score >= 70:
            return "depression_anxiety_nexus"
        if self.platform_accountability_deficit_score >= 70:
            return "platform_negligence"
        return "platform_responsible"

    def _key_signals(self) -> List[str]:
        """Return 3 domain-specific signals for this entity."""
        signals_map: Dict[str, List[str]] = {
            "MNH-001": [
                "Algorithme de recommandation TikTok expose 85% des mineurs à des contenus d'anxiété en moins de 10 min",
                "Durée moyenne de session de 95 min/jour chez les adolescents corrélée à une hausse de 47% de dépression",
                "Fonctionnalité d'affichage du compteur de vues amplificatrice de comportements compulsifs chez les jeunes",
            ],
            "MNH-002": [
                "Filtre beauté Instagram renforce les troubles dysmorphiques corporels chez 62% des utilisatrices 13-17 ans",
                "Algorithme Explore amplifie les contenus pro-anorexie malgré les politiques de contenu déclarées",
                "Absence de limite de temps d'écran native entraîne une addiction documentée par 38 études cliniques",
            ],
            "MNH-003": [
                "Suppression de 80% des équipes de modération corrélée à une explosion des contenus haineux et suicidaires",
                "Algorithme de trending amplifie le contenu polarisant multipliant l'exposition à la détresse émotionnelle",
                "Déficit critique de mécanismes de signalement pour contenus à risque suicidaire depuis la restructuration",
            ],
            "MNH-004": [
                "Intégration WeChat aux plateformes de jeu amplifie les comportements addictifs chez les utilisateurs isolés",
                "Corrélation de 0.71 entre usage intensif WeChat et symptômes dépressifs dans les études longitudinales",
                "Manque de transparence algorithmique empêche l'audit indépendant des impacts santé mentale",
            ],
            "MNH-005": [
                "Snaps éphémères génèrent une anxiété de FOMO (Fear Of Missing Out) chez 54% des utilisateurs adolescents",
                "Streak feature entraîne des comportements compulsifs documentés chez les utilisateurs de 13 à 19 ans",
                "Exposition à des contenus de bullying via Snap Maps supérieure à la moyenne des plateformes équivalentes",
            ],
            "MNH-006": [
                "LinkedIn génère du stress de comparaison professionnelle modéré mais gérable selon les études de 2025",
                "Mécanismes de modération actifs limitent l'exposition aux contenus de détresse professionnelle",
                "Politiques de bien-être numérique conformes aux directives DSA avec audits trimestriels documentés",
            ],
            "MNH-007": [
                "Discord Nordic met en oeuvre des outils de bien-être mental intégrés et des ressources d'aide en crise",
                "Communautés de soutien modérées activement réduisent l'isolement social et favorisent la résilience",
                "Faible corrélation entre usage Discord et symptômes dépressifs grâce aux protocoles de protection",
            ],
            "MNH-008": [
                "Pinterest Benelux présente des impacts positifs sur créativité et estime de soi dans 73% des études",
                "Algorithme orienté inspiration plutôt qu'engagement compulsif réduit les risques de dépendance",
                "Initiatives bien-être numérique proactives incluant des limites de temps et filtres de contenu robustes",
            ],
        }
        return signals_map.get(self.entity_id, [
            "Signal santé mentale non documenté pour cette entité",
            "Données insuffisantes pour établir une corrélation clinique",
            "Audit indépendant recommandé pour évaluation approfondie",
        ])

    def _confidence_level(self) -> float:
        confidence_map: Dict[str, float] = {
            "MNH-001": 0.91,
            "MNH-002": 0.87,
            "MNH-003": 0.83,
            "MNH-004": 0.79,
            "MNH-005": 0.76,
            "MNH-006": 0.72,
            "MNH-007": 0.68,
            "MNH-008": 0.65,
        }
        return confidence_map.get(self.entity_id, 0.70)

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        pattern_name = self._primary_pattern()
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "algorithmic_harm_amplification_score": self.algorithmic_harm_amplification_score,
            "youth_vulnerability_exposure_score": self.youth_vulnerability_exposure_score,
            "mental_disorder_correlation_score": self.mental_disorder_correlation_score,
            "platform_accountability_deficit_score": self.platform_accountability_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": pattern_name,
            "key_signals": self._key_signals(),
            "estimated_mentalhealth_index": round(self.composite_score / 100 * 10, 2),
            "last_updated": "2026-06-20",
            "confidence_level": self._confidence_level(),
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class SocialMediaMentalHealthEngine:
    """
    Swarm Intelligence module for social media mental health impact tracking.

    Computes composite risk scores across 4 dimensions, detects mental health
    harm patterns, and surfaces actionable insights for Caelum Partners.
    """

    def __init__(self) -> None:
        self.entities: List[EntityRecord] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "SocialMediaMentalHealthEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[EntityRecord]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Composite formula verification:
          MNH-001: 65*0.30 + 88*0.25 + 74*0.25 + 62*0.20
                 = 19.50 + 22.00 + 18.50 + 12.40 = 72.40 → critique ✓ (youth_mental_crisis: aha=65<70, yve=88>=70)
          MNH-002: 78*0.30 + 65*0.25 + 66*0.25 + 72*0.20
                 = 23.40 + 16.25 + 16.50 + 14.40 = 70.55 → critique ✓ (algorithmic_radicalization: aha=78>=70)
          MNH-003: 60*0.30 + 58*0.25 + 62*0.25 + 76*0.20
                 = 18.00 + 14.50 + 15.50 + 15.20 = 63.20 → critique ✓ (platform_negligence: pad=76>=70, aha=60<70, yve=58<70, mdc=62<70)
          MNH-004: 48*0.30 + 55*0.25 + 72*0.25 + 42*0.20
                 = 14.40 + 13.75 + 18.00 + 8.40  = 54.55 → élevé ✓  (depression_anxiety_nexus: mdc=72>=70, aha=48<70, yve=55<70)
          MNH-005: 42*0.30 + 58*0.25 + 44*0.25 + 38*0.20
                 = 12.60 + 14.50 + 11.00 + 7.60  = 45.70 → élevé ✓  (platform_responsible: all <70)
          MNH-006: 22*0.30 + 25*0.25 + 28*0.25 + 30*0.20
                 = 6.60  + 6.25  + 7.00  + 6.00  = 25.85 → modéré ✓ (platform_responsible)
          MNH-007: 10*0.30 + 12*0.25 + 15*0.25 + 8*0.20
                 = 3.00  + 3.00  + 3.75  + 1.60  = 11.35 → faible ✓ (platform_responsible)
          MNH-008: 5*0.30  + 8*0.25  + 10*0.25 + 6*0.20
                 = 1.50  + 2.00  + 2.50  + 1.20  = 7.20  → faible ✓ (platform_responsible)
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            # MNH-001: TikTok US — youth_mental_crisis (aha=65<70, yve=88>=70)
            {
                "entity_id": "MNH-001",
                "name": "TikTok US Operations",
                "country": "USA",
                "sector": "Social Media",
                "algorithmic_harm_amplification_score": 65.0,
                "youth_vulnerability_exposure_score": 88.0,
                "mental_disorder_correlation_score": 74.0,
                "platform_accountability_deficit_score": 62.0,
            },
            # MNH-002: Instagram Meta — algorithmic_radicalization (aha=78 >= 70)
            {
                "entity_id": "MNH-002",
                "name": "Instagram Meta Platform",
                "country": "USA",
                "sector": "Social Media",
                "algorithmic_harm_amplification_score": 78.0,
                "youth_vulnerability_exposure_score": 65.0,
                "mental_disorder_correlation_score": 66.0,
                "platform_accountability_deficit_score": 72.0,
            },
            # MNH-003: Twitter/X — platform_negligence (pad=76 >= 70, aha=60<70, yve=58<70, mdc=62<70)
            {
                "entity_id": "MNH-003",
                "name": "Twitter/X Platform",
                "country": "USA",
                "sector": "Social Media",
                "algorithmic_harm_amplification_score": 60.0,
                "youth_vulnerability_exposure_score": 58.0,
                "mental_disorder_correlation_score": 62.0,
                "platform_accountability_deficit_score": 76.0,
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            # MNH-004: WeChat — depression_anxiety_nexus (mdc=72 >= 70, aha=48<70, yve=55<70)
            {
                "entity_id": "MNH-004",
                "name": "WeChat International",
                "country": "China",
                "sector": "Social Media",
                "algorithmic_harm_amplification_score": 48.0,
                "youth_vulnerability_exposure_score": 55.0,
                "mental_disorder_correlation_score": 72.0,
                "platform_accountability_deficit_score": 42.0,
            },
            # MNH-005: Snapchat EU — platform_responsible (all <70)
            {
                "entity_id": "MNH-005",
                "name": "Snapchat EU Operations",
                "country": "UK",
                "sector": "Social Media",
                "algorithmic_harm_amplification_score": 42.0,
                "youth_vulnerability_exposure_score": 58.0,
                "mental_disorder_correlation_score": 44.0,
                "platform_accountability_deficit_score": 38.0,
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            # MNH-006: LinkedIn DACH — platform_responsible
            {
                "entity_id": "MNH-006",
                "name": "LinkedIn DACH",
                "country": "Germany",
                "sector": "Professional Network",
                "algorithmic_harm_amplification_score": 22.0,
                "youth_vulnerability_exposure_score": 25.0,
                "mental_disorder_correlation_score": 28.0,
                "platform_accountability_deficit_score": 30.0,
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            # MNH-007: Discord Nordic — platform_responsible
            {
                "entity_id": "MNH-007",
                "name": "Discord Nordic",
                "country": "Finland",
                "sector": "Gaming/Social",
                "algorithmic_harm_amplification_score": 10.0,
                "youth_vulnerability_exposure_score": 12.0,
                "mental_disorder_correlation_score": 15.0,
                "platform_accountability_deficit_score": 8.0,
            },
            # MNH-008: Pinterest Benelux — platform_responsible
            {
                "entity_id": "MNH-008",
                "name": "Pinterest Benelux",
                "country": "Netherlands",
                "sector": "Creative Platform",
                "algorithmic_harm_amplification_score": 5.0,
                "youth_vulnerability_exposure_score": 8.0,
                "mental_disorder_correlation_score": 10.0,
                "platform_accountability_deficit_score": 6.0,
            },
        ]

        return [EntityRecord(**d) for d in raw]  # type: ignore[arg-type]

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

        pattern_distribution: Dict[str, int] = {p["name"]: 0 for p in PATTERNS}
        for e in self.entities:
            pat = e._primary_pattern()
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1

        top_three = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)[:3]
        critical_alerts = [e.name for e in self.entities if e.risk_level == "critique"]
        avg_confidence = round(
            sum(e._confidence_level() for e in self.entities) / n, 2
        )

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": [e.name for e in top_three],
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20T00:00:00Z",
            "engine_version": "1.0.0",
            "domain": "mentalhealth",
            "confidence_score": avg_confidence,
            "data_sources": [
                "WHO Mental Health Reports",
                "American Psychological Association",
                "EU Digital Services Act Reports",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_mentalhealth_index": round(avg_composite / 100 * 10, 2),
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[EntityRecord]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module-level function ─────────────────────────────────────────────────────

def analyze_mentalhealth() -> dict:
    return SocialMediaMentalHealthEngine().summary()
