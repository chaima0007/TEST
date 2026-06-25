"""
Caelum Partners — Techno-Darwinism Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La sélection technologique des sociétés : dans chaque grande transition
technologique (imprimerie, vapeur, électricité, internet, IA), les sociétés
qui s'adaptent rapidement prospèrent ; celles qui résistent ou n'ont pas accès
sont marginalisées, dépendantes ou absorbées.

Le techno-darwinisme n'est pas une métaphore — c'est le mécanisme réel
par lequel les puissances mondiales émergent, stagnent et déclinent.
Aujourd'hui, l'IA et la biotechnologie sont le moteur sélectif.

Score élevé = VULNÉRABILITÉ élevée à la sélection technologique (risque de décrochage).

Risk levels :
  critique  → composite ≥ 60  (extinction technologique imminente)
  élevé     → composite ≥ 40  (décrochage numérique avancé)
  modéré    → composite ≥ 20  (adaptation partielle)
  faible    → composite < 20  (darwinisme technologique positif)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "extinction_technologique": {
        "severity_fr": "Critique",
        "action_fr": "Plan Marshall technologique d'urgence — transfert de technologie et infrastructure numérique critique",
        "signal_fr": "adaptation_lag > 80 AND workforce_vulnerability > 75 — extinction technologique imminente",
    },
    "decrochage_numerique": {
        "severity_fr": "Critique",
        "action_fr": "Programme national de rattrapage technologique — formation massive et partenariats tech",
        "signal_fr": "Décrochage numérique critique — fossé technologique s'élargissant avec les leaders",
    },
    "transition_douloureuse": {
        "severity_fr": "Élevé",
        "action_fr": "Accompagnement social des transitions technologiques et réforme du système éducatif",
        "signal_fr": "Transition technologique douloureuse — adaptation en cours mais destructrice socialement",
    },
    "adaptation_partielle": {
        "severity_fr": "Modéré",
        "action_fr": "Accélération de l'écosystème d'innovation et réforme réglementaire pro-innovation",
        "signal_fr": "Adaptation technologique partielle — capacité de rattrapage existante mais insuffisante",
    },
    "darwinisme_positif": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de l'avance technologique et diffusion responsable des technologies souveraines",
        "signal_fr": "composite_score < 20 — darwinisme technologique positif, adaptation rapide et continue",
    },
}


@dataclass
class TechnoDarwinismEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    technological_adaptation_lag_score: float
    workforce_displacement_vulnerability_score: float
    innovation_ecosystem_deficit_score: float
    regulatory_agility_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_technodarwin_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.technological_adaptation_lag_score * 0.30
            + self.workforce_displacement_vulnerability_score * 0.25
            + self.innovation_ecosystem_deficit_score * 0.25
            + self.regulatory_agility_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_technodarwin_index = round(self.composite_score / 100 * 10, 2)

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
        if self.technological_adaptation_lag_score >= 80 and self.workforce_displacement_vulnerability_score >= 75:
            return "extinction_technologique"
        if self.technological_adaptation_lag_score >= 65:
            return "decrochage_numerique"
        if self.composite_score >= 45:
            return "transition_douloureuse"
        if self.composite_score >= 25:
            return "adaptation_partielle"
        return "darwinisme_positif"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Extinction technologique imminente pour {n} — fossé avec les leaders s'élargissant",
                "Main-d'œuvre massivement vulnérable à l'automatisation sans filet social suffisant",
                "Absence d'écosystème d'innovation local — dépendance technologique totale",
            ]
        if self.risk_level == "élevé":
            return [
                f"Décrochage numérique avancé dans {n} — transition technologique douloureuse",
                "Workforce displacement massif sans reconversion suffisante — choc social tech",
                "Écosystème d'innovation insuffisant — dépendance aux technologies étrangères",
            ]
        if self.risk_level == "modéré":
            return [
                f"Adaptation technologique partielle dans {n} — capacité de rattrapage existante",
                "Tensions entre vitesse d'adaptation tech et protection sociale des travailleurs",
                "Réglementation en retard sur les nouvelles technologies — risque d'inadaptation",
            ]
        return [
            f"{n} démontre un darwinisme technologique positif — adaptation rapide et continue",
            "Écosystème d'innovation robuste — capacité à créer et adopter les nouvelles technologies",
            "Modèle de transition technologique exemplaire à étudier et diffuser",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "technological_adaptation_lag_score": self.technological_adaptation_lag_score,
            "workforce_displacement_vulnerability_score": self.workforce_displacement_vulnerability_score,
            "innovation_ecosystem_deficit_score": self.innovation_ecosystem_deficit_score,
            "regulatory_agility_deficit_score": self.regulatory_agility_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_technodarwin_index": self.estimated_technodarwin_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[TechnoDarwinismEntity] = [
    TechnoDarwinismEntity("TD-001", "Afrique Subsaharienne", "Afrique", "Sans Infrastructure Numérique", 92.0, 88.0, 90.0, 82.0),
    TechnoDarwinismEntity("TD-002", "MENA Rentier (hors Golfe)", "Moyen-Orient", "Dépendance Hydrocarbures & Stagnation Tech", 85.0, 80.0, 85.0, 75.0),
    TechnoDarwinismEntity("TD-003", "Amérique Latine Moyenne", "Amériques", "Sans Écosystème Innovation", 80.0, 78.0, 82.0, 70.0),
    TechnoDarwinismEntity("TD-004", "Asie du Sud (hors Inde Tech)", "Asie du Sud", "Croissance Sans Innovation Endogène", 72.0, 70.0, 75.0, 65.0),
    TechnoDarwinismEntity("TD-005", "Europe Continentale — Sur-réglementée", "Europe", "Innovation vs Précaution Réglementaire", 50.0, 45.0, 52.0, 58.0),
    TechnoDarwinismEntity("TD-006", "USA/UK — Inégalités d'Accès Tech", "Anglosaxon", "Innovation Maximale & Exclusion Sociale", 30.0, 35.0, 22.0, 28.0),
    TechnoDarwinismEntity("TD-007", "Asie du Nord-Est (Japon/Corée)", "Asie", "Adaptation Rapide & Résilience", 18.0, 15.0, 20.0, 12.0),
    TechnoDarwinismEntity("TD-008", "Chine & Singapour — Leaders Tech", "Asie", "Darwinisme Technologique Positif Total", 8.0, 10.0, 5.0, 6.0),
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
        "domain": "technodarwin",
        "confidence_score": 0.80,
        "data_sources": ["global_innovation_index", "automation_vulnerability_tracker", "digital_readiness_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_technodarwin_index": round(avg / 100 * 10, 2),
    }


def analyze_techno_darwinism() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Techno-Darwinism Engine — {r['total_entities']} zones, avg vulnérabilité: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
