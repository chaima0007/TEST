"""
Caelum Partners — Maternal Mortality Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La mortalité maternelle comme indicateur géopolitique de la capacité
étatique : chaque décès maternel évitable révèle une faillite du système
de santé, une inégalité de genre systémique et un désengagement de l'État
envers les femmes. Les pays avec des taux élevés de mortalité maternelle
ne sont pas seulement des crises sanitaires — ce sont des États qui ont
choisi, implicitement ou explicitement, de ne pas protéger la moitié de
leur population.

De la Sierra Leone au Niger, du Tchad à la Somalie, les 10 pays avec les
plus hauts taux de mortalité maternelle partagent un profil commun :
conflits armés, systèmes de santé sous-financés, inégalités de genre
extrêmes, et gouvernements qui considèrent la santé reproductive comme
une priorité secondaire. La mortalité maternelle est une honte géopolitique
mesurable — et un prédicteur de la stabilité à long terme.

Risk levels (mortalité maternelle comme échec de l'État) :
  critique  → composite ≥ 60  (crise sanitaire maternelle systémique)
  élevé     → composite ≥ 40  (défaillances graves du système obstétrical)
  modéré    → composite ≥ 20  (lacunes persistantes dans les soins maternels)
  faible    → composite < 20  (système de santé maternelle fonctionnel)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "crise_humanitaire_maternelle": {
        "severity_fr": "Critique",
        "action_fr": "Déploiement d'urgence de sages-femmes qualifiées et d'unités obstétriques mobiles",
        "signal_fr": "healthcare_system_collapse > 80 AND gender_inequality_score > 75 — crise maternelle systémique",
    },
    "desengagement_etatique": {
        "severity_fr": "Critique",
        "action_fr": "Pression internationale et conditionnalité aide au financement de la santé maternelle",
        "signal_fr": "État refusant d'investir dans la santé reproductrice — mortalité maternelle délibérément tolérée",
    },
    "fragilite_systemique": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des capacités obstétriques et formation accélérée des sages-femmes",
        "signal_fr": "Fragilité systémique obstétricale — accès aux soins insuffisant en zones rurales et conflictuelles",
    },
    "lacunes_rurales": {
        "severity_fr": "Modéré",
        "action_fr": "Programmes de santé maternelle ruraux et télémédecine obstétricale",
        "signal_fr": "Lacunes rurales — mortalité maternelle concentrée dans les zones reculées sans accès aux soins",
    },
    "systeme_performant": {
        "severity_fr": "Faible",
        "action_fr": "Partage des bonnes pratiques obstétriques et coopération Sud-Sud en santé maternelle",
        "signal_fr": "composite_score < 20 — système de santé maternelle performant et équitable",
    },
}


@dataclass
class MaternalMortalityEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    healthcare_system_collapse_score: float
    gender_inequality_score: float
    obstetric_access_deficit_score: float
    conflict_health_impact_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_maternal_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.healthcare_system_collapse_score * 0.30
            + self.gender_inequality_score * 0.25
            + self.obstetric_access_deficit_score * 0.25
            + self.conflict_health_impact_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_maternal_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.healthcare_system_collapse_score >= 80 and self.gender_inequality_score >= 75:
            return "crise_humanitaire_maternelle"
        if self.composite_score >= 65:
            return "desengagement_etatique"
        if self.composite_score >= 40:
            return "fragilite_systemique"
        if self.composite_score >= 20:
            return "lacunes_rurales"
        return "systeme_performant"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Crise de mortalité maternelle en {n} — décès obstétriques évitables massifs révélant une faillite de l'État",
                "Inégalité de genre systémique — femmes exclues de l'accès aux soins obstétriques de base",
                "Système de santé en effondrement — manque de sages-femmes qualifiées et d'infrastructures obstétriques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Fragilité obstétricale grave dans {n} — mortalité maternelle élevée malgré des ressources disponibles",
                "Accès aux soins anténataux insuffisant — couverture rurale et zones de conflit déficitaires",
                "Inégalités de genre freinant le recours aux soins — barrières culturelles et économiques persistantes",
            ]
        if self.risk_level == "modéré":
            return [
                f"Lacunes persistantes en santé maternelle dans {n} — disparités rural-urbain et inégalités sociales",
                "Progrès insuffisants vers les objectifs ODD de réduction de mortalité maternelle",
                "Formation des personnels de santé obstétricaux insuffisante dans les zones reculées",
            ]
        return [
            f"{n} maintient un système de santé maternelle performant — mortalité maternelle maîtrisée",
            "Couverture obstétricale universelle avec accès équitable aux soins anténataux et postnataux",
            "Modèle de santé maternelle à diffuser — investissement public fort et approche genrée des soins",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "healthcare_system_collapse_score": self.healthcare_system_collapse_score,
            "gender_inequality_score": self.gender_inequality_score,
            "obstetric_access_deficit_score": self.obstetric_access_deficit_score,
            "conflict_health_impact_score": self.conflict_health_impact_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_maternal_risk_index": self.estimated_maternal_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[MaternalMortalityEntity] = [
    MaternalMortalityEntity("MM-001", "Sierra Leone — Mortalité Maternelle Record", "Afrique de l'Ouest", "1er Taux Mondial — 443 Décès/100k Naissances Vivantes", 92.0, 88.0, 90.0, 78.0),
    MaternalMortalityEntity("MM-002", "Tchad & Niger — Sahel Obstétrical", "Afrique Subsaharienne", "Crise Obstétricale Silencieuse dans les Déserts Médicaux", 88.0, 85.0, 87.0, 82.0),
    MaternalMortalityEntity("MM-003", "Somalie & RDC — Conflit & Maternité", "Afrique de l'Est/Centrale", "Conflits Armés Détruisant les Infrastructures Obstétriques", 85.0, 80.0, 82.0, 92.0),
    MaternalMortalityEntity("MM-004", "Afghanistan — Régime Taliban & Santé Féminine", "Asie Centrale", "Interdiction des Soignantes Féminines — Crise Obstétricale Délibérée", 78.0, 95.0, 85.0, 70.0),
    MaternalMortalityEntity("MM-005", "Haïti — Effondrement Sanitaire Post-Séisme", "Amériques", "Gangs Bloquant l'Accès aux Maternités — Crise Urbaine", 72.0, 68.0, 75.0, 80.0),
    MaternalMortalityEntity("MM-006", "Inde — Disparités Rurales Persistantes", "Asie du Sud", "Mortalité Maternelle Concentrée en Zones Rurales et Dalits", 45.0, 58.0, 62.0, 35.0),
    MaternalMortalityEntity("MM-007", "Brésil & Mexique — Inégalités Raciales", "Amériques", "Mortalité Maternelle Disproportionnée chez les Femmes Noires/Indigènes", 38.0, 42.0, 40.0, 28.0),
    MaternalMortalityEntity("MM-008", "Scandinavie & Canada — Excellence Obstétricale", "Global Nord", "Mortalité Maternelle Quasi-Nulle — Modèles Universels", 5.0, 8.0, 4.0, 3.0),
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
        "domain": "maternal_mortality",
        "confidence_score": 0.91,
        "data_sources": ["who_maternal_mortality_estimates", "unfpa_obstetric_fistula_tracker", "unicef_antenatal_care_coverage"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_maternal_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_maternal_mortality() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Maternal Mortality Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
