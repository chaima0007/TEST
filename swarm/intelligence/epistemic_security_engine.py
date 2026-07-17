"""
Caelum Partners — Epistemic Security Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La sécurité épistémique mesure la capacité d'une société à maintenir
une réalité partagée face aux attaques informationnelles, à la désinformation
industrielle et à la fragmentation de l'écosystème médiatique.

Quand la réalité partagée s'effondre, la démocratie devient impossible —
on ne peut pas débattre de politiques publiques si les faits eux-mêmes
sont contestés. L'attaque épistémique est la guerre du XXIe siècle.

Risk levels :
  critique  → composite ≥ 60  (chaos épistémique)
  élevé     → composite ≥ 40  (guerre narrative active)
  modéré    → composite ≥ 20  (brouillard informationnel)
  faible    → composite < 20  (résilience épistémique)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "chaos_epistemique_total": {
        "severity_fr": "Critique",
        "action_fr": "Contre-offensives épistémiques d'urgence — éducation aux médias et régulation des plateformes",
        "signal_fr": "disinformation > 80 AND reality_consensus_deficit > 75 — effondrement de la réalité partagée",
    },
    "fracture_cognitive": {
        "severity_fr": "Critique",
        "action_fr": "Reconstruction du consensus factuel — institutions de vérification et médias publics renforcés",
        "signal_fr": "Fracture cognitive critique — groupes vivant dans des réalités parallèles incompatibles",
    },
    "guerre_narrative": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des capacités de fact-checking et de littératie médiatique",
        "signal_fr": "Guerre narrative active — manipulation de l'information à grande échelle détectée",
    },
    "brouillard_informationnel": {
        "severity_fr": "Modéré",
        "action_fr": "Amélioration de la transparence algorithmique et promotion de sources fiables",
        "signal_fr": "Brouillard informationnel modéré — confusion et saturation sans orchestration claire",
    },
    "resilience_epistemique": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des programmes de littératie médiatique et de vérification des faits",
        "signal_fr": "composite_score < 20 — résilience épistémique confirmée, réalité partagée préservée",
    },
}


@dataclass
class EpistemicSecurityEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    disinformation_saturation_score: float
    reality_consensus_deficit_score: float
    media_ecosystem_fragmentation_score: float
    epistemic_vulnerability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_epistemic_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.disinformation_saturation_score * 0.30
            + self.reality_consensus_deficit_score * 0.25
            + self.media_ecosystem_fragmentation_score * 0.25
            + self.epistemic_vulnerability_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_epistemic_index = round(self.composite_score / 100 * 10, 2)

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
        if self.disinformation_saturation_score >= 80 and self.reality_consensus_deficit_score >= 75:
            return "chaos_epistemique_total"
        if self.reality_consensus_deficit_score >= 70:
            return "fracture_cognitive"
        if self.composite_score >= 45:
            return "guerre_narrative"
        if self.composite_score >= 25:
            return "brouillard_informationnel"
        return "resilience_epistemique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Chaos épistémique critique dans {n} — réalité partagée en effondrement",
                "Désinformation industrielle saturant l'espace informationnel public",
                "Fragmentation cognitive irréversible — bulles de réalité incompatibles coexistant",
            ]
        if self.risk_level == "élevé":
            return [
                f"Guerre narrative intense dans {n} — manipulation de l'information à grande échelle",
                "Écosystème médiatique fragmenté — algorithmes amplifiant les biais cognitifs",
                "Vulnérabilité épistémique élevée aux attaques de désinformation coordonnées",
            ]
        if self.risk_level == "modéré":
            return [
                f"Brouillard informationnel modéré dans {n} — saturation sans orchestration claire",
                "Littératie médiatique insuffisante face à la complexité de l'espace info",
                "Signaux de fragmentation narrative à surveiller",
            ]
        return [
            f"{n} maintient une résilience épistémique solide — réalité partagée préservée",
            "Littératie médiatique et fact-checking opérationnels",
            "Écosystème informationnel relativement sain — veille épistémique maintenue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "disinformation_saturation_score": self.disinformation_saturation_score,
            "reality_consensus_deficit_score": self.reality_consensus_deficit_score,
            "media_ecosystem_fragmentation_score": self.media_ecosystem_fragmentation_score,
            "epistemic_vulnerability_score": self.epistemic_vulnerability_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_epistemic_index": self.estimated_epistemic_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[EpistemicSecurityEntity] = [
    EpistemicSecurityEntity("ES-001", "Russie — Machine de Propagande", "Europe de l'Est", "Désinformation d'État Systémique", 95.0, 88.0, 85.0, 90.0),
    EpistemicSecurityEntity("ES-002", "Myanmar — Génocide Algorithmique", "Asie du Sud-Est", "Manipulation Plateforme & Violence", 88.0, 85.0, 82.0, 80.0),
    EpistemicSecurityEntity("ES-003", "États-Unis — Post-Vérité", "Amérique du Nord", "Polarisation Épistémique Extrême", 82.0, 80.0, 88.0, 75.0),
    EpistemicSecurityEntity("ES-004", "Espac Numérique Global (TikTok/X)", "Cyberespace", "Algorithmes & Bulles Cognitives", 85.0, 78.0, 90.0, 72.0),
    EpistemicSecurityEntity("ES-005", "Brésil — WhatsApp & Désinformation", "Amériques", "Crise Informationnelle Endémique", 68.0, 62.0, 65.0, 58.0),
    EpistemicSecurityEntity("ES-006", "Philippines — Ère Duterte", "Asie du Sud-Est", "Désinformation Politique Organisée", 62.0, 58.0, 60.0, 55.0),
    EpistemicSecurityEntity("ES-007", "Europe Occidentale — DSA & Régulation", "Europe", "Résilience Institutionnelle Partielle", 35.0, 30.0, 38.0, 28.0),
    EpistemicSecurityEntity("ES-008", "Nordiques & Estonie — Littératie Max", "Europe du Nord", "Résilience Épistémique Exemplaire", 12.0, 10.0, 14.0, 8.0),
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
        "domain": "epistemic",
        "confidence_score": 0.77,
        "data_sources": ["reuters_institute_digital_news", "disinfo_tracker", "cognitive_security_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_epistemic_index": round(avg / 100 * 10, 2),
    }


def analyze_epistemic_security() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Epistemic Security Engine — {r['total_entities']} zones, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
