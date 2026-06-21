"""
Caelum Partners — Forced Marriage Child Marriage Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Mariage forcé et mariage des enfants : violations systémiques du consentement, de l'éducation
et des droits fondamentaux des femmes et des filles.

Le mariage des enfants et le mariage forcé constituent des violations graves des droits humains
reconnus par la Convention relative aux droits de l'enfant (CRC, 1989), la CEDAW (1979) et
les résolutions de l'Assemblée générale de l'ONU. Ces pratiques privent les filles de leur
droit à l'éducation, à la santé reproductive, et à un avenir libre de violence conjugale.

Le Niger détient le taux mondial le plus élevé de mariage des enfants : 76% des filles sont
mariées avant leurs 18 ans selon UNICEF 2023, principalement dans les régions rurales du Sahel
où la pauvreté, les normes sociales et le manque d'éducation perpétuent le cycle. Au Bangladesh,
52% des filles sont mariées avant 18 ans, avec une concentration dans les ménages sous le seuil
de pauvreté. En Éthiopie, le conflit du Tigré (2020-2022) a exacerbé les mariages forcés de
survie, les familles mariant leurs filles pour obtenir une dot en période de famine.

Risk levels (mariage forcé et mariage des enfants) :
  critique  -> composite >= 60  (prévalence systémique — mariage des enfants institutionnalisé)
  élevé     -> composite >= 40  (exploitation active — millions de filles mariées chaque année)
  modéré    -> composite >= 20  (risque résiduel — cadres légaux insuffisants sans application)
  faible    -> composite < 20   (protection exemplaire — normes internationales respectées)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "mariage_enfants_prevalence_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Éradication urgente — programmes conditionnels de maintien des filles à l'école, interdiction légale stricte avec poursuites des parents et officiers, financement UNFPA programmes autonomisation",
        "signal_fr": "child_marriage_prevalence_harm_severity_score > 85 — taux de mariage des enfants supérieur à 50% indiquant une pratique institutionnalisée profondément ancrée dans les normes sociales",
    },
    "mariage_force_coercition_consentement": {
        "severity_fr": "Critique",
        "action_fr": "Intervention judiciaire — sanctions pénales des auteurs de mariages forcés, lignes d'urgence pour filles et femmes, centres d'accueil protégés et procédures d'annulation simplifiées",
        "signal_fr": "forced_marriage_coercion_consent_violation_scale_score > 85 — violation systémique du consentement par coercition familiale, pressions économiques ou menaces de violence",
    },
    "exclusion_education_filles": {
        "severity_fr": "Critique",
        "action_fr": "Scolarisation prioritaire — transferts conditionnels pour maintien à l'école, centres d'accueil pour filles fuyant mariages forcés et programmes de rattrapage scolaire post-mariage",
        "signal_fr": "girl_education_disruption_exclusion_score > 85 — déscolarisation massive des filles liée au mariage précoce, cycle intergénérationnel de pauvreté et exclusion",
    },
    "deficit_age_legal_application": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme législative — révision codes familiaux, suppression exceptions judiciaires et parentales, systèmes d'état civil renforcés et formation des magistrats au droit des filles",
        "signal_fr": "Écart significatif entre l'âge légal minimum au mariage et l'application réelle par manque de systèmes d'état civil ou de volonté politique",
    },
    "protection_mariage_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter standards protection — financement Girls Not Brides, partage bonnes pratiques légales et soutien financier aux pays à haute prévalence",
        "signal_fr": "composite_score < 20 — respect effectif des normes CRC Art.16 et CEDAW avec âge minimum 18 ans appliqué sans exception",
    },
}


@dataclass
class ForcedMarriageChildMarriageRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    child_marriage_prevalence_harm_severity_score: float
    forced_marriage_coercion_consent_violation_scale_score: float
    girl_education_disruption_exclusion_score: float
    legal_minimum_age_enforcement_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_forced_marriage_child_marriage_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.child_marriage_prevalence_harm_severity_score * 0.30
            + self.forced_marriage_coercion_consent_violation_scale_score * 0.25
            + self.girl_education_disruption_exclusion_score * 0.25
            + self.legal_minimum_age_enforcement_deficit_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_forced_marriage_child_marriage_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.child_marriage_prevalence_harm_severity_score >= 85:
            return "mariage_enfants_prevalence_systemique"
        if self.forced_marriage_coercion_consent_violation_scale_score >= 85:
            return "mariage_force_coercition_consentement"
        if self.girl_education_disruption_exclusion_score >= 85:
            return "exclusion_education_filles"
        if self.composite_score >= 20:
            return "deficit_age_legal_application"
        return "protection_mariage_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Mariage des enfants critique de {n} — filles mariées de force avant 18 ans, privées d'éducation, exposées aux violences conjugales et aux grossesses précoces mettant leur vie en danger",
                "Violation systémique du consentement — le mariage forcé constitue une forme d'esclavage moderne reconnue par le Statut de Rome, avec responsabilité des États qui le tolèrent",
                "Cercle vicieux intergénérationnel — les mères-enfants reproduisent les schémas de pauvreté, leurs filles étant à leur tour exposées au mariage précoce sans accès à l'éducation",
            ]
        if self.risk_level == "élevé":
            return [
                f"Exploitation matrimoniale de {n} — millions de filles mariées avant 18 ans dans un contexte de prévalence élevée sans mécanismes efficaces de protection et d'application légale",
                "Impunité des pratiques traditionnelles — l'absence de poursuites judiciaires normalise le mariage des enfants comme norme sociale acceptable malgré les interdictions légales",
                "Exclusion éducative structurelle — le décrochage scolaire lié au mariage précoce perpétue la vulnérabilité économique et la dépendance des femmes vis-à-vis de leurs époux",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque résiduel mariage enfants de {n} — incidents documentés sans institutionnalisation, cadres légaux insuffisamment appliqués ou exceptions judiciaires permettant des mariages précoces",
                "Vulnérabilités structurelles — pauvreté, normes de genre et systèmes d'état civil défaillants créent des conditions propices au maintien des mariages d'enfants",
                "Progrès fragiles — les avancées législatives peuvent être inversées par des pressions conservatrices, des conflits armés ou des crises économiques réduisant l'accès à l'éducation",
            ]
        return [
            f"{n} représente les standards de protection exemplaire contre le mariage des enfants — application stricte de l'âge minimum de 18 ans sans exception judiciaire ou parentale",
            "Normes CRC et CEDAW respectées — systèmes d'état civil solides, éducation accessible aux filles et programmes de sensibilisation communautaire actifs",
            "Modèle exportable — financement Girls Not Brides, partage de bonnes pratiques légales et soutien technique aux pays à haute prévalence de mariage des enfants",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "child_marriage_prevalence_harm_severity_score": self.child_marriage_prevalence_harm_severity_score,
            "forced_marriage_coercion_consent_violation_scale_score": self.forced_marriage_coercion_consent_violation_scale_score,
            "girl_education_disruption_exclusion_score": self.girl_education_disruption_exclusion_score,
            "legal_minimum_age_enforcement_deficit_gap_score": self.legal_minimum_age_enforcement_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_forced_marriage_child_marriage_rights_index": self.estimated_forced_marriage_child_marriage_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ForcedMarriageChildMarriageRightsEntity] = [
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-001",
        "Niger/75% Filles Mariées Avant 18 Ans Sahel",
        "Afrique de l'Ouest",
        "Taux Mondial Le Plus Élevé, 76% Mariées <18 Ans UNICEF 2023, Régions Rurales Zinder & Maradi, Dot Bétail & Pauvreté Extrême",
        92.0, 88.0, 90.0, 85.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-002",
        "Bangladesh/52% Mariage Enfants Pauvreté",
        "Asie du Sud",
        "52% Filles Mariées <18 Ans, Ménages Sous Seuil Pauvreté, Cyclones & Déplacements Accélèrent Mariages & Filles Garçons Charge",
        87.0, 82.0, 85.0, 88.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-003",
        "Éthiopie/Tigré Mariages Forcés Conflit",
        "Afrique de l'Est",
        "Conflit Tigré 2020-2022, Mariages Survie Famine, Filles 12-15 Ans Mariées Dot Bétail, UNICEF 2M Filles À Risque & Déplacement",
        85.0, 90.0, 82.0, 80.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-004",
        "Soudan du Sud/Dot Bétail Filles 12 Ans",
        "Afrique de l'Est",
        "Dot En Bétail Filles 12-15 Ans, Conflit Civil Aggrave Pratiques, 52% Filles Mariées <18 Ans & Impunité Totale Tradition",
        83.0, 88.0, 80.0, 86.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-005",
        "Yemen/32% Filles Avant 15 Ans Guerre",
        "MENA",
        "Guerre Civile Houthis 2015+, 32% Filles Mariées <15 Ans, Mariages Survie Économique, UNICEF 1.4M Filles À Risque 2023",
        55.0, 62.0, 58.0, 52.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-006",
        "Inde/Rajasthan Akha Teej Millions Mariages",
        "Asie du Sud",
        "Festival Akha Teej Mariages Enfants Massifs, 27% Filles Mariées <18 Ans, Rajasthan Bihar UP Zones Haute Prévalence",
        48.0, 52.0, 55.0, 48.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-007",
        "UNICEF/Girls Not Brides Alliance",
        "Global",
        "Alliance 1500 ONG 100 Pays, Plaidoyer Légal & Communautaire, Programmes Maintien Filles École & Sensibilisation",
        22.0, 18.0, 25.0, 20.0,
    ),
    ForcedMarriageChildMarriageRightsEntity(
        "FMCM-008",
        "ONU/CRC Art.16 & CEDAW Mariage Minimum 18 Ans",
        "Global",
        "CRC 1989 Art.16 Consentement, CEDAW 1979 Art.16 Âge Minimum, Résolution AG 73/148 2018 & Protocoles Droits Filles",
        5.0, 4.0, 6.0, 8.0,
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
        "domain": "forced_marriage_child_marriage_rights",
        "confidence_score": 0.86,
        "data_sources": [
            "unicef_child_marriage_database_2023",
            "girls_not_brides_global_tracking",
            "un_cedaw_committee_periodic_reports",
            "hrw_child_marriage_investigations",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_forced_marriage_child_marriage_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_forced_marriage_child_marriage_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Forced Marriage Child Marriage Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
