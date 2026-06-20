"""
Caelum Partners — Shadow Economy Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'économie parallèle comme indicateur de défaillance de gouvernance :
quand le secteur informel dépasse 50% du PIB, quand l'évasion fiscale
est systémique et la corruption un lubrifiant indispensable, l'État
formel devient une façade derrière laquelle opère une économie réelle
non-régulée, non-taxée et potentiellement criminelle.

L'économie de l'ombre n'est pas qu'une question fiscale — c'est
la mesure du divorce entre l'État et ses citoyens.

Risk levels (intensité de l'économie parallèle) :
  critique  → composite ≥ 60  (dualisme économique total)
  élevé     → composite ≥ 40  (évasion systémique avancée)
  modéré    → composite ≥ 20  (secteur informel significatif)
  faible    → composite < 20  (économie formelle dominante)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "economie_parallele_totale": {
        "severity_fr": "Critique",
        "action_fr": "Réforme fiscale radicale et simplification administrative — formalisation incitative urgente",
        "signal_fr": "informal_sector > 80 AND corruption_lubricant > 75 — économie parallèle totale",
    },
    "evasion_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Lutte anti-corruption systémique et modernisation de l'administration fiscale",
        "signal_fr": "Évasion fiscale systémique — secteur informel structurant l'économie nationale",
    },
    "dualisme_economique": {
        "severity_fr": "Élevé",
        "action_fr": "Politique de formalisation progressive et protection sociale incitant à l'intégration",
        "signal_fr": "Dualisme économique avancé — deux économies parallèles coexistant sans convergence",
    },
    "tensions_formelles": {
        "severity_fr": "Modéré",
        "action_fr": "Réformes fiscales simplificatrices et réduction des barrières à la formalisation",
        "signal_fr": "Tensions entre secteur formel et informel — équilibre fragile à consolider",
    },
    "economie_formelle": {
        "severity_fr": "Faible",
        "action_fr": "Maintien du cadre fiscal équitable et vigilance sur les nouvelles formes d'économie grise",
        "signal_fr": "composite_score < 20 — économie formelle dominante, compliance fiscale élevée",
    },
}


@dataclass
class ShadowEconomyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    informal_sector_dominance_score: float
    tax_evasion_systemic_score: float
    corruption_lubricant_score: float
    regulatory_arbitrage_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_shadow_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.informal_sector_dominance_score * 0.30
            + self.tax_evasion_systemic_score * 0.25
            + self.corruption_lubricant_score * 0.25
            + self.regulatory_arbitrage_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_shadow_index = round(self.composite_score / 100 * 10, 2)

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
        if self.informal_sector_dominance_score >= 80 and self.corruption_lubricant_score >= 75:
            return "economie_parallele_totale"
        if self.informal_sector_dominance_score >= 65:
            return "evasion_systemique"
        if self.composite_score >= 45:
            return "dualisme_economique"
        if self.composite_score >= 25:
            return "tensions_formelles"
        return "economie_formelle"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Économie parallèle totale dans {n} — secteur informel dominant l'économie réelle",
                "Corruption structurelle comme lubrifiant indispensable des transactions économiques",
                "Divorce État-économie — administration fiscale contournée à grande échelle",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dualisme économique avancé dans {n} — deux économies coexistant sans convergence",
                "Évasion fiscale systémique compromettant les finances publiques",
                "Arbitrage réglementaire structurel — acteurs économiques évitant le cadre formel",
            ]
        if self.risk_level == "modéré":
            return [
                f"Secteur informel significatif dans {n} — tensions entre formalité et informalité",
                "Évasion fiscale partielle — réformes simplificatrices nécessaires",
                "Barrières à la formalisation à réduire pour intégrer l'économie parallèle",
            ]
        return [
            f"{n} maintient une économie formelle dominante — compliance fiscale élevée",
            "Administration fiscale efficace et barrières à la formalisation basses",
            "Modèle de gouvernance économique à préserver et exporter",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "informal_sector_dominance_score": self.informal_sector_dominance_score,
            "tax_evasion_systemic_score": self.tax_evasion_systemic_score,
            "corruption_lubricant_score": self.corruption_lubricant_score,
            "regulatory_arbitrage_score": self.regulatory_arbitrage_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_shadow_index": self.estimated_shadow_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ShadowEconomyEntity] = [
    ShadowEconomyEntity("SE-001", "Afrique Subsaharienne Moyenne", "Afrique", "Informalité Structurelle >60% PIB", 90.0, 85.0, 88.0, 82.0),
    ShadowEconomyEntity("SE-002", "Myanmar & Cambodge", "Asie du Sud-Est", "Économie Grise & Trafics Légalisés", 85.0, 80.0, 88.0, 78.0),
    ShadowEconomyEntity("SE-003", "Venezuela & Bolivie", "Amériques", "Marché Noir Structurant l'Économie", 82.0, 85.0, 80.0, 75.0),
    ShadowEconomyEntity("SE-004", "Nigeria & Cameroun", "Afrique", "Informalité Commerciale Totale", 80.0, 78.0, 82.0, 72.0),
    ShadowEconomyEntity("SE-005", "Mexique — Économie Cartel", "Amériques", "Pénétration Criminelle des Marchés", 65.0, 62.0, 68.0, 60.0),
    ShadowEconomyEntity("SE-006", "Russie Post-Soviétique", "Europe de l'Est", "Oligarchie & Évasion Structurelle", 55.0, 58.0, 60.0, 52.0),
    ShadowEconomyEntity("SE-007", "Italie du Sud & Grèce", "Europe", "Économie Grise Méditerranéenne", 38.0, 42.0, 35.0, 30.0),
    ShadowEconomyEntity("SE-008", "Suisse & Pays-Bas", "Europe du Nord", "Économie Formelle Exemplaire", 10.0, 8.0, 6.0, 12.0),
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
        "domain": "shadow_econ",
        "confidence_score": 0.72,
        "data_sources": ["ilo_informal_economy", "world_bank_informality", "tax_justice_network"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_shadow_index": round(avg / 100 * 10, 2),
    }


def analyze_shadow_economy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Shadow Economy Engine — {r['total_entities']} zones, avg informalité: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
