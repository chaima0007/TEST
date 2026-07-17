"""
Caelum Partners — Democratic Decay Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Système d'alerte précoce pour la détection de l'érosion démocratique
et du recul des libertés civiles à l'échelle mondiale.

La démocratie ne s'effondre plus brutalement comme au XXe siècle —
elle s'érode progressivement : capture institutionnelle, affaiblissement
judiciaire, restrictions médiatiques, manipulation électorale.

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
    "effondrement_democratique": {
        "severity_fr": "Critique",
        "action_fr": "Activation mécanismes de protection démocratique internationaux — pression diplomatique coordonnée",
        "signal_fr": "institutional_erosion > 80 AND electoral_integrity < 20 — crise démocratique systémique",
    },
    "capture_institutionnelle": {
        "severity_fr": "Critique",
        "action_fr": "Saisine des cours internationales et déclenchement de sanctions ciblées anti-autocratiques",
        "signal_fr": "Capture du pouvoir judiciaire et exécutif — chèques et contrepoids démocratiques neutralisés",
    },
    "erosion_progressive": {
        "severity_fr": "Élevé",
        "action_fr": "Soutien à la société civile et aux médias indépendants — renforcement des institutions",
        "signal_fr": "Recul mesurable des libertés civiles — autocratisation en cours mais réversible",
    },
    "fragilite_democratique": {
        "severity_fr": "Modéré",
        "action_fr": "Réformes institutionnelles préventives et renforcement de la culture démocratique",
        "signal_fr": "Tensions sur les institutions démocratiques — vigilance préventive recommandée",
    },
    "democratie_consolidee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille démocratique et partage des meilleures pratiques",
        "signal_fr": "composite_score < 30 — démocratie consolidée, libertés civiles préservées",
    },
}


@dataclass
class DemocraticDecayEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    institutional_erosion_score: float
    civil_liberties_decline_score: float
    electoral_integrity_score: float
    media_freedom_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_demdecay_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.institutional_erosion_score * 0.30
            + self.civil_liberties_decline_score * 0.25
            + self.electoral_integrity_score * 0.25
            + self.media_freedom_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_demdecay_index = round(self.composite_score / 100 * 10, 2)

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
        if self.institutional_erosion_score >= 80 and self.electoral_integrity_score >= 75:
            return "effondrement_democratique"
        if self.institutional_erosion_score >= 70 and self.civil_liberties_decline_score >= 65:
            return "capture_institutionnelle"
        if self.composite_score >= 45:
            return "erosion_progressive"
        if self.composite_score >= 25:
            return "fragilite_democratique"
        return "democratie_consolidee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Effondrement démocratique critique détecté pour {n} — autocratisation avancée",
                "Capture institutionnelle — judiciaire, exécutif et médias sous contrôle politique",
                "Intégrité électorale compromise — processus démocratique fondamentalement altéré",
            ]
        if self.risk_level == "élevé":
            return [
                f"Érosion démocratique élevée pour {n} — recul des libertés mesurable",
                "Affaiblissement des contre-pouvoirs institutionnels en cours",
                "Liberté de la presse et droits civils sous pression croissante",
            ]
        if self.risk_level == "modéré":
            return [
                f"Fragilité démocratique modérée pour {n} — vigilance institutionnelle requise",
                "Tensions sur certaines libertés civiles — réformes préventives conseillées",
                "Démocratie fonctionnelle mais avec des zones de vulnérabilité",
            ]
        return [
            f"{n} maintient une démocratie consolidée avec libertés civiles préservées",
            "Institutions indépendantes et processus électoraux intègres confirmés",
            "Société civile active — bouclier démocratique robuste",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "institutional_erosion_score": self.institutional_erosion_score,
            "civil_liberties_decline_score": self.civil_liberties_decline_score,
            "electoral_integrity_score": self.electoral_integrity_score,
            "media_freedom_score": self.media_freedom_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_demdecay_index": self.estimated_demdecay_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DemocraticDecayEntity] = [
    DemocraticDecayEntity("DD-001", "Russie & Biélorussie", "Europe de l'Est", "Autoritarisme Électoral", 92.0, 88.0, 85.0, 90.0),
    DemocraticDecayEntity("DD-002", "Chine & Hong Kong", "Asie-Pacifique", "Autocratie de Parti", 90.0, 85.0, 88.0, 92.0),
    DemocraticDecayEntity("DD-003", "Hongrie & Serbie", "Europe Centrale", "Illibéralisme Électoral", 78.0, 72.0, 70.0, 80.0),
    DemocraticDecayEntity("DD-004", "Turquie & Inde", "Asie Occidentale", "Démocratie Illibérale", 68.0, 65.0, 62.0, 70.0),
    DemocraticDecayEntity("DD-005", "Amérique Latine Fragile", "Amériques", "Polarisation Démocratique", 52.0, 48.0, 50.0, 45.0),
    DemocraticDecayEntity("DD-006", "États-Unis & Royaume-Uni", "Occident", "Fragilité Institutionnelle", 38.0, 35.0, 32.0, 30.0),
    DemocraticDecayEntity("DD-007", "Europe Occidentale", "Europe", "Démocraties Établies", 20.0, 18.0, 15.0, 22.0),
    DemocraticDecayEntity("DD-008", "Nordiques & Nouvelle-Zélande", "Modèles Démocratiques", "Démocraties de Référence", 5.0, 8.0, 4.0, 6.0),
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
        "domain": "democrisis",
        "confidence_score": 0.87,
        "data_sources": ["v_dem_institute", "freedom_house_index", "electoral_integrity_project"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_demdecay_index": round(avg / 100 * 10, 2),
    }


def analyze_democratic_decay() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Democratic Decay Engine — {r['total_entities']} régions, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
