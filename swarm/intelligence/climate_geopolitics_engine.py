"""
Caelum Partners — Climate Geopolitics Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La géopolitique climatique : quand le changement climatique redessine les rapports de force mondiaux.
Le changement climatique n'est pas seulement une crise environnementale — c'est
un multiplicateur de menaces géopolitiques sans précédent qui remodèle les équilibres
de puissance, crée de nouvelles ressources stratégiques et déclenche des migrations
de masse susceptibles de déstabiliser les démocraties occidentales.

L'Arctique est devenu le nouveau champ de bataille géopolitique prioritaire : le
dégel de la calotte polaire ouvre des routes commerciales raccourcissant de 40% le
transit entre l'Asie et l'Europe, déverrouille 90 milliards de barils de pétrole
et 47 000 milliards de m³ de gaz. La Russie a militarisé l'Arctique avec 14 bases
militaires nouvelles, des missiles S-400 déployés et des brise-glaces nucléaires.
La Chine se qualifie d'État "quasi-arctique" malgré l'absence de territoire.

Le monopole chinois sur les terres rares (85% de la production mondiale) et les
technologies solaires/éoliennes (80% des panneaux, 70% des batteries) constitue
un vecteur de dépendance technologique que Pékin utilise déjà comme levier
géopolitique. La Turquie weaponise les migrations climatiques en relâchant les
flux de réfugiés vers l'Europe. La Biélorussie de Lukashenka a instrumentalisé
les migrants climatiques comme arme hybride contre la Pologne et les Pays-Bas.

Risk levels (géopolitique climatique et weaponisation des ressources vertes) :
  critique  → composite ≥ 60  (arme climatique — militarisation de l'Arctique ou monopole technologie verte)
  élevé     → composite ≥ 40  (pression climatique géopolitique — exploitation des vulnérabilités climatiques adverses)
  modéré    → composite ≥ 20  (transition géopolitique — reconfigurations en cours sans weaponisation active)
  faible    → composite < 20  (leadership climatique coopératif — Accords de Paris et diplomatie verte exemplaires)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "militarisation_arctique_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Traité arctique militaire — moratoire sur les nouvelles installations militaires, mécanisme de résolution des différends frontaliers arctiques et partage des données climatiques souveraines",
        "signal_fr": "arctic_resources_militarization_score > 85 AND green_tech_monopoly_score > 85 — militarisation arctique combinée au monopole des technologies vertes comme double levier de domination géopolitique",
    },
    "weaponisation_migrations_climatiques": {
        "severity_fr": "Critique",
        "action_fr": "Cadre juridique migrations climatiques — statut de réfugié climatique reconnu, fonds d'adaptation dans les pays émetteurs et sanctions contre la weaponisation des flux migratoires",
        "signal_fr": "climate_migration_weaponization_score > 85 — weaponisation active des migrations climatiques comme outil de déstabilisation des démocraties d'accueil",
    },
    "monopole_technologie_verte": {
        "severity_fr": "Critique",
        "action_fr": "Diversification technologique verte — investissements massifs dans les chaînes de valeur alternatives, Minerals Security Partnership élargi et audit des dépendances aux terres rares chinoises",
        "signal_fr": "green_tech_monopoly_score > 85 — monopole sur les technologies de transition énergétique comme levier de dépendance stratégique imposable aux adversaires",
    },
    "pression_climatique_geopolitique": {
        "severity_fr": "Élevé",
        "action_fr": "Diplomatie climatique multilatérale — COP renforcée avec mécanismes de sanctions contraignants, fonds pertes et dommages opérationnel et transferts technologiques conditionnels",
        "signal_fr": "Pression climatique géopolitique — exploitation des vulnérabilités climatiques adverses sans qualification de weaponisation systémique",
    },
    "leadership_climatique_cooperatif": {
        "severity_fr": "Faible",
        "action_fr": "Exporter le modèle climatique coopératif — financement du Fonds Vert pour le Climat, transferts de technologie verte et diplomatie climatique inclusive dans les pays les plus vulnérables",
        "signal_fr": "composite_score < 20 — leadership climatique exemplaire via les Accords de Paris, financement climatique et diplomatie verte multilatérale",
    },
}


@dataclass
class ClimateGeopoliticsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    arctic_resources_militarization_score: float
    climate_migration_weaponization_score: float
    green_tech_monopoly_score: float
    climate_sabotage_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_climate_geopolitics_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.arctic_resources_militarization_score * 0.30
            + self.climate_migration_weaponization_score * 0.25
            + self.green_tech_monopoly_score * 0.25
            + self.climate_sabotage_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_climate_geopolitics_index = round(self.composite_score / 100 * 10, 2)

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
        if self.arctic_resources_militarization_score >= 85 and self.green_tech_monopoly_score >= 85:
            return "militarisation_arctique_strategique"
        if self.climate_migration_weaponization_score >= 85:
            return "weaponisation_migrations_climatiques"
        if self.green_tech_monopoly_score >= 85:
            return "monopole_technologie_verte"
        if self.composite_score >= 20:
            return "pression_climatique_geopolitique"
        return "leadership_climatique_cooperatif"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Weaponisation climatique de {n} — exploitation des ressources arctiques, monopoles technologiques verts ou migrations climatiques comme instruments de puissance géopolitique",
                "Domination des ressources de la transition — contrôle des terres rares, batteries et énergies renouvelables comme levier de dépendance stratégique imposable aux démocraties",
                "Escalade géopolitique climatique — la compétition pour les ressources arctiques et les technologies vertes crée des tensions risquant d'éclater en conflits ouverts",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression climatique géopolitique de {n} — exploitation des vulnérabilités climatiques adverses comme outil de coercition sans weaponisation systémique avérée",
                "Compétition pour les ressources de transition — course aux minerais critiques, terres rares et positions arctiques sans règles du jeu claires",
                "Risque de conflits climatiques — les migrations massives induites par le réchauffement alimentent les tensions politiques internes et les crises humanitaires régionales",
            ]
        if self.risk_level == "modéré":
            return [
                f"Transition géopolitique de {n} — reconfigurations des équilibres de puissance liées au changement climatique sans weaponisation active documentée",
                "Vulnérabilités émergentes — dépendances énergétiques fossiles ou aux technologies vertes étrangères créant des expositions géopolitiques croissantes",
                "Risque de bascule — l'aggravation du changement climatique pourrait transformer des vulnérabilités actuelles en crises sécuritaires majeures",
            ]
        return [
            f"{n} incarne le leadership climatique coopératif — financement du Fonds Vert, Accords de Paris respectés et diplomatie climatique inclusive exemplaire",
            "Transition verte exemplaire — déploiement massif des énergies renouvelables domestiques et exportation de technologies vertes sans conditions géopolitiques",
            "Modèle de coopération climatique — partage des données, transferts technologiques et mécanismes d'adaptation pour les États les plus vulnérables",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "arctic_resources_militarization_score": self.arctic_resources_militarization_score,
            "climate_migration_weaponization_score": self.climate_migration_weaponization_score,
            "green_tech_monopoly_score": self.green_tech_monopoly_score,
            "climate_sabotage_score": self.climate_sabotage_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_climate_geopolitics_index": self.estimated_climate_geopolitics_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ClimateGeopoliticsEntity] = [
    ClimateGeopoliticsEntity("CG-001", "Chine — Monopole Terres Rares & BeiDou Vert Stratégique", "Asie", "85% Terres Rares Mondiales, 80% Panneaux Solaires, 70% Batteries & BRI Dépendances Tech Verte", 80.0, 75.0, 92.0, 72.0),
    ClimateGeopoliticsEntity("CG-002", "Russie — Militarisation Arctique & Sabotage Énergies Vertes", "Europe de l'Est", "14 Bases Arctiques Nouvelles, Sabotage Nord Stream & Désinformation Énergies Vertes Via RT/Sputnik", 92.0, 82.0, 45.0, 88.0),
    ClimateGeopoliticsEntity("CG-003", "USA — Sanctions Climatiques & Domination Technologique Verte", "Amérique du Nord", "IRA 369Md$ Subventions Tech Verte, Minerals Security Partnership & Sanctions Pétrole Adversaires", 85.0, 70.0, 80.0, 78.0),
    ClimateGeopoliticsEntity("CG-004", "Turquie & Biélorussie — Weaponisation Migrations Climatiques", "MENA/Europe", "Turquie 4M Réfugiés Levier UE, Lukashenka Migrants Irak/Syrie Pologne & Frontex Instrumentalisée", 72.0, 88.0, 55.0, 68.0),
    ClimateGeopoliticsEntity("CG-005", "Arabie Saoudite & OPEP — Sabotage Transition Énergétique", "MENA", "OPEP+ Cuts Stratégiques, Lobbying COP Combustibles Fossiles & Saudi Aramco 2050 Net Zero Fictif", 48.0, 45.0, 38.0, 75.0),
    ClimateGeopoliticsEntity("CG-006", "Australie & Canada — Ressources Minérales Critiques", "Pacifique/Amérique", "Lithium/Nickel/Cobalt Stratégiques, AUKUS Arctique & Minéraux Critiques vs Chine Alternatives", 55.0, 42.0, 62.0, 42.0),
    ClimateGeopoliticsEntity("CG-007", "Inde — Émissions & Vulnérabilité Climatique Croissante", "Asie du Sud", "3ème Émetteur Mondial, Fonte Glaciers Himalaya 800M, Canicules Mortelles & Stress Hydrique Ganges", 30.0, 28.0, 38.0, 25.0),
    ClimateGeopoliticsEntity("CG-008", "UE & Accords Paris — Leadership Climatique Coopératif", "Europe", "Pacte Vert 55% Réduction 2030, Fonds Vert 100Md$/An & CBAM Taxe Carbone Frontières Mondiale", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "climate_geopolitics",
        "confidence_score": 0.76,
        "data_sources": ["ipcc_sixth_assessment_report", "arctic_council_monitoring", "iea_critical_minerals_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_climate_geopolitics_index": round(avg / 100 * 10, 2),
    }


def analyze_climate_geopolitics() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Climate Geopolitics Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
