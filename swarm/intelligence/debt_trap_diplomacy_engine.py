"""
Caelum Partners — Debt Trap Diplomacy Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La diplomatie du piège de la dette comme stratégie géopolitique chinoise :
la Chine utilise l'Initiative Ceinture et Route (BRI) pour accorder des
prêts massifs à des pays en développement à des conditions opaques, créant
des dépendances souveraines qui se convertissent en concessions stratégiques
lorsque les emprunteurs ne peuvent pas rembourser.

Du port de Hambantota au Sri Lanka (loué 99 ans à la Chine en 2017)
aux ports africains, aéroports et infrastructures critiques hypothéqués
à Pékin, la BRI n'est pas un programme de développement — c'est un
instrument d'extension de l'influence géopolitique chinoise déguisé en
aide au développement. Les pays endettés perdent leur souveraineté de
politique étrangère : ils votent avec Pékin à l'ONU, refusent de critiquer
la situation au Xinjiang, et ouvrent leurs eaux territoriales aux navires
militaires chinois.

Risk levels (dépendance souveraine via piège de la dette) :
  critique  → composite ≥ 60  (souveraineté compromettée par la dette chinoise)
  élevé     → composite ≥ 40  (dépendance financière significative envers Pékin)
  modéré    → composite ≥ 20  (exposition BRI à surveiller)
  faible    → composite < 20  (indépendance financière préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "souverainete_compromise": {
        "severity_fr": "Critique",
        "action_fr": "Renégociation de la dette avec soutien FMI/G7 et audit des clauses secrètes BRI",
        "signal_fr": "bri_debt_ratio > 80 AND strategic_asset_collateral > 75 — souveraineté compromise par la dette",
    },
    "dependance_infrastructurelle": {
        "severity_fr": "Critique",
        "action_fr": "Diversification des partenaires de financement et transparence des contrats BRI",
        "signal_fr": "Infrastructure critique sous contrôle chinois — ports, aéroports et télécoms hypothéqués",
    },
    "capture_politique": {
        "severity_fr": "Élevé",
        "action_fr": "Conditionnalité démocratique de l'aide alternative et renforcement de la gouvernance locale",
        "signal_fr": "Capture politique via la dette — votes ONU alignés sur Pékin et silence sur violations droits humains",
    },
    "exposition_croissante": {
        "severity_fr": "Modéré",
        "action_fr": "Audit des contrats BRI et développement de sources de financement alternatives",
        "signal_fr": "Exposition BRI croissante — accumulation de dette chinoise sans garde-fous suffisants",
    },
    "independance_preservee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la diversification des partenaires financiers et vigilance sur les offres BRI",
        "signal_fr": "composite_score < 20 — indépendance financière préservée, pas de dépendance BRI critique",
    },
}


@dataclass
class DebtTrapDiplomacyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    bri_debt_ratio_score: float
    strategic_asset_collateral_score: float
    political_alignment_coercion_score: float
    repayment_capacity_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_debt_trap_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.bri_debt_ratio_score * 0.30
            + self.strategic_asset_collateral_score * 0.25
            + self.political_alignment_coercion_score * 0.25
            + self.repayment_capacity_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_debt_trap_index = round(self.composite_score / 100 * 10, 2)

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
        if self.bri_debt_ratio_score >= 80 and self.strategic_asset_collateral_score >= 75:
            return "souverainete_compromise"
        if self.strategic_asset_collateral_score >= 70:
            return "dependance_infrastructurelle"
        if self.composite_score >= 40:
            return "capture_politique"
        if self.composite_score >= 20:
            return "exposition_croissante"
        return "independance_preservee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Piège de la dette actif dans {n} — dette BRI insoutenable convertie en concessions souveraines à Pékin",
                "Actifs stratégiques hypothéqués à la Chine — ports, aéroports ou ressources naturelles sous contrôle chinois",
                "Souveraineté de politique étrangère compromise — alignement forcé sur Pékin dans les enceintes internationales",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dépendance financière significative de {n} envers la Chine — BRI représentant une part critique du PIB",
                "Infrastructure critique financée par la Chine avec clauses de rachat opaques — risque de perte d'actifs",
                "Alignement politique partiel sur Pékin — pressions chinoises sur la politique étrangère du pays débiteur",
            ]
        if self.risk_level == "modéré":
            return [
                f"Exposition BRI croissante dans {n} — projets d'infrastructure chinois sans audit suffisant des conditions",
                "Accumulation de dette bilatérale chinoise — ratio en hausse sans diversification des créanciers",
                "Risques de capture à moyen terme si la trajectoire BRI n'est pas rééquilibrée",
            ]
        return [
            f"{n} préserve son indépendance financière — financement diversifié et résistance aux offres BRI",
            "Contrats d'infrastructure transparents et refus des clauses secrètes chinoises",
            "Modèle de souveraineté financière — diversification active des partenaires de développement",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "bri_debt_ratio_score": self.bri_debt_ratio_score,
            "strategic_asset_collateral_score": self.strategic_asset_collateral_score,
            "political_alignment_coercion_score": self.political_alignment_coercion_score,
            "repayment_capacity_deficit_score": self.repayment_capacity_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_debt_trap_index": self.estimated_debt_trap_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[DebtTrapDiplomacyEntity] = [
    DebtTrapDiplomacyEntity("DT-001", "Sri Lanka — Hambantota Loué 99 ans", "Asie du Sud", "Port Stratégique Cédé à Pékin — Modèle du Piège BRI", 92.0, 95.0, 85.0, 90.0),
    DebtTrapDiplomacyEntity("DT-002", "Zambie — Mines de Cuivre & Aéroport Menacés", "Afrique Australe", "Dette Chinoise 1/3 du PIB — Lusaka International Hypothéqué", 88.0, 85.0, 82.0, 90.0),
    DebtTrapDiplomacyEntity("DT-003", "Pakistan — CPEC & Dépendance Structurelle", "Asie du Sud", "Corridor Économique Chine-Pakistan — 62 Mds $ Engagés", 85.0, 80.0, 88.0, 82.0),
    DebtTrapDiplomacyEntity("DT-004", "Éthiopie & Djibouti — Chemin de Fer & Port", "Afrique de l'Est", "Chemin de Fer Addis-Djibouti et Port de Doraleh Sous Contrôle Chinois", 80.0, 82.0, 78.0, 85.0),
    DebtTrapDiplomacyEntity("DT-005", "Laos & Cambodge — Asie du SE Enclavée", "Asie du Sud-Est", "Chemin de Fer Laos-Chine — 6 Mds $ pour Pays de 7 Mds PIB", 72.0, 68.0, 75.0, 78.0),
    DebtTrapDiplomacyEntity("DT-006", "Kenya & Tanzanie — SGR Ferroviaire BRI", "Afrique de l'Est", "Standard Gauge Railway — Ports Mombasa et Dar es Salam Exposés", 58.0, 60.0, 55.0, 62.0),
    DebtTrapDiplomacyEntity("DT-007", "Brésil & Argentine — BRI Entrante en AL", "Amériques", "Pénétration Croissante BRI en Amérique Latine — Soja et Lithium", 35.0, 32.0, 40.0, 28.0),
    DebtTrapDiplomacyEntity("DT-008", "Inde & USA — Résistance Systémique à la BRI", "Global", "Refus Stratégique de la BRI — Financement Alternatif PGII/IMEC", 5.0, 4.0, 8.0, 3.0),
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
        "domain": "debt_trap",
        "confidence_score": 0.86,
        "data_sources": ["aiddata_bri_debt_tracker", "china_africa_research_initiative", "global_development_policy_center"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_debt_trap_index": round(avg / 100 * 10, 2),
    }


def analyze_debt_trap_diplomacy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Debt Trap Diplomacy Engine — {r['total_entities']} pays, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
