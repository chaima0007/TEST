"""
Caelum Partners — Narrative Sovereignty Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La souveraineté narrative comme dimension fondamentale du pouvoir géopolitique :
qui contrôle les récits dominants contrôle les perceptions, les désirs,
les identités et in fine les choix collectifs des populations mondiales.

Hollywood, les GAFA, les agences de presse, les séries et les algorithmes
de recommandation sont les nouvelles armes narratives du XXIe siècle.
Ceux qui ne produisent pas de récits propres sont colonisés narrativement.

Score élevé = DÉFICIT de souveraineté narrative (dépendance aux récits étrangers).

Risk levels :
  critique  → composite ≥ 60  (colonisation narrative totale)
  élevé     → composite ≥ 40  (dépendance culturelle avancée)
  modéré    → composite ≥ 20  (tensions narratives)
  faible    → composite < 20  (souveraineté narrative consolidée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "colonisation_narrative": {
        "severity_fr": "Critique",
        "action_fr": "Stratégie narrative souveraine d'urgence — industrie culturelle nationale et contre-récits",
        "signal_fr": "narrative_dependency > 80 AND cultural_deficit > 75 — colonisation narrative critique",
    },
    "dependance_culturelle_structurelle": {
        "severity_fr": "Critique",
        "action_fr": "Investissement massif dans les industries créatives et l'infrastructure narrative nationale",
        "signal_fr": "Dépendance culturelle structurelle — identité narrative sous influence étrangère totale",
    },
    "guerre_recits": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement de la production narrative et diffusion des contre-récits sur les plateformes mondiales",
        "signal_fr": "Guerre des récits active — compétition narrative sans souveraineté culturelle suffisante",
    },
    "tension_narrative": {
        "severity_fr": "Modéré",
        "action_fr": "Soutien aux industries culturelles nationales et développement du soft power narratif",
        "signal_fr": "Tensions narratives modérées — influence étrangère partielle sur les récits nationaux",
    },
    "souverainete_narrative": {
        "severity_fr": "Faible",
        "action_fr": "Maintien et expansion du pouvoir narratif — rayonnement culturel mondial responsable",
        "signal_fr": "composite_score < 20 — souveraineté narrative consolidée, puissance culturelle rayonnante",
    },
}


@dataclass
class NarrativeSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    narrative_dependency_score: float
    counter_narrative_vulnerability_score: float
    cultural_infrastructure_deficit_score: float
    narrative_production_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_narrative_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.narrative_dependency_score * 0.30
            + self.counter_narrative_vulnerability_score * 0.25
            + self.cultural_infrastructure_deficit_score * 0.25
            + self.narrative_production_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_narrative_index = round(self.composite_score / 100 * 10, 2)

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
        if self.narrative_dependency_score >= 80 and self.cultural_infrastructure_deficit_score >= 75:
            return "colonisation_narrative"
        if self.narrative_dependency_score >= 65:
            return "dependance_culturelle_structurelle"
        if self.composite_score >= 45:
            return "guerre_recits"
        if self.composite_score >= 25:
            return "tension_narrative"
        return "souverainete_narrative"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Colonisation narrative critique de {n} — récits identitaires sous contrôle étranger",
                "Absence d'industrie culturelle nationale compétitive — dépendance aux contenus importés",
                "Vulnérabilité aux contre-récits et à la manipulation narrative étrangère",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dépendance culturelle avancée dans {n} — influence narrative étrangère dominante",
                "Infrastructure narrative insuffisante — production locale dépassée par l'import culturel",
                "Guerre des récits défavorable — difficulté à faire rayonner les valeurs nationales",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions narratives modérées dans {n} — influence étrangère partielle sur les récits",
                "Industries créatives en développement mais compétitivité mondiale encore limitée",
                "Soft power narratif en construction — potentiel de souveraineté à consolider",
            ]
        return [
            f"{n} jouit d'une souveraineté narrative consolidée — puissance culturelle rayonnante",
            "Production narrative exportée mondialement — capacité à fixer les récits dominants",
            "Infrastructure culturelle robuste — résistance naturelle aux contre-récits étrangers",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "narrative_dependency_score": self.narrative_dependency_score,
            "counter_narrative_vulnerability_score": self.counter_narrative_vulnerability_score,
            "cultural_infrastructure_deficit_score": self.cultural_infrastructure_deficit_score,
            "narrative_production_gap_score": self.narrative_production_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_narrative_index": self.estimated_narrative_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[NarrativeSovereigntyEntity] = [
    NarrativeSovereigntyEntity("NR-001", "Afrique Francophone", "Afrique", "Colonisation Narrative Totale", 92.0, 88.0, 90.0, 85.0),
    NarrativeSovereigntyEntity("NR-002", "MENA — Dépendance Narrative", "Moyen-Orient", "Récits Occidentaux Dominants", 85.0, 82.0, 88.0, 80.0),
    NarrativeSovereigntyEntity("NR-003", "Asie du Sud-Est", "Asie", "Sandwich USA/Chine Narratif", 80.0, 78.0, 82.0, 75.0),
    NarrativeSovereigntyEntity("NR-004", "Amérique Latine", "Amériques", "Soft Power Américain Dominant", 72.0, 68.0, 70.0, 65.0),
    NarrativeSovereigntyEntity("NR-005", "Inde — Bollywood & Résistance", "Asie du Sud", "Puissance Narrative Émergente", 45.0, 42.0, 48.0, 40.0),
    NarrativeSovereigntyEntity("NR-006", "Europe — Dépendance GAFA", "Europe", "Récits Technologiques US Dominants", 38.0, 35.0, 42.0, 32.0),
    NarrativeSovereigntyEntity("NR-007", "Russie — Narratif Alternatif", "Europe de l'Est", "Contre-Récit Mondial Partiel", 25.0, 22.0, 28.0, 20.0),
    NarrativeSovereigntyEntity("NR-008", "USA & Chine — Duopole Narratif", "Global", "Souveraineté Narrative Absolue", 5.0, 8.0, 4.0, 6.0),
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
        "domain": "narrative",
        "confidence_score": 0.76,
        "data_sources": ["cultural_power_index", "soft_power_tracker", "narrative_influence_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_narrative_index": round(avg / 100 * 10, 2),
    }


def analyze_narrative_sovereignty() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Narrative Sovereignty Engine — {r['total_entities']} zones, avg déficit: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
