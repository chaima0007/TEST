"""Caelum Partners — AMR Global Response Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import dataclasses
import logging
import typing

logger = logging.getLogger("swarm.amr")

DOMAIN = "amr"

PATTERNS: typing.Dict[str, typing.Dict[str, str]] = {
    "resistance_totale": {
        "name": "resistance_totale",
        "severity_fr": "Résistance totale aux antimicrobiens — crise systémique",
        "action_fr": "Déclenchement immédiat du protocole AMR d'urgence mondiale",
        "signal_fr": "Résistance totale détectée — tous antibiotiques de dernier recours inefficaces",
    },
    "pipeline_vide": {
        "name": "pipeline_vide",
        "severity_fr": "Pipeline thérapeutique vide — absence de nouveaux antimicrobiens",
        "action_fr": "Mobilisation d'urgence des investissements en R&D antimicrobienne",
        "signal_fr": "Aucun traitement alternatif disponible — déficit thérapeutique critique",
    },
    "confinement_echoue": {
        "name": "confinement_echoue",
        "severity_fr": "Confinement épidémique échoué — propagation incontrôlée",
        "action_fr": "Renforcement immédiat des mesures de quarantaine et de surveillance",
        "signal_fr": "Confinement inefficace — dissémination AMR hors de contrôle",
    },
    "cooperation_absente": {
        "name": "cooperation_absente",
        "severity_fr": "Absence totale de coopération internationale AMR",
        "action_fr": "Convocation d'urgence d'un sommet mondial de coordination AMR",
        "signal_fr": "Déficit de coopération — réponse mondiale fragmentée et inefficace",
    },
    "reponse_amr_coordonnee": {
        "name": "reponse_amr_coordonnee",
        "severity_fr": "Réponse AMR coordonnée — surveillance active en cours",
        "action_fr": "Maintien et renforcement des protocoles de surveillance AMR existants",
        "signal_fr": "Coordination AMR opérationnelle — systèmes de veille actifs",
    },
}


@dataclasses.dataclass
class AmrEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    detection_score: float
    treatment_score: float
    containment_score: float
    cooperation_score: float
    outbreak_count: int
    last_updated: str = "2026-06-20"

    def composite_score(self) -> float:
        return round(
            self.detection_score * 0.30
            + self.treatment_score * 0.25
            + self.containment_score * 0.25
            + self.cooperation_score * 0.20,
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
        if self.detection_score >= 70:
            return "resistance_totale"
        if self.treatment_score >= 70:
            return "pipeline_vide"
        if self.containment_score >= 70:
            return "confinement_echoue"
        if self.cooperation_score >= 70:
            return "cooperation_absente"
        return "reponse_amr_coordonnee"

    def key_signals(self) -> typing.List[str]:
        risk = self.risk_level()
        pattern = self.primary_pattern()
        pat_info = PATTERNS[pattern]
        if risk == "critique":
            return [
                f"Détection AMR critique — score {self.detection_score:.1f}/100 : {pat_info['signal_fr']}",
                f"Pipeline thérapeutique en déficit sévère — {self.treatment_score:.1f}/100 traitements disponibles",
                f"Coopération mondiale insuffisante — indice {self.cooperation_score:.1f}/100 : coordination AMR urgente",
            ]
        if risk == "élevé":
            return [
                f"Détection AMR élevée — score {self.detection_score:.1f}/100 : surveillance renforcée requise",
                f"Pipeline thérapeutique sous tension — {self.treatment_score:.1f}/100 options thérapeutiques",
                f"Coopération internationale partielle — indice {self.cooperation_score:.1f}/100 : renforcement nécessaire",
            ]
        if risk == "modéré":
            return [
                f"Détection AMR modérée — score {self.detection_score:.1f}/100 : veille épidémiologique maintenue",
                f"Pipeline thérapeutique opérationnel — {self.treatment_score:.1f}/100 traitements en développement",
                f"Coopération internationale satisfaisante — indice {self.cooperation_score:.1f}/100 : protocoles actifs",
            ]
        return [
            f"Détection AMR faible — score {self.detection_score:.1f}/100 : situation sous contrôle",
            f"Pipeline thérapeutique solide — {self.treatment_score:.1f}/100 antimicrobiens disponibles",
            f"Coopération internationale forte — indice {self.cooperation_score:.1f}/100 : réponse coordonnée",
        ]

    def estimated_amr_index(self) -> float:
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
            "detection_score": self.detection_score,
            "treatment_score": self.treatment_score,
            "containment_score": self.containment_score,
            "cooperation_score": self.cooperation_score,
            "risk_level": self.risk_level(),
            "primary_pattern": pattern_key,
            "key_signals": self.key_signals(),
            "estimated_amr_index": self.estimated_amr_index(),
            "last_updated": self.last_updated,
            "outbreak_count": self.outbreak_count,
        }


_MOCK_ENTITIES: typing.List[AmrEntity] = [
    # 3 critique (~74, ~69, ~62)
    AmrEntity(
        entity_id="ENT-001",
        name="WHO AMR Task Force",
        country="Suisse",
        sector="Santé Mondiale",
        detection_score=80.0,
        treatment_score=72.0,
        containment_score=68.0,
        cooperation_score=71.0,
        outbreak_count=47,
    ),
    AmrEntity(
        entity_id="ENT-002",
        name="South Asia AMR Hub",
        country="Inde",
        sector="Santé Publique",
        detection_score=76.0,
        treatment_score=65.0,
        containment_score=68.0,
        cooperation_score=62.0,
        outbreak_count=312,
    ),
    AmrEntity(
        entity_id="ENT-003",
        name="African Resistance Network",
        country="Nigeria",
        sector="Épidémiologie",
        detection_score=68.0,
        treatment_score=62.0,
        containment_score=60.0,
        cooperation_score=54.0,
        outbreak_count=189,
    ),
    # 2 élevé (~52, ~45)
    AmrEntity(
        entity_id="ENT-004",
        name="EU AMR Action Plan",
        country="Belgique",
        sector="Politique Sanitaire",
        detection_score=56.0,
        treatment_score=52.0,
        containment_score=50.0,
        cooperation_score=48.0,
        outbreak_count=23,
    ),
    AmrEntity(
        entity_id="ENT-005",
        name="LATAM Health Consortium",
        country="Brésil",
        sector="Recherche Clinique",
        detection_score=50.0,
        treatment_score=44.0,
        containment_score=44.0,
        cooperation_score=40.0,
        outbreak_count=78,
    ),
    # 1 modéré (~29)
    AmrEntity(
        entity_id="ENT-006",
        name="Nordic AMR Institute",
        country="Suède",
        sector="Recherche & Développement",
        detection_score=32.0,
        treatment_score=28.0,
        containment_score=28.0,
        cooperation_score=26.0,
        outbreak_count=8,
    ),
    # 2 faible (~14, ~8)
    AmrEntity(
        entity_id="ENT-007",
        name="Singapore Biomed Centre",
        country="Singapour",
        sector="Biotechnologie",
        detection_score=16.0,
        treatment_score=14.0,
        containment_score=12.0,
        cooperation_score=12.0,
        outbreak_count=3,
    ),
    AmrEntity(
        entity_id="ENT-008",
        name="Swiss Precision Health",
        country="Suisse",
        sector="Médecine de Précision",
        detection_score=9.0,
        treatment_score=8.0,
        containment_score=7.0,
        cooperation_score=8.0,
        outbreak_count=1,
    ),
]


class AmrEngine:
    """AMR Global Response Intelligence Engine — Caelum Partners."""

    domain: str = DOMAIN

    def analyze(self) -> typing.List[typing.Dict[str, typing.Any]]:
        logger.debug("AmrEngine.analyze() — processing %d entities", len(_MOCK_ENTITIES))
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
            "resistance_totale": 0,
            "pipeline_vide": 0,
            "confinement_echoue": 0,
            "cooperation_absente": 0,
            "reponse_amr_coordonnee": 0,
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
                    f"Score {ent['composite_score']:.1f} — Foyers: {ent['outbreak_count']}"
                )

        n = len(entities) or 1
        avg_composite = round(total_composite / n, 2)

        sorted_by_risk = sorted(entities, key=lambda x: x["composite_score"], reverse=True)
        top_risk_entities = [e["name"] for e in sorted_by_risk[:3]]

        logger.info(
            "AmrEngine.summary() — avg_composite=%.2f, critique=%d",
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
            "confidence_score": 0.89,
            "data_sources": [
                "who_surveillance",
                "clinical_trials_db",
                "resistance_monitoring",
            ],
            "entities": entities,
            "avg_estimated_amr_index": round(avg_composite / 100 * 10, 2),
        }


def analyze_amr() -> dict:
    engine = AmrEngine()
    return engine.summary()
