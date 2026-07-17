"""
Caelum Partners — Attention Economy Disruption Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'économie de l'attention comme nouvelle ressource géopolitique :
les plateformes numériques capturent et monétisent l'attention humaine
via des algorithmes d'optimisation de l'engagement — transformant
la cognition collective en vecteur de manipulation politique et commerciale.

Celui qui contrôle l'attention contrôle les perceptions, les comportements
et in fine les votes et les choix économiques des populations.

Risk levels (disruption attentionnelle) :
  critique  → composite ≥ 60  (colonisation cognitive)
  élevé     → composite ≥ 40  (fragmentation attentionnelle avancée)
  modéré    → composite ≥ 20  (stress informationnel)
  faible    → composite < 20  (hygiène numérique préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "colonisation_cognitive": {
        "severity_fr": "Critique",
        "action_fr": "Régulation d'urgence des plateformes — design éthique et droits numériques fondamentaux",
        "signal_fr": "platform_capture > 80 AND algorithmic_manipulation > 75 — colonisation cognitive en cours",
    },
    "addiction_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Interdiction des dark patterns addictifs et régulation du temps d'écran par plateformes",
        "signal_fr": "Addiction algorithmique systémique — modification comportementale à grande échelle confirmée",
    },
    "fragmentation_attentionnelle": {
        "severity_fr": "Élevé",
        "action_fr": "Promotion de l'hygiène numérique et régulation de la publicité comportementale",
        "signal_fr": "Fragmentation attentionnelle avancée — capacité de concentration collective dégradée",
    },
    "stress_informationnel": {
        "severity_fr": "Modéré",
        "action_fr": "Programmes de littératie numérique et promotion d'alternatives éthiques",
        "signal_fr": "Stress informationnel modéré — surcharge cognitive sans capture totale",
    },
    "hygiene_numerique": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des pratiques d'hygiène numérique et vigilance sur les nouvelles plateformes",
        "signal_fr": "composite_score < 20 — hygiène numérique préservée, autonomie cognitive maintenue",
    },
}


@dataclass
class AttentionEconomyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    platform_capture_score: float
    algorithmic_manipulation_score: float
    cognitive_bandwidth_erosion_score: float
    behavioral_modification_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_attention_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.platform_capture_score * 0.30
            + self.algorithmic_manipulation_score * 0.25
            + self.cognitive_bandwidth_erosion_score * 0.25
            + self.behavioral_modification_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_attention_index = round(self.composite_score / 100 * 10, 2)

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
        if self.platform_capture_score >= 80 and self.algorithmic_manipulation_score >= 75:
            return "colonisation_cognitive"
        if self.algorithmic_manipulation_score >= 70:
            return "addiction_systematique"
        if self.composite_score >= 45:
            return "fragmentation_attentionnelle"
        if self.composite_score >= 25:
            return "stress_informationnel"
        return "hygiene_numerique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Colonisation cognitive critique dans {n} — autonomie attentionnelle compromise",
                "Algorithmes d'optimisation de l'engagement modifiant les comportements à grande échelle",
                "Capture de l'attention par les plateformes — infrastructure de manipulation opérationnelle",
            ]
        if self.risk_level == "élevé":
            return [
                f"Fragmentation attentionnelle élevée dans {n} — capacité de concentration dégradée",
                "Addiction algorithmique normalisée — dark patterns omniprésents",
                "Érosion de la bande passante cognitive collective — vulnérabilité à la manipulation",
            ]
        if self.risk_level == "modéré":
            return [
                f"Stress informationnel modéré dans {n} — surcharge sans capture totale",
                "Tensions entre autonomie numérique et capture attentionnelle",
                "Conscience croissante des risques — régulation partielle en cours",
            ]
        return [
            f"{n} préserve une hygiène numérique satisfaisante — autonomie cognitive maintenue",
            "Régulation efficace des plateformes et littératie numérique développée",
            "Modèle de souveraineté attentionnelle à étudier et diffuser",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "platform_capture_score": self.platform_capture_score,
            "algorithmic_manipulation_score": self.algorithmic_manipulation_score,
            "cognitive_bandwidth_erosion_score": self.cognitive_bandwidth_erosion_score,
            "behavioral_modification_score": self.behavioral_modification_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_attention_index": self.estimated_attention_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AttentionEconomyEntity] = [
    AttentionEconomyEntity("AE-001", "Espace Numérique Global (Meta/TikTok)", "Cyberespace", "Plateformes Prédatrices de l'Attention", 95.0, 92.0, 88.0, 90.0),
    AttentionEconomyEntity("AE-002", "Adolescents Mondiaux — Crise Mentale", "Global", "Génération Z & Santé Mentale Numérique", 90.0, 85.0, 88.0, 82.0),
    AttentionEconomyEntity("AE-003", "États-Unis — Empire de l'Attention", "Amérique du Nord", "Silicon Valley & Capture Cognitive", 88.0, 80.0, 82.0, 78.0),
    AttentionEconomyEntity("AE-004", "Chine — Export d'Attention (TikTok)", "Asie", "Géopolitique de l'Attention Numérique", 82.0, 78.0, 75.0, 80.0),
    AttentionEconomyEntity("AE-005", "Inde & Asie du Sud-Est", "Asie", "Disruption Numérique à Grande Vitesse", 65.0, 60.0, 62.0, 55.0),
    AttentionEconomyEntity("AE-006", "Europe — GDPR & DSA Partiels", "Europe", "Régulation vs Capture Attentionnelle", 50.0, 45.0, 48.0, 42.0),
    AttentionEconomyEntity("AE-007", "Corée du Sud — Conscience Numérique", "Asie du Nord-Est", "Hygiène Numérique en Construction", 35.0, 28.0, 32.0, 25.0),
    AttentionEconomyEntity("AE-008", "Finlande & Pays-Bas — Modèle Numérique", "Europe du Nord", "Souveraineté Attentionnelle Exemplaire", 15.0, 12.0, 14.0, 10.0),
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
        "domain": "attention",
        "confidence_score": 0.75,
        "data_sources": ["screen_time_data", "attention_economy_research", "digital_wellbeing_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_attention_index": round(avg / 100 * 10, 2),
    }


def analyze_attention_economy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Attention Economy Engine — {r['total_entities']} zones, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
