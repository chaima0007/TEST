"""
Caelum Partners — Currency War Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La guerre des monnaies : dé-dollarisation et nouveaux ordres monétaires.
Le dollar américain représente 59% des réserves mondiales et 88% des
transactions FOREX — une hégémonie monétaire qui confère aux USA une
capacité unique de projeter leur puissance économique via les sanctions,
le contrôle de SWIFT et la politique monétaire de la Fed. Les États
adversaires ont identifié cette dépendance comme leur principale vulnérabilité
et organisent méthodiquement leur sortie du dollar.

La Chine déploie le yuan numérique (e-CNY) dans 26 provinces avec 260Md$
de transactions testées, tout en signant des accords pétro-yuan avec l'Arabie
Saoudite, la Russie et l'Iran. Les BRICS ont lancé à Johannesburg 2023 une
monnaie commune d'échanges commerciaux adossée à l'or — et ont intégré Arabie
Saoudite, EAU, Éthiopie, Égypte, Iran et Argentine. La Russie a basculé 70%
de ses réserves en or et yuans après le gel de ses réserves en euros post-2022.

La Banque Populaire de Chine achète 600+ tonnes d'or par an pour constituer
des réserves hors-dollar. L'Inde facture une part croissante de son pétrole
russe en roupies. Le système CIPS (Cross-border Interbank Payment System)
chinois traite 6 800Md$ de transactions alternatives à SWIFT, avec 103 pays
participants. Le monde est en train de se fragmenter en blocs monétaires.

Risk levels (guerres des monnaies et dé-dollarisation) :
  critique  → composite ≥ 60  (dé-dollarisation active — stratégie monétaire offensive et systémique)
  élevé     → composite ≥ 40  (guerre monétaire régionale — manœuvres actives de découplage du dollar)
  modéré    → composite ≥ 20  (souveraineté monétaire défensive — protections sans stratégie offensive)
  faible    → composite < 20  (stabilité monétaire coopérative — soutien à l'architecture financière multilatérale)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "dedollarisation_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Défense proactive du dollar — accords de swap bilatéraux élargis, réforme du FMI et modernisation de l'architecture SWIFT pour maintenir la centralité du dollar",
        "signal_fr": "dedollarization_strategy_score > 85 AND cbdc_geopolitical_score > 85 — stratégie de dé-dollarisation systémique avec CBDC géopolitique offensive",
    },
    "or_comme_arme_monetaire": {
        "severity_fr": "Critique",
        "action_fr": "Coordination G7 sur les réserves d'or — mécanismes de transparence et surveillance des accumulations massives de réserves à visée géopolitique",
        "signal_fr": "gold_reserve_weaponization_score > 85 — weaponisation des réserves d'or pour construire une alternative hors-dollar aux réserves mondiales",
    },
    "manipulation_monetaire_offensive": {
        "severity_fr": "Critique",
        "action_fr": "Surveillance FMI des taux de change — mécanismes anti-manipulation et sanctions ciblées contre les dévaluations compétitives délibérées",
        "signal_fr": "currency_manipulation_score > 85 — manipulation offensive des taux de change comme instrument de guerre commerciale",
    },
    "guerre_monetaire_regionale": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcer la coopération monétaire régionale — accords de swap bilatéraux, zones de libre-échange en monnaie locale et réduction de la dépendance SWIFT",
        "signal_fr": "Guerre monétaire régionale — manœuvres actives pour réduire la dépendance au dollar dans les échanges bilatéraux",
    },
    "stabilite_monetaire_cooperative": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer les institutions de Bretton Woods — réforme du FMI, droits de tirage spéciaux étendus et gouvernance monétaire multilatérale renforcée",
        "signal_fr": "composite_score < 20 — soutien actif à la stabilité monétaire internationale et au système multilatéral de Bretton Woods",
    },
}


@dataclass
class CurrencyWarEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    dedollarization_strategy_score: float
    currency_manipulation_score: float
    cbdc_geopolitical_score: float
    gold_reserve_weaponization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_currency_war_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.dedollarization_strategy_score * 0.30
            + self.currency_manipulation_score * 0.25
            + self.cbdc_geopolitical_score * 0.25
            + self.gold_reserve_weaponization_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_currency_war_index = round(self.composite_score / 100 * 10, 2)

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
        if self.dedollarization_strategy_score >= 85 and self.cbdc_geopolitical_score >= 85:
            return "dedollarisation_systemique"
        if self.gold_reserve_weaponization_score >= 85:
            return "or_comme_arme_monetaire"
        if self.currency_manipulation_score >= 85:
            return "manipulation_monetaire_offensive"
        if self.composite_score >= 20:
            return "guerre_monetaire_regionale"
        return "stabilite_monetaire_cooperative"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Dé-dollarisation active par {n} — stratégie monétaire offensive visant à réduire l'hégémonie du dollar dans les échanges internationaux",
                "Construction d'alternatives monétaires — CBDC géopolitiques, yuan pétrolier, accord BRICS et réserves d'or hors-dollar",
                "Fragmentation du système monétaire mondial — émergence de blocs monétaires incompatibles et fin du dollar comme monnaie de réserve unique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Guerre monétaire régionale par {n} — manœuvres actives pour réduire la dépendance au dollar dans les échanges bilatéraux",
                "Accords de swap bilatéraux — transactions en monnaies locales contournant SWIFT et les sanctions américaines",
                "Instabilité monétaire — volatilité des taux de change alimentée par des politiques monétaires à visée géopolitique",
            ]
        if self.risk_level == "modéré":
            return [
                f"Souveraineté monétaire défensive de {n} — mesures de protection sans stratégie offensive de dé-dollarisation",
                "Dépendance aux conditions financières mondiales — exposition aux décisions de la Fed et aux flux de capitaux spéculatifs",
                "CBDC défensive en développement — euro numérique ou monnaie digitale nationale pour préserver la souveraineté monétaire",
            ]
        return [
            f"{n} soutient la stabilité monétaire multilatérale — coopération FMI, droits de tirage spéciaux et transparence des réserves",
            "Architecture de Bretton Woods renforcée — maintien du dollar comme ancre de stabilité et coordination des politiques monétaires G20",
            "Modèle de gouvernance monétaire à préserver — FMI réformé, surveillance des taux de change et mécanismes de prévention des crises",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "dedollarization_strategy_score": self.dedollarization_strategy_score,
            "currency_manipulation_score": self.currency_manipulation_score,
            "cbdc_geopolitical_score": self.cbdc_geopolitical_score,
            "gold_reserve_weaponization_score": self.gold_reserve_weaponization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_currency_war_index": self.estimated_currency_war_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[CurrencyWarEntity] = [
    CurrencyWarEntity("CW-001", "Chine — e-CNY & Pétro-Yuan BRICS Dé-Dollarisation", "Asie", "e-CNY 260Md$ Testé, Accord Pétro-Yuan Arabie/Russie, CIPS 103 Pays & BRICS Monnaie Commune", 92.0, 88.0, 95.0, 85.0),
    CurrencyWarEntity("CW-002", "Russie — Réserves Or 70% & SWIFT Alternatif MIR", "Europe de l'Est", "Or 2355 Tonnes Réserves, Système MIR 90 Pays, SPFS SWIFT Alternatif & Yuanisation Échanges", 88.0, 85.0, 80.0, 92.0),
    CurrencyWarEntity("CW-003", "Arabie Saoudite — Pétrodollar & Diversification BRICS", "MENA", "Ventes Pétrole en Yuan Négociées, BRICS+ Membership 2024 & Réserves Or en Augmentation", 82.0, 78.0, 75.0, 85.0),
    CurrencyWarEntity("CW-004", "Inde — Rupee Internationalisation & BRICS+", "Asie du Sud", "Pétrole Russe en Roupies, Accords Swap Bilatéraux 22 Pays & UPI System International", 78.0, 72.0, 70.0, 80.0),
    CurrencyWarEntity("CW-005", "Turquie — Livre & Indépendance Monétaire Erdoğan", "MENA/Europe", "Dévaluation Délibérée Livre, Réserves Or Achat Massif & Swap Chine/Qatar Sans Dollar", 55.0, 65.0, 48.0, 52.0),
    CurrencyWarEntity("CW-006", "Iran & BRICS — Économies Sanctionnées Hors-Dollar", "MENA", "Troc Pétrole-Marchandises, Crypto-Rial Envisagé & Commerce Bilatéral Yuan/Rouble/Roupie", 52.0, 58.0, 55.0, 48.0),
    CurrencyWarEntity("CW-007", "UE — Euro Digital & Souveraineté Monétaire Défensive", "Europe", "Digital Euro BCE Projet Pilote, Réforme SWIFT Européen & Instruments Anti-Coercition Monétaire", 28.0, 25.0, 38.0, 22.0),
    CurrencyWarEntity("CW-008", "FMI & Dollar — Stabilité Monétaire Multilatérale", "Global", "DTS 650Md$ Allocation Covid, Surveillance Articles IV & Prêteur Dernier Ressort Mondial", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "currency_war",
        "confidence_score": 0.79,
        "data_sources": ["bis_currency_report", "imf_reserve_currency_monitor", "atlantic_council_geoeconomics"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_currency_war_index": round(avg / 100 * 10, 2),
    }


def analyze_currency_war() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Currency War Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
