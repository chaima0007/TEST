"""
Caelum Partners — Food Weaponization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'alimentation comme arme géopolitique : qui contrôle la nourriture contrôle
les peuples. Dans un monde où 5 pays fournissent 70% des exportations
céréalières mondiales, la dépendance alimentaire est un vecteur de coercition
extraordinaire. La Russie a utilisé le blocage des exportations ukrainiennes
de blé comme arme après l'invasion de 2022 — menaçant directement la sécurité
alimentaire de 47 pays dépendant du couloir de la Mer Noire.

L'accaparement des terres agricoles (land grabbing) est la stratégie discrète
de sécurisation alimentaire offensive : la Chine a acquis ou loué plus de
3 millions d'hectares en Afrique subsaharienne. Les pays du Golfe ont acheté
des millions d'hectares au Soudan, en Éthiopie et en Indonésie après 2008.
L'Inde a banni ses exportations de riz en 2023 — faisant exploser les prix
mondiaux et exposant les nations importatrices. Moscou contrôle 30% des
exportations mondiales de blé et a utilisé cette position dominante comme
chantage explicite contre les pays MENA. L'Égypte dépend à 80% des imports
céréaliers. La Tunisie à 70%. Ces chiffres sont des vulnérabilités existentielles
que des États ne se privent pas d'exploiter.

Risk levels (weaponisation de l'alimentation et coercition par la faim) :
  critique  → composite ≥ 60  (arme alimentaire active — coercition existentielle)
  élevé     → composite ≥ 40  (levier alimentaire significatif — pression politisée)
  modéré    → composite ≥ 20  (nationalisme alimentaire — protectionnisme à risque)
  faible    → composite < 20  (gouvernance alimentaire mondiale équitable)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "arme_alimentaire_active": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions contre les États weaponisant les exportations et constitution de stocks alimentaires stratégiques régionaux",
        "signal_fr": "grain_export_control_score > 80 AND fertilizer_monopolization_score > 75 — arme alimentaire active et délibérée",
    },
    "accaparement_terres_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Régulation internationale du land grabbing et protection des droits fonciers des communautés locales",
        "signal_fr": "Accaparement stratégique des terres agricoles mondiales pour sécuriser l'approvisionnement alimentaire offensif",
    },
    "coercition_alimentaire": {
        "severity_fr": "Élevé",
        "action_fr": "Diversification des sources d'approvisionnement alimentaire et coopération régionale de sécurité alimentaire",
        "signal_fr": "Coercition alimentaire — utilisation des exportations ou de l'aide alimentaire comme conditionnalité politique",
    },
    "nationalisme_alimentaire": {
        "severity_fr": "Modéré",
        "action_fr": "Dialogue OMC et normes de prévisibilité des exportations pour éviter les crises alimentaires en cascade",
        "signal_fr": "Nationalisme alimentaire — restrictions d'exportation protectionnistes créant des chocs sur les marchés mondiaux",
    },
    "gouvernance_alimentaire_mondiale": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer l'architecture de gouvernance alimentaire mondiale et les mécanismes de stabilisation des prix",
        "signal_fr": "composite_score < 20 — gouvernance alimentaire équitable et multilatérale sans weaponisation des flux",
    },
}


@dataclass
class FoodWeaponizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    grain_export_control_score: float
    fertilizer_monopolization_score: float
    agricultural_land_grab_score: float
    food_aid_coercion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_food_weapon_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.grain_export_control_score * 0.30
            + self.fertilizer_monopolization_score * 0.25
            + self.agricultural_land_grab_score * 0.25
            + self.food_aid_coercion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_food_weapon_index = round(self.composite_score / 100 * 10, 2)

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
        if self.grain_export_control_score >= 80 and self.fertilizer_monopolization_score >= 75:
            return "arme_alimentaire_active"
        if self.agricultural_land_grab_score >= 80:
            return "accaparement_terres_strategique"
        if self.composite_score >= 40:
            return "coercition_alimentaire"
        if self.composite_score >= 20:
            return "nationalisme_alimentaire"
        return "gouvernance_alimentaire_mondiale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Arme alimentaire active dans {n} — contrôle des exportations céréalières comme levier de coercition géopolitique existentielle",
                "Weaponisation des flux alimentaires — restrictions d'exportation ou accaparement de terres déstabilisant les marchés mondiaux",
                "Dépendances alimentaires exploitées — pays importateurs sous menace existentielle de pénurie et chantage alimentaire",
            ]
        if self.risk_level == "élevé":
            return [
                f"Coercition alimentaire significative dans {n} — politisation des exportations ou de l'aide alimentaire",
                "Conditionnalité alimentaire — aide ou accès aux marchés liés à des concessions politiques explicites",
                "Concentration alimentaire risquée — dépendance excessive d'États vulnérables à un fournisseur dominant",
            ]
        if self.risk_level == "modéré":
            return [
                f"Nationalisme alimentaire dans {n} — restrictions d'exportation protectionnistes créant des tensions mondiales",
                "Protectionnisme agricole non coordonné — chocs en cascade sur les marchés alimentaires des pays les plus pauvres",
                "Risque de dérapage — nationalisme alimentaire pouvant basculer vers weaponisation sous pression géopolitique",
            ]
        return [
            f"{n} contribue positivement à la gouvernance alimentaire mondiale — architecture multilatérale équitable",
            "Systèmes d'alerte précoce alimentaire et mécanismes de stabilisation des prix efficaces et inclusifs",
            "Modèle de partage alimentaire à diffuser — solidarité alimentaire mondiale sans conditionnalité politique",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "grain_export_control_score": self.grain_export_control_score,
            "fertilizer_monopolization_score": self.fertilizer_monopolization_score,
            "agricultural_land_grab_score": self.agricultural_land_grab_score,
            "food_aid_coercion_score": self.food_aid_coercion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_food_weapon_index": self.estimated_food_weapon_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FoodWeaponizationEntity] = [
    FoodWeaponizationEntity("FW-001", "Russie — Blé comme Arme & Blocage Mer Noire", "Europe de l'Est", "30% Exports Blé Mondial & Accord Mer Noire Sabordé comme Chantage MENA", 92.0, 85.0, 72.0, 88.0),
    FoodWeaponizationEntity("FW-002", "Chine — Land Grab Africain & Stocks Stratégiques", "Asie", "3M Ha Africains & 65% Stocks Mondiaux Maïs/Blé/Riz — Arsenal Alimentaire", 75.0, 80.0, 88.0, 72.0),
    FoodWeaponizationEntity("FW-003", "USA — Sanctions Alimentaires & Aid Conditionnalité", "Amérique du Nord", "Embargo Alimentaire Cuba/Iran & USAID comme Levier de Politique Étrangère", 68.0, 72.0, 65.0, 80.0),
    FoodWeaponizationEntity("FW-004", "Inde — Interdiction Export Riz 2023 & Blé", "Asie du Sud", "Bans Export Riz/Blé Explosant Prix Mondiaux — 1.4Mds Mangent d'Abord", 82.0, 60.0, 68.0, 55.0),
    FoodWeaponizationEntity("FW-005", "Ukraine/UE — Couloir Céréalier & Dépendance MENA", "Europe/MENA", "47 Pays Dépendants Corridor Mer Noire — Blocus Russe comme Levier", 55.0, 48.0, 45.0, 52.0),
    FoodWeaponizationEntity("FW-006", "Brésil/Argentine — Soja & Influence Régionale", "Amériques", "60% Soja Mondial & Pouvoir de Marché sur Protéines Animales Globales", 45.0, 42.0, 52.0, 38.0),
    FoodWeaponizationEntity("FW-007", "Indonésie — Palm Oil Ban & Nationalisme Agricole", "Asie du Sud-Est", "Interdiction Export Huile Palme 2022 — Souveraineté vs Marchés Mondiaux", 35.0, 38.0, 28.0, 25.0),
    FoodWeaponizationEntity("FW-008", "FAO & PAM — Architecture Alimentaire Mondiale", "Global", "Systèmes Alerte Précoce, Réserves Humanitaires & Gouvernance Neutre FAO", 5.0, 4.0, 6.0, 8.0),
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
        "domain": "food_weapon",
        "confidence_score": 0.88,
        "data_sources": ["fao_food_insecurity_monitor", "grain_market_international_panel", "oxfam_land_rights_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_food_weapon_index": round(avg / 100 * 10, 2),
    }


def analyze_food_weaponization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Food Weaponization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
