"""
Caelum Partners — Criminal State Capture Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La capture de l'État par la criminalité organisée comme forme ultime
de corruption systémique : au-delà de la simple corruption, la capture
criminelle de l'État désigne le processus par lequel les organisations
criminelles (cartels, mafias, groupes trafiquants) infiltrent et
contrôlent les institutions souveraines — police, justice, armée,
parlement, présidence — jusqu'à devenir l'État lui-même.

Le Mexique illustre la forme la plus avancée : des cartels comme le
Sinaloa ou le CJNG contrôlent des régions entières, corrompent des
généraux et des juges, et définissent de facto la politique de certains
États fédéraux. La Guinée-Bissau est le premier narco-État africain
certifié. Les Balkans ont vu naître des États créés expressément pour
faciliter le trafic. La Colombie des années 90, l'Afghanistan sous
les talibans (héroïne), la Birmanie du Nord (méthamphétamine), et
la Russie post-soviétique (oligarchie mafieuse) sont des modèles de
capture criminelle à différents stades. C'est la corruption élevée au
rang de constitution.

Risk levels (intensité de la capture criminelle de l'État) :
  critique  → composite ≥ 60  (capture criminelle avancée — État partiellement contrôlé par la criminalité)
  élevé     → composite ≥ 40  (infiltration criminelle significative des institutions)
  modéré    → composite ≥ 20  (risques de capture criminelle à surveiller)
  faible    → composite < 20  (État de droit résistant à la capture criminelle)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "narco_etat_avere": {
        "severity_fr": "Critique",
        "action_fr": "Aide internationale d'urgence et pression diplomatique pour restaurer l'État de droit",
        "signal_fr": "criminal_territorial_control > 80 AND institutional_penetration > 75 — narco-État avéré",
    },
    "oligarchie_mafieuse": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions ciblées sur les oligarques et soutien aux institutions judiciaires indépendantes",
        "signal_fr": "Oligarchie mafieuse — élites économiques criminelles contrôlant l'État sans affrontement direct",
    },
    "infiltration_institutionnelle": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement de la magistrature indépendante et programmes anti-blanchiment renforcés",
        "signal_fr": "Infiltration institutionnelle — criminalité organisée ayant capturé des pans de l'appareil d'État",
    },
    "corruption_systemique": {
        "severity_fr": "Modéré",
        "action_fr": "Réformes anti-corruption et renforcement des capacités de la société civile",
        "signal_fr": "Corruption systémique — risque de capture criminelle accélérée sans contre-mesures institutionnelles",
    },
    "etat_de_droit_resilient": {
        "severity_fr": "Faible",
        "action_fr": "Maintenir la vigilance anti-corruption et partager les bonnes pratiques d'État de droit",
        "signal_fr": "composite_score < 20 — État de droit résilient avec institutions indépendantes et intègres",
    },
}


@dataclass
class CriminalStateCaptureEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    criminal_territorial_control_score: float
    institutional_penetration_score: float
    illicit_economy_dominance_score: float
    judicial_capture_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_capture_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.criminal_territorial_control_score * 0.30
            + self.institutional_penetration_score * 0.25
            + self.illicit_economy_dominance_score * 0.25
            + self.judicial_capture_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_capture_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.criminal_territorial_control_score >= 80 and self.institutional_penetration_score >= 75:
            return "narco_etat_avere"
        if self.illicit_economy_dominance_score >= 75:
            return "oligarchie_mafieuse"
        if self.composite_score >= 40:
            return "infiltration_institutionnelle"
        if self.composite_score >= 20:
            return "corruption_systemique"
        return "etat_de_droit_resilient"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Capture criminelle avancée dans {n} — organisations criminelles contrôlant des pans entiers de l'État",
                "Territoires sous contrôle criminel — État incapable d'exercer son autorité dans des zones entières",
                "Justice capturée — juges, procureurs et forces de l'ordre sous influence directe des organisations criminelles",
            ]
        if self.risk_level == "élevé":
            return [
                f"Infiltration institutionnelle significative dans {n} — criminalité organisée corrompant les institutions clés",
                "Économie illicite importante — narcotrafic, contrebande ou blanchiment représentant une part du PIB",
                "Système judiciaire partiellement compromis — impunité des acteurs criminels connectés au pouvoir",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risques de capture criminelle dans {n} — corruption systémique fragilisant les institutions",
                "Infiltration partielle des administrations locales par des réseaux criminels organisés",
                "Économie grise significative — risque de normalisation de l'illicite dans les circuits économiques",
            ]
        return [
            f"{n} maintient un État de droit résilient — institutions indépendantes résistant à la capture criminelle",
            "Justice indépendante et effective contre la criminalité organisée — poursuites effectives des acteurs criminels",
            "Modèle de résistance à la capture criminelle — transparence institutionnelle et société civile vigilante",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "criminal_territorial_control_score": self.criminal_territorial_control_score,
            "institutional_penetration_score": self.institutional_penetration_score,
            "illicit_economy_dominance_score": self.illicit_economy_dominance_score,
            "judicial_capture_score": self.judicial_capture_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_capture_index": self.estimated_capture_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[CriminalStateCaptureEntity] = [
    CriminalStateCaptureEntity("CS-001", "Mexique — Cartels comme Co-Gouvernants", "Amériques", "Sinaloa & CJNG Contrôlant États Entiers — Narco-État Partiel", 90.0, 85.0, 88.0, 82.0),
    CriminalStateCaptureEntity("CS-002", "Guinée-Bissau — 1er Narco-État Africain", "Afrique de l'Ouest", "Cocaïne Sud-Américaine Transitant & Finançant l'Armée au Pouvoir", 82.0, 88.0, 85.0, 80.0),
    CriminalStateCaptureEntity("CS-003", "Russie — Oligarchie Mafieuse d'État", "Europe de l'Est", "Siloviki & Oligarques — Fusion Criminalité Organisée et Pouvoir d'État", 70.0, 80.0, 92.0, 78.0),
    CriminalStateCaptureEntity("CS-004", "Myanmar — Junte & Économie de Drogue", "Asie du Sud-Est", "Triangle d'Or — Armée Contrôlant Méthamphétamine comme Source de Financement", 85.0, 78.0, 85.0, 72.0),
    CriminalStateCaptureEntity("CS-005", "Honduras & El Salvador — États Post-Capture", "Amériques", "Maras Ayant Pénétré Police & Politique — Bukele à El Salvador", 55.0, 52.0, 50.0, 55.0),
    CriminalStateCaptureEntity("CS-006", "Albanie & Macédoine du Nord — Balkans Criminels", "Europe du Sud-Est", "Trafic Drogue & Humains avec Complicité Partielle des Institutions", 50.0, 55.0, 60.0, 52.0),
    CriminalStateCaptureEntity("CS-007", "Nigeria — État Fédéral Fragilisé par Boko Haram/EFCC", "Afrique de l'Ouest", "Corruption Pétrolière & Boko Haram Contrôlant le Nord-Est — Fragilité", 28.0, 32.0, 30.0, 22.0),
    CriminalStateCaptureEntity("CS-008", "Suisse & Pays-Bas — Résistance Exemplaire", "Europe", "Droit Pénal Robuste et FIOD/MROS contre Blanchiment & Crime Organisé", 5.0, 8.0, 6.0, 4.0),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "criminal_capture",
        "confidence_score": 0.79,
        "data_sources": ["global_initiative_against_transnational_crime", "transparency_international_capture_index", "unodc_crime_statistics"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_capture_index": round(avg / 100 * 10, 2),
    }


def analyze_criminal_state_capture() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Criminal State Capture Engine — {r['total_entities']} États, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
