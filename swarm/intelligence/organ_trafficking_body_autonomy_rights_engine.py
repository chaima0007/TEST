"""
Caelum Partners — Organ Trafficking Body Autonomy Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Trafic d'organes et autonomie corporelle : violations systémiques du consentement, de l'intégrité
physique et des droits fondamentaux des personnes vulnérables soumises à l'extraction forcée.

Le trafic d'organes constitue une des formes les plus graves de violations des droits humains,
ciblant les populations les plus vulnérables — prisonniers politiques, migrants, personnes vivant
dans l'extrême pauvreté — pour alimenter un marché mondial estimé à 1,2 milliard USD/an selon
l'OMS. Le Tribunal China sur le prélèvement d'organes (2019) a conclu que la Chine pratique le
prélèvement d'organes vivants sur des prisonniers de conscience, notamment des Falun Gong et des
Ouïghours, à une échelle estimée entre 60 000 et 100 000 greffes par an.

La Déclaration d'Istanbul (2008) et le Protocole de Palerme exigent l'auto-suffisance en organes
via le don volontaire post-mortem, mais l'application reste limitée. Les pays comme l'Espagne
démontrent qu'un système de don éthique peut atteindre 47 donneurs par million d'habitants,
rendant le trafic inutile — un modèle que la communauté internationale tarde à adopter.

Risk levels (trafic d'organes et autonomie corporelle) :
  critique  -> composite >= 60  (prélèvement forcé institutionnalisé — crimes contre l'humanité)
  élevé     -> composite >= 40  (marché noir actif — exploitation systémique des vulnérables)
  modéré    -> composite >= 20  (cadres insuffisants — risque résiduel documenté)
  faible    -> composite < 20   (modèle éthique exemplaire — don volontaire post-mortem)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "prelevement_force_prisonnier_politique": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions internationales immédiates — embargo transplantations, tribunal pénal international, sanctions ciblées sur hôpitaux et officiers impliqués, arrêt coopération médicale",
        "signal_fr": "organ_trafficking_forced_extraction_score > 85 — prélèvement d'organes sur prisonniers politiques vivants, crime contre l'humanité selon le droit international",
    },
    "marche_noir_organes_pauvrete": {
        "severity_fr": "Critique",
        "action_fr": "Intervention multi-acteurs — criminalisation acheteurs et intermédiaires, protection des vendeurs-victimes, réforme hospitalière avec traçabilité obligatoire des organes",
        "signal_fr": "organ_trafficking_forced_extraction_score > 75 — marché noir d'organes alimenté par la pauvreté, exploitation des vendeurs contraints par nécessité économique",
    },
    "procedures_medicales_coercitives": {
        "severity_fr": "Critique",
        "action_fr": "Réforme bioéthique — comités d'éthique indépendants, consentement éclairé obligatoire, sanctions médicales pour violations, accès avocat avant procédures invasives",
        "signal_fr": "body_autonomy_coercive_medical_procedures_score > 75 — procédures médicales sans consentement éclairé, violations de l'autonomie corporelle documentées",
    },
    "experimentation_detenus": {
        "severity_fr": "Élevé",
        "action_fr": "Inspection internationale — accès ONU aux établissements pénitentiaires, commission d'enquête indépendante, suspension accords médicaux avec États non coopératifs",
        "signal_fr": "prison_medical_experimentation_score > 60 — expérimentation médicale sur détenus sans consentement, violation des principes de Nuremberg et de la Déclaration d'Helsinki",
    },
    "modele_don_ethique_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter le modèle — financement OMS pour réplication, formation équipes médicales étrangères, plaidoyer Déclaration Istanbul et partage protocoles don post-mortem",
        "signal_fr": "composite_score < 20 — système de don éthique exemplaire, auto-suffisance en organes via consentement volontaire post-mortem respectant la dignité humaine",
    },
}


@dataclass
class OrganTraffickingBodyAutonomyRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    organ_trafficking_forced_extraction_score: float
    body_autonomy_coercive_medical_procedures_score: float
    prison_medical_experimentation_score: float
    trafficking_prosecution_impunity_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_organ_trafficking_body_autonomy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.organ_trafficking_forced_extraction_score * 0.30
            + self.body_autonomy_coercive_medical_procedures_score * 0.25
            + self.prison_medical_experimentation_score * 0.25
            + self.trafficking_prosecution_impunity_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_organ_trafficking_body_autonomy_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.organ_trafficking_forced_extraction_score >= 90:
            return "prelevement_force_prisonnier_politique"
        if self.organ_trafficking_forced_extraction_score >= 75:
            return "marche_noir_organes_pauvrete"
        if self.body_autonomy_coercive_medical_procedures_score >= 75:
            return "procedures_medicales_coercitives"
        if self.composite_score >= 20:
            return "experimentation_detenus"
        return "modele_don_ethique_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Trafic d'organes critique de {n} — prélèvement forcé ou marché noir actif constituant une violation grave du droit à l'intégrité physique et à l'autonomie corporelle",
                "Crime contre l'humanité documenté — le prélèvement d'organes sans consentement sur des prisonniers politiques ou des personnes vulnérables viole le Statut de Rome et les Principes de Nuremberg",
                "Impunité systémique des trafiquants — l'absence de poursuites efficaces perpétue l'exploitation des corps humains comme marchandise et alimente un marché criminel international estimé à 1,2 milliard USD/an",
            ]
        if self.risk_level == "élevé":
            return [
                f"Exploitation corporelle de {n} — marché noir d'organes ou coercition médicale documentés, populations pauvres réduites à vendre leurs organes sous contrainte économique",
                "Tourisme de transplantation actif — patients étrangers achetant des organes de sources illégales, contournant la Déclaration d'Istanbul et finançant l'exploitation des vendeurs-victimes",
                "Contrôle hospitalier insuffisant — absence de traçabilité obligatoire des organes permettant l'intégration d'organes de sources illicites dans les circuits médicaux légaux",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel trafic organes de {n} — incidents documentés sans institutionnalisation, cadres légaux insuffisamment appliqués ou coopération internationale limitée",
                "Débat éthique non résolu — tension entre protection de la vie privée des communications chiffrées et nécessité de détecter les réseaux criminels de trafic d'organes",
                "Progrès fragiles — les avancées législatives peuvent être contournées sans systèmes de traçabilité robustes et de contrôle indépendant des établissements de transplantation",
            ]
        return [
            f"{n} représente le modèle éthique mondial de don d'organes — auto-suffisance via consentement volontaire post-mortem respectant la dignité humaine et l'autonomie corporelle",
            "Principes Déclaration Istanbul respectés — don altruiste sans compensation financière, traçabilité complète, comités d'éthique indépendants et taux de don exemplaire",
            "Modèle exportable — financement OMS pour réplication internationale, formation équipes médicales étrangères et plaidoyer pour l'abandon du tourisme de transplantation",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "organ_trafficking_forced_extraction_score": self.organ_trafficking_forced_extraction_score,
            "body_autonomy_coercive_medical_procedures_score": self.body_autonomy_coercive_medical_procedures_score,
            "prison_medical_experimentation_score": self.prison_medical_experimentation_score,
            "trafficking_prosecution_impunity_gap_score": self.trafficking_prosecution_impunity_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_organ_trafficking_body_autonomy_rights_index": self.estimated_organ_trafficking_body_autonomy_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[OrganTraffickingBodyAutonomyRightsEntity] = [
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-001",
        "Chine/Falun Gong & Ouïghours Prélèvements Organes Vivants",
        "Chine",
        "Prélèvements Organes Prisonniers Politiques Vivants, Rapports Tribunal 2019, 60K-100K Greffes/An, Falun Gong Ouïghours Principaux Groupes Ciblés",
        97.0, 93.0, 95.0, 92.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-002",
        "Pakistan/Reins Marché Noir Village Punjab",
        "Pakistan",
        "Marché Noir Rein Villages Punjab, Pauvres Vendeurs Contraints, 2500 Reins/An Illégaux Estimés, Acheteurs Riches Nationaux & Étrangers",
        89.0, 85.0, 82.0, 86.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-003",
        "Égypte/Sinai Organes Migrants Africains Extorqués",
        "Égypte",
        "Camp Réfugiés Sinai, Organes Migrants Africains Extorqués, Groupes Armés Intermédiaires, HCR Rapports Non Suivis D'effet",
        87.0, 83.0, 80.0, 84.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-004",
        "Kosovo/Enquête Thaçi Organes Combattants Serbes 1999",
        "Kosovo",
        "Enquête Thaçi Organes Combattants Serbes 1999, SITF Tribunal Spécial, Dossiers Classés 20 Ans, Impunité Post-Conflit Documentée",
        83.0, 79.0, 78.0, 81.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-005",
        "Inde/Mafias Médicales États Tampons Reins",
        "Inde",
        "Mafias Médicales États Tampons, Vendeurs Ruraux Trompés, Contrôle Insuffisant Hôpitaux, THOA 1994 Application Lacunaire",
        56.0, 52.0, 50.0, 54.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-006",
        "Philippines/Vendeurs Reins Bidonvilles 2022",
        "Philippines",
        "Vendeurs Reins Bidonvilles, 2022 Loi Renforcement Insuffisante, Fuite Médicale Vers Chine & Turquie, PHILHEALTH Contrôle Limité",
        52.0, 48.0, 46.0, 50.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-007",
        "OMS/Déclaration Istanbul Auto-Suffisance Don Organes",
        "Global",
        "Principe Auto-Suffisance Don Organes, Protocole Transplant International, Application Limitée 60% Pays Signataires, Suivi Insuffisant",
        27.0, 24.0, 23.0, 25.0,
    ),
    OrganTraffickingBodyAutonomyRightsEntity(
        "OTB-008",
        "Espagne/ONT Don Volontaire Post-Mortem Modèle Mondial",
        "Espagne",
        "Organización Nacional de Trasplantes, Don Volontaire Post-Mortem, Modèle Mondial 47 Donneurs/Million, Auto-Suffisance Totale Exemplaire",
        5.0, 4.0, 3.0, 4.0,
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
        "domain": "organ_trafficking_body_autonomy_rights",
        "confidence_score": 0.88,
        "data_sources": [
            "china_tribunal_2019_report",
            "who_global_observatory_transplantation",
            "declaration_of_istanbul_custodian_group",
            "interpol_trafficking_human_beings_reports",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_organ_trafficking_body_autonomy_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_organ_trafficking_body_autonomy_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Organ Trafficking Body Autonomy Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    print(f"Distribution: {r['risk_distribution']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
