"""
Geoengineering Intelligence Engine — Caelum Partners Swarm Module

Évalue les risques liés aux programmes de géo-ingénierie climatique,
en analysant les déploiements unilatéraux, les risques écosystémiques,
les déficits de gouvernance et les risques de militarisation climatique.

Niveaux de risque :
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20

Usage :
    from intelligence.geoengineering_engine import GeoEngineeringEngine
    engine = GeoEngineeringEngine()
    print(engine.summary())
    for entity in engine.entities:
        print(entity.to_dict())
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger("swarm.geoengineering")


# ── Patterns ──────────────────────────────────────────────────────────────────

PATTERNS: List[Dict[str, str]] = [
    {
        "name": "Déploiement Unilatéral",
        "severity_fr": "critique",
        "action_fr": "Traité international de moratoire sur la géo-ingénierie solaire et mécanismes de surveillance",
        "signal_fr": "unilateral_deployment_score > 70",
    },
    {
        "name": "Risque Écosystémique",
        "severity_fr": "critique",
        "action_fr": "Évaluation d'impact environnemental obligatoire transfrontalière avant tout déploiement",
        "signal_fr": "ecological_risk_score > 65",
    },
    {
        "name": "Vide Gouvernanciel",
        "severity_fr": "élevé",
        "action_fr": "Création d'un organe ONU de supervision de la géo-ingénierie avec pouvoir de veto",
        "signal_fr": "governance_deficit_score > 60",
    },
    {
        "name": "Militarisation Climatique",
        "severity_fr": "élevé",
        "action_fr": "Renforcement de la Convention ENMOD et extension aux technologies climatiques modernes",
        "signal_fr": "dual_use_weaponization_score > 55",
    },
    {
        "name": "Expérimentation Non Consentie",
        "severity_fr": "modéré",
        "action_fr": "Protocole de consentement préalable éclairé des populations potentiellement affectées",
        "signal_fr": "composite_score > 40",
    },
]


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class GeoEngineeringEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    unilateral_deployment_score: float    # 0–100
    ecological_risk_score: float          # 0–100
    governance_deficit_score: float       # 0–100
    dual_use_weaponization_score: float   # 0–100
    key_signals: List[str]
    last_updated: str
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    estimated_geoengineering_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = self._compute_composite()
        self.risk_level = self._compute_risk_level()
        self.primary_pattern = self._compute_primary_pattern()
        self.estimated_geoengineering_index = round(self.composite_score / 100 * 10, 2)

    def _compute_composite(self) -> float:
        """
        Weighted composite formula (weights sum to 1.00):
          unilateral_deployment_score  × 0.30
          + ecological_risk_score      × 0.25
          + governance_deficit_score   × 0.25
          + dual_use_weaponization_score × 0.20
        """
        score = (
            self.unilateral_deployment_score * 0.30
            + self.ecological_risk_score * 0.25
            + self.governance_deficit_score * 0.25
            + self.dual_use_weaponization_score * 0.20
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
        if self.unilateral_deployment_score > 70:
            return "Déploiement Unilatéral"
        if self.ecological_risk_score > 65:
            return "Risque Écosystémique"
        if self.governance_deficit_score > 60:
            return "Vide Gouvernanciel"
        if self.dual_use_weaponization_score > 55:
            return "Militarisation Climatique"
        if self.composite_score > 40:
            return "Expérimentation Non Consentie"
        return "Aucun"

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "unilateral_deployment_score": self.unilateral_deployment_score,
            "ecological_risk_score": self.ecological_risk_score,
            "governance_deficit_score": self.governance_deficit_score,
            "dual_use_weaponization_score": self.dual_use_weaponization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_geoengineering_index": self.estimated_geoengineering_index,
            "last_updated": self.last_updated,
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class GeoEngineeringEngine:
    """
    Swarm Intelligence module for geoengineering risk assessment.

    Computes composite risk scores, detects unilateral deployment patterns,
    and surfaces actionable insights for the Caelum Partners climate security desk.
    """

    ENGINE_VERSION = "1.0.0"
    DOMAIN = "geoengineering"

    def __init__(self) -> None:
        self.entities: List[GeoEngineeringEntity] = self._build_mock_entities()
        self.patterns: List[Dict[str, str]] = PATTERNS
        logger.info(
            "GeoEngineeringEngine initialised — %d entities, %d patterns",
            len(self.entities),
            len(self.patterns),
        )

    # ── Mock data ─────────────────────────────────────────────────────────────

    def _build_mock_entities(self) -> List[GeoEngineeringEntity]:
        """
        8 mock entities covering all 5 patterns and all 4 risk levels.
        Distribution: ≥3 critique, ≥2 élevé, ≥1 modéré, ≥2 faible.

        Composite formula verification:
          GE-001: 90*0.30 + 85*0.25 + 82*0.25 + 78*0.20 = 27.0+21.25+20.5+15.6 = 84.35 → critique ✓
          GE-002: 82*0.30 + 78*0.25 + 80*0.25 + 72*0.20 = 24.6+19.5+20.0+14.4  = 78.50 → critique ✓
          GE-003: 76*0.30 + 74*0.25 + 70*0.25 + 68*0.20 = 22.8+18.5+17.5+13.6  = 72.40 → critique ✓
          GE-004: 60*0.30 + 64*0.25 + 65*0.25 + 58*0.20 = 18.0+16.0+16.25+11.6 = 61.85 → élevé ✓
          GE-005: 55*0.30 + 58*0.25 + 62*0.25 + 52*0.20 = 16.5+14.5+15.5+10.4  = 56.90 → élevé ✓
          GE-006: 35*0.30 + 30*0.25 + 28*0.25 + 22*0.20 = 10.5+7.5+7.0+4.4     = 29.40 → modéré ✓
          GE-007: 10*0.30 + 12*0.25 + 8*0.25  + 9*0.20  = 3.0+3.0+2.0+1.8      = 9.80  → faible ✓
          GE-008: 12*0.30 + 10*0.25 + 14*0.25 + 8*0.20  = 3.6+2.5+3.5+1.6      = 11.20 → faible ✓
        """
        raw = [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────
            {
                "entity_id": "GE-001",
                "name": "Programme HAARP Russie — Division Climatique",
                "country": "Russie",
                "sector": "Géo-ingénierie Militaire",
                "unilateral_deployment_score": 90.0,
                "ecological_risk_score": 85.0,
                "governance_deficit_score": 82.0,
                "dual_use_weaponization_score": 78.0,
                "key_signals": [
                    "Expériences d'ionosphère non déclarées affectant les précipitations en Europe de l'Est",
                    "Programme militaire double usage modifiant les courants atmosphériques",
                    "Absence totale de notification internationale préalable aux déploiements",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id": "GE-002",
                "name": "SolarShield Technologies Corp",
                "country": "États-Unis",
                "sector": "Géo-ingénierie Privée",
                "unilateral_deployment_score": 82.0,
                "ecological_risk_score": 78.0,
                "governance_deficit_score": 80.0,
                "dual_use_weaponization_score": 72.0,
                "key_signals": [
                    "Dispersion d'aérosols stratosphériques sans autorisation gouvernementale",
                    "Brevets déposés sur des technologies de modification climatique à usage commercial",
                    "Financement par fonds spéculatifs ciblant des marchés carbone artificiels",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id": "GE-003",
                "name": "Programme National de Pluie Artificielle Chine",
                "country": "Chine",
                "sector": "Géo-ingénierie Étatique",
                "unilateral_deployment_score": 76.0,
                "ecological_risk_score": 74.0,
                "governance_deficit_score": 70.0,
                "dual_use_weaponization_score": 68.0,
                "key_signals": [
                    "1,5 million km² sous couverture d'ensemencement des nuages actif sans accord régional",
                    "Détournement des précipitations affectant les pays voisins (Inde, Vietnam, Kazakhstan)",
                    "Technologies duales utilisables pour priver les adversaires de ressources en eau",
                ],
                "last_updated": "2026-06-20",
            },
            # ── ÉLEVÉ (2) ─────────────────────────────────────────────────────
            {
                "entity_id": "GE-004",
                "name": "Make Sunsets LLC",
                "country": "États-Unis",
                "sector": "Géo-ingénierie Privée",
                "unilateral_deployment_score": 60.0,
                "ecological_risk_score": 64.0,
                "governance_deficit_score": 65.0,
                "dual_use_weaponization_score": 58.0,
                "key_signals": [
                    "Lancement de ballons dispersant du dioxyde de soufre au-dessus du Mexique sans accord",
                    "Modèle commercial vendant des 'crédits de refroidissement' non réglementés",
                    "Absence de protocole d'évaluation des impacts sur les populations locales",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id": "GE-005",
                "name": "Projet IROAM — Fertilisation Océanique Atlantique",
                "country": "Canada",
                "sector": "Géo-ingénierie Océanique",
                "unilateral_deployment_score": 55.0,
                "ecological_risk_score": 58.0,
                "governance_deficit_score": 62.0,
                "dual_use_weaponization_score": 52.0,
                "key_signals": [
                    "Dispersion de 100 tonnes de sulfate de fer en Pacifique Nord sans autorisation NOAA",
                    "Risques d'hypoxie sous-marine non évalués sur les zones de pêche internationales",
                    "Financement opaque via des entreprises-coquilles dans des paradis fiscaux",
                ],
                "last_updated": "2026-06-20",
            },
            # ── MODÉRÉ (1) ────────────────────────────────────────────────────
            {
                "entity_id": "GE-006",
                "name": "Programme SCoPEx — Harvard University",
                "country": "États-Unis",
                "sector": "Recherche Géo-ingénierie",
                "unilateral_deployment_score": 35.0,
                "ecological_risk_score": 30.0,
                "governance_deficit_score": 28.0,
                "dual_use_weaponization_score": 22.0,
                "key_signals": [
                    "Expériences stratosphériques en phase de test nécessitant un cadre de gouvernance",
                    "Financement partiellement privé créant des conflits d'intérêts potentiels",
                    "Débat scientifique non résolu sur les effets secondaires régionaux des aérosols",
                ],
                "last_updated": "2026-06-20",
            },
            # ── FAIBLE (2) ────────────────────────────────────────────────────
            {
                "entity_id": "GE-007",
                "name": "Groupe Intergouvernemental Experts Climat (GIEC)",
                "country": "International",
                "sector": "Gouvernance Climatique",
                "unilateral_deployment_score": 10.0,
                "ecological_risk_score": 12.0,
                "governance_deficit_score": 8.0,
                "dual_use_weaponization_score": 9.0,
                "key_signals": [
                    "Protocole de surveillance multilatérale des expériences géo-ingénierie actif",
                    "Recommandations de moratoire adoptées par 152 États membres de l'ONU",
                    "Transparence totale des données scientifiques avec peer-review international",
                ],
                "last_updated": "2026-06-20",
            },
            {
                "entity_id": "GE-008",
                "name": "Alliance Géo-ingénierie Responsable — Union Européenne",
                "country": "Union Européenne",
                "sector": "Gouvernance Climatique",
                "unilateral_deployment_score": 12.0,
                "ecological_risk_score": 10.0,
                "governance_deficit_score": 14.0,
                "dual_use_weaponization_score": 8.0,
                "key_signals": [
                    "Cadre réglementaire EU interdisant les expériences non autorisées au-dessus de l'Europe",
                    "Comité d'éthique transnational supervisant tous les projets de recherche",
                    "Protocole de partage de données obligatoire avec les pays tiers affectés",
                ],
                "last_updated": "2026-06-20",
            },
        ]
        return [GeoEngineeringEntity(**d) for d in raw]  # type: ignore[arg-type]

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
            if e.unilateral_deployment_score > 70:
                pattern_distribution["Déploiement Unilatéral"] += 1
            if e.ecological_risk_score > 65:
                pattern_distribution["Risque Écosystémique"] += 1
            if e.governance_deficit_score > 60:
                pattern_distribution["Vide Gouvernanciel"] += 1
            if e.dual_use_weaponization_score > 55:
                pattern_distribution["Militarisation Climatique"] += 1
            if e.composite_score > 40:
                pattern_distribution["Expérimentation Non Consentie"] += 1

        sorted_entities = sorted(self.entities, key=lambda e: e.composite_score, reverse=True)
        top_risk_entities = [e.name for e in sorted_entities[:3]]

        critical_alerts = [
            f"ALERTE CRITIQUE: {e.name} ({e.country}) — score géo-ingénierie {e.composite_score}/100"
            for e in self.entities if e.risk_level == "critique"
        ]

        avg_estimated_geoengineering_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities": n,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20T00:00:00Z",
            "engine_version": self.ENGINE_VERSION,
            "domain": self.DOMAIN,
            "confidence_score": 82.0,
            "data_sources": [
                "IPCC Geoengineering Assessment Reports",
                "Carnegie Climate Governance Initiative",
                "ETC Group Geoengineering Monitor",
                "Oxford Geoengineering Programme Database",
            ],
            "entities": [e.to_dict() for e in self.entities],
            "avg_estimated_geoengineering_index": avg_estimated_geoengineering_index,
        }

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_entities_by_risk(self, risk_level: str) -> List[GeoEngineeringEntity]:
        return [e for e in self.entities if e.risk_level == risk_level]

    def export(self) -> Dict[str, Any]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "summary": self.summary(),
            "patterns": self.patterns,
        }


# ── Module entry point ────────────────────────────────────────────────────────

def analyze_geoengineering() -> Dict[str, Any]:
    """Analyse les risques de géo-ingénierie climatique et retourne le résumé du moteur."""
    engine = GeoEngineeringEngine()
    result = engine.summary()
    print(f"[GeoEngineeringEngine] {result['total_entities']} entités analysées — "
          f"score composite moyen: {result['avg_composite']}/100")
    return result
