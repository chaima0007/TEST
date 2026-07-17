"""
Caelum Partners — Refugee Weaponization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'instrumentalisation des réfugiés comme arme géopolitique :
au-delà de la crise humanitaire, les flux migratoires forcés sont
délibérément utilisés par des États comme levier de pression politique,
comme outil de déstabilisation des voisins, ou comme moyen de chantage
envers des partenaires économiques. Cette forme de warfare hybride
est particulièrement perverse car elle utilise des populations
vulnérables comme munitions.

La Biélorussie de Loukachenko a orchestré en 2021 le transit de
migrants moyen-orientaux vers la Pologne pour déstabiliser l'UE.
La Turquie d'Erdoğan a menacé à plusieurs reprises d'ouvrir les
vannes des réfugiés syriens vers l'Europe pour obtenir des concessions
politiques. La Libye sous Kadhafi et après utilisait les migrants
sub-sahariens comme outil de chantage. La Russie instrumentalise les
déplacements en Ukraine pour créer des crises humanitaires en Europe.
Cette stratégie est bon marché, asymétrique, et crée des divisions
politiques profondes dans les sociétés d'accueil. C'est l'hybridité
géopolitique dans toute sa perversité.

Risk levels (instrumentalisation des flux migratoires comme arme) :
  critique  → composite ≥ 60  (weaponisation active des réfugiés avérée)
  élevé     → composite ≥ 40  (instrumentalisation partielle documentée)
  modéré    → composite ≥ 20  (risques d'instrumentalisation migratoire)
  faible    → composite < 20  (gestion humanitaire des flux migratoires)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "weaponisation_active": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions ciblées contre les États armant délibérément les flux migratoires et aide humanitaire renforcée",
        "signal_fr": "deliberate_flow_manipulation > 80 AND political_leverage_score > 75 — weaponisation active avérée",
    },
    "chantage_migratoire": {
        "severity_fr": "Critique",
        "action_fr": "Refus des concessions sous chantage migratoire et coopération régionale de gestion des flux",
        "signal_fr": "Chantage migratoire — menaces explicites d'ouvrir les flux pour extorquer des concessions politiques",
    },
    "destabilisation_frontaliere": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement de la résilience frontalière et de la coopération humanitaire régionale",
        "signal_fr": "Déstabilisation frontalière — flux migratoires utilisés pour fragiliser les États voisins",
    },
    "instrumentalisation_partielle": {
        "severity_fr": "Modéré",
        "action_fr": "Monitoring des flux migratoires et dialogue bilatéral pour prévenir l'instrumentalisation",
        "signal_fr": "Instrumentalisation partielle — exploitation opportuniste de flux migratoires sans weaponisation complète",
    },
    "gestion_humanitaire": {
        "severity_fr": "Faible",
        "action_fr": "Maintenir les standards humanitaires et partager les bonnes pratiques de gestion des réfugiés",
        "signal_fr": "composite_score < 20 — gestion humanitaire des flux migratoires conforme au droit international",
    },
}


@dataclass
class RefugeeWeaponizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    deliberate_flow_manipulation_score: float
    political_leverage_score: float
    humanitarian_access_denial_score: float
    destabilization_intent_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_refugee_weapon_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.deliberate_flow_manipulation_score * 0.30
            + self.political_leverage_score * 0.25
            + self.humanitarian_access_denial_score * 0.25
            + self.destabilization_intent_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_refugee_weapon_index = round(self.composite_score / 100 * 10, 2)

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
        if self.deliberate_flow_manipulation_score >= 80 and self.political_leverage_score >= 75:
            return "weaponisation_active"
        if self.political_leverage_score >= 75:
            return "chantage_migratoire"
        if self.composite_score >= 40:
            return "destabilisation_frontaliere"
        if self.composite_score >= 20:
            return "instrumentalisation_partielle"
        return "gestion_humanitaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Weaponisation active des réfugiés par {n} — flux migratoires délibérément orchestrés comme arme géopolitique",
                "Chantage migratoire explicite — menaces d'ouvrir les frontières utilisées pour extorquer des concessions politiques",
                "Populations réfugiées instrumentalisées — violation du droit humanitaire international à des fins géopolitiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Instrumentalisation migratoire significative par {n} — flux exploités pour fragiliser les États voisins ou partenaires",
                "Facilitation opaque des flux transfrontaliers — complaisance délibérée envers les passeurs pour créer des pressions",
                "Utilisation des réfugiés comme variable d'ajustement dans les négociations politiques bilatérales",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risques d'instrumentalisation migratoire dans {n} — tension entre gestion humanitaire et calculs géopolitiques",
                "Flux migratoires partiellement utilisés à des fins de pression politique modérée",
                "Monitoring humanitaire nécessaire pour distinguer gestion légitime et weaponisation émergente",
            ]
        return [
            f"{n} gère les flux migratoires conformément au droit humanitaire international",
            "Protection effective des réfugiés sans instrumentalisation à des fins de pression politique",
            "Modèle de gestion humanitaire à partager — accueil, protection et intégration sans weaponisation",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "deliberate_flow_manipulation_score": self.deliberate_flow_manipulation_score,
            "political_leverage_score": self.political_leverage_score,
            "humanitarian_access_denial_score": self.humanitarian_access_denial_score,
            "destabilization_intent_score": self.destabilization_intent_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_refugee_weapon_index": self.estimated_refugee_weapon_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[RefugeeWeaponizationEntity] = [
    RefugeeWeaponizationEntity("RW-001", "Biélorussie — Crise Frontalière 2021 UE", "Europe de l'Est", "Loukachenko Orchestrant Transit Migrants Moyen-Orientaux vers Pologne", 92.0, 88.0, 85.0, 90.0),
    RefugeeWeaponizationEntity("RW-002", "Turquie — Chantage Migratoire Chronique", "MENA/Europe", "Erdoğan Menaçant l'UE d'Ouvrir les Vannes — 3.6M Syriens comme Levier", 80.0, 92.0, 72.0, 85.0),
    RefugeeWeaponizationEntity("RW-003", "Russie — Déplacements Ukrainiens Instrumentalisés", "Europe de l'Est", "Attaques Infrastructures Créant Vagues Migratoires vers l'Europe", 85.0, 78.0, 88.0, 82.0),
    RefugeeWeaponizationEntity("RW-004", "Libye — Trafic Migrants comme Industrie d'État", "MENA", "Factions Libyennes Contrôlant Flux Africains vers l'Europe — Chantage", 78.0, 80.0, 82.0, 75.0),
    RefugeeWeaponizationEntity("RW-005", "Maroc — Flux Ceutistes 2021 comme Pression", "MENA/Europe", "Crise Ceuta 2021 — Ouverture Frontière pour Punir l'Espagne sur Sahara", 48.0, 55.0, 42.0, 50.0),
    RefugeeWeaponizationEntity("RW-006", "Éthiopie & Érythrée — Flux comme Arme de Guerre", "Afrique de l'Est", "Déplacements Tigré Utilisés comme Arme de Pression Régionale", 52.0, 48.0, 60.0, 55.0),
    RefugeeWeaponizationEntity("RW-007", "Venezuela — Crise Migratoire Exportée", "Amériques", "6M de Réfugiés Vénézuéliens comme Fardeau pour les Voisins Régionaux", 38.0, 42.0, 35.0, 45.0),
    RefugeeWeaponizationEntity("RW-008", "UNHCR & Canada — Modèles d'Accueil", "Global", "Systèmes de Parrainage Privé et Réinstallation Planifiée Non-Instrumentalisée", 5.0, 4.0, 6.0, 3.0),
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
        "domain": "refugee_weapon",
        "confidence_score": 0.81,
        "data_sources": ["unhcr_global_trends", "iom_migration_data_portal", "migrants_as_weapon_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_refugee_weapon_index": round(avg / 100 * 10, 2),
    }


def analyze_refugee_weaponization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Refugee Weaponization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
