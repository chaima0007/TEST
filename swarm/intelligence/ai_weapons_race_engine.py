"""
Caelum Partners — AI Weapons Race Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La course aux armes autonomes létales (LAWS) : la révolution militaire la
plus dangereuse depuis la bombe atomique. Un système d'armes autonome peut
sélectionner et engager des cibles sans intervention humaine — il peut décider
de tuer sans que personne ne soit responsable de la décision. Cette dissociation
entre la décision létale et la responsabilité humaine pose une question
existentielle : qui répond des crimes de guerre commis par une machine ?

Les USA développent via DARPA des avions de chasse autonomes (X-62A VISTA,
F-16 autonome testé en 2023), des essaims de drones tueurs, et intègrent
l'IA dans leur boucle de décision OODA via le projet MAVEN. La Chine a
déployé des drones autonomes Sharp Sword en Mer de Chine, intègre l'IA
dans ses systèmes de missiles hypersoniques DF-17, et construit des drones
tueurs sous-marins. Israël opère déjà des systèmes semi-autonomes — l'IAF
a utilisé une IA pour cibler des milliers d'objectifs à Gaza en quelques
secondes via le système "Lavender". La Russie développe le char Uran-9 et
le missile nucléaire autonome Poseidon. La Turquie exporte des Bayraktar TB2
— premier drone de guerre à avoir changé l'issue d'un conflit (Nagorno-Karabakh).

La Campagne Stop Killer Robots regroupe 200 ONG. L'ONU négocie depuis 2014
sans aboutir. Pendant ce temps, les LAWS prolifèrent.

Risk levels (armes autonomes et militarisation de l'IA) :
  critique  → composite ≥ 60  (programme LAWS opérationnel — armes IA déployées)
  élevé     → composite ≥ 40  (capacités LAWS en développement actif — prolifération)
  modéré    → composite ≥ 20  (débat LAWS — régulation insuffisante face aux risques)
  faible    → composite < 20  (normes anti-LAWS — plaidoyer pour l'interdiction)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "suprematie_ia_militaire": {
        "severity_fr": "Critique",
        "action_fr": "Traité d'interdiction des LAWS et mécanismes de vérification internationale des systèmes autonomes létaux",
        "signal_fr": "lethal_autonomous_weapons_score > 80 AND ai_decision_loop_integration_score > 80 — suprématie IA militaire",
    },
    "integration_ia_decision": {
        "severity_fr": "Critique",
        "action_fr": "Maintien du contrôle humain meaningful dans toutes les décisions létales et supervision des algorithmes militaires",
        "signal_fr": "IA dans boucle décision — systèmes militaires déléguant les décisions de ciblage à des algorithmes autonomes",
    },
    "cyberguerre_ia_offensive": {
        "severity_fr": "Critique",
        "action_fr": "Normes de conduite responsable dans le cyberespace et limitations des cyberoffensives autonomes par IA",
        "signal_fr": "Cyberguerre IA offensive — utilisation d'IA offensives autonomes dans les opérations cyber militaires",
    },
    "proliferation_drones_autonomes": {
        "severity_fr": "Élevé",
        "action_fr": "Régime de contrôle des exportations de drones autonomes et standards de comportement responsable",
        "signal_fr": "Prolifération de drones autonomes — diffusion des LAWS à des acteurs non-étatiques et États instables",
    },
    "regulation_ia_militaire": {
        "severity_fr": "Modéré",
        "action_fr": "Soutien aux négociations ONU sur les LAWS et renforcement des mécanismes de contrôle humain mandatory",
        "signal_fr": "composite_score < 40 — débat réglementaire sur les LAWS sans capacités offensives significatives",
    },
}


@dataclass
class AIWeaponsRaceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    lethal_autonomous_weapons_score: float
    ai_decision_loop_integration_score: float
    cyber_ai_offensive_score: float
    regulation_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_ai_weapons_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.lethal_autonomous_weapons_score * 0.30
            + self.ai_decision_loop_integration_score * 0.25
            + self.cyber_ai_offensive_score * 0.25
            + self.regulation_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_ai_weapons_index = round(self.composite_score / 100 * 10, 2)

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
        if self.lethal_autonomous_weapons_score >= 80 and self.ai_decision_loop_integration_score >= 80:
            return "suprematie_ia_militaire"
        if self.ai_decision_loop_integration_score >= 80:
            return "integration_ia_decision"
        if self.cyber_ai_offensive_score >= 75:
            return "cyberguerre_ia_offensive"
        if self.composite_score >= 40:
            return "proliferation_drones_autonomes"
        return "regulation_ia_militaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Course aux armes autonomes létales critique dans {n} — LAWS déployés ou testés en conditions opérationnelles",
                "IA dans la boucle de ciblage — systèmes militaires délégant des décisions létales à des algorithmes sans contrôle humain",
                "Absence de responsabilité — les crimes de guerre commis par des machines autonomes sans traité d'interdiction opérationnel",
            ]
        if self.risk_level == "élevé":
            return [
                f"Prolifération de drones autonomes dans {n} — exportation de LAWS sans régulation éthique ou traçabilité",
                "Course à l'IA militaire — investissements massifs en essaims de drones autonomes et systèmes de ciblage algorithmique",
                "Normalisation des LAWS — seuil psychologique de la décision létale autonome abaissé sans consensus international",
            ]
        if self.risk_level == "modéré":
            return [
                f"Débat LAWS insuffisant dans {n} — réglementation intérieure insuffisante face aux risques des armes autonomes",
                "Fragmentation réglementaire — absence de position nationale claire sur l'interdiction des LAWS offensifs",
                "Risque de retard réglementaire — la course technologique dépasse les capacités normatives nationales et internationales",
            ]
        return [
            f"{n} soutient activement l'interdiction des LAWS — plaidoyer pour le contrôle humain meaningful",
            "Engagement pour un traité LAWS contraignant — participation aux négociations ONU et soutien à la Campagne Stop Killer Robots",
            "Modèle de régulation éthique de l'IA militaire — principes d'utilisation responsable de l'IA en contexte de conflit",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "lethal_autonomous_weapons_score": self.lethal_autonomous_weapons_score,
            "ai_decision_loop_integration_score": self.ai_decision_loop_integration_score,
            "cyber_ai_offensive_score": self.cyber_ai_offensive_score,
            "regulation_deficit_score": self.regulation_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ai_weapons_index": self.estimated_ai_weapons_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AIWeaponsRaceEntity] = [
    AIWeaponsRaceEntity("AW-001", "USA — DARPA AI Next & F-16 Autonome", "Amérique du Nord", "Projet MAVEN, X-62A VISTA & Essaims Drones Tueurs Autonomes Pentagone", 85.0, 88.0, 82.0, 80.0),
    AIWeaponsRaceEntity("AW-002", "Chine — Sharp Sword & Drones Autonomes DF-17", "Asie", "Drones UCAV Autonomes Mer de Chine, Missiles IA & Algorithmes Ciblage Gaza-Style", 90.0, 85.0, 88.0, 78.0),
    AIWeaponsRaceEntity("AW-003", "Russie — Uran-9 & Poseidon Nucléaire Autonome", "Europe de l'Est", "Char Uran-9, Missile Nucléaire Poseidon Autonome & SORM-IA Intégré", 78.0, 82.0, 75.0, 85.0),
    AIWeaponsRaceEntity("AW-004", "Israël — Harpy & Système Lavender Gaza", "MENA", "Drones Autonomes Harpy, Système IA Lavender 37000 Cibles & Iron Dome IA", 80.0, 72.0, 78.0, 68.0),
    AIWeaponsRaceEntity("AW-005", "Corée du Sud/Corée du Nord — Course LAWS Péninsule", "Asie", "SGR-A1 Robot Sentinelle Autonome vs DPRK Drones Suicide Autonomes", 55.0, 52.0, 48.0, 60.0),
    AIWeaponsRaceEntity("AW-006", "Turquie — Bayraktar TB2 & Export LAWS", "MENA/Europe", "TB2 Nagorno-Karabakh, Aksungur & Export Drones Autonomes 30+ Pays", 52.0, 45.0, 42.0, 55.0),
    AIWeaponsRaceEntity("AW-007", "UE — Débat Fragmentation Réglementaire LAWS", "Europe", "IA Act EU sans Volet Militaire & Positions Nationales Contradictoires LAWS", 25.0, 30.0, 22.0, 35.0),
    AIWeaponsRaceEntity("AW-008", "ICRC & Stop Killer Robots — Normes Anti-LAWS", "Global", "Campagne 200 ONG & Négociations ONU depuis 2014 — Plaidoyer Interdiction", 5.0, 4.0, 6.0, 3.0),
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
        "domain": "ai_weapons",
        "confidence_score": 0.79,
        "data_sources": ["sipri_military_ai_database", "campaign_stop_killer_robots", "icrc_autonomous_weapons_report"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_ai_weapons_index": round(avg / 100 * 10, 2),
    }


def analyze_ai_weapons_race() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"AI Weapons Race Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
