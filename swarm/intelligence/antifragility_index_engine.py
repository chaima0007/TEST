"""Caelum Partners — Antifragility Index Intelligence Engine
Inspiré de Nassim Taleb — mesure la capacité des nations/systèmes à se RENFORCER
sous le stress (pas juste résister). Propriété exclusive de Chaima Mhadbi,
Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import dataclasses
import logging
import typing

logger = logging.getLogger("swarm.antifragility")

DOMAIN = "antifragility"

PATTERNS: typing.Dict[str, typing.Dict[str, str]] = {
    "systeme_antifragile": {
        "name": "systeme_antifragile",
        "severity_fr": "Système antifragile — se renforce sous le stress",
        "action_fr": "Capitaliser sur les chocs pour accélérer la croissance systémique",
        "signal_fr": "Antifragilité avérée — les perturbations génèrent des gains nets",
    },
    "resilience_adaptive": {
        "name": "resilience_adaptive",
        "severity_fr": "Résilience adaptive — absorption et adaptation rapide",
        "action_fr": "Renforcer les mécanismes d'adaptation institutionnelle existants",
        "signal_fr": "Capacité d'adaptation élevée — rebond post-choc structuré",
    },
    "fragilite_cachee": {
        "name": "fragilite_cachee",
        "severity_fr": "Fragilité cachée — vulnérabilités masquées par la stabilité apparente",
        "action_fr": "Audit approfondi des dépendances systémiques non visibles",
        "signal_fr": "Fragilité latente détectée — exposition aux chocs sous-estimée",
    },
    "vulnerabilite_systemique": {
        "name": "vulnerabilite_systemique",
        "severity_fr": "Vulnérabilité systémique — manque d'options stratégiques",
        "action_fr": "Diversification d'urgence des options et des capacités de réponse",
        "signal_fr": "Vulnérabilité systémique confirmée — optionnalité stratégique insuffisante",
    },
    "fragilite_critique": {
        "name": "fragilite_critique",
        "severity_fr": "Fragilité critique — effondrement systémique sous stress",
        "action_fr": "Intervention immédiate de stabilisation et réduction des expositions",
        "signal_fr": "Fragilité critique — tout choc majeur risque l'effondrement systémique",
    },
}


@dataclasses.dataclass
class AntifragilityEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    stress_response_score: float
    adaptive_capacity_score: float
    optionality_score: float
    convexity_score: float
    last_updated: str = "2026-06-20"

    def composite_score(self) -> float:
        return round(
            self.stress_response_score * 0.30
            + self.adaptive_capacity_score * 0.25
            + self.optionality_score * 0.25
            + self.convexity_score * 0.20,
            2,
        )

    def risk_level(self) -> str:
        c = self.composite_score()
        if c < 40:
            return "critique"
        if c < 70:
            return "élevé"
        if c < 80:
            return "modéré"
        return "faible"

    def primary_pattern(self) -> str:
        c = self.composite_score()
        if c >= 80:
            return "systeme_antifragile"
        if c >= 60:
            return "resilience_adaptive"
        if c >= 40:
            return "fragilite_cachee"
        if c >= 20:
            return "vulnerabilite_systemique"
        return "fragilite_critique"

    def key_signals(self) -> typing.List[str]:
        risk = self.risk_level()
        pattern = self.primary_pattern()
        pat_info = PATTERNS[pattern]
        if risk == "critique":
            return [
                f"Réponse au stress critique — score {self.stress_response_score:.1f}/100 : {pat_info['signal_fr']}",
                f"Capacité adaptive insuffisante — {self.adaptive_capacity_score:.1f}/100 — institutions rigides",
                f"Optionnalité stratégique quasi nulle — indice {self.optionality_score:.1f}/100 : intervention urgente requise",
            ]
        if risk == "élevé":
            return [
                f"Réponse au stress faible — score {self.stress_response_score:.1f}/100 : fragilité préoccupante",
                f"Capacité adaptive limitée — {self.adaptive_capacity_score:.1f}/100 — adaptation lente",
                f"Optionnalité restreinte — indice {self.optionality_score:.1f}/100 : diversification nécessaire",
            ]
        if risk == "modéré":
            return [
                f"Réponse au stress modérée — score {self.stress_response_score:.1f}/100 : résilience partielle",
                f"Capacité adaptive fonctionnelle — {self.adaptive_capacity_score:.1f}/100 — amélioration possible",
                f"Optionnalité satisfaisante — indice {self.optionality_score:.1f}/100 : renforcement recommandé",
            ]
        return [
            f"Réponse au stress excellente — score {self.stress_response_score:.1f}/100 : renforcement sous pression",
            f"Capacité adaptive élevée — {self.adaptive_capacity_score:.1f}/100 — institutions agiles",
            f"Optionnalité stratégique forte — indice {self.optionality_score:.1f}/100 : asymétrie positive",
        ]

    def estimated_antifragility_index(self) -> float:
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
            "stress_response_score": self.stress_response_score,
            "adaptive_capacity_score": self.adaptive_capacity_score,
            "optionality_score": self.optionality_score,
            "convexity_score": self.convexity_score,
            "risk_level": self.risk_level(),
            "primary_pattern": pattern_key,
            "key_signals": self.key_signals(),
            "estimated_antifragility_index": self.estimated_antifragility_index(),
            "last_updated": self.last_updated,
        }


_MOCK_ENTITIES: typing.List[AntifragilityEntity] = [
    # 3 faible risque (très antifragiles, composite ≥ 80)
    AntifragilityEntity(
        entity_id="AF-001",
        name="Singapour",
        country="Singapour",
        sector="Nation-État",
        stress_response_score=92.0,
        adaptive_capacity_score=88.0,
        optionality_score=85.0,
        convexity_score=90.0,
    ),
    AntifragilityEntity(
        entity_id="AF-002",
        name="Suisse",
        country="Suisse",
        sector="Nation-État",
        stress_response_score=88.0,
        adaptive_capacity_score=90.0,
        optionality_score=92.0,
        convexity_score=85.0,
    ),
    AntifragilityEntity(
        entity_id="AF-003",
        name="Israël",
        country="Israël",
        sector="Nation-État",
        stress_response_score=85.0,
        adaptive_capacity_score=82.0,
        optionality_score=78.0,
        convexity_score=88.0,
    ),
    # 1 modéré (composite ≥ 60 et < 80)
    AntifragilityEntity(
        entity_id="AF-004",
        name="États-Unis",
        country="États-Unis",
        sector="Nation-État",
        stress_response_score=72.0,
        adaptive_capacity_score=68.0,
        optionality_score=75.0,
        convexity_score=70.0,
    ),
    # 2 élevé (composite ≥ 40 et < 60)
    AntifragilityEntity(
        entity_id="AF-005",
        name="Allemagne",
        country="Allemagne",
        sector="Nation-État",
        stress_response_score=65.0,
        adaptive_capacity_score=70.0,
        optionality_score=68.0,
        convexity_score=62.0,
    ),
    AntifragilityEntity(
        entity_id="AF-006",
        name="Brésil",
        country="Brésil",
        sector="Nation-État",
        stress_response_score=48.0,
        adaptive_capacity_score=42.0,
        optionality_score=45.0,
        convexity_score=40.0,
    ),
    # 2 critique (composite < 40)
    AntifragilityEntity(
        entity_id="AF-007",
        name="Pakistan",
        country="Pakistan",
        sector="Nation-État",
        stress_response_score=28.0,
        adaptive_capacity_score=22.0,
        optionality_score=30.0,
        convexity_score=25.0,
    ),
    AntifragilityEntity(
        entity_id="AF-008",
        name="Venezuela",
        country="Venezuela",
        sector="Nation-État",
        stress_response_score=15.0,
        adaptive_capacity_score=12.0,
        optionality_score=18.0,
        convexity_score=10.0,
    ),
]


class AntifragilityEngine:
    """Antifragility Index Intelligence Engine — Caelum Partners."""

    domain: str = DOMAIN

    def analyze(self) -> typing.List[typing.Dict[str, typing.Any]]:
        logger.debug(
            "AntifragilityEngine.analyze() — processing %d entities", len(_MOCK_ENTITIES)
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
            "systeme_antifragile": 0,
            "resilience_adaptive": 0,
            "fragilite_cachee": 0,
            "vulnerabilite_systemique": 0,
            "fragilite_critique": 0,
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
                    f"Score antifragilité {ent['composite_score']:.1f}/100 — Fragilité systémique avérée"
                )

        n = len(entities) or 1
        avg_composite = round(total_composite / n, 2)

        # Pour le risque, on trie par score croissant (les moins antifragiles en premier)
        sorted_by_risk = sorted(entities, key=lambda x: x["composite_score"])
        top_risk_entities = [e["name"] for e in sorted_by_risk[:3]]

        logger.info(
            "AntifragilityEngine.summary() — avg_composite=%.2f, critique=%d",
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
            "confidence_score": 0.79,
            "data_sources": [
                "resilience_tracker",
                "institutional_quality_index",
                "adaptive_capacity_monitor",
            ],
            "entities": entities,
            "avg_estimated_antifragility_index": round(avg_composite / 100 * 10, 2),
        }


def analyze_antifragility() -> dict:
    engine = AntifragilityEngine()
    return engine.summary()
