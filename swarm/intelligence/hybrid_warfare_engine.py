"""
Caelum Partners — Hybrid Warfare Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Détection et analyse des opérations de guerre hybride :
la fusion de la cyberguerre, des opérations informationnelles,
de la coercition économique et des actions militaires conventionnelles
en une stratégie grise unifiée et déniable.

La guerre hybride efface la frontière entre paix et guerre —
l'agresseur frappe sans déclaration, opère sous le seuil d'une réponse
conventionnelle, et nie toute implication.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "offensive_hybride_totale": {
        "severity_fr": "Critique",
        "action_fr": "Activation défenses hybrides multi-domaines et coordination OTAN/EU — réponse coordonnée sous 24h",
        "signal_fr": "cyber_intensity > 85 AND proxy_activity > 80 — offensive hybride totale en cours",
    },
    "campagne_grise_ciblee": {
        "severity_fr": "Critique",
        "action_fr": "Contre-mesures hybrides actives et désignation officielle de l'agresseur — réponse asymétrique",
        "signal_fr": "Opérations grises coordonnées cyber+info+coercition — cible stratégique sous pression",
    },
    "pression_hybride_elevee": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des défenses hybrides et surveillance multi-domaines intensifiée",
        "signal_fr": "Opérations hybrides identifiées mais sous le seuil de réponse conventionnelle",
    },
    "signaux_hybrides_detectes": {
        "severity_fr": "Modéré",
        "action_fr": "Surveillance hybride renforcée et préparation des contre-mesures préventives",
        "signal_fr": "Signaux d'opérations hybrides naissantes — attribution incertaine mais préoccupante",
    },
    "securite_hybride": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille hybride et entraînement des capacités de résilience",
        "signal_fr": "composite_score < 30 — environnement sécuritaire stable, activité hybride minimale",
    },
}


@dataclass
class HybridWarfareEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    cyber_intensity_score: float
    proxy_activity_score: float
    info_operations_score: float
    subthreshold_coercion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_hybrid_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.cyber_intensity_score * 0.30
            + self.proxy_activity_score * 0.25
            + self.info_operations_score * 0.25
            + self.subthreshold_coercion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_hybrid_index = round(self.composite_score / 100 * 10, 2)

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
        if self.cyber_intensity_score >= 85 and self.proxy_activity_score >= 80:
            return "offensive_hybride_totale"
        if self.info_operations_score >= 75 and self.subthreshold_coercion_score >= 70:
            return "campagne_grise_ciblee"
        if self.composite_score >= 45:
            return "pression_hybride_elevee"
        if self.composite_score >= 25:
            return "signaux_hybrides_detectes"
        return "securite_hybride"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Offensive hybride critique contre {n} — multi-domaines cyber+info+proxy",
                "Intensité cyber et activité proxy au-delà des seuils d'attribution",
                "Zone grise totale — attaque sans déclaration, déni plausible maintenu",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression hybride élevée sur {n} — opérations grises multi-vecteurs",
                "Campagnes informationnelles et cyber coordonnées identifiées",
                "Coercition sous-seuil progressive — escalade hybride probable",
            ]
        if self.risk_level == "modéré":
            return [
                f"Signaux hybrides modérés pour {n} — surveillance multi-domaines recommandée",
                "Activités suspectes cyber et informationnelles — attribution en cours",
                "Défenses hybrides en alerte préventive",
            ]
        return [
            f"{n} présente un profil de sécurité hybride favorable",
            "Activité cyber et proxy dans les normes — aucune opération grise détectée",
            "Résilience hybride confirmée — veille multi-domaines maintenue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cyber_intensity_score": self.cyber_intensity_score,
            "proxy_activity_score": self.proxy_activity_score,
            "info_operations_score": self.info_operations_score,
            "subthreshold_coercion_score": self.subthreshold_coercion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_hybrid_index": self.estimated_hybrid_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[HybridWarfareEntity] = [
    HybridWarfareEntity("HW-001", "Ukraine & Frontière Est-Européenne", "Europe de l'Est", "Zone de Conflit Hybride", 92.0, 88.0, 85.0, 82.0),
    HybridWarfareEntity("HW-002", "Mer de Chine Méridionale", "Asie-Pacifique", "Contestation Maritime Hybride", 82.0, 90.0, 75.0, 78.0),
    HybridWarfareEntity("HW-003", "Mer Baltique & Nordiques", "Europe du Nord", "Campagne Russe Hybride", 78.0, 72.0, 85.0, 68.0),
    HybridWarfareEntity("HW-004", "Afrique Sahélienne", "Afrique", "Présence Milices & Proxies", 60.0, 80.0, 65.0, 72.0),
    HybridWarfareEntity("HW-005", "Moyen-Orient Étendu", "MENA", "Opérations Proxy Régionales", 65.0, 75.0, 70.0, 60.0),
    HybridWarfareEntity("HW-006", "Balkans Occidentaux", "Europe Centrale", "Déstabilisation Graduelle", 48.0, 42.0, 52.0, 38.0),
    HybridWarfareEntity("HW-007", "Amérique Latine", "Amériques", "Influence Hybride Limitée", 30.0, 25.0, 35.0, 22.0),
    HybridWarfareEntity("HW-008", "Pacifique Sud", "Océanie", "Zone Relativement Stable", 12.0, 15.0, 18.0, 10.0),
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
        "domain": "hybridwar",
        "confidence_score": 0.81,
        "data_sources": ["nato_hybrid_tracker", "cyber_threat_intelligence", "proxy_activity_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_hybrid_index": round(avg / 100 * 10, 2),
    }


def analyze_hybrid_warfare() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Hybrid Warfare Engine — {r['total_entities']} zones, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
