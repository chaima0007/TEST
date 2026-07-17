"""Caelum Partners — AI Bias Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("swarm.bias")

DOMAIN = "bias"

PATTERNS: list[dict[str, str]] = [
    {
        "name": "biais_algorithmique",
        "severity_fr": "Critique",
        "action_fr": "Audit immédiat des algorithmes de décision automatisée",
        "signal_fr": "Score algorithmique élevé détecté",
    },
    {
        "name": "biais_données",
        "severity_fr": "Élevé",
        "action_fr": "Révision des jeux de données d'entraînement et de validation",
        "signal_fr": "Déséquilibre majeur dans les données sources",
    },
    {
        "name": "impact_discriminatoire",
        "severity_fr": "Critique",
        "action_fr": "Évaluation d'impact sur les groupes protégés requise",
        "signal_fr": "Impacts discriminatoires identifiés sur populations vulnérables",
    },
    {
        "name": "opacite_systematique",
        "severity_fr": "Élevé",
        "action_fr": "Mise en place d'un cadre d'explicabilité (XAI)",
        "signal_fr": "Manque de transparence systémique dans les décisions",
    },
    {
        "name": "equilibre_biais",
        "severity_fr": "Faible",
        "action_fr": "Surveillance continue et rapports périodiques",
        "signal_fr": "Équilibre relatif des biais observé",
    },
]


def _detect_pattern(algorithmic: float, data: float, impact: float, transparency: float) -> dict[str, str]:
    if algorithmic >= 70:
        return PATTERNS[0]
    if data >= 70:
        return PATTERNS[1]
    if impact >= 70:
        return PATTERNS[2]
    if transparency >= 70:
        return PATTERNS[3]
    return PATTERNS[4]


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critique"
    if composite >= 40:
        return "élevé"
    if composite >= 20:
        return "modéré"
    return "faible"


@dataclass
class BiasEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    algorithmic_score: float
    data_score: float
    impact_score: float
    transparency_score: float
    model_count: int
    key_signals: list[str] = field(default_factory=list)

    def composite_score(self) -> float:
        return round(
            self.algorithmic_score * 0.30
            + self.data_score * 0.25
            + self.impact_score * 0.25
            + self.transparency_score * 0.20,
            2,
        )

    def to_dict(self) -> dict[str, Any]:
        composite = self.composite_score()
        pattern = _detect_pattern(
            self.algorithmic_score,
            self.data_score,
            self.impact_score,
            self.transparency_score,
        )
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": composite,
            "algorithmic_score": self.algorithmic_score,
            "data_score": self.data_score,
            "impact_score": self.impact_score,
            "transparency_score": self.transparency_score,
            "risk_level": _risk_level(composite),
            "primary_pattern": pattern["name"],
            "key_signals": self.key_signals,
            "estimated_bias_index": round(composite / 100 * 10, 2),
            "last_updated": "2026-06-20",
            "model_count": self.model_count,
        }


# Sub-score design to hit target composites:
# formula: algo×0.30 + data×0.25 + impact×0.25 + transparency×0.20
#
# ENT-001: 85×.30+80×.25+72×.25+68×.20 = 25.5+20+18+13.6 = 77.1  → critique
# ENT-002: 75×.30+72×.25+68×.25+65×.20 = 22.5+18+17+13   = 70.5  → critique
# ENT-003: 70×.30+66×.25+62×.25+55×.20 = 21+16.5+15.5+11 = 64.0  → critique
# ENT-004: 55×.30+58×.25+52×.25+48×.20 = 16.5+14.5+13+9.6= 53.6  → élevé
# ENT-005: 48×.30+50×.25+44×.25+40×.20 = 14.4+12.5+11+8  = 45.9  → élevé
# ENT-006: 35×.30+32×.25+30×.25+26×.20 = 10.5+8+7.5+5.2  = 31.2  → modéré
# ENT-007: 15×.30+14×.25+13×.25+12×.20 = 4.5+3.5+3.25+2.4= 13.65 → faible
# ENT-008: 10×.30+9×.25+8×.25+7×.20   = 3+2.25+2+1.4    = 8.65  → faible

_MOCK_ENTITIES: list[BiasEntity] = [
    BiasEntity(
        entity_id="ENT-001",
        name="AlgoDecide Corp",
        country="États-Unis",
        sector="Justice & Juridique",
        algorithmic_score=85.0,
        data_score=80.0,
        impact_score=72.0,
        transparency_score=68.0,
        model_count=47,
        key_signals=[
            "Taux de faux positifs 3× plus élevé pour les minorités ethniques",
            "Absence de mécanisme d'appel algorithmique documenté",
            "Opacité totale sur les variables de prédiction de récidive",
        ],
    ),
    BiasEntity(
        entity_id="ENT-002",
        name="HireAI Systems",
        country="Royaume-Uni",
        sector="Ressources Humaines",
        algorithmic_score=75.0,
        data_score=72.0,
        impact_score=68.0,
        transparency_score=65.0,
        model_count=23,
        key_signals=[
            "Sous-représentation féminine dans les profils sélectionnés (+40%)",
            "Données d'entraînement issues de 92% d'hommes blancs",
            "Aucun audit externe d'équité réalisé depuis 2023",
        ],
    ),
    BiasEntity(
        entity_id="ENT-003",
        name="CreditBot Finance",
        country="Allemagne",
        sector="Services Financiers",
        algorithmic_score=70.0,
        data_score=66.0,
        impact_score=62.0,
        transparency_score=55.0,
        model_count=89,
        key_signals=[
            "Discrimination indirecte basée sur le code postal",
            "Score de crédit défavorable corrélé à l'origine nationale",
            "Absence d'explication individuelle des refus de prêt",
        ],
    ),
    BiasEntity(
        entity_id="ENT-004",
        name="MedPredict AI",
        country="France",
        sector="Santé & Médical",
        algorithmic_score=55.0,
        data_score=58.0,
        impact_score=52.0,
        transparency_score=48.0,
        model_count=12,
        key_signals=[
            "Sous-représentation des femmes dans les essais cliniques sources",
            "Biais de confirmation dans les diagnostics assistés",
            "Données manquantes pour les populations âgées de plus de 75 ans",
        ],
    ),
    BiasEntity(
        entity_id="ENT-005",
        name="PolicePredAI",
        country="Pays-Bas",
        sector="Sécurité Publique",
        algorithmic_score=48.0,
        data_score=50.0,
        impact_score=44.0,
        transparency_score=40.0,
        model_count=8,
        key_signals=[
            "Surpopulation de certains quartiers dans les données de surveillance",
            "Boucle de rétroaction amplifiant les biais historiques",
            "Validation limitée sur populations culturellement diversifiées",
        ],
    ),
    BiasEntity(
        entity_id="ENT-006",
        name="AdTargetML",
        country="Espagne",
        sector="Marketing & Publicité",
        algorithmic_score=35.0,
        data_score=32.0,
        impact_score=30.0,
        transparency_score=26.0,
        model_count=156,
        key_signals=[
            "Ciblage différentiel selon genre pour offres d'emploi",
            "Exclusion partielle de segments démographiques vulnérables",
            "Profils comportementaux non audités pour équité",
        ],
    ),
    BiasEntity(
        entity_id="ENT-007",
        name="FairLens Analytics",
        country="Suède",
        sector="Recherche & Développement",
        algorithmic_score=15.0,
        data_score=14.0,
        impact_score=13.0,
        transparency_score=12.0,
        model_count=5,
        key_signals=[
            "Protocoles d'équité intégrés dans le cycle de développement",
            "Audits internes trimestriels d'équité algorithmique",
            "Publication transparente des métriques de biais",
        ],
    ),
    BiasEntity(
        entity_id="ENT-008",
        name="EthicAI Solutions",
        country="Canada",
        sector="Conseil & Audit",
        algorithmic_score=10.0,
        data_score=9.0,
        impact_score=8.0,
        transparency_score=7.0,
        model_count=3,
        key_signals=[
            "Certification ISO/IEC 42001 obtenue en 2025",
            "Comité d'éthique indépendant actif depuis la création",
            "Données d'entraînement diversifiées et documentées publiquement",
        ],
    ),
]


class BiasEngine:
    """AI Bias Intelligence Engine for Caelum Partners."""

    def analyze(self) -> list[dict[str, Any]]:
        """Return list of 8 entity dicts."""
        logger.info("BiasEngine.analyze() — domain=%s, entities=%d", DOMAIN, len(_MOCK_ENTITIES))
        return [entity.to_dict() for entity in _MOCK_ENTITIES]

    def summary(self) -> dict[str, Any]:
        """Return summary dict with exactly 13 keys."""
        entities = self.analyze()

        total = len(entities)
        avg_composite = round(sum(e["composite_score"] for e in entities) / total, 2)

        risk_distribution: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
        pattern_distribution: dict[str, int] = {
            "biais_algorithmique": 0,
            "biais_données": 0,
            "impact_discriminatoire": 0,
            "opacite_systematique": 0,
            "equilibre_biais": 0,
        }

        for e in entities:
            risk_distribution[e["risk_level"]] += 1
            pattern_distribution[e["primary_pattern"]] += 1

        sorted_by_composite = sorted(entities, key=lambda x: x["composite_score"], reverse=True)
        top_risk_entities = [e["name"] for e in sorted_by_composite[:3]]

        critical_alerts: list[str] = []
        for e in entities:
            if e["risk_level"] == "critique":
                critical_alerts.append(
                    f"ALERTE CRITIQUE — {e['name']} ({e['country']}) : "
                    f"score composite {e['composite_score']:.1f}/100, "
                    f"pattern '{e['primary_pattern']}' détecté"
                )

        avg_estimated_bias_index = round(avg_composite / 100 * 10, 2)

        logger.info(
            "BiasEngine.summary() — avg_composite=%.2f, critiques=%d",
            avg_composite,
            risk_distribution["critique"],
        )

        return {
            "total_entities": total,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": "1.0.0",
            "domain": DOMAIN,
            "confidence_score": 0.91,
            "data_sources": ["audit_reports", "model_registries", "discrimination_complaints"],
            "entities": entities,
            "avg_estimated_bias_index": avg_estimated_bias_index,
        }


def analyze_bias() -> dict:
    engine = BiasEngine()
    return engine.summary()
