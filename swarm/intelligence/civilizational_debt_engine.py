"""Caelum Partners — Civilizational Debt Intelligence Engine
Mesure la dette TOTALE (financière + écologique + sociale + intergénérationnelle)
léguée aux générations futures — un concept unique à Caelum Partners.
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import dataclasses
import logging
import typing

logger = logging.getLogger("swarm.civdebt")

DOMAIN = "civdebt"

PATTERNS: typing.Dict[str, typing.Dict[str, str]] = {
    "effondrement_generationnel": {
        "name": "effondrement_generationnel",
        "severity_fr": "Effondrement générationnel — dette intégrale insoutenable pour les héritiers",
        "action_fr": "Plan d'urgence de réduction drastique de la dette civilisationnelle totale",
        "signal_fr": "Effondrement générationnel imminent — les générations futures ne pourront honorer cet héritage",
    },
    "transfert_massif_risques": {
        "name": "transfert_massif_risques",
        "severity_fr": "Transfert massif des risques vers les générations futures",
        "action_fr": "Instauration immédiate de mécanismes de responsabilité intergénérationnelle",
        "signal_fr": "Transfert massif avéré — accumulation accélérée de passifs intergénérationnels",
    },
    "erosion_heritages": {
        "name": "erosion_heritages",
        "severity_fr": "Érosion progressive des héritages — capital transmis en déclin",
        "action_fr": "Renforcement des politiques de préservation du capital intergénérationnel",
        "signal_fr": "Érosion confirmée — capital naturel, social et institutionnel en dégradation",
    },
    "accumulation_silencieuse": {
        "name": "accumulation_silencieuse",
        "severity_fr": "Accumulation silencieuse — dettes invisibles croissantes",
        "action_fr": "Audit complet des passifs cachés et engagement de transparence générationnelle",
        "signal_fr": "Accumulation sous-radar détectée — passifs non comptabilisés en progression",
    },
    "equilibre_intergenerationnel": {
        "name": "equilibre_intergenerationnel",
        "severity_fr": "Équilibre intergénérationnel — gestion responsable du patrimoine commun",
        "action_fr": "Maintien et renforcement des politiques d'équité intergénérationnelle",
        "signal_fr": "Équilibre maintenu — transmission équitable du patrimoine aux générations futures",
    },
}


@dataclasses.dataclass
class CivDebtEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    ecological_debt_score: float
    financial_debt_score: float
    social_debt_score: float
    institutional_debt_score: float
    last_updated: str = "2026-06-20"

    def composite_score(self) -> float:
        return round(
            self.ecological_debt_score * 0.30
            + self.financial_debt_score * 0.25
            + self.social_debt_score * 0.25
            + self.institutional_debt_score * 0.20,
            2,
        )

    def risk_level(self) -> str:
        c = self.composite_score()
        if c >= 60:
            return "critique"
        if c >= 40:
            return "élevé"
        if c >= 20:
            return "modéré"
        return "faible"

    def primary_pattern(self) -> str:
        c = self.composite_score()
        if c >= 70:
            return "effondrement_generationnel"
        if c >= 55:
            return "transfert_massif_risques"
        if c >= 40:
            return "erosion_heritages"
        if c >= 20:
            return "accumulation_silencieuse"
        return "equilibre_intergenerationnel"

    def key_signals(self) -> typing.List[str]:
        risk = self.risk_level()
        pattern = self.primary_pattern()
        pat_info = PATTERNS[pattern]
        if risk == "critique":
            return [
                f"Dette écologique critique — score {self.ecological_debt_score:.1f}/100 : {pat_info['signal_fr']}",
                f"Dette financière souveraine alarmante — {self.financial_debt_score:.1f}/100 — engagements non financés massifs",
                f"Dette sociale explosive — indice {self.social_debt_score:.1f}/100 : inégalités et désinvestissements structurels",
            ]
        if risk == "élevé":
            return [
                f"Dette écologique élevée — score {self.ecological_debt_score:.1f}/100 : pression environnementale forte",
                f"Dette financière préoccupante — {self.financial_debt_score:.1f}/100 — trajectoire insoutenable",
                f"Dette sociale en hausse — indice {self.social_debt_score:.1f}/100 : tensions intergénérationnelles croissantes",
            ]
        if risk == "modéré":
            return [
                f"Dette écologique modérée — score {self.ecological_debt_score:.1f}/100 : surveillance maintenue",
                f"Dette financière gérable — {self.financial_debt_score:.1f}/100 — vigilance nécessaire",
                f"Dette sociale contenue — indice {self.social_debt_score:.1f}/100 : politiques d'équité actives",
            ]
        return [
            f"Dette écologique faible — score {self.ecological_debt_score:.1f}/100 : gestion durable exemplaire",
            f"Dette financière maîtrisée — {self.financial_debt_score:.1f}/100 — équilibre budgétaire intergénérationnel",
            f"Dette sociale minimale — indice {self.social_debt_score:.1f}/100 : cohésion sociale et équité préservées",
        ]

    def estimated_civdebt_index(self) -> float:
        return round(self.composite_score() / 100 * 10, 2)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        comp = self.composite_score()
        pattern_key = self.primary_pattern()
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": comp,
            "ecological_debt_score": self.ecological_debt_score,
            "financial_debt_score": self.financial_debt_score,
            "social_debt_score": self.social_debt_score,
            "institutional_debt_score": self.institutional_debt_score,
            "risk_level": self.risk_level(),
            "primary_pattern": pattern_key,
            "key_signals": self.key_signals(),
            "estimated_civdebt_index": self.estimated_civdebt_index(),
            "last_updated": self.last_updated,
        }


_MOCK_ENTITIES: typing.List[CivDebtEntity] = [
    # 4 critique (composite ≥ 60)
    CivDebtEntity(
        entity_id="CD-001",
        name="États-Unis",
        country="États-Unis",
        sector="Nation-État",
        ecological_debt_score=75.0,
        financial_debt_score=80.0,
        social_debt_score=72.0,
        institutional_debt_score=65.0,
    ),
    CivDebtEntity(
        entity_id="CD-002",
        name="Chine",
        country="Chine",
        sector="Nation-État",
        ecological_debt_score=82.0,
        financial_debt_score=70.0,
        social_debt_score=68.0,
        institutional_debt_score=78.0,
    ),
    CivDebtEntity(
        entity_id="CD-003",
        name="Brésil",
        country="Brésil",
        sector="Nation-État",
        ecological_debt_score=78.0,
        financial_debt_score=65.0,
        social_debt_score=75.0,
        institutional_debt_score=70.0,
    ),
    CivDebtEntity(
        entity_id="CD-005",
        name="Nigéria",
        country="Nigéria",
        sector="Nation-État",
        ecological_debt_score=68.0,
        financial_debt_score=55.0,
        social_debt_score=80.0,
        institutional_debt_score=62.0,
    ),
    # 2 élevé (composite ≥ 40 et < 60)
    CivDebtEntity(
        entity_id="CD-004",
        name="Italie",
        country="Italie",
        sector="Nation-État",
        ecological_debt_score=55.0,
        financial_debt_score=72.0,
        social_debt_score=52.0,
        institutional_debt_score=48.0,
    ),
    CivDebtEntity(
        entity_id="CD-006",
        name="Allemagne",
        country="Allemagne",
        sector="Nation-État",
        ecological_debt_score=42.0,
        financial_debt_score=52.0,
        social_debt_score=38.0,
        institutional_debt_score=35.0,
    ),
    # 1 modéré (composite ≥ 20 et < 40)
    CivDebtEntity(
        entity_id="CD-007",
        name="Danemark",
        country="Danemark",
        sector="Nation-État",
        ecological_debt_score=28.0,
        financial_debt_score=22.0,
        social_debt_score=18.0,
        institutional_debt_score=15.0,
    ),
    # 1 faible (composite < 20)
    CivDebtEntity(
        entity_id="CD-008",
        name="Singapour",
        country="Singapour",
        sector="Nation-État",
        ecological_debt_score=15.0,
        financial_debt_score=12.0,
        social_debt_score=10.0,
        institutional_debt_score=8.0,
    ),
]


class CivDebtEngine:
    """Civilizational Debt Intelligence Engine — Caelum Partners."""

    domain: str = DOMAIN

    def analyze(self) -> typing.List[typing.Dict[str, typing.Any]]:
        logger.debug(
            "CivDebtEngine.analyze() — processing %d entities", len(_MOCK_ENTITIES)
        )
        return [e.to_dict() for e in _MOCK_ENTITIES]

    def summary(self) -> typing.Dict[str, typing.Any]:
        entities = self.analyze()

        risk_distribution: typing.Dict[str, int] = {
            "critique": 0,
            "élevé": 0,
            "modéré": 0,
            "faible": 0,
        }
        pattern_distribution: typing.Dict[str, int] = {
            "effondrement_generationnel": 0,
            "transfert_massif_risques": 0,
            "erosion_heritages": 0,
            "accumulation_silencieuse": 0,
            "equilibre_intergenerationnel": 0,
        }
        total_composite = 0.0
        critical_alerts: typing.List[str] = []

        for ent in entities:
            risk = ent["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1

            pat = ent["primary_pattern"]
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1

            total_composite += ent["composite_score"]

            if risk == "critique":
                critical_alerts.append(
                    f"[ALERTE CRITIQUE] {ent['name']} ({ent['country']}) — "
                    f"Dette civilisationnelle {ent['composite_score']:.1f}/100 — Urgence intergénérationnelle"
                )

        n = len(entities) or 1
        avg_composite = round(total_composite / n, 2)

        sorted_by_risk = sorted(entities, key=lambda x: x["composite_score"], reverse=True)
        top_risk_entities = [e["name"] for e in sorted_by_risk[:3]]

        logger.info(
            "CivDebtEngine.summary() — avg_composite=%.2f, critique=%d",
            avg_composite,
            risk_distribution["critique"],
        )

        return {
            "total_entities": len(entities),
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": "1.0.0",
            "domain": DOMAIN,
            "confidence_score": 0.86,
            "data_sources": [
                "intergenerational_justice_index",
                "ecological_debt_tracker",
                "sovereign_debt_monitor",
            ],
            "entities": entities,
            "avg_estimated_civdebt_index": round(avg_composite / 100 * 10, 2),
        }


def analyze_civdebt() -> dict:
    engine = CivDebtEngine()
    return engine.summary()
