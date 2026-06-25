"""
Caelum Partners — Pension Crisis Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'effondrement des systèmes de retraite comme bombe à retardement
géopolitique et sociale : le vieillissement démographique combiné
aux promesses de retraite non-financées crée des crises fiscales
intergénérationnelles sans précédent. Les gouvernements ont promis
des pensions que leurs économies ne peuvent plus financer.

Du Japon où les plus de 65 ans représentent 30% de la population,
à l'Europe du Sud où les systèmes par répartition s'effondrent
sous le poids démographique, en passant par les États-Unis où les
fonds de pension publics affichent des déficits de plusieurs milliers
de milliards de dollars, la crise des retraites est la crise silencieuse
la plus prévisible de l'histoire. Elle génère des conflits politiques
intergénérationnels intenses, des réformes impopulaires qui déstabilisent
les gouvernements, et des arbitrages budgétaires qui affament les
investissements en éducation et infrastructure.

Risk levels (insoutenabilité du système de retraite) :
  critique  → composite ≥ 60  (crise de solvabilité retraite imminente)
  élevé     → composite ≥ 40  (pressions retraite sévères sans réforme)
  modéré    → composite ≥ 20  (tensions retraite gérables à court terme)
  faible    → composite < 20  (système de retraite soutenable et réformé)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "insolvabilite_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Réforme structurelle d'urgence des retraites et recapitalisation des fonds déficitaires",
        "signal_fr": "demographic_pressure > 80 AND funding_gap > 75 — insolvabilité systémique des retraites",
    },
    "bombe_intergenerationnelle": {
        "severity_fr": "Critique",
        "action_fr": "Pacte intergénérationnel et diversification vers capitalisation individuelle supervisée",
        "signal_fr": "Bombe intergénérationnelle — actifs insuffisants face à explosion des retraités",
    },
    "pression_fiscale_critique": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme paramétrique des retraites et diversification des sources de financement",
        "signal_fr": "Pression fiscale critique — dépenses retraite dévorant investissements et services publics",
    },
    "ajustement_douloureux": {
        "severity_fr": "Modéré",
        "action_fr": "Réformes graduelles des retraites avec consultation sociale pour minimiser les tensions",
        "signal_fr": "Ajustement douloureux — réformes nécessaires mais politiquement difficiles à mener",
    },
    "equilibre_soutenable": {
        "severity_fr": "Faible",
        "action_fr": "Maintenir les réformes préventives et partager les modèles de durabilité des retraites",
        "signal_fr": "composite_score < 20 — système de retraite soutenable avec réformes préventives réussies",
    },
}


@dataclass
class PensionCrisisEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    demographic_pressure_score: float
    funding_gap_score: float
    intergenerational_conflict_score: float
    reform_political_resistance_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_pension_crisis_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.demographic_pressure_score * 0.30
            + self.funding_gap_score * 0.25
            + self.intergenerational_conflict_score * 0.25
            + self.reform_political_resistance_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_pension_crisis_index = round(self.composite_score / 100 * 10, 2)

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
        if self.demographic_pressure_score >= 80 and self.funding_gap_score >= 75:
            return "insolvabilite_systemique"
        if self.intergenerational_conflict_score >= 75:
            return "bombe_intergenerationnelle"
        if self.composite_score >= 40:
            return "pression_fiscale_critique"
        if self.composite_score >= 20:
            return "ajustement_douloureux"
        return "equilibre_soutenable"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Crise de solvabilité des retraites dans {n} — déficits actuariels insoutenables sans réforme immédiate",
                "Bombe démographique — ratio actifs/retraités en chute libre, financement par répartition insoutenable",
                "Conflit intergénérationnel latent — jeunes actifs subventionnant des retraites promises non-financées",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression retraite sévère dans {n} — déficits des fonds de pension nécessitant réformes urgentes",
                "Dépenses retraite dévorant le budget — arbitrages défavorables pour éducation et infrastructure",
                "Résistance politique aux réformes — syndicats et partis bloquant les ajustements nécessaires",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions retraite gérables dans {n} — ajustements nécessaires mais marge de manœuvre existante",
                "Pression démographique croissante — vieillissement accélérant les déséquilibres actuariels",
                "Réformes paramétriques en discussion — âge de départ, taux de cotisation et conditions d'indexation",
            ]
        return [
            f"{n} maintient un système de retraite soutenable — réformes préventives réussies et démographie maîtrisée",
            "Fonds de pension bien capitalisés et mix répartition-capitalisation équilibré",
            "Modèle de durabilité retraite à partager — gouvernance actuarielle transparente et adaptation continue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "demographic_pressure_score": self.demographic_pressure_score,
            "funding_gap_score": self.funding_gap_score,
            "intergenerational_conflict_score": self.intergenerational_conflict_score,
            "reform_political_resistance_score": self.reform_political_resistance_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_pension_crisis_index": self.estimated_pension_crisis_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PensionCrisisEntity] = [
    PensionCrisisEntity("PC-001", "Japon — Archipel du Vieillissement", "Asie", "30% de 65+ — Ratio Actifs/Retraités en Effondrement Structurel", 95.0, 88.0, 80.0, 72.0),
    PensionCrisisEntity("PC-002", "Italie & Grèce — Europe du Sud Sous Pression", "Europe", "Retraites 16% PIB — Réformes Bloquées par Résistance Syndicale", 85.0, 82.0, 78.0, 88.0),
    PensionCrisisEntity("PC-003", "Chine — Vieillissement Post-Enfant Unique", "Asie", "Politique Enfant Unique — Bombe Démographique Actuarielle à Retardement", 82.0, 78.0, 75.0, 65.0),
    PensionCrisisEntity("PC-004", "France — Conflit Générationnel Retraites", "Europe", "Réforme 64 ans 2023 — Crise Sociale & Légitimité Démocratique Fragilisée", 70.0, 65.0, 85.0, 88.0),
    PensionCrisisEntity("PC-005", "USA — Fonds Publics Locaux Déficitaires", "Amérique du Nord", "Pensions Illinois/New Jersey — Déficits Actuariels Multi-Milliards $", 55.0, 68.0, 55.0, 55.0),
    PensionCrisisEntity("PC-006", "Russie — Réforme 2018 & Impopularité", "Europe de l'Est", "Âge Retraite Relevé à 60/65 ans — Résistance Populaire & Fragilité Sociale", 52.0, 52.0, 55.0, 45.0),
    PensionCrisisEntity("PC-007", "Brésil & Argentine — Retraites & Populisme", "Amériques", "Systèmes par Répartition Déséquilibrés — Clientélisme et Déficits Chroniques", 32.0, 38.0, 35.0, 28.0),
    PensionCrisisEntity("PC-008", "Scandinavie — Modèles NDC Réformés", "Europe du Nord", "Systèmes à Comptes Notionnels — Durabilité Actuarielle Garantie", 15.0, 10.0, 8.0, 5.0),
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
        "domain": "pension_crisis",
        "confidence_score": 0.89,
        "data_sources": ["oecd_pension_outlook", "imf_fiscal_monitor_pensions", "mercer_melbourne_global_pension_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_pension_crisis_index": round(avg / 100 * 10, 2),
    }


def analyze_pension_crisis() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Pension Crisis Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
