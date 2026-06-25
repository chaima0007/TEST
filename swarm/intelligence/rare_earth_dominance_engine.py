"""
Caelum Partners — Rare Earth Dominance Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La domination chinoise des terres rares comme levier géopolitique critique :
la Chine contrôle 85% du raffinage mondial des terres rares (REE — Rare
Earth Elements), 60% de l'extraction, et détient les brevets clés du
traitement. Ces 17 métaux sont irremplaçables dans les batteries des
véhicules électriques, les éoliennes, les semi-conducteurs, les missiles
de précision, les moteurs d'avion et les smartphones.

La dépendance occidentale aux REE chinoises est une vulnérabilité
stratégique de premier ordre : Pékin peut couper l'approvisionnement
en représailles à des sanctions (comme en 2010 contre le Japon) ou
comme levier dans les négociations commerciales. La course aux alternatives
(mines australiennes, canadiennes, africaines) est en cours mais la Chine
conserve une avance technologique et industrielle décisive. Les REE sont
les nouveaux hydrocarbures — qui les contrôle contrôle la transition
énergétique et la supériorité militaire du XXIe siècle.

Risk levels (dépendance aux terres rares et vulnérabilité stratégique) :
  critique  → composite ≥ 60  (vulnérabilité stratégique majeure aux REE chinoises)
  élevé     → composite ≥ 40  (dépendance significative sans diversification suffisante)
  modéré    → composite ≥ 20  (exposition REE à gérer activement)
  faible    → composite < 20  (diversification REE suffisante ou production domestique)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "monopole_extraction_total": {
        "severity_fr": "Critique",
        "action_fr": "Diversification d'urgence des sources d'approvisionnement REE et stockpiles stratégiques nationaux",
        "signal_fr": "chinese_supply_dependency > 80 AND processing_monopoly > 75 — monopole extraction et raffinage total",
    },
    "capture_technologique": {
        "severity_fr": "Critique",
        "action_fr": "Investissements massifs en R&D pour alternatives aux REE et recyclage circulaire",
        "signal_fr": "Capture technologique — brevets de traitement REE concentrés en Chine sans alternative viable",
    },
    "dependance_sectorielle": {
        "severity_fr": "Élevé",
        "action_fr": "Accords de diversification avec pays producteurs alternatifs (Australie, Canada, Afrique)",
        "signal_fr": "Dépendance sectorielle aux REE — industries critiques exposées aux décisions chinoises",
    },
    "transition_en_cours": {
        "severity_fr": "Modéré",
        "action_fr": "Accélérer la diversification des fournisseurs REE et développer les capacités de recyclage",
        "signal_fr": "Transition en cours — alternatives REE en développement mais dépendance résiduelle significative",
    },
    "souverainete_minerale": {
        "severity_fr": "Faible",
        "action_fr": "Maintenir les investissements en souveraineté minérale et partager les bonnes pratiques",
        "signal_fr": "composite_score < 20 — souveraineté minérale préservée avec diversification REE robuste",
    },
}


@dataclass
class RareEarthDominanceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    chinese_supply_dependency_score: float
    processing_monopoly_score: float
    strategic_sector_exposure_score: float
    alternative_source_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_ree_vulnerability_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.chinese_supply_dependency_score * 0.30
            + self.processing_monopoly_score * 0.25
            + self.strategic_sector_exposure_score * 0.25
            + self.alternative_source_deficit_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_ree_vulnerability_index = round(self.composite_score / 100 * 10, 2)

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
        if self.chinese_supply_dependency_score >= 80 and self.processing_monopoly_score >= 75:
            return "monopole_extraction_total"
        if self.processing_monopoly_score >= 75:
            return "capture_technologique"
        if self.composite_score >= 40:
            return "dependance_sectorielle"
        if self.composite_score >= 20:
            return "transition_en_cours"
        return "souverainete_minerale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Vulnérabilité stratégique majeure de {n} — dépendance critique aux terres rares chinoises",
                "Monopole chinois du raffinage REE — aucune alternative industrielle à l'échelle pour les secteurs critiques",
                "Exposition militaire et technologique — défense, véhicules électriques et semi-conducteurs sous dépendance REE",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dépendance significative de {n} aux terres rares chinoises — secteurs critiques vulnérables",
                "Concentration du raffinage REE en Chine — chaînes d'approvisionnement fragiles en cas de tensions",
                "Diversification insuffisante — alternatives australiennes, canadiennes et africaines encore insuffisantes",
            ]
        if self.risk_level == "modéré":
            return [
                f"Exposition REE modérée dans {n} — transition de diversification en cours mais incomplète",
                "Investissements en cours dans des sources alternatives mais délais industriels longs",
                "Recyclage REE en développement — réduction progressive de la dépendance aux nouvelles extractions",
            ]
        return [
            f"{n} préserve sa souveraineté minérale — diversification REE robuste et production domestique",
            "Sources d'approvisionnement REE diversifiées — pas de dépendance critique à un fournisseur unique",
            "Modèle de souveraineté minérale à partager — investissements précoces dans l'extraction et le recyclage REE",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "chinese_supply_dependency_score": self.chinese_supply_dependency_score,
            "processing_monopoly_score": self.processing_monopoly_score,
            "strategic_sector_exposure_score": self.strategic_sector_exposure_score,
            "alternative_source_deficit_score": self.alternative_source_deficit_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ree_vulnerability_index": self.estimated_ree_vulnerability_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[RareEarthDominanceEntity] = [
    RareEarthDominanceEntity("RE-001", "UE — Dépendance Industrielle Critique", "Europe", "Industrie Automobile & Éolienne 95% Dépendante REE Chinoises", 88.0, 90.0, 85.0, 82.0),
    RareEarthDominanceEntity("RE-002", "USA — Défense & Semi-Conducteurs Exposés", "Amérique du Nord", "Missiles Guidés, Moteurs F-35 et Puces TSMC sous REE Chinoises", 75.0, 82.0, 88.0, 78.0),
    RareEarthDominanceEntity("RE-003", "Japon — Leçon 2010 Non Oubliée", "Asie", "Embargo REE Chine 2010 — Diversification Partielle mais Incomplète", 65.0, 80.0, 75.0, 60.0),
    RareEarthDominanceEntity("RE-004", "Corée du Sud & Taïwan — Semi-Conducteurs REE", "Asie", "TSMC/Samsung Dépendant des REE Chinoises pour Wafers & Magnets", 72.0, 75.0, 82.0, 68.0),
    RareEarthDominanceEntity("RE-005", "Inde — Extraction Sous-Développée", "Asie du Sud", "Réserves REE Conséquentes mais Raffinage Inexistant — Paradoxe", 55.0, 68.0, 52.0, 58.0),
    RareEarthDominanceEntity("RE-006", "Australie & Canada — Alternatives en Transition", "Global Occident", "Mines Pilbara & Québec — Alternatives en Construction sous Pression", 52.0, 58.0, 48.0, 42.0),
    RareEarthDominanceEntity("RE-007", "Afrique — Réserves sans Chaîne de Valeur", "Afrique", "RDC/Malawi/Tanzanie Riches en REE — Exportation Brute sans Raffinage", 22.0, 28.0, 20.0, 22.0),
    RareEarthDominanceEntity("RE-008", "Chine — Monopole Mondial REE", "Asie", "85% du Raffinage Mondial — Producteur Dominant sans Vulnérabilité REE", 5.0, 8.0, 5.0, 3.0),
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
        "domain": "rare_earth",
        "confidence_score": 0.85,
        "data_sources": ["usgs_mineral_resources_survey", "iea_critical_minerals_tracker", "roskill_rare_earth_outlook"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_ree_vulnerability_index": round(avg / 100 * 10, 2),
    }


def analyze_rare_earth_dominance() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Rare Earth Dominance Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
