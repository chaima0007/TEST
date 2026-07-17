"""
Caelum Partners — Biosafety Infrastructure Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La prolifération des laboratoires de haute sécurité biologique (BSL-3/4)
et la recherche sur la fonction de gain comme menace géopolitique :
quand plus de 50 laboratoires BSL-4 opèrent dans 23 pays avec des
standards de sécurité inégaux, quand la recherche gain-of-function
crée des pathogènes plus dangereux que leurs versions naturelles,
la question n'est plus si une pandémie d'origine laboratoire se produira
— mais quand et depuis quel labo.

La biosécurité est la dimension oubliée de la sécurité nationale :
les missiles ont des traités de non-prolifération, les armes chimiques
sont interdites par convention, mais les pathogènes améliorés en
laboratoire prolifèrent dans l'opacité géopolitique totale.

Risk levels (vulnérabilité de l'infrastructure biosécurité) :
  critique  → composite ≥ 60  (risque de fuite laboratoire majeur)
  élevé     → composite ≥ 40  (standards biosécurité insuffisants)
  modéré    → composite ≥ 20  (lacunes dans la gouvernance BSL)
  faible    → composite < 20  (biosécurité exemplaire)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "risque_fuite_critique": {
        "severity_fr": "Critique",
        "action_fr": "Inspection internationale d'urgence et moratoire sur la recherche gain-of-function non-supervisée",
        "signal_fr": "biosafety_compliance_gap > 80 AND gain_of_function_opacity > 75 — risque de fuite critique",
    },
    "proliferation_non_supervisee": {
        "severity_fr": "Critique",
        "action_fr": "Traité international sur la biosécurité des laboratoires et transparence totale des recherches",
        "signal_fr": "Prolifération non-supervisée de laboratoires BSL — standards de sécurité non-vérifiables",
    },
    "gouvernance_inadequate": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des inspections internationales et standards minimaux contraignants pour BSL-3/4",
        "signal_fr": "Gouvernance biosécurité inadéquate — cadre légal insuffisant pour superviser les recherches risquées",
    },
    "lacunes_reglementaires": {
        "severity_fr": "Modéré",
        "action_fr": "Réforme réglementaire de la recherche sur pathogènes à risque et transparence accrue",
        "signal_fr": "Lacunes réglementaires — supervision partielle mais risques résiduels significatifs",
    },
    "biosecurite_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des standards stricts et partage des bonnes pratiques avec les pays à risque élevé",
        "signal_fr": "composite_score < 20 — biosécurité exemplaire, transparence et supervision maximale",
    },
}


@dataclass
class BiosafetyInfrastructureEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    biosafety_compliance_gap_score: float
    gain_of_function_opacity_score: float
    laboratory_proliferation_score: float
    international_oversight_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_biosafety_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.biosafety_compliance_gap_score * 0.30
            + self.gain_of_function_opacity_score * 0.25
            + self.laboratory_proliferation_score * 0.25
            + self.international_oversight_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_biosafety_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.biosafety_compliance_gap_score >= 80 and self.gain_of_function_opacity_score >= 75:
            return "risque_fuite_critique"
        if self.laboratory_proliferation_score >= 70:
            return "proliferation_non_supervisee"
        if self.composite_score >= 45:
            return "gouvernance_inadequate"
        if self.composite_score >= 25:
            return "lacunes_reglementaires"
        return "biosecurite_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Risque de fuite laboratoire critique dans {n} — standards BSL insuffisants et opacité totale",
                "Recherche gain-of-function sans supervision internationale adéquate — pathogènes renforcés non-contrôlés",
                "Prolifération incontrôlée de laboratoires BSL — capacités biologique sans gouvernance internationale",
            ]
        if self.risk_level == "élevé":
            return [
                f"Gouvernance biosécurité inadéquate dans {n} — supervision insuffisante des recherches risquées",
                "Standards de sécurité BSL non-harmonisés — incidents containment non-déclarés probables",
                "Cadre légal insuffisant pour superviser la recherche sur les agents pathogènes à risque",
            ]
        if self.risk_level == "modéré":
            return [
                f"Lacunes réglementaires biosécurité dans {n} — supervision partielle mais améliorable",
                "Transparence insuffisante sur les recherches à double usage — risque de détournement civil/militaire",
                "Coopération internationale biosécurité existante mais incomplète",
            ]
        return [
            f"{n} maintient une biosécurité exemplaire — standards stricts, transparence et supervision maximale",
            "Inspections régulières des laboratoires BSL et données partagées avec les organisations internationales",
            "Modèle de gouvernance biosécurité à diffuser pour prévenir les pandémies d'origine laboratoire",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "biosafety_compliance_gap_score": self.biosafety_compliance_gap_score,
            "gain_of_function_opacity_score": self.gain_of_function_opacity_score,
            "laboratory_proliferation_score": self.laboratory_proliferation_score,
            "international_oversight_deficit_score": self.international_oversight_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_biosafety_risk_index": self.estimated_biosafety_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[BiosafetyInfrastructureEntity] = [
    BiosafetyInfrastructureEntity("BI-001", "Chine — Wuhan BSL-4 & Opacité", "Asie", "Institut de Virologie Wuhan & Gain-of-Function Non-Transparent", 92.0, 95.0, 85.0, 90.0),
    BiosafetyInfrastructureEntity("BI-002", "Russie — Biopreparat Héritage Soviétique", "Europe de l'Est", "Vecteurs Biologiques Militaires & Laboratoires Non-Inspectés", 88.0, 85.0, 82.0, 88.0),
    BiosafetyInfrastructureEntity("BI-003", "Pays en Développement — BSL Non-Certifiés", "Global Sud", "Laboratoires BSL-2/3 sans Standards Internationaux", 80.0, 72.0, 88.0, 78.0),
    BiosafetyInfrastructureEntity("BI-004", "Iran — Programme Biologique Dual-Use", "MENA", "Recherche Biologique Militaire & Civile Non-Démêlée", 78.0, 82.0, 75.0, 80.0),
    BiosafetyInfrastructureEntity("BI-005", "USA — Gain-of-Function Controversé", "Amérique du Nord", "NIH Financement GOF & Moratorium Partiel Insuffisant", 60.0, 70.0, 65.0, 58.0),
    BiosafetyInfrastructureEntity("BI-006", "Afrique — Capacités Biosécurité Limitées", "Afrique", "Lacunes Standards BSL & Dépendance Expertise Étrangère", 55.0, 48.0, 62.0, 52.0),
    BiosafetyInfrastructureEntity("BI-007", "France & Allemagne — Standards Stricts", "Europe", "Régulation Européenne Robuste mais Perfectible", 28.0, 25.0, 30.0, 22.0),
    BiosafetyInfrastructureEntity("BI-008", "UK & Suisse — Biosécurité Exemplaire", "Europe", "Porton Down & Spiez — Transparence et Supervision Maximale", 8.0, 6.0, 12.0, 5.0),
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
        "domain": "biosafety",
        "confidence_score": 0.69,
        "data_sources": ["nuclear_threat_initiative_bio_index", "who_ihhr_compliance_tracker", "ghs_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_biosafety_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_biosafety_infrastructure() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Biosafety Infrastructure Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
