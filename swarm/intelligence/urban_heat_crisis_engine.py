"""
Caelum Partners — Urban Heat Crisis Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La chaleur urbaine extrême comme enjeu géopolitique, social et
migratoire du XXIe siècle : l'effet d'îlot de chaleur urbain (ICU)
transforme les mégapoles du Sud global en zones de survie impossible
pendant les mois d'été. À 50°C dans les rues de Karachi, Baghdad,
Phoenix ou Delhi, les corps humains cessent de fonctionner. Les
climatiseurs consomment jusqu'à 70% de l'électricité locale, créant
des spirales infernales de consommation-émission-réchauffement.

La chaleur urbaine extrême n'est pas seulement un problème environnemental :
c'est un accélérateur de migrations forcées, un révélateur d'inégalités
(les pauvres sans climatisation meurent, les riches survivent), un
déstabilisateur de gouvernements (quand l'État ne peut plus protéger
ses citoyens de la chaleur), et un multiplicateur de stress hydrique.
Les vagues de chaleur tuent déjà plus de personnes que n'importe quelle
autre catastrophe naturelle dans de nombreux pays. Ce n'est que le début.

Risk levels (vulnérabilité à la crise de chaleur urbaine) :
  critique  → composite ≥ 60  (chaleur urbaine menaçant la survie et la stabilité)
  élevé     → composite ≥ 40  (stress thermique urbain sévère sans adaptation suffisante)
  modéré    → composite ≥ 20  (risques de chaleur urbaine à gérer activement)
  faible    → composite < 20  (adaptation urbaine à la chaleur satisfaisante)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "zone_inhabitabilite_imminente": {
        "severity_fr": "Critique",
        "action_fr": "Plan d'urgence climatisation publique et relogement des populations les plus vulnérables",
        "signal_fr": "peak_temperature_score > 80 AND cooling_infrastructure_deficit > 75 — zone d'inhabilitabilité",
    },
    "migration_thermique_forcee": {
        "severity_fr": "Critique",
        "action_fr": "Corridors de migration climatique et accueil des réfugiés climatiques thermiques",
        "signal_fr": "Migration thermique forcée — populations fuyant des villes devenues invivables en été",
    },
    "stress_energetique_thermique": {
        "severity_fr": "Élevé",
        "action_fr": "Investissements massifs en infrastructure de refroidissement et réseaux électriques résilients",
        "signal_fr": "Stress énergétique thermique — demande de climatisation saturant les réseaux électriques",
    },
    "inegalites_thermiques": {
        "severity_fr": "Modéré",
        "action_fr": "Programmes de végétalisation urbaine et climatisation publique pour les quartiers défavorisés",
        "signal_fr": "Inégalités thermiques — populations pauvres surexposées à la chaleur sans accès au refroidissement",
    },
    "adaptation_reussie": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles d'adaptation urbaine à la chaleur et soutenir les villes vulnérables",
        "signal_fr": "composite_score < 20 — adaptation urbaine à la chaleur réussie avec infrastructure adéquate",
    },
}


@dataclass
class UrbanHeatCrisisEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    peak_temperature_score: float
    cooling_infrastructure_deficit_score: float
    social_vulnerability_score: float
    energy_grid_saturation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_heat_crisis_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.peak_temperature_score * 0.30
            + self.cooling_infrastructure_deficit_score * 0.25
            + self.social_vulnerability_score * 0.25
            + self.energy_grid_saturation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_heat_crisis_index = round(self.composite_score / 100 * 10, 2)

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
        if self.peak_temperature_score >= 80 and self.cooling_infrastructure_deficit_score >= 75:
            return "zone_inhabitabilite_imminente"
        if self.social_vulnerability_score >= 80:
            return "migration_thermique_forcee"
        if self.composite_score >= 40:
            return "stress_energetique_thermique"
        if self.composite_score >= 20:
            return "inegalites_thermiques"
        return "adaptation_reussie"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Crise de chaleur urbaine critique dans {n} — températures extrêmes menaçant la vie humaine et la stabilité",
                "Déficit d'infrastructure de refroidissement — populations vulnérables sans accès à la climatisation ou à l'eau",
                "Spirale thermique-énergétique — demande de refroidissement saturant les réseaux et amplifiant le réchauffement",
            ]
        if self.risk_level == "élevé":
            return [
                f"Stress thermique urbain sévère dans {n} — vagues de chaleur récurrentes sans adaptation suffisante",
                "Inégalités d'accès au refroidissement — pauvres surexposés à la chaleur dans des logements non-climatisés",
                "Réseau électrique sous tension maximale lors des pics de chaleur — risques de pannes en cascade",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risques de chaleur urbaine dans {n} — tendances au réchauffement nécessitant adaptation préventive",
                "Végétalisation urbaine insuffisante — manque d'espaces verts aggravant l'effet d'îlot de chaleur",
                "Plans d'adaptation climatique en développement — délais de mise en œuvre à accélérer",
            ]
        return [
            f"{n} a réussi son adaptation urbaine à la chaleur — végétalisation, architecture bioclimatique et réseaux résilients",
            "Infrastructure de refroidissement accessible à tous — climatisation publique et espaces rafraîchissants inclusifs",
            "Modèle d'adaptation thermique urbaine à partager — réduction de l'îlot de chaleur par design urbain",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "peak_temperature_score": self.peak_temperature_score,
            "cooling_infrastructure_deficit_score": self.cooling_infrastructure_deficit_score,
            "social_vulnerability_score": self.social_vulnerability_score,
            "energy_grid_saturation_score": self.energy_grid_saturation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_heat_crisis_index": self.estimated_heat_crisis_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[UrbanHeatCrisisEntity] = [
    UrbanHeatCrisisEntity("UH-001", "Baghdad & Bassora — Villes au-delà du Vivable", "MENA", "50°C Estivaux & Coupures Électriques Chroniques — Exode Thermique", 95.0, 90.0, 88.0, 85.0),
    UrbanHeatCrisisEntity("UH-002", "Karachi & Delhi — Méga-Cités Thermiques", "Asie du Sud", "Canicules Meurtrières 45-50°C — Bidonvilles sans Climatisation", 90.0, 85.0, 92.0, 80.0),
    UrbanHeatCrisisEntity("UH-003", "Phoenix & Las Vegas — Déserts Urbanisés", "Amérique du Nord", "55°C Sol, Étalement Urbain & Dépendance Totale à la Climatisation", 88.0, 78.0, 65.0, 90.0),
    UrbanHeatCrisisEntity("UH-004", "Lagos & Accra — Côtes d'Afrique Tropicale", "Afrique de l'Ouest", "Chaleur Tropicale & Humidité — Villes de 15M+ sans Infrastructure Froide", 82.0, 88.0, 85.0, 72.0),
    UrbanHeatCrisisEntity("UH-005", "Shanghai & Chongqing — Fours Urbains", "Asie", "45°C Estivaux & 400M de Climatiseurs — Spirale Énergétique-Thermique", 50.0, 45.0, 42.0, 55.0),
    UrbanHeatCrisisEntity("UH-006", "Madrid & Athènes — Méditerranée Brûlante", "Europe du Sud", "Canicules Annuelles & Vieux Bâtiments Non-Isolés — Mortalité Estivale", 45.0, 42.0, 45.0, 40.0),
    UrbanHeatCrisisEntity("UH-007", "São Paulo & Rio — Chaleur Inégalitaire", "Amériques", "Favelas Surchauffées vs Quartiers Climatisés — Apartheid Thermique", 35.0, 38.0, 45.0, 30.0),
    UrbanHeatCrisisEntity("UH-008", "Singapour & Rotterdam — Adaptation Exemplaire", "Asie/Europe", "Architecture Bioclimatique, Toits Verts & Refroidissement District", 18.0, 12.0, 10.0, 8.0),
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
        "domain": "urban_heat",
        "confidence_score": 0.87,
        "data_sources": ["copernicus_climate_change_service", "urban_heat_island_effect_monitor", "who_heat_health_action_plans"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_heat_crisis_index": round(avg / 100 * 10, 2),
    }


def analyze_urban_heat_crisis() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Urban Heat Crisis Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
