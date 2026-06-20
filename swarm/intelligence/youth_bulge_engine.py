"""
Caelum Partners — Youth Bulge Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le « youth bulge » comme précurseur des instabilités politiques : quand
les sociétés développent une proportion massive de jeunes (15-29 ans)
sans offrir d'opportunités économiques, éducatives et politiques, elles
créent les conditions structurelles de la violence, de la radicalisation
et de la révolution.

La théorie du « youth bulge » (Urdal, 2006 ; Heinsohn, 2007) prédit que
les pays où les 15-29 ans représentent plus de 20% de la population adulte,
combinés à un chômage structurel élevé, deviennent des terrains fertiles
pour les groupes armés non-étatiques, les mouvements révolutionnaires et
les conflits civils. Le Sahel, le Moyen-Orient et l'Asie du Sud concentrent
les plus grands défis démographiques du XXIe siècle. Comprendre la pyramide
des âges, c'est prédire les crises de la prochaine décennie.

Risk levels (pression démographique jeunesse et instabilité) :
  critique  → composite ≥ 60  (pression démographique explosive — risque d'instabilité élevé)
  élevé     → composite ≥ 40  (youth bulge significatif sans absorption économique suffisante)
  modéré    → composite ≥ 20  (tensions démographiques à surveiller)
  faible    → composite < 20  (transition démographique stabilisante)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "explosion_demographique_conflictuelle": {
        "severity_fr": "Critique",
        "action_fr": "Politiques massives d'emploi jeunesse et déradicalisation préventive des cohortes à risque",
        "signal_fr": "youth_ratio > 80 AND youth_unemployment > 75 — explosion démographique sans débouchés",
    },
    "radicalisation_structurelle": {
        "severity_fr": "Critique",
        "action_fr": "Investissements d'urgence en éducation technique et création d'emplois formels pour les 15-29 ans",
        "signal_fr": "Youth bulge avec chômage structurel — cohortes massives sans intégration économique ni politique",
    },
    "pression_migratoire_forte": {
        "severity_fr": "Élevé",
        "action_fr": "Politiques de migration ordonnée et partenariats de développement ciblant la jeunesse",
        "signal_fr": "Pression migratoire forte — jeunes sans perspective intérieure cherchant exutoires à l'étranger",
    },
    "tension_generationnelle": {
        "severity_fr": "Modéré",
        "action_fr": "Réformes du marché du travail et participation politique inclusive des jeunes",
        "signal_fr": "Tensions générationnelles — jeunes mal intégrés dans les systèmes politiques et économiques",
    },
    "dividende_demographique": {
        "severity_fr": "Faible",
        "action_fr": "Capitaliser le dividende démographique par l'investissement en capital humain et l'innovation",
        "signal_fr": "composite_score < 20 — transition démographique maîtrisée avec dividende potentiel",
    },
}


@dataclass
class YouthBulgeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    youth_ratio_pressure_score: float
    youth_unemployment_score: float
    political_exclusion_score: float
    radicalization_vectors_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_youth_instability_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.youth_ratio_pressure_score * 0.30
            + self.youth_unemployment_score * 0.25
            + self.political_exclusion_score * 0.25
            + self.radicalization_vectors_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_youth_instability_index = round(self.composite_score / 100 * 10, 2)

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
        if self.youth_ratio_pressure_score >= 80 and self.youth_unemployment_score >= 75:
            return "explosion_demographique_conflictuelle"
        if self.radicalization_vectors_score >= 75:
            return "radicalisation_structurelle"
        if self.composite_score >= 40:
            return "pression_migratoire_forte"
        if self.composite_score >= 20:
            return "tension_generationnelle"
        return "dividende_demographique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Youth bulge explosif dans {n} — cohortes massives de jeunes sans débouchés économiques ni politiques",
                "Chômage structurel des jeunes alimentant recrutement par groupes armés et mouvements radicaux",
                "Exclusion politique de la jeunesse — frustration générationnelle convertissable en instabilité violente",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression démographique jeunesse significative dans {n} — absorption économique insuffisante",
                "Taux de chômage jeunesse critique — génération entière sans perspectives formelles d'emploi",
                "Tensions générationnelles avec établissement politique — risque de mobilisation contestataire",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions démographiques jeunesse dans {n} — déséquilibres entre cohortes et opportunités",
                "Inadéquation formation-emploi — jeunes diplômés en inadéquation avec marché du travail",
                "Risque migratoire modéré — fuite des cerveaux et pressions sur les systèmes sociaux",
            ]
        return [
            f"{n} capitalise son dividende démographique — jeunesse intégrée dans la croissance économique",
            "Marché du travail inclusif avec formations adaptées aux besoins économiques actuels",
            "Participation politique jeunesse active — relève générationnelle institutionnellement encadrée",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "youth_ratio_pressure_score": self.youth_ratio_pressure_score,
            "youth_unemployment_score": self.youth_unemployment_score,
            "political_exclusion_score": self.political_exclusion_score,
            "radicalization_vectors_score": self.radicalization_vectors_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_youth_instability_index": self.estimated_youth_instability_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[YouthBulgeEntity] = [
    YouthBulgeEntity("YB-001", "Sahel — Bombe Démographique Djihadiste", "Afrique de l'Ouest", "Niger/Mali/Burkina : 50%+ de Moins de 15 ans Sans Avenir Économique", 95.0, 90.0, 88.0, 92.0),
    YouthBulgeEntity("YB-002", "Nigeria — Génération Perdue du Pétrole", "Afrique de l'Ouest", "220M d'Habitants — 70% Moins de 30 ans Sans Emploi Formel", 90.0, 85.0, 82.0, 88.0),
    YouthBulgeEntity("YB-003", "Afghanistan & Pakistan — FATA Powder Keg", "Asie Centrale/Sud", "Jeunesse Pachtoune Sans École ni Emploi — Recrutement Taliban Facilité", 85.0, 88.0, 80.0, 90.0),
    YouthBulgeEntity("YB-004", "Yémen & Irak — Jeunesse de Guerre", "MENA", "Générations Entières Formées à la Guerre — Traumatisme et Radicalisation", 80.0, 82.0, 78.0, 85.0),
    YouthBulgeEntity("YB-005", "Égypte & Algérie — Murs du Chômage Jeune", "MENA/Afrique du Nord", "Taux Chômage Jeunes 25-30% — Printemps Arabes en Attente", 72.0, 78.0, 65.0, 70.0),
    YouthBulgeEntity("YB-006", "Inde — Dividende ou Bombe ?", "Asie du Sud", "600M de Moins de 25 ans — Course Emploi vs Automatisation", 65.0, 60.0, 55.0, 58.0),
    YouthBulgeEntity("YB-007", "Brésil & Mexique — Jeunesse Périurbaine", "Amériques", "Favelas et Périphéries Urbaines — Recrutement par Gangs Structurel", 48.0, 52.0, 45.0, 55.0),
    YouthBulgeEntity("YB-008", "Europe & Japon — Vieillissement Inverse", "Global Nord", "Crise de Vieillissement — Youth Bulge Inversé, Pénuries Main d'Oeuvre", 8.0, 10.0, 12.0, 5.0),
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
        "domain": "youth_bulge",
        "confidence_score": 0.88,
        "data_sources": ["un_population_division", "ilo_youth_unemployment_tracker", "conflict_early_warning_systems"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_youth_instability_index": round(avg / 100 * 10, 2),
    }


def analyze_youth_bulge() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Youth Bulge Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
