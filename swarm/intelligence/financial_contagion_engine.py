"""
Caelum Partners — Financial Contagion Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La contagion financière comme risque systémique global : dans un système
financier hyper-interconnecté, la défaillance d'une institution peut déclencher
une réaction en chaîne qui traverse frontières et marchés en quelques heures.
Lehman Brothers a mis 72 heures pour contaminer l'économie mondiale.

L'interconnexion financière est le paradoxe de la mondialisation :
elle crée l'efficience et la fragilité simultanément. Les nœuds
systemically important — les banques trop grandes pour faire faillite,
les marchés de dérivés opaques, les corridors du dollar — sont les
vecteurs de transmission d'une crise qui peut surgir de n'importe
quel point du réseau et frapper simultanément partout.

Risk levels (vulnérabilité à la contagion financière systémique) :
  critique  → composite ≥ 60  (contagion systémique imminente)
  élevé     → composite ≥ 40  (vulnérabilité financière sévère)
  modéré    → composite ≥ 20  (risques de contagion modérés)
  faible    → composite < 20  (résilience financière systémique)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "contagion_systemique_imminente": {
        "severity_fr": "Critique",
        "action_fr": "Mécanismes de résolution d'urgence et filets de sécurité multilatéraux activés immédiatement",
        "signal_fr": "interconnection_density > 80 AND leverage_excess > 75 — contagion systémique imminente",
    },
    "noeud_fragile_critique": {
        "severity_fr": "Critique",
        "action_fr": "Résolution ordonnée des institutions too-big-to-fail et réduction du levier systémique",
        "signal_fr": "Nœud financier fragile critique — institution too-big-to-fail avec levier excessif",
    },
    "vulnerabilite_contagion": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des stress tests et coussins de capital anti-cycliques renforcés",
        "signal_fr": "Vulnérabilité à la contagion — exposition croisée élevée sans pare-feu suffisants",
    },
    "risque_modere_interconnecte": {
        "severity_fr": "Modéré",
        "action_fr": "Surveillance macroprudentielle renforcée et coordination internationale des régulateurs",
        "signal_fr": "Risque modéré d'interconnexion — canaux de contagion existants mais absorbeurs de choc présents",
    },
    "resilience_systemique": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des standards prudentiels et vigilance sur les nouvelles formes de risque systémique",
        "signal_fr": "composite_score < 20 — résilience systémique, pare-feu financiers robustes et régulation efficace",
    },
}


@dataclass
class FinancialContagionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    interconnection_density_score: float
    leverage_excess_score: float
    regulatory_arbitrage_exposure_score: float
    crisis_transmission_speed_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_contagion_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.interconnection_density_score * 0.30
            + self.leverage_excess_score * 0.25
            + self.regulatory_arbitrage_exposure_score * 0.25
            + self.crisis_transmission_speed_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_contagion_index = round(self.composite_score / 100 * 10, 2)

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
        if self.interconnection_density_score >= 80 and self.leverage_excess_score >= 75:
            return "contagion_systemique_imminente"
        if self.leverage_excess_score >= 70:
            return "noeud_fragile_critique"
        if self.composite_score >= 45:
            return "vulnerabilite_contagion"
        if self.composite_score >= 25:
            return "risque_modere_interconnecte"
        return "resilience_systemique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Contagion systémique imminente dans {n} — nœuds too-big-to-fail avec levier excessif",
                "Vitesse de transmission de crise maximale — effets dominos potentiellement mondiaux en 72h",
                "Arbitrage réglementaire exposant le système — risques accumulés hors bilan et hors régulation",
            ]
        if self.risk_level == "élevé":
            return [
                f"Vulnérabilité à la contagion sévère dans {n} — expositions croisées élevées sans pare-feux",
                "Effet de levier systémique excessif — amplification des pertes en cas de choc exogène",
                "Canaux de transmission de crise identifiés — stress tests révélant des lacunes critiques",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque modéré d'interconnexion dans {n} — canaux de contagion présents mais absorbeurs actifs",
                "Surveillance macroprudentielle en place — régulateurs alertes aux risques systémiques émergents",
                "Coussins de capital partiellement suffisants mais stress tests révélant des fragilités résiduelles",
            ]
        return [
            f"{n} maintient une résilience systémique — pare-feux financiers robustes et régulation efficace",
            "Standards prudentiels stricts et coordination internationale des régulateurs opérationnelle",
            "Modèle de résilience financière systémique — capacité d'absorption des chocs sans contagion externe",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "interconnection_density_score": self.interconnection_density_score,
            "leverage_excess_score": self.leverage_excess_score,
            "regulatory_arbitrage_exposure_score": self.regulatory_arbitrage_exposure_score,
            "crisis_transmission_speed_score": self.crisis_transmission_speed_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_contagion_index": self.estimated_contagion_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FinancialContagionEntity] = [
    FinancialContagionEntity("FC-001", "Marché des Dérivés OTC Global", "Global", "700 Trilliards$ Dérivés Hors Bilan — Risque Systémique #1", 95.0, 92.0, 90.0, 88.0),
    FinancialContagionEntity("FC-002", "Chine — Immobilier & Evergrande Effect", "Asie", "Bulle Immobilière & Banques Fantômes (Shadow Banking)", 88.0, 85.0, 82.0, 85.0),
    FinancialContagionEntity("FC-003", "Wall Street — Trop Grande pour Faire Faillite", "Amérique du Nord", "JPMorgan/Goldman — Nœuds Systemically Important Globaux", 82.0, 78.0, 75.0, 80.0),
    FinancialContagionEntity("FC-004", "Europe — Banques en Réseau Dense", "Europe", "Deutsche Bank & Contagion Intra-Européenne", 75.0, 72.0, 68.0, 78.0),
    FinancialContagionEntity("FC-005", "Cryptomonnaies — Contagion DeFi", "Cyberespace", "FTX Collapse Effect & Interconnexion DeFi-TradFi", 70.0, 68.0, 85.0, 65.0),
    FinancialContagionEntity("FC-006", "Marchés Émergents — Effet Dollar", "Global", "Vulnérabilité au Dollar Fort & Sudden Stop des Capitaux", 60.0, 55.0, 58.0, 62.0),
    FinancialContagionEntity("FC-007", "Japon — Dette Souveraine & Yen Carry Trade", "Asie du Nord-Est", "Yen Carry Trade Dénouement & JGB Bubble", 48.0, 52.0, 42.0, 45.0),
    FinancialContagionEntity("FC-008", "Canada & Australie — Résilience Régulée", "Anglo-Saxon", "Supervision Macroprudentielle Robuste & Coussins Capital", 22.0, 18.0, 15.0, 20.0),
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
        "domain": "financial_contagion",
        "confidence_score": 0.76,
        "data_sources": ["bis_systemic_risk_tracker", "fsb_interconnection_monitor", "imf_financial_stability_report"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_contagion_index": round(avg / 100 * 10, 2),
    }


def analyze_financial_contagion() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Financial Contagion Engine — {r['total_entities']} nœuds, avg contagion: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
