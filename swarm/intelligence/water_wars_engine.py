"""
Caelum Partners — Water Wars Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Les guerres de l'eau : la prochaine frontière des conflits géopolitiques.
L'eau douce, ressource vitale et non substituable, devient le pétrole du
XXIe siècle. 40% de la population mondiale vit dans des bassins fluviaux
transfrontaliers où les États amont construisent des barrages géants sans
consulter les États aval — transformant l'eau en arme de pouvoir.

Le GERD éthiopien (Grand Ethiopian Renaissance Dam) sur le Nil menace
l'existence même de l'Égypte, qui dépend à 95% du fleuve. Le Traité des
Eaux de l'Indus entre Inde et Pakistan, vestige de 1960, est désormais
contesté dans le contexte d'hostilité croissante. La Turquie contrôle
les sources de l'Euphrate et du Tigre via les barrages Atatürk et Ilısu,
réduisant le débit irakien et syrien à sa guise. La Chine, pays sourcier
de 8 grands fleuves asiatiques (Mékong, Brahmapoutre, Salouen, Irrawaddy,
Yangtsé, Fleuve Jaune, Tarim, Ili) est la puissance hydraulique la plus
influente du monde — sans avoir signé aucune convention sur les eaux
partagées. La scarcité hydrique amplifie les conflits : d'ici 2050,
5 milliards d'humains vivront sous stress hydrique sévère.

Risk levels (conflictualité hydrique et weaponisation de l'eau) :
  critique  → composite ≥ 60  (guerre de l'eau active ou imminente — existentielle)
  élevé     → composite ≥ 40  (stress hydrique politisé — tensions bilatérales sévères)
  modéré    → composite ≥ 20  (tensions ripariennes gérées — risques de dérapage)
  faible    → composite < 20  (coopération hydraulique exemplaire)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "guerre_eau_active": {
        "severity_fr": "Critique",
        "action_fr": "Médiation internationale urgente sur le partage des eaux et sanctions contre les États weaponisant les fleuves",
        "signal_fr": "transboundary_water_dispute_score > 80 AND dam_weaponization_score > 80 — guerre de l'eau active ou imminente",
    },
    "crise_eau_vitale": {
        "severity_fr": "Critique",
        "action_fr": "Accord d'urgence sur le débit minimal garanti et fonds international d'adaptation hydrique",
        "signal_fr": "Crise d'eau vitale — pénurie hydrique extrême utilisée comme levier d'État et pression politique existentielle",
    },
    "stress_hydrique_conflictuel": {
        "severity_fr": "Élevé",
        "action_fr": "Traité bilatéral de partage des eaux et mécanismes de surveillance hydrologique conjoints",
        "signal_fr": "Stress hydrique conflictuel — politisation de la gestion des eaux dans un contexte de tension bilatérale",
    },
    "tensions_ripariennes": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcer les institutions ripariennes et les conventions internationales sur les cours d'eau transfrontaliers",
        "signal_fr": "Tensions ripariennes — conflits d'usage gérés mais risques de dérapage sous pression climatique et démographique",
    },
    "cooperation_hydraulique": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de gestion hydraulique coopérative et les conventions de bassin versant comme standards",
        "signal_fr": "composite_score < 20 — coopération hydraulique exemplaire et gestion équitable des eaux transfrontalières",
    },
}


@dataclass
class WaterWarsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    transboundary_water_dispute_score: float
    dam_weaponization_score: float
    water_scarcity_political_score: float
    riparian_conflict_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_water_conflict_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.transboundary_water_dispute_score * 0.30
            + self.dam_weaponization_score * 0.25
            + self.water_scarcity_political_score * 0.25
            + self.riparian_conflict_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_water_conflict_index = round(self.composite_score / 100 * 10, 2)

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
        if self.transboundary_water_dispute_score >= 80 and self.dam_weaponization_score >= 80:
            return "guerre_eau_active"
        if self.water_scarcity_political_score >= 80:
            return "crise_eau_vitale"
        if self.composite_score >= 40:
            return "stress_hydrique_conflictuel"
        if self.composite_score >= 20:
            return "tensions_ripariennes"
        return "cooperation_hydraulique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Guerre de l'eau imminente autour de {n} — conflits hydriques menaçant la survie et la stabilité régionale",
                "Weaponisation des barrages — réduction unilatérale des débits fluviaux comme levier de coercition géopolitique",
                "Stress hydrique existentiel — populations et économies entières dépendant d'un fleuve contesté ou capturé",
            ]
        if self.risk_level == "élevé":
            return [
                f"Stress hydrique politisé dans {n} — tensions bilatérales sévères sur le partage des ressources en eau",
                "Contestation des traités hydrauliques — remise en cause des accords de partage sous pression démographique et climatique",
                "Risque d'escalade hydrique — incidents frontaliers autour des infrastructures hydrauliques stratégiques",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tensions ripariennes dans {n} — conflits d'usage gérés mais vulnérables à la pression climatique",
                "Négociations hydrauliques fragiles — cadre institutionnel insuffisant face aux besoins croissants en eau",
                "Surveillance hydrologique nécessaire — risques de dérapage sous pression de la sécheresse et de la croissance démographique",
            ]
        return [
            f"{n} gère ses ressources hydriques de manière coopérative et équitable",
            "Conventions de bassin versant respectées — partage transparent et institutionnalisé des eaux transfrontalières",
            "Modèle de coopération hydraulique internationale à diffuser — gouvernance inclusive et durable de l'eau",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "transboundary_water_dispute_score": self.transboundary_water_dispute_score,
            "dam_weaponization_score": self.dam_weaponization_score,
            "water_scarcity_political_score": self.water_scarcity_political_score,
            "riparian_conflict_score": self.riparian_conflict_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_water_conflict_index": self.estimated_water_conflict_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[WaterWarsEntity] = [
    WaterWarsEntity("WW-001", "Égypte/Éthiopie/Soudan — Guerre du Nil GERD", "Afrique de l'Est", "GERD Barrage 145Mds m³ Menaçant l'Existence Hydrique de l'Égypte", 88.0, 92.0, 85.0, 78.0),
    WaterWarsEntity("WW-002", "Inde/Pakistan — Traité Indus sous Tension Nucléaire", "Asie du Sud", "Traité 1960 Contesté — Conflits Himalayens & Guerres de l'Eau Nucléaires", 82.0, 75.0, 88.0, 80.0),
    WaterWarsEntity("WW-003", "Turquie — Barrages Atatürk & Contrôle Euphrate-Tigre", "MENA", "Ilısu & Atatürk Réduisant le Débit Irakien et Syrien à Sa Guise", 80.0, 88.0, 82.0, 75.0),
    WaterWarsEntity("WW-004", "Chine — Maître des Sources des Grands Fleuves Asiatiques", "Asie", "8 Fleuves Majeurs (Mékong, Brahmapoutre) Contrôlés & Barrages en Cascade", 85.0, 82.0, 72.0, 80.0),
    WaterWarsEntity("WW-005", "Israël/Palestine/Jordanie — Aquifère Cisjordanie Capturé", "MENA", "Eau comme Outil de Contrôle — Colons 3x Plus d'Eau que Palestiniens", 60.0, 55.0, 65.0, 52.0),
    WaterWarsEntity("WW-006", "Mexique/USA — Colorado River Épuisé Avant la Mer", "Amériques", "Conflits Frontaliers Hydrique & Delta Colorado Mort — Traité de 1944 Obsolète", 48.0, 42.0, 52.0, 45.0),
    WaterWarsEntity("WW-007", "Espagne/Portugal — Tensions Ibériques Tejo-Douro", "Europe du Sud", "Sécheresses Ibériques & Conventions de l'Albufeira Insuffisantes", 28.0, 22.0, 32.0, 25.0),
    WaterWarsEntity("WW-008", "Suisse/UE — Gestion Exemplaire des Alpes Hydrauliques", "Europe", "Convention de l'UNECE & Gestion Coopérative des Bassins Versants Alpins", 8.0, 5.0, 10.0, 6.0),
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
        "domain": "water_war",
        "confidence_score": 0.85,
        "data_sources": ["fao_aquastat_water_resources", "world_resources_institute_aqueduct", "pacific_institute_water_conflict_chronology"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_water_conflict_index": round(avg / 100 * 10, 2),
    }


def analyze_water_wars() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Water Wars Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
