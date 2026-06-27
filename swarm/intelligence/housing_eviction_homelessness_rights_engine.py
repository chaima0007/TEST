"""
Caelum Partners — Housing, Eviction & Homelessness Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droit au logement convenable face aux expulsions forcées et à la criminalisation des sans-abri.
Le droit au logement convenable, consacré à l'article 11 du Pacte International relatif aux
Droits Économiques, Sociaux et Culturels (PIDESC) et précisé par l'Observation Générale n°4
du Comité DESC, est l'un des droits humains les plus systématiquement violés à travers le monde.
Les expulsions forcées, la criminalisation des sans-domicile-fixe et l'inaccessibilité du
logement abordable constituent les trois vecteurs principaux de cette crise mondiale.

En Inde, la pratique du "Bulldozer Justice" — démolition extrajudiciaire de maisons appartenant
à des minorités musulmanes — a déplacé des millions de personnes sans relogement. Au Kenya, les
bidonvilles de Nairobi comme Kibera (250 000 habitants sur 2.5 km²) font l'objet d'expulsions
répétées pour des projets immobiliers ou d'infrastructure. Au Brésil, les favelas sont ciblées
par des évictions massives lors des grands événements sportifs (Coupe du Monde 2014, JO 2016).
Aux États-Unis, 580 000 sans-abri font face à la criminalisation de leur situation via des
lois anti-camping adoptées dans 23 États suite à l'arrêt Grants Pass v. Johnson (2024).

Risk levels (droit au logement et expulsions) :
  critique  → composite ≥ 60  (crise systémique — expulsions forcées massives et criminalisation)
  élevé     → composite ≥ 40  (violations graves — expulsions répétées et insécurité foncière)
  modéré    → composite ≥ 20  (dérive politique — restrictions croissantes du droit au logement)
  faible    → composite < 20  (protection exemplaire — droit au logement effectif et recours disponibles)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "expulsions_forcees_minorites": {
        "severity_fr": "Critique",
        "action_fr": "Moratoire sur les démolitions — interdiction des expulsions sans relogement préalable et réparations pour les victimes de Bulldozer Justice",
        "signal_fr": "forced_eviction_score > 85 AND land_tenure_score > 85 — expulsions forcées massives ciblant les minorités et les populations pauvres sans protection légale",
    },
    "evictions_slums_projets_infra": {
        "severity_fr": "Critique",
        "action_fr": "Principes Pinheiro — application des principes de restitution des logements et des terres pour les déplacés et rétablissement de la tenure sécurisée",
        "signal_fr": "forced_eviction_score > 80 — expulsions massives de bidonvilles pour projets d'infrastructure sans relogement décent ni compensation juste",
    },
    "criminalisation_sdf_anti_camping": {
        "severity_fr": "Critique",
        "action_fr": "Logement d'abord — Housing First policies et abrogation des lois anti-camping inconstitutionnelles ciblant les personnes sans-abri",
        "signal_fr": "homelessness_criminalization_score > 80 — criminalisation systématique des personnes sans-abri via lois anti-camping et sweeps des campements",
    },
    "insecurite_fonciere_gentrification": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme foncière — sécurisation de la tenure informelle, encadrement des loyers et protection contre les expulsions gentrification",
        "signal_fr": "Insécurité foncière et gentrification — populations pauvres expulsées par la montée des loyers et l'investissement immobilier spéculatif",
    },
    "protection_droit_logement": {
        "severity_fr": "Faible",
        "action_fr": "Observation Générale 4 — promouvoir les standards de logement convenable via les mécanismes de suivi du Comité DESC et UN-Habitat",
        "signal_fr": "composite_score < 20 — protection exemplaire du droit au logement — mécanismes de monitoring et standards internationaux",
    },
}


@dataclass
class HousingEvictionHomelessnessRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_displacement_severity_score: float
    homelessness_criminalization_scale_score: float
    land_tenure_insecurity_indigenous_score: float
    affordable_housing_right_enforcement_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_housing_eviction_homelessness_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_eviction_displacement_severity_score * 0.30
            + self.homelessness_criminalization_scale_score * 0.25
            + self.land_tenure_insecurity_indigenous_score * 0.25
            + self.affordable_housing_right_enforcement_deficit_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_housing_eviction_homelessness_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.forced_eviction_displacement_severity_score >= 85 and self.land_tenure_insecurity_indigenous_score >= 85:
            return "expulsions_forcees_minorites"
        if self.forced_eviction_displacement_severity_score >= 80:
            return "evictions_slums_projets_infra"
        if self.homelessness_criminalization_scale_score >= 80:
            return "criminalisation_sdf_anti_camping"
        if self.composite_score >= 20:
            return "insecurite_fonciere_gentrification"
        return "protection_droit_logement"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Crise systémique du logement par {n} — expulsions forcées massives sans relogement décent ni compensation juste",
                "Droit au logement bafoué — violations systématiques de l'article 11 PIDESC et de l'Observation Générale n°4 du Comité DESC",
                "Populations vulnérables ciblées — minorités, populations pauvres et autochtones frappées de manière disproportionnée par les expulsions",
            ]
        if self.risk_level == "élevé":
            return [
                f"Violations graves documentées par {n} — expulsions répétées et insécurité foncière touchant des millions de personnes",
                "Logement informel menacé — bidonvilles et squats sous pression des projets d'infrastructure et de la gentrification",
                "Anti-camping laws — criminalisation des personnes sans-abri et sweeps policiers des campements informels",
            ]
        if self.risk_level == "modéré":
            return [
                f"Monitoring et plaidoyer par {n} — documentation des expulsions forcées et promotion des Principes Pinheiro",
                "UN-Habitat standards — mécanismes de suivi des violations du droit au logement dans les pays en développement",
                "Campagnes tenure sécurisée — promotion de la sécurisation foncière pour les 1.8 milliard de personnes sans titre de propriété",
            ]
        return [
            f"{n} protège le droit au logement — cadre normatif et mécanismes de suivi du droit au logement convenable",
            "Observation Générale n°4 — définition des sept composantes du droit au logement convenable selon le Comité DESC",
            "SDG 11.1 — objectif de villes inclusives et d'accès universel à un logement sûr et abordable d'ici 2030",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "forced_eviction_displacement_severity_score": self.forced_eviction_displacement_severity_score,
            "homelessness_criminalization_scale_score": self.homelessness_criminalization_scale_score,
            "land_tenure_insecurity_indigenous_score": self.land_tenure_insecurity_indigenous_score,
            "affordable_housing_right_enforcement_deficit_gap_score": self.affordable_housing_right_enforcement_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_housing_eviction_homelessness_rights_index": self.estimated_housing_eviction_homelessness_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[HousingEvictionHomelessnessRightsEntity] = [
    HousingEvictionHomelessnessRightsEntity(
        "HEH-001",
        "Inde/Bulldozer Justice — Démolitions Maisons Minorités Musulmanes, Expulsions Slums Pré-Olympiques & 15M Déplacés Projets Infra",
        "Inde",
        96.0, 88.0, 92.0, 90.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-002",
        "Kenya/Nairobi — Bidonvilles Kibera Expulsions Répétées, Police Violence Squatters, Tenure Informelle 70% Population & Nairobi Expressway",
        "Kenya",
        90.0, 85.0, 90.0, 88.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-003",
        "Brésil/Rio — Favela Expulsions Coupe Monde/JO, Milice Propriété, Cadastre Exclu Pauvres & Réforme Foncière Bloquée",
        "Brésil",
        88.0, 82.0, 85.0, 85.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-004",
        "USA — Sans-Abri 580 000, Anti-Camping Lois 23 États, Sweeps Camps & Loyers San Francisco/NY Inaccessibles",
        "États-Unis",
        75.0, 88.0, 75.0, 85.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-005",
        "Philippines — Évacuations Forcées Duterte/Marcos, 4M SDF Estimés, Anti-Squatter Laws & DMCI Gentrification",
        "Philippines",
        58.0, 52.0, 55.0, 50.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-006",
        "France/UE — Squats Expulsés Hiver, DALO Droit Non Opposable, Migrants Tentes Évacuées Paris & Loi Anti-Squat",
        "France/Union Européenne",
        50.0, 55.0, 47.0, 55.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-007",
        "UN-Habitat/HIC — Monitoring Expulsions Forcées, Principes Pinheiro, Campagnes Sécurité Tenure & Rapports Fonciers",
        "International",
        25.0, 26.0, 28.0, 24.0,
    ),
    HousingEvictionHomelessnessRightsEntity(
        "HEH-008",
        "ONU/Art.11 DESC — Droit Logement Convenable, Comité DESC Observation Générale 4 & SDG 11.1 Habitat",
        "International",
        4.0, 3.0, 4.0, 5.0,
    ),
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
        "agent": "housing_eviction_homelessness_rights_engine",
        "domain": "housing_eviction_homelessness_rights",
        "total_entities": n,
        "avg_composite": avg,
        "confidence_score": 0.84,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_housing_eviction_homelessness_rights_index": round(avg / 100 * 10, 2),
        "data_sources": [
            "un_habitat_forced_eviction_global_report",
            "cohre_housing_rights_violations_database",
            "feantsa_european_homelessness_monitoring_report",
        ],
        "entities": [e.to_dict() for e in entities],
    }


def analyze_housing_eviction_homelessness_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Housing, Eviction & Homelessness Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    print(f"avg_estimated_index: {r['avg_estimated_housing_eviction_homelessness_rights_index']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name[:60]} → {e.risk_level} ({e.composite_score})")
