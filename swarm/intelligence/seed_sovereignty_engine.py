"""
Caelum Partners — Seed Sovereignty Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le contrôle des semences comme arme géopolitique : quand quelques
multinationales détiennent les brevets sur 70% des semences mondiales,
quand les OGM propriétaires remplacent les variétés ancestrales,
quand les agriculteurs ne peuvent plus replanter sans payer une licence,
c'est la souveraineté alimentaire des nations qui est confisquée.

La semence n'est pas un produit industriel — c'est le code source
du vivant, la mémoire génétique de dix millénaires d'agriculture,
et le vecteur de dépendance le plus profond qui soit. Qui contrôle
les semences contrôle l'alimentation. Qui contrôle l'alimentation
contrôle les peuples. La guerre des semences est la guerre alimentaire
la plus silencieuse et la plus durable du XXIe siècle.

Risk levels (menace sur la souveraineté semencière) :
  critique  → composite ≥ 60  (dépendance semencière totale)
  élevé     → composite ≥ 40  (érosion de l'autonomie génétique)
  modéré    → composite ≥ 20  (pression sur la biodiversité agricole)
  faible    → composite < 20  (souveraineté semencière préservée)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "dependance_semenciere_totale": {
        "severity_fr": "Critique",
        "action_fr": "Programmes d'urgence de conservation des variétés paysannes et interdiction des brevets sur le vivant",
        "signal_fr": "corporate_seed_control > 80 AND genetic_erosion > 75 — dépendance semencière totale",
    },
    "erosion_genetique_critique": {
        "severity_fr": "Critique",
        "action_fr": "Banques de semences nationales renforcées et réglementation stricte des OGM propriétaires",
        "signal_fr": "Érosion génétique critique — variétés ancestrales disparaissant sous pression des semences commerciales",
    },
    "oligopole_semencier": {
        "severity_fr": "Élevé",
        "action_fr": "Politiques anti-monopole semencier et soutien aux programmes de sélection paysanne",
        "signal_fr": "Oligopole semencier dominant — dépendance croissante aux multinationales des semences",
    },
    "pression_biodiversite": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des droits des agriculteurs sur les semences et protection des variétés locales",
        "signal_fr": "Pression sur la biodiversité agricole — équilibre fragile entre semences commerciales et paysannes",
    },
    "souverainete_preservee": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des politiques de conservation et des droits des paysans sur leurs semences",
        "signal_fr": "composite_score < 20 — souveraineté semencière préservée, biodiversité agricole protégée",
    },
}


@dataclass
class SeedSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    corporate_seed_control_score: float
    genetic_erosion_score: float
    farmer_seed_rights_violation_score: float
    gmo_dependency_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_seed_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.corporate_seed_control_score * 0.30
            + self.genetic_erosion_score * 0.25
            + self.farmer_seed_rights_violation_score * 0.25
            + self.gmo_dependency_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_seed_risk_index = round(self.composite_score / 100 * 10, 2)

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
        if self.corporate_seed_control_score >= 80 and self.genetic_erosion_score >= 75:
            return "dependance_semenciere_totale"
        if self.genetic_erosion_score >= 70:
            return "erosion_genetique_critique"
        if self.composite_score >= 45:
            return "oligopole_semencier"
        if self.composite_score >= 25:
            return "pression_biodiversite"
        return "souverainete_preservee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Dépendance semencière totale dans {n} — souveraineté alimentaire confisquée par les multinationales",
                "Érosion génétique irréversible — variétés ancestrales disparaissant sous brevets corporatifs",
                "Agriculteurs condamnés à acheter des semences chaque saison — fin du droit millénaire de replanter",
            ]
        if self.risk_level == "élevé":
            return [
                f"Oligopole semencier dominant dans {n} — dépendance croissante aux 4 géants mondiaux",
                "Biodiversité agricole en déclin accéléré — homogénéisation génétique fragilisant la résilience",
                "Droits paysans sur les semences érodés par la pression commerciale et les brevets",
            ]
        if self.risk_level == "modéré":
            return [
                f"Pression sur la biodiversité agricole dans {n} — équilibre fragile semences commerciales/paysannes",
                "Concentration semencière partielle — variétés locales encore présentes mais menacées",
                "Législation semencière insuffisante pour protéger pleinement la souveraineté des agriculteurs",
            ]
        return [
            f"{n} préserve sa souveraineté semencière — biodiversité agricole et droits paysans protégés",
            "Banques de semences actives et programmes de sélection paysanne opérationnels",
            "Modèle de résistance à l'oligopole semencier à valoriser et diffuser mondialement",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "corporate_seed_control_score": self.corporate_seed_control_score,
            "genetic_erosion_score": self.genetic_erosion_score,
            "farmer_seed_rights_violation_score": self.farmer_seed_rights_violation_score,
            "gmo_dependency_score": self.gmo_dependency_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_seed_risk_index": self.estimated_seed_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SeedSovereigntyEntity] = [
    SeedSovereigntyEntity("SS-001", "Amérique Centrale & Caraïbes", "Amériques", "Monocultures OGM & Brevets Monsanto/Bayer", 92.0, 88.0, 90.0, 85.0),
    SeedSovereigntyEntity("SS-002", "Afrique Subsaharienne — Semences Hybrides", "Afrique", "Green Revolution 2.0 & Perte Variétés Ancestrales", 85.0, 82.0, 88.0, 78.0),
    SeedSovereigntyEntity("SS-003", "Inde — Coton OGM & Suicide des Agriculteurs", "Asie du Sud", "Bt Cotton Monopoly & Dépendance Chimique Totale", 80.0, 85.0, 82.0, 88.0),
    SeedSovereigntyEntity("SS-004", "USA — Berceau de l'Oligopole Semencier", "Amérique du Nord", "Bayer/Corteva/Syngenta/BASF Dominant le Marché", 90.0, 72.0, 75.0, 80.0),
    SeedSovereigntyEntity("SS-005", "Brésil — Agrobusiness & Soja OGM", "Amériques", "96% Soja OGM & Dépendance aux Géants Semenciers", 78.0, 68.0, 72.0, 82.0),
    SeedSovereigntyEntity("SS-006", "Europe — Résistance au Tout-OGM", "Europe", "Réglementation OGM Stricte mais Concentration Croissante", 50.0, 42.0, 38.0, 35.0),
    SeedSovereigntyEntity("SS-007", "Pérou & Bolivie — Patrimoine Andin", "Amériques", "Protection des Variétés Ancestrales de Pomme de Terre", 28.0, 25.0, 22.0, 18.0),
    SeedSovereigntyEntity("SS-008", "Suisse (FiBL) & Pays-Bas (Wageningen)", "Europe", "Recherche Semencière Publique & Biodiversité Exemplaire", 15.0, 10.0, 12.0, 8.0),
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
        "domain": "seed_sovr",
        "confidence_score": 0.84,
        "data_sources": ["grain_seed_sovereignty_index", "fao_plant_genetic_resources", "eto_corporate_seed_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_seed_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_seed_sovereignty() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Seed Sovereignty Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
