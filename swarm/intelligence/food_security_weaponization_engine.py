"""
Caelum Partners — Food Security Weaponization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La faim comme arme de guerre : quand la sécurité alimentaire devient un instrument géopolitique.
La nourriture a toujours été une arme de guerre — mais l'ère des flux agricoles
mondialisés, des marchés à terme et des sanctions économiques a transformé la
weaponisation alimentaire en instrument de coercition sophistiqué disponible
pour les puissances qui contrôlent les greniers du monde.

La Russie a weaponisé le blé ukrainien en bloquant les exportations via la
mer Noire après l'invasion de 2022, précipitant une crise alimentaire mondiale
touchant 345 millions de personnes dans 82 pays. La Chine contrôle 70% des
réserves mondiales de blé, riz et maïs — une domination stratégique qui lui
permet d'absorber les chocs alimentaires tout en achetant massivement les terres
agricoles africaines. La Corée du Nord maintient délibérément ses citoyens dans
la malnutrition pour concentrer les ressources sur l'armée.

Le Yémen et le Soudan illustrent la famine induite politiquement — les blocus
militaires coupant délibérément les populations civiles de l'aide alimentaire.
L'Éthiopie a utilisé la faim comme arme de guerre au Tigré (2020-2022).
Les Nations Unies considèrent l'utilisation délibérée de la famine contre des
civils comme un crime de guerre depuis 2018.

Risk levels (weaponisation de la sécurité alimentaire) :
  critique  → composite ≥ 60  (famine induite — utilisation de la faim comme arme de guerre ou de coercition)
  élevé     → composite ≥ 40  (pression alimentaire stratégique — manipulation des flux céréaliers à fins géopolitiques)
  modéré    → composite ≥ 20  (vulnérabilité alimentaire — dépendances exploitables dans les crises internationales)
  faible    → composite < 20  (sécurité alimentaire coopérative — PAM, FAO et filets de sécurité efficaces)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "famine_induite_politique": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme d'urgence alimentaire onusien — tribunal international pour crimes de famine, corridors humanitaires imposés par mandat CSNU et sanctions sectorielles agricoles",
        "signal_fr": "famine_induction_score > 85 AND grain_export_weaponization_score > 85 — famine induite politiquement combinant blocus alimentaire actif et weaponisation des exportations céréalières",
    },
    "weaponisation_cereales": {
        "severity_fr": "Critique",
        "action_fr": "Initiative céréalière internationale — fonds stratégique d'achats groupés, diversification des sources d'approvisionnement et sanctions contre les manipulateurs de marchés agricoles",
        "signal_fr": "grain_export_weaponization_score > 85 — weaponisation des exportations céréalières comme levier de coercition géopolitique contre les États dépendants",
    },
    "manipulation_aide_alimentaire": {
        "severity_fr": "Critique",
        "action_fr": "Réforme de l'aide alimentaire internationale — canaux d'acheminement indépendants des gouvernements hôtes, contrôle par des ONG neutres et criminalisation du détournement d'aide",
        "signal_fr": "food_aid_manipulation_score > 85 — manipulation systématique de l'aide alimentaire internationale à des fins politiques internes",
    },
    "pression_alimentaire_strategique": {
        "severity_fr": "Élevé",
        "action_fr": "Diversification des chaînes d'approvisionnement alimentaires — investissements dans les agricultures locales, stocks stratégiques nationaux et traités de sécurité alimentaire bilatéraux",
        "signal_fr": "Pression alimentaire stratégique — utilisation des flux agricoles comme levier géopolitique sans qualification de weaponisation active",
    },
    "securite_alimentaire_cooperative": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer le système alimentaire mondial — financement du PAM, coordination FAO et mécanismes d'alerte précoce sur les crises alimentaires naissantes",
        "signal_fr": "composite_score < 20 — contribution sincère à la sécurité alimentaire mondiale via le PAM, la FAO et les mécanismes d'aide humanitaire",
    },
}


@dataclass
class FoodSecurityWeaponizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    grain_export_weaponization_score: float
    food_aid_manipulation_score: float
    agricultural_sanctions_score: float
    famine_induction_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_food_security_weaponization_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.grain_export_weaponization_score * 0.30
            + self.food_aid_manipulation_score * 0.25
            + self.agricultural_sanctions_score * 0.25
            + self.famine_induction_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_food_security_weaponization_index = round(self.composite_score / 100 * 10, 2)

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
        if self.famine_induction_score >= 85 and self.grain_export_weaponization_score >= 85:
            return "famine_induite_politique"
        if self.grain_export_weaponization_score >= 85:
            return "weaponisation_cereales"
        if self.food_aid_manipulation_score >= 85:
            return "manipulation_aide_alimentaire"
        if self.composite_score >= 20:
            return "pression_alimentaire_strategique"
        return "securite_alimentaire_cooperative"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Weaponisation alimentaire de {n} — utilisation délibérée de la faim comme instrument de coercition géopolitique ou de répression interne",
                "Criminalisation de la faim — blocus alimentaire actif, détournement de l'aide humanitaire et manipulation des marchés céréaliers mondiaux",
                "Violation du droit humanitaire — l'utilisation de la famine contre des civils constitue un crime de guerre selon le droit international depuis 2018",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression alimentaire stratégique de {n} — manipulation des flux céréaliers et des sanctions agricoles à des fins de coercition géopolitique",
                "Dépendance alimentaire exploitée — les États importateurs de denrées subissent une vulnérabilité structurelle face aux exportateurs dominants",
                "Risque de crise alimentaire induite — tout blocage des exportations déclencherait une cascade de pénuries alimentaires dans les pays dépendants",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité alimentaire de {n} — dépendances aux importations ou restrictions d'exportation exploitables dans les crises internationales",
                "Filets de sécurité insuffisants — stocks stratégiques sous-dimensionnés et capacités agricoles locales insuffisantes pour absorber les chocs externes",
                "Risque de pression alimentaire — la concentration des exportations mondiales de denrées crée des vulnérabilités structurelles exploitables",
            ]
        return [
            f"{n} incarne la sécurité alimentaire coopérative — financement du PAM, contribution à la FAO et systèmes d'alerte précoce efficaces",
            "Distribution alimentaire équitable — mécanismes d'urgence humanitaire indépendants des pressions politiques et accès universel à l'aide alimentaire",
            "Modèle de résilience alimentaire — stocks stratégiques nationaux, diversification des fournisseurs et aide internationale inconditionnelle",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "grain_export_weaponization_score": self.grain_export_weaponization_score,
            "food_aid_manipulation_score": self.food_aid_manipulation_score,
            "agricultural_sanctions_score": self.agricultural_sanctions_score,
            "famine_induction_score": self.famine_induction_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_food_security_weaponization_index": self.estimated_food_security_weaponization_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FoodSecurityWeaponizationEntity] = [
    FoodSecurityWeaponizationEntity("FS-001", "Russie — Blocus Mer Noire & Arme Céréalière Ukraine", "Europe de l'Est", "Blocus Céréalier 2022 345M Personnes Menacées, Missiles Ports Odessa & Mines Grain Deal ONU Saboté", 92.0, 85.0, 80.0, 88.0),
    FoodSecurityWeaponizationEntity("FS-002", "Chine — Monopole Réserves & Terres Agricoles Africaines", "Asie", "70% Réserves Mondiales Blé/Riz/Maïs, 10M Ha Terres Africaines Achetées & BRI Dépendances Alimentaires", 88.0, 80.0, 85.0, 75.0),
    FoodSecurityWeaponizationEntity("FS-003", "Yémen & Soudan — Blocus Militaire & Famine Induite", "MENA/Afrique", "Yémen 21M Personnes Insécurité Alimentaire, Soudan 25M & Blocus Saoudien/RSF Détournement Aide PAM", 65.0, 90.0, 72.0, 95.0),
    FoodSecurityWeaponizationEntity("FS-004", "RPDC — Malnutrition Systémique & Contrôle Distribution", "Asie", "42% Population Malnutrie, PDS Distribution Politique-Dépendante & Détournement Aide Alimentaire Internationale", 80.0, 78.0, 68.0, 85.0),
    FoodSecurityWeaponizationEntity("FS-005", "Éthiopie & Tigré — Famine comme Arme de Guerre", "Afrique de l'Est", "Siège Tigré 2020-2022 500K Famine, Blocage Convois PAM & Criminalisation Aide Humanitaire Documentée", 55.0, 60.0, 52.0, 58.0),
    FoodSecurityWeaponizationEntity("FS-006", "USA & Occident — Sanctions Agricoles Stratégiques", "Amérique du Nord", "Sanctions Cuba/Iran/Russie Volet Agricole, SWIFT Restrictions Achats Alimentaires & Embargo Dual-Use", 52.0, 48.0, 62.0, 45.0),
    FoodSecurityWeaponizationEntity("FS-007", "Inde — Interdictions Export Riz/Blé & Chocs Marchés", "Asie du Sud", "Ban Export Riz 2023 Choc Prix Mondial, Restrictions Blé & Accaparement Terres Népal/Bangladesh", 28.0, 25.0, 35.0, 22.0),
    FoodSecurityWeaponizationEntity("FS-008", "PAM & FAO — Sécurité Alimentaire Mondiale Coopérative", "Global", "PAM 137M Personnes Assistées, FAO Monitoring Récoltes Mondial & SMIAR Système Alerte Précoce 92 Pays", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "food_security_weaponization",
        "confidence_score": 0.81,
        "data_sources": ["wfp_global_food_crisis_report", "fao_food_security_indicators", "fews_net_famine_early_warning"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_food_security_weaponization_index": round(avg / 100 * 10, 2),
    }


def analyze_food_security_weaponization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Food Security Weaponization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
