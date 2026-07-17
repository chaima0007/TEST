"""
Caelum Partners — Sovereign AI Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La souveraineté en intelligence artificielle comme nouvel enjeu géopolitique
majeur : les nations qui contrôlent leur infrastructure IA domestique
dominent ; celles qui dépendent de systèmes étrangers sont exposées à
une nouvelle forme de vassalité technologique et cognitive.

L'IA souveraine n'est pas un luxe — c'est la condition de l'autonomie
stratégique au XXIe siècle. Modèles de langage, puces, données,
et talent sont les quatre piliers de la puissance IA nationale.

Risk levels (dépendance IA / déficit souveraineté) :
  critique  → composite ≥ 60  (vassalité IA totale)
  élevé     → composite ≥ 40  (dépendance IA avancée)
  modéré    → composite ≥ 20  (autonomie IA partielle)
  faible    → composite < 20  (souveraineté IA consolidée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "vassalite_ia_totale": {
        "severity_fr": "Critique",
        "action_fr": "Stratégie nationale IA d'urgence — investissements souverains en puces, données et talent IA",
        "signal_fr": "dependency_exposure > 80 AND compute_autonomy_deficit > 75 — vassalité IA critique",
    },
    "dependance_ia_structurelle": {
        "severity_fr": "Critique",
        "action_fr": "Plan de désengagement progressif — partenariats IA multilatéraux et champions nationaux",
        "signal_fr": "Dépendance IA structurelle — systèmes critiques sous contrôle technologique étranger",
    },
    "autonomie_ia_partielle": {
        "severity_fr": "Élevé",
        "action_fr": "Accélération des capacités IA domestiques — formation talent et investissement compute souverain",
        "signal_fr": "Autonomie IA partielle — capacités domestiques insuffisantes face aux défis géopolitiques",
    },
    "strategie_ia_emergente": {
        "severity_fr": "Modéré",
        "action_fr": "Consolidation des capacités IA — roadmap souveraineté à 5 ans et partenariats stratégiques",
        "signal_fr": "Stratégie IA en construction — potentiel de souveraineté mais exécution encore incomplète",
    },
    "souverainete_ia_consolidee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de l'avance technologique et diffusion responsable des standards IA souverains",
        "signal_fr": "composite_score < 20 — souveraineté IA consolidée, infrastructure et talent domestiques solides",
    },
}


@dataclass
class SovereignAIEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    ai_dependency_exposure_score: float
    domestic_ai_capability_deficit_score: float
    ai_talent_gap_score: float
    compute_autonomy_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_ai_sovereignty_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.ai_dependency_exposure_score * 0.30
            + self.domestic_ai_capability_deficit_score * 0.25
            + self.ai_talent_gap_score * 0.25
            + self.compute_autonomy_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_ai_sovereignty_index = round(self.composite_score / 100 * 10, 2)

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
        if self.ai_dependency_exposure_score >= 80 and self.compute_autonomy_deficit_score >= 75:
            return "vassalite_ia_totale"
        if self.domestic_ai_capability_deficit_score >= 70:
            return "dependance_ia_structurelle"
        if self.composite_score >= 45:
            return "autonomie_ia_partielle"
        if self.composite_score >= 25:
            return "strategie_ia_emergente"
        return "souverainete_ia_consolidee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Vassalité IA critique pour {n} — infrastructure IA sous contrôle technologique étranger",
                "Déficit de capacités IA domestiques — dépendance aux modèles et puces étrangers totale",
                "Risque géopolitique majeur — coupure IA possible en cas de tension diplomatique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dépendance IA avancée pour {n} — autonomie stratégique compromise",
                "Talent IA insuffisant et absence de champions nationaux compétitifs",
                "Compute souverain inexistant — cloud et puces sous juridiction étrangère",
            ]
        if self.risk_level == "modéré":
            return [
                f"Autonomie IA partielle pour {n} — stratégie souveraineté en construction",
                "Capacités IA domestiques émergentes mais insuffisantes face aux géants technologiques",
                "Investissements en cours — horizont de souveraineté réaliste à moyen terme",
            ]
        return [
            f"{n} dispose d'une souveraineté IA consolidée — infrastructure et talent domestiques solides",
            "Champions IA nationaux compétitifs et compute souverain opérationnel",
            "Capacité d'exportation technologique — influence IA mondiale significative",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "ai_dependency_exposure_score": self.ai_dependency_exposure_score,
            "domestic_ai_capability_deficit_score": self.domestic_ai_capability_deficit_score,
            "ai_talent_gap_score": self.ai_talent_gap_score,
            "compute_autonomy_deficit_score": self.compute_autonomy_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ai_sovereignty_index": self.estimated_ai_sovereignty_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SovereignAIEntity] = [
    SovereignAIEntity("SA-001", "Afrique Subsaharienne", "Afrique", "Vassalité IA Totale", 90.0, 88.0, 85.0, 92.0),
    SovereignAIEntity("SA-002", "Amérique Latine (hors Brésil)", "Amériques", "Dépendance IA Structurelle", 85.0, 80.0, 82.0, 78.0),
    SovereignAIEntity("SA-003", "Moyen-Orient (hors Golfe)", "MENA", "Capacités IA Minimales", 82.0, 78.0, 80.0, 75.0),
    SovereignAIEntity("SA-004", "Asie du Sud-Est", "Asie", "Dépendance Mixte USA/Chine", 78.0, 72.0, 75.0, 70.0),
    SovereignAIEntity("SA-005", "Europe (hors France/Allemagne)", "Europe", "Dépendance Cloud US", 60.0, 55.0, 58.0, 52.0),
    SovereignAIEntity("SA-006", "Inde — IA Émergente", "Asie du Sud", "Autonomie IA en Construction", 42.0, 38.0, 35.0, 40.0),
    SovereignAIEntity("SA-007", "Europe (France+Allemagne+UK)", "Europe", "Stratégie IA Souveraine Partielle", 28.0, 22.0, 25.0, 20.0),
    SovereignAIEntity("SA-008", "USA & Chine — Duopole IA", "Global", "Souveraineté IA Maximale", 5.0, 8.0, 6.0, 4.0),
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
        "domain": "aisovreignty",
        "confidence_score": 0.82,
        "data_sources": ["stanford_ai_index", "compute_tracker", "ai_talent_concentration_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_ai_sovereignty_index": round(avg / 100 * 10, 2),
    }


def analyze_sovereign_ai() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Sovereign AI Engine — {r['total_entities']} zones, avg déficit: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
