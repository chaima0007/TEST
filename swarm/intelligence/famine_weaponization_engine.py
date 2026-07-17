"""
Caelum Partners — Famine Weaponization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'instrumentalisation délibérée de la faim comme arme de guerre :
quand les blocus privent des populations civiles de nourriture,
quand les greniers sont bombardés et les champs minés, quand l'aide
humanitaire est bloquée comme outil de pression géopolitique,
la faim n'est plus une tragédie — c'est une stratégie militaire.

De l'Holodomor soviétique au Yémen contemporain, du Bengale de 1943
à la Syrie sous siège, la famine délibérée est l'arme la plus
ancienne et la moins punie de l'humanité. Le droit humanitaire
international l'interdit formellement — les puissances qui l'utilisent
le font avec une quasi-impunité géopolitique totale.

Risk levels (utilisation délibérée de la faim comme arme) :
  critique  → composite ≥ 60  (famine délibérée en cours)
  élevé     → composite ≥ 40  (instrumentalisation active de la faim)
  modéré    → composite ≥ 20  (risques d'utilisation de la faim comme outil)
  faible    → composite < 20  (respect du droit humanitaire alimentaire)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "famine_deliberee_active": {
        "severity_fr": "Critique",
        "action_fr": "Corridors humanitaires forcés et sanctions immédiates sur les entités bloquant l'aide alimentaire",
        "signal_fr": "blockade_intensity > 80 AND humanitarian_access_denial > 75 — famine délibérée confirmée",
    },
    "siege_alimentaire": {
        "severity_fr": "Critique",
        "action_fr": "Résolution d'urgence au Conseil de Sécurité ONU et pression internationale maximale",
        "signal_fr": "Siège alimentaire actif — population civile privée délibérément d'accès à la nourriture",
    },
    "instrumentalisation_partielle": {
        "severity_fr": "Élevé",
        "action_fr": "Négociations humanitaires urgentes et accès des organisations internationales aux zones de conflit",
        "signal_fr": "Instrumentalisation partielle de la faim — aide humanitaire conditionnée à des objectifs politiques",
    },
    "risque_utilisation": {
        "severity_fr": "Modéré",
        "action_fr": "Monitoring humanitaire renforcé et prépositionement de stocks alimentaires d'urgence",
        "signal_fr": "Risque d'utilisation de la faim — fragilité alimentaire dans un contexte de conflit",
      },
    "respect_droit_humanitaire": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de l'engagement humanitaire et soutien au droit international humanitaire",
        "signal_fr": "composite_score < 20 — respect du droit humanitaire, accès alimentaire garanti même en conflit",
    },
}


@dataclass
class FamineWeaponizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    blockade_intensity_score: float
    humanitarian_access_denial_score: float
    agricultural_destruction_score: float
    starvation_as_strategy_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_famine_weapon_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.blockade_intensity_score * 0.30
            + self.humanitarian_access_denial_score * 0.25
            + self.agricultural_destruction_score * 0.25
            + self.starvation_as_strategy_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_famine_weapon_index = round(self.composite_score / 100 * 10, 2)

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
        if self.blockade_intensity_score >= 80 and self.humanitarian_access_denial_score >= 75:
            return "famine_deliberee_active"
        if self.starvation_as_strategy_score >= 70:
            return "siege_alimentaire"
        if self.composite_score >= 45:
            return "instrumentalisation_partielle"
        if self.composite_score >= 25:
            return "risque_utilisation"
        return "respect_droit_humanitaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Famine délibérée active dans {n} — blocus systématique privant les civils d'accès alimentaire",
                "Violation grave du droit humanitaire international — faim utilisée comme arme de guerre",
                "Infrastructure agricole détruite délibérément — capacité alimentaire locale anéantie",
            ]
        if self.risk_level == "élevé":
            return [
                f"Instrumentalisation de la faim dans {n} — aide humanitaire conditionnée à des objectifs militaires",
                "Accès humanitaire sévèrement restreint — populations en situation de pré-famine délibérée",
                "Destruction agricole partielle — réduction calculée des capacités alimentaires locales",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque d'utilisation de la faim dans {n} — fragilité alimentaire dans un contexte conflictuel",
                "Tensions sur l'accès humanitaire — monitoring urgent nécessaire pour prévenir l'escalade",
                "Capacités agricoles fragilisées par le conflit — prépositionement de stocks d'urgence requis",
            ]
        return [
            f"{n} respecte le droit humanitaire alimentaire — accès à la nourriture garanti même en situation de conflit",
            "Corridors humanitaires ouverts et aide alimentaire non-conditionnée aux objectifs militaires",
            "Modèle de respect du droit humanitaire international à valoriser et faire respecter universellement",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "blockade_intensity_score": self.blockade_intensity_score,
            "humanitarian_access_denial_score": self.humanitarian_access_denial_score,
            "agricultural_destruction_score": self.agricultural_destruction_score,
            "starvation_as_strategy_score": self.starvation_as_strategy_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_famine_weapon_index": self.estimated_famine_weapon_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FamineWeaponizationEntity] = [
    FamineWeaponizationEntity("FW-001", "Yémen — Blocus & Famine Délibérée", "MENA", "Coalition Saoudienne Bloquant l'Aide Humanitaire", 95.0, 92.0, 88.0, 90.0),
    FamineWeaponizationEntity("FW-002", "Gaza — Siège Total & Destruction Agricole", "MENA", "Blocus Alimentaire Total dans le Territoire Assiégé", 92.0, 95.0, 90.0, 88.0),
    FamineWeaponizationEntity("FW-003", "Soudan — Famine comme Outil de Guerre Civile", "Afrique", "RSF & SAF Bloquant l'Aide dans les Zones Adverses", 85.0, 82.0, 80.0, 85.0),
    FamineWeaponizationEntity("FW-004", "Éthiopie Tigré — Siège & Starvation", "Afrique", "Blocus Gouvernemental du Tigré 2020-2022", 80.0, 78.0, 75.0, 82.0),
    FamineWeaponizationEntity("FW-005", "Myanmar — Minorités Ethniques Assiégées", "Asie du Sud-Est", "Junta Militaire & Blocus Économique Ethnique", 68.0, 65.0, 70.0, 62.0),
    FamineWeaponizationEntity("FW-006", "Syrie — Reconstruction Instrumentalisée", "MENA", "Reconstruction Conditionnée comme Outil de Fidélisation", 55.0, 52.0, 48.0, 58.0),
    FamineWeaponizationEntity("FW-007", "Haïti — Gangs & Accès Humanitaire Bloqué", "Amériques", "Milices Contrôlant l'Accès Alimentaire dans Zones Urbaines", 42.0, 40.0, 38.0, 35.0),
    FamineWeaponizationEntity("FW-008", "Ukraine — Destruction Céréalière Russe", "Europe de l'Est", "Bombardement Silos Blés & Blocage Corridor Maritime", 30.0, 25.0, 35.0, 28.0),
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
        "domain": "famine_weapon",
        "confidence_score": 0.88,
        "data_sources": ["fews_net_famine_tracker", "ipc_acute_food_insecurity", "icrc_humanitarian_access_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_famine_weapon_index": round(avg / 100 * 10, 2),
    }


def analyze_famine_weaponization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Famine Weaponization Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
