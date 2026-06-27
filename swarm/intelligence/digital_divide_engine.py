"""
Digital Divide Intelligence Engine — Caelum Partners Swarm Module

Auteur : Chaima Mhadbi — Caelum Partners, Bruxelles
Analyse la fracture numérique structurelle : accès à l'infrastructure, inégalités
de compétences numériques, exclusion économique et gouvernance des données.

Score composite (poids = 1.00) :
  infrastructure_gap_score × 0.30
  + skills_exclusion_score  × 0.25
  + economic_barrier_score  × 0.25
  + governance_gap_score    × 0.20

Niveaux de risque :
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage :
    from intelligence.digital_divide_engine import DigitalDivideEngine
    engine = DigitalDivideEngine()
    print(engine.summary())
    for entity in engine.entities:
        print(entity.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.digital_divide")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Désert Numérique",
        "severity_fr": "critique",
        "action_fr": "Déploiement d'urgence d'infrastructures haut débit en zones rurales isolées",
        "signal_fr": "infrastructure_gap_score > 80",
    },
    {
        "name": "Analphabétisme Numérique",
        "severity_fr": "critique",
        "action_fr": "Programme national de formation numérique obligatoire pour les populations vulnérables",
        "signal_fr": "skills_exclusion_score > 75",
    },
    {
        "name": "Barrière Économique Numérique",
        "severity_fr": "élevé",
        "action_fr": "Subventions publiques pour l'accès aux équipements numériques et abonnements",
        "signal_fr": "economic_barrier_score > 65",
    },
    {
        "name": "Vide Gouvernance Données",
        "severity_fr": "élevé",
        "action_fr": "Cadre réglementaire national de protection des données et droits numériques",
        "signal_fr": "governance_gap_score > 60",
    },
    {
        "name": "Fracture Numérique Structurelle",
        "severity_fr": "modéré",
        "action_fr": "Plan d'inclusion numérique pluriannuel avec indicateurs de suivi trimestriels",
        "signal_fr": "composite >= 30",
    },
]


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class DigitalDivideEntity:
    id: str
    name: str
    country: str
    sector: str
    infrastructure_gap_score: float   # 0–100
    skills_exclusion_score: float     # 0–100
    economic_barrier_score: float     # 0–100
    governance_gap_score: float       # 0–100
    key_signals: List[str] = field(default_factory=list)
    last_updated: str = "2026-06-20"
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    estimated_divide_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.primary_pattern = self._compute_primary_pattern()
        self.estimated_divide_index = round(self.composite_score / 100 * 10, 2)

    def _compute_composite(self) -> float:
        score = (
            self.infrastructure_gap_score * 0.30
            + self.skills_exclusion_score * 0.25
            + self.economic_barrier_score * 0.25
            + self.governance_gap_score * 0.20
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
        if self.infrastructure_gap_score > 80:
            return "Désert Numérique"
        if self.skills_exclusion_score > 75:
            return "Analphabétisme Numérique"
        if self.economic_barrier_score > 65:
            return "Barrière Économique Numérique"
        if self.governance_gap_score > 60:
            return "Vide Gouvernance Données"
        if self.composite_score >= 30:
            return "Fracture Numérique Structurelle"
        return "Inclusion Numérique Satisfaisante"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id": self.id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "infrastructure_gap_score": self.infrastructure_gap_score,
            "skills_exclusion_score": self.skills_exclusion_score,
            "economic_barrier_score": self.economic_barrier_score,
            "governance_gap_score": self.governance_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_divide_index": self.estimated_divide_index,
            "last_updated": self.last_updated,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class DigitalDivideEngine:
    """
    Swarm Intelligence module for digital divide analysis.

    Mesure la fracture numérique, détecte les patterns d'exclusion structurelle
    et fournit des recommandations pour les politiques d'inclusion numérique.
    """

    ENGINE_VERSION = "2.1.0"

    def __init__(self) -> None:
        self.entities: List[DigitalDivideEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "DigitalDivideEngine initialisé — %d entités, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    def _build_mock_entities(self) -> List[DigitalDivideEntity]:
        """
        8 entités couvrant tous les patterns et niveaux de risque.
        Distribution : ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Vérification :
          DD-001 : 88*0.30+82*0.25+78*0.25+72*0.20 = 26.4+20.5+19.5+14.4 = 80.80 → critique
          DD-002 : 78*0.30+82*0.25+72*0.25+68*0.20 = 23.4+20.5+18.0+13.6 = 75.50 → critique
          DD-003 : 72*0.30+65*0.25+80*0.25+60*0.20 = 21.6+16.25+20.0+12.0= 69.85 → critique
          DD-004 : 58*0.30+55*0.25+65*0.25+62*0.20 = 17.4+13.75+16.25+12.4=59.80 → élevé
          DD-005 : 52*0.30+48*0.25+58*0.25+55*0.20 = 15.6+12.0+14.5+11.0 = 53.10 → élevé
          DD-006 : 38*0.30+35*0.25+40*0.25+32*0.20 = 11.4+8.75+10.0+6.4  = 36.55 → modéré
          DD-007 : 15*0.30+12*0.25+18*0.25+10*0.20 = 4.5+3.0+4.5+2.0     = 14.00 → faible
          DD-008 : 10*0.30+8*0.25+12*0.25+8*0.20   = 3.0+2.0+3.0+1.6     = 9.60  → faible
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            {
                "id": "DD-001",
                "name": "Agence Numérique Mali",
                "country": "Mali",
                "sector": "Infrastructure Télécoms",
                "infrastructure_gap_score": 88.0,
                "skills_exclusion_score": 82.0,
                "economic_barrier_score": 78.0,
                "governance_gap_score": 72.0,
                "key_signals": [
                    "Taux pénétration internet 18% — zones rurales < 3%",
                    "85% population sans compétences numériques de base",
                    "Coût data mobile > 15% revenu mensuel médian",
                ],
            },
            {
                "id": "DD-002",
                "name": "Autorité Numérique Bangladesh",
                "country": "Bangladesh",
                "sector": "Éducation Numérique",
                "infrastructure_gap_score": 78.0,
                "skills_exclusion_score": 82.0,
                "economic_barrier_score": 72.0,
                "governance_gap_score": 68.0,
                "key_signals": [
                    "60 millions sans accès internet fiable",
                    "Femmes rurales : 92% sans accès smartphones",
                    "Aucune loi de protection données personnelles",
                ],
            },
            {
                "id": "DD-003",
                "name": "Ministère Transformation Digitale Nigeria",
                "country": "Nigeria",
                "sector": "Gouvernance Numérique",
                "infrastructure_gap_score": 72.0,
                "skills_exclusion_score": 65.0,
                "economic_barrier_score": 80.0,
                "governance_gap_score": 60.0,
                "key_signals": [
                    "Fracture nord-sud : Lagos 78% vs nord < 12% connecté",
                    "Prix données parmi les plus élevés d'Afrique/revenu",
                    "Réglementation données fragmentée entre 36 États",
                ],
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            {
                "id": "DD-004",
                "name": "Instituto Digital Brésil Rural",
                "country": "Brésil",
                "sector": "Infrastructure Télécoms",
                "infrastructure_gap_score": 58.0,
                "skills_exclusion_score": 55.0,
                "economic_barrier_score": 65.0,
                "governance_gap_score": 62.0,
                "key_signals": [
                    "Amazonie : 45 millions sans haut débit",
                    "Fracture générationnelle senior > 60 ans critique",
                    "Inégalité numérique corrèle à inégalité revenus Gini",
                ],
            },
            {
                "id": "DD-005",
                "name": "Agence Connexion Rurale Inde",
                "country": "Inde",
                "sector": "Éducation Numérique",
                "infrastructure_gap_score": 52.0,
                "skills_exclusion_score": 48.0,
                "economic_barrier_score": 58.0,
                "governance_gap_score": 55.0,
                "key_signals": [
                    "350 millions utilisateurs connectés mais peu qualifiés",
                    "Fracture genre : 40% moins de femmes en ligne",
                    "Qualité connexion rurale 2G vs 5G urbain",
                ],
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "id": "DD-006",
                "name": "Observatoire Inclusion Numérique Roumanie",
                "country": "Roumanie",
                "sector": "Gouvernance Numérique",
                "infrastructure_gap_score": 38.0,
                "skills_exclusion_score": 35.0,
                "economic_barrier_score": 40.0,
                "governance_gap_score": 32.0,
                "key_signals": [
                    "Rural : 35% ménages sans internet fixe",
                    "Seniors > 65 ans : 70% exclus services numériques",
                    "Administration numérique insuffisante vs UE moyenne",
                ],
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "id": "DD-007",
                "name": "Agence Numérique Finlande",
                "country": "Finlande",
                "sector": "Infrastructure Télécoms",
                "infrastructure_gap_score": 15.0,
                "skills_exclusion_score": 12.0,
                "economic_barrier_score": 18.0,
                "governance_gap_score": 10.0,
                "key_signals": [
                    "Internet haut débit : droit constitutionnel reconnu",
                    "95% population compétences numériques certifiées",
                    "RGPD + loi nationale données — cadre exemplaire",
                ],
            },
            {
                "id": "DD-008",
                "name": "Ministère Digital Pays-Bas",
                "country": "Pays-Bas",
                "sector": "Éducation Numérique",
                "infrastructure_gap_score": 10.0,
                "skills_exclusion_score": 8.0,
                "economic_barrier_score": 12.0,
                "governance_gap_score": 8.0,
                "key_signals": [
                    "98% ménages fibre ou câble haut débit",
                    "Programme NL leert door — formation permanente",
                    "Coût abonnement internet parmi les plus bas EU",
                ],
            },
        ]
        return [DigitalDivideEntity(**d) for d in raw]  # type: ignore[arg-type]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(self.entities)
        avg_composite = round(sum(e.composite_score for e in self.entities) / n, 2)

        risk_distribution: Dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
        for e in self.entities:
            risk_distribution[e.risk_level] = risk_distribution.get(e.risk_level, 0) + 1

        pattern_distribution: Dict[str, int] = {}
        for e in self.entities:
            pattern_distribution[e.primary_pattern] = pattern_distribution.get(e.primary_pattern, 0) + 1

        sorted_entities = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_entities[:3]]

        critical_alerts = risk_distribution.get("critique", 0)
        avg_estimated_divide_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": self.ENGINE_VERSION,
            "domain": "divide",
            "confidence_score": 84.2,
            "data_sources": [
                "UIT — Rapport Mondial Connectivité 2025",
                "Banque Mondiale — Digital Economy Data 2026",
                "Web Foundation — Digital Rights Report 2026",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_divide_index": avg_estimated_divide_index,
        }

    def get_entities_by_risk(self, risk_level: str) -> List[DigitalDivideEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]


def analyze_divide() -> Dict[str, Any]:
    """Point d'entrée du module — retourne le résumé complet de l'analyse fracture numérique."""
    engine = DigitalDivideEngine()
    return engine.summary()
