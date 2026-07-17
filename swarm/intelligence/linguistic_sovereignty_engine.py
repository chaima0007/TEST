"""
Caelum Partners — Linguistic Sovereignty Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La disparition des langues comme perte stratégique et géopolitique :
sur les 7 000 langues du monde, la moitié est en voie d'extinction d'ici 2100.
Chaque langue qui disparaît emporte avec elle des systèmes de connaissance
irremplaçables — taxonomies écologiques, architectures conceptuelles, modes
de raisonnement qui n'existent nulle part ailleurs.

La souveraineté linguistique n'est pas un romantisme culturel — c'est
la résistance à l'homogénéisation cognitive du monde. Quand l'anglais
et le mandarin absorbent les espaces discursifs, c'est la diversité
épistémique de l'humanité qui s'effondre. La domination linguistique
est la forme la plus durable de colonialisme.

Risk levels (menace sur la souveraineté linguistique) :
  critique  → composite ≥ 60  (extinction linguistique imminente)
  élevé     → composite ≥ 40  (érosion linguistique accélérée)
  modéré    → composite ≥ 20  (pression linguistique significative)
  faible    → composite < 20  (vitalité linguistique préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "extinction_linguistique": {
        "severity_fr": "Critique",
        "action_fr": "Programme d'urgence de revitalisation — documentation, enseignement et transmission inter-générationnelle",
        "signal_fr": "speakers_collapse > 80 AND intergenerational_transmission_failure > 75 — extinction imminente",
    },
    "domination_coloniale_linguistique": {
        "severity_fr": "Critique",
        "action_fr": "Politiques linguistiques protectrices et décolonisation des espaces éducatifs et médiatiques",
        "signal_fr": "Domination linguistique coloniale — langues autochtones marginalisées par les politiques étatiques",
    },
    "erosion_acceleree": {
        "severity_fr": "Élevé",
        "action_fr": "Politiques d'immersion linguistique et protection des espaces de transmission naturelle",
        "signal_fr": "Érosion linguistique accélérée — jeunes générations abandonnant la langue ancestrale",
    },
    "pression_linguistique": {
        "severity_fr": "Modéré",
        "action_fr": "Politiques de soutien à la vitalité linguistique et reconnaissance officielle des langues minoritaires",
        "signal_fr": "Pression linguistique — concurrence avec langue dominante mais transmission encore active",
    },
    "vitalite_preservee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des politiques de vitalité linguistique et documentation proactive du patrimoine",
        "signal_fr": "composite_score < 20 — vitalité linguistique préservée, transmission intergénérationnelle active",
    },
}


@dataclass
class LinguisticSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    speakers_collapse_score: float
    intergenerational_transmission_failure_score: float
    digital_language_exclusion_score: float
    colonial_language_dominance_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_linguistic_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.speakers_collapse_score * 0.30
            + self.intergenerational_transmission_failure_score * 0.25
            + self.digital_language_exclusion_score * 0.25
            + self.colonial_language_dominance_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_linguistic_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.speakers_collapse_score >= 80 and self.intergenerational_transmission_failure_score >= 75:
            return "extinction_linguistique"
        if self.colonial_language_dominance_score >= 70:
            return "domination_coloniale_linguistique"
        if self.composite_score >= 45:
            return "erosion_acceleree"
        if self.composite_score >= 25:
            return "pression_linguistique"
        return "vitalite_preservee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Extinction linguistique imminente pour {n} — dernier locuteurs âgés, aucune transmission aux jeunes",
                "Perte irréversible de systèmes de connaissance — taxonomies écologiques et architectures conceptuelles",
                "Domination de la langue coloniale effaçant l'identité culturelle et la souveraineté épistémique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Érosion linguistique accélérée dans {n} — jeunes générations migrant vers la langue dominante",
                "Exclusion numérique — langue absente des plateformes digitales et IA, accélérant l'abandon",
                "Politique linguistique insuffisante face à la pression économique vers l'assimilation",
            ]
        if self.risk_level == "modéré":
            return [
                f"Pression linguistique significative dans {n} — concurrence avec langue dominante en cours",
                "Transmission intergénérationnelle fragilisée mais encore active dans contextes familiaux",
                "Présence numérique limitée — renforcement des espaces digitaux nécessaire pour la survie",
            ]
        return [
            f"{n} préserve sa vitalité linguistique — transmission intergénérationnelle active et politique de soutien",
            "Diversité linguistique maintenue — modèle de coexistence entre langues locales et globales",
            "Leadership mondial sur la protection du patrimoine linguistique et de la souveraineté culturelle",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "speakers_collapse_score": self.speakers_collapse_score,
            "intergenerational_transmission_failure_score": self.intergenerational_transmission_failure_score,
            "digital_language_exclusion_score": self.digital_language_exclusion_score,
            "colonial_language_dominance_score": self.colonial_language_dominance_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_linguistic_risk_index": self.estimated_linguistic_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[LinguisticSovereigntyEntity] = [
    LinguisticSovereigntyEntity("LS-001", "Langues Autochtones Australie", "Océanie", "250 Langues Aborigènes en Extinction Terminale", 95.0, 92.0, 90.0, 88.0),
    LinguisticSovereigntyEntity("LS-002", "Amazonie — Langues des Peuples Premiers", "Amériques", "400+ Langues Amazoniennes sous Pression Déforestation", 90.0, 88.0, 85.0, 92.0),
    LinguisticSovereigntyEntity("LS-003", "Afrique Subsaharienne — Langues Bantoues", "Afrique", "Français/Anglais Colonial Effaçant 2000 Langues", 75.0, 72.0, 80.0, 88.0),
    LinguisticSovereigntyEntity("LS-004", "Sibérie & Arctique — Langues Autochtones", "Russie/Arctique", "Russification & Exodus Rural Tuant les Langues", 78.0, 80.0, 78.0, 72.0),
    LinguisticSovereigntyEntity("LS-005", "Asie du Sud-Est — Minorités Linguistiques", "Asie du Sud-Est", "Assimilation Forcée aux Langues Nationales Officielles", 62.0, 65.0, 70.0, 60.0),
    LinguisticSovereigntyEntity("LS-006", "Europe — Langues Régionales", "Europe", "Occitan, Breton, Basque — Résistance vs Homogénéisation", 40.0, 38.0, 35.0, 30.0),
    LinguisticSovereigntyEntity("LS-007", "Québec & Catalogne — Langues en Résistance", "Amériques/Europe", "Politiques Actives de Préservation et Revendication", 22.0, 18.0, 25.0, 15.0),
    LinguisticSovereigntyEntity("LS-008", "Finlande & Pays Basque — Vitalité Exemplaire", "Europe", "Politiques d'Immersion et Bilinguisme Officiel", 8.0, 5.0, 12.0, 6.0),
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
        "domain": "linguistic_sovr",
        "confidence_score": 0.81,
        "data_sources": ["ethnologue_language_status", "unesco_endangered_languages", "digital_language_inclusion_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_linguistic_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_linguistic_sovereignty() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Linguistic Sovereignty Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
