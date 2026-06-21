"""
Caelum Partners — Organ Trafficking Transplant Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Trafic d'organes et droits des donneurs : violations des droits humains fondamentaux liées
au commerce illicite d'organes humains, au tourisme de transplantation et à la récolte forcée
d'organes sur des prisonniers d'opinion et des minorités vulnérables.

Le trafic d'organes représente l'une des formes les plus graves de traite des êtres humains.
Des prisonniers politiques, des Ouïghours, des Falun Gong et des détenus dans des contextes
de conflit armé sont victimes de prélèvements forcés d'organes, pratique documentée en Chine
par le Tribunal indépendant China Tribunal (2019) qui a conclu à des crimes contre l'humanité.

Le tourisme de transplantation — quand des patients aisés voyagent vers des pays à faible
gouvernance pour acheter des organes — alimente une économie souterraine estimée à 1,5 milliard
de dollars annuels selon l'OMS, exploitant les populations pauvres et marginalisées qui vendent
leurs organes sous contrainte économique.

La Convention de Grenade (1997) et le Protocole de Palerme (2000) fournissent le cadre
juridique international, mais les lacunes dans les systèmes nationaux de don d'organes,
les inégalités économiques profondes et la corruption judiciaire perpetuent ces violations.

Risk levels (trafic d'organes et droits des transplantés) :
  critique  -> composite >= 60  (récolte forcée systémique — crimes contre l'humanité)
  élevé     -> composite >= 40  (tourisme transplantation — exploitation grave documentée)
  modéré    -> composite >= 20  (lacunes systémiques — risque d'exploitation résiduel)
  faible    -> composite < 20   (système encadré — don éthique et contrôle effectif)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "recolte_forcee_prisonniers_opinion": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions internationales ciblées — embargo médical, exclusion congrès transplantation, tribunal pénal international, audit indépendant hôpitaux, arrêt immédiat pratiques criminelles",
        "signal_fr": "forced_organ_harvesting_state_score > 85 — prélèvements forcés d'organes sur prisonniers d'opinion, minorities ou détenus, constituant des crimes contre l'humanité selon le droit international",
    },
    "tourisme_transplantation_exploitation": {
        "severity_fr": "Critique",
        "action_fr": "Législation extraterritoriale — criminalisation tourisme transplantation, coopération interpol, gel avoirs trafiquants, protection victimes donneurs contraints, réparations médicales",
        "signal_fr": "organ_trafficking_network_score > 80 — réseaux trafic organes actifs, tourisme transplantation exploitant pauvreté, violation des droits des donneurs contraints économiquement",
    },
    "vente_organes_pauvrete_contrainte": {
        "severity_fr": "Critique",
        "action_fr": "Réforme systémique don organes — expansion liste don volontaire, allocation ressources médicales, protection donneurs vulnérables, criminalisation intermédiaires, réhabilitation victimes",
        "signal_fr": "economic_coercion_organ_sale_score > 75 — vente d'organes sous contrainte économique sévère, exploitation des populations pauvres par des réseaux criminels organisés transnationaux",
    },
    "insuffisance_systeme_don_legal": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement infrastructure transplantation — campagnes sensibilisation don volontaire, registres nationaux donneurs, coopération internationale allocations équitables, audit éthique hôpitaux",
        "signal_fr": "organ_donation_system_gap_score > 60 — déficits graves dans le système légal de don d'organes alimentant la demande de transplantations illicites et le marché noir médical",
    },
    "systeme_don_ethique_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Partager les bonnes pratiques — exporter modèle don présumé efficace, former équipes médicales des pays à risque, financer coopération transplantation éthique internationale",
        "signal_fr": "composite_score < 20 — système de transplantation éthique, don volontaire encadré, liste attente transparente, contrôle indépendant effectif, taux auto-suffisance élevé",
    },
}


@dataclass
class OrganTraffickingTransplantRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_organ_harvesting_state_score: float
    organ_trafficking_network_score: float
    economic_coercion_organ_sale_score: float
    organ_donation_system_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_organ_trafficking_transplant_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_organ_harvesting_state_score * 0.30
            + self.organ_trafficking_network_score * 0.25
            + self.economic_coercion_organ_sale_score * 0.25
            + self.organ_donation_system_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_organ_trafficking_transplant_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.forced_organ_harvesting_state_score >= 85:
            return "recolte_forcee_prisonniers_opinion"
        if self.organ_trafficking_network_score >= 80:
            return "tourisme_transplantation_exploitation"
        if self.economic_coercion_organ_sale_score >= 75:
            return "vente_organes_pauvrete_contrainte"
        if self.composite_score >= 20:
            return "insuffisance_systeme_don_legal"
        return "systeme_don_ethique_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Trafic d'organes critique de {n} — prélèvements forcés ou exploitation économique grave documentés, violations des droits humains fondamentaux constituant des crimes contre l'humanité",
                "Réseaux transnationaux de trafic d'organes actifs — complicité d'acteurs médicaux, judiciaires ou étatiques permettant l'industrialisation du commerce illicite d'organes humains",
                "Violation du droit à l'intégrité corporelle — la marchandisation des organes humains nie la dignité fondamentale des personnes contraintes à vendre ou à subir des prélèvements forcés",
            ]
        if self.risk_level == "élevé":
            return [
                f"Risque élevé trafic organes de {n} — déficits systémiques du système légal de don, tourisme de transplantation documenté ou réseaux criminels actifs sans réponse étatique adéquate",
                "Lacunes dans l'allocation éthique des organes — listes d'attente inéquitables, corruption dans les processus d'attribution, vulnérabilité des populations pauvres à l'exploitation médicale",
                "Insuffisance du cadre légal — les législations nationales ne criminalisent pas suffisamment le tourisme de transplantation ou protègent insuffisamment les donneurs contraints économiquement",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel trafic organes de {n} — incidents documentés ou lacunes dans les registres nationaux de donneurs, sans système criminel établi mais vulnérabilités structurelles présentes",
                "Don d'organes sous-développé — l'insuffisance du système légal crée une demande non satisfaite pouvant alimenter des circuits parallèles ou le recours à des transplantations à l'étranger",
                "Contrôle médical perfectible — les audits des établissements de transplantation restent insuffisants pour garantir le caractère éthique et volontaire de tous les prélèvements effectués",
            ]
        return [
            f"{n} représente un modèle de transplantation éthique — système de don volontaire encadré, listes d'attente transparentes, taux d'auto-suffisance élevé et contrôle indépendant effectif",
            "Convention de Grenade respectée — interdit de toute rémunération pour les organes, allocation selon critères médicaux objectifs, traçabilité complète des donneurs et receveurs",
            "Modèle de don présumé ou opt-out efficace — augmentation des dons, réduction tourisme de transplantation, coopération internationale sur les listes d'attente et échanges d'organes",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_organ_harvesting_state_score": self.forced_organ_harvesting_state_score,
            "organ_trafficking_network_score": self.organ_trafficking_network_score,
            "economic_coercion_organ_sale_score": self.economic_coercion_organ_sale_score,
            "organ_donation_system_gap_score": self.organ_donation_system_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_organ_trafficking_transplant_rights_index": self.estimated_organ_trafficking_transplant_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[OrganTraffickingTransplantRightsEntity] = [
    OrganTraffickingTransplantRightsEntity(
        "OTT-001",
        "Chine/Récolte Forcée Falun Gong Ouïghours Prisonniers Conscience",
        "Chine",
        "Prélèvements Forcés Prisonniers Conscience, Falun Gong & Ouïghours, China Tribunal 2019 Crimes Contre Humanité, Hôpitaux Militaires PLA",
        96.0, 93.0, 88.0, 90.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-002",
        "Pakistan/Rein Marché Noir Punjab Villages Donneurs Forcés",
        "Pakistan",
        "Marché Noir Reins Punjab, Villages Donneurs Forcés Dette, Réseaux Trafiquants Multan Lahore, FIA Enquêtes Insuffisantes",
        85.0, 88.0, 90.0, 82.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-003",
        "Égypte/Réfugiés Syriens Soudanais Organes Exploitation Caire",
        "Égypte",
        "Réfugiés Syriens & Soudanais Exploitation Organes, Hôpitaux Caire Transactions Illicites, Pauvreté Extrême Vente Contrainte Rein",
        82.0, 84.0, 87.0, 80.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-004",
        "Kosovo/Crime Organisé Organes Guerre 1999 Thaçi Tribunal",
        "Kosovo",
        "Crime Organisé Organes Conflits Armés 1999, Thaçi & KLA Accusés Tribunal Spécial La Haye, Victimes Serbes Prisonniers Guerre",
        88.0, 80.0, 72.0, 78.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-005",
        "Inde/Tourisme Transplantation Rein Hôpitaux Chennai Mumbai",
        "Inde",
        "Tourisme Transplantation Rein, Hôpitaux Privés Chennai & Mumbai, Donneurs Pauvres Contrainte Économique, THOTA 1994 Application Partielle",
        55.0, 58.0, 62.0, 52.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-006",
        "Philippines/Vente Reins Légalisée Pauvreté Bidonvilles Manille",
        "Philippines",
        "Vente Reins Bidonvilles Manille, Pauvreté Extrême Donneurs Vivants, Loi 1991 Insuffisante Contrôle, OMS Recommandations Ignorées",
        52.0, 54.0, 58.0, 50.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-007",
        "OMS/Principes Directeurs Transplantation 2010 Application Lacunaire",
        "Global",
        "Principes Directeurs OMS 2010 Don Volontaire, Application Nationale Insuffisante, Echelon Transparence Mondiale GODT, Lacunes Rapport États",
        28.0, 25.0, 22.0, 30.0,
    ),
    OrganTraffickingTransplantRightsEntity(
        "OTT-008",
        "Espagne/Système Don Présumé ONT Modèle Mondial Auto-Suffisance",
        "Espagne",
        "Organización Nacional de Trasplantes, Don Présumé Opt-Out Efficace, Taux Donneur Mondial Record, Zéro Tourisme Transplantation, Transparence Totale",
        5.0, 4.0, 3.0, 6.0,
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
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "domain": "organ_trafficking_transplant_rights",
        "confidence_score": 0.89,
        "data_sources": [
            "china_tribunal_2019_report",
            "who_global_observatory_donation_transplantation",
            "interpol_organ_trafficking_investigations",
            "council_europe_convention_actions_against_trafficking_organs",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_organ_trafficking_transplant_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_organ_trafficking_transplant_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Organ Trafficking Transplant Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
