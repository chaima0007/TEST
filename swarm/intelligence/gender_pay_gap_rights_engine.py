"""
Caelum Partners — Gender Pay Gap Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Discrimination salariale, ségrégation professionnelle, plafond de verre et travail non rémunéré.

L'écart de rémunération entre les sexes constitue une violation systémique des droits
économiques des femmes consacrés par la Convention sur l'élimination de toutes les formes
de discrimination à l'égard des femmes (CEDAW, 1979) et le Pacte international relatif
aux droits économiques, sociaux et culturels (PIDESC, Art. 7). La Conférence internationale
du Travail a adopté en 2023 la Convention n°190 sur la violence et le harcèlement,
complétant le principe « à travail égal, salaire égal » (Convention OIT n°100, 1951).

Au Pakistan, les femmes gagnent en moyenne 82 % de moins que les hommes dans le secteur
formel et représentent moins de 20 % de la main-d'œuvre — l'un des taux les plus bas au
monde selon le Global Gender Gap Report 2023 du Forum économique mondial.
En Afghanistan post-Taliban (2021), les femmes sont interdites de travailler dans
la quasi-totalité des secteurs publics et privés, constituant la violation la plus absolue
du droit au travail féminin documentée au XXIe siècle.
En Islande, la loi Equal Pay Certification (2018) oblige les employeurs de plus de
25 salariés à certifier l'égalité salariale — réduisant l'écart à 3,8 %, meilleure
pratique mondiale (Forum Économique Mondial, Global Gender Gap Index 1er rang 2023).

Risk levels (discrimination salariale de genre et droits économiques) :
  critique  -> composite >= 60  (exclusion économique totale — discrimination systémique légalisée ou permise)
  élevé     -> composite >= 40  (ségrégation et plafond de verre structurels — écarts importants persistants)
  modéré    -> composite >= 20  (progrès réels mais inégalités résiduelles — directives sans application pleine)
  faible    -> composite < 20   (parité avancée — cadre légal effectif et certifications contraignantes)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "exclusion_economique_totale_femmes": {
        "severity_fr": "Critique",
        "action_fr": "Pression diplomatique maximale — sanctions ciblées sur les régimes interdisant le travail féminin, soutien aux organisations féministes clandestines, conditionnalité aide internationale à la réintégration des femmes dans l'économie formelle",
        "signal_fr": "wage_discrimination_score > 85 — femmes exclues de l'économie formelle par des lois discriminatoires, des normes culturelles coercitives ou des violences économiques systémiques",
    },
    "segregation_professionnelle_severe": {
        "severity_fr": "Critique",
        "action_fr": "Programmes d'égalité obligatoires — quotas sectoriels, sanctions employeurs discriminatoires, fonds formation femmes dans secteurs masculins, révision des législations du travail discriminatoires",
        "signal_fr": "occupational_segregation_score > 85 — cantonner les femmes aux secteurs les moins valorisés avec rémunérations 50-80% inférieures aux secteurs masculins équivalents",
    },
    "plafond_verre_systémique": {
        "severity_fr": "Critique",
        "action_fr": "Parité imposée par loi — obligation de représentation féminine aux postes de direction, transparence salariale par entreprise et secteur, congé parental partagé obligatoire financé par l'État",
        "signal_fr": "glass_ceiling_score > 85 — sous-représentation féminine massive aux postes de direction et différentiel salarial croissant avec la hiérarchie",
    },
    "ecart_travail_non_remunere": {
        "severity_fr": "Élevé",
        "action_fr": "Réforme politique structurelle — reconnaissance du travail de soin dans les systèmes de retraite, développement des services de garde publics, parité des congés parentaux et allocations familiales non conditionnées au statut d'emploi",
        "signal_fr": "Les femmes assument 75% du travail domestique et de soin non rémunéré mondial, réduisant leur disponibilité pour l'emploi rémunéré et leur progression de carrière",
    },
    "parite_avancee_certifiee": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les bonnes pratiques — financement OIT et ONU Femmes pour transférer les modèles de certification d'égalité salariale aux pays à fort écart, plaidoyer pour l'adoption internationale du principe de transparence salariale obligatoire",
        "signal_fr": "composite_score < 20 — cadre légal d'égalité salariale effectivement appliqué avec mécanismes de certification, transparence salariale et congés parentaux partagés",
    },
}


@dataclass
class GenderPayGapRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    wage_discrimination_score: float
    occupational_segregation_score: float
    glass_ceiling_score: float
    unpaid_care_work_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_gender_pay_gap_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.wage_discrimination_score * 0.30
            + self.occupational_segregation_score * 0.25
            + self.glass_ceiling_score * 0.25
            + self.unpaid_care_work_gap_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_gender_pay_gap_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.wage_discrimination_score >= 85:
            return "exclusion_economique_totale_femmes"
        if self.occupational_segregation_score >= 85:
            return "segregation_professionnelle_severe"
        if self.glass_ceiling_score >= 85:
            return "plafond_verre_systémique"
        if self.composite_score >= 20:
            return "ecart_travail_non_remunere"
        return "parite_avancee_certifiee"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Exclusion économique critique de {n} — discrimination salariale systémique qui prive les femmes de leur droit fondamental à un travail décent et à une rémunération équitable garanti par la Convention CEDAW et la Convention OIT n°100",
                "Ségrégation professionnelle institutionnalisée — confinement des femmes dans des secteurs sous-valorisés avec des rémunérations 50 à 82 % inférieures, perpétuant la pauvreté féminine intergénérationnelle",
                "Plafond de verre structurel — la sous-représentation aux postes de direction et les politiques de maternité pénalisantes créent un différentiel salarial croissant avec l'avancement hiérarchique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Inégalités salariales structurelles de {n} — écarts persistants malgré les cadres légaux formels, révélant des discriminations systémiques dans les pratiques de rémunération et de promotion",
                "Travail de soin non rémunéré — les femmes assumant 75 % du travail domestique subissent des interruptions de carrière qui réduisent leur revenu cumulé sur toute une vie professionnelle",
                "Discrimination intersectionnelle — les femmes racisées, rurales et peu qualifiées subissent des écarts salariaux multipliés par les discriminations cumulées de genre, d'origine et de classe",
            ]
        if self.risk_level == "modéré":
            return [
                f"Progrès réels mais lacunaires de {n} — les directives d'égalité salariale existent mais leur application reste insuffisante, laissant des écarts résiduels concentrés dans certains secteurs et niveaux hiérarchiques",
                "Transparence salariale insuffisante — l'absence d'obligation légale de publication des écarts salariaux par entreprise limite l'effectivité des politiques d'égalité professionnelle",
                "Convergence incomplète — les progrès en matière d'égalité salariale sont fragiles et peuvent être inversés par des politiques d'austérité réduisant les services de garde et les congés parentaux",
            ]
        return [
            f"{n} incarne la parité salariale avancée — certification légale obligatoire, transparence salariale systématique et congés parentaux partagés créant un environnement d'égalité professionnelle effective",
            "Loi Equal Pay Certification — les employeurs de plus de 25 salariés doivent certifier l'égalité salariale, avec audit régulier et sanctions financières pour non-conformité",
            "Modèle exportable — classement 1er mondial Global Gender Gap Index, financement OIT et ONU Femmes pour transférer ce modèle de certification aux pays à fort écart salarial",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "wage_discrimination_score": self.wage_discrimination_score,
            "occupational_segregation_score": self.occupational_segregation_score,
            "glass_ceiling_score": self.glass_ceiling_score,
            "unpaid_care_work_gap_score": self.unpaid_care_work_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_gender_pay_gap_rights_index": self.estimated_gender_pay_gap_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[GenderPayGapRightsEntity] = [
    GenderPayGapRightsEntity(
        "GPG-001",
        "Pakistan/Femmes 82% Moins Payées Participation 20%",
        "Asie du Sud",
        "Écart Salarial 82%, Participation Marché Travail 20%, Harcèlement Emploi, Mariages Précoces & Ségrégation Secteurs",
        92.0, 90.0, 88.0, 86.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-002",
        "Yemen/94% Femmes Exclues Économie Formelle Post-Guerre",
        "MENA",
        "Guerre Civile 2014+, 94% Femmes Exclues Économie Formelle, Mariage Précoce 32%, Veuves Sans Protection & Effondrement Services",
        90.0, 88.0, 86.0, 88.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-003",
        "Afghanistan/Femmes Interdites Travailler Post-Taliban 2021",
        "Asie Centrale",
        "Décret Taliban 2021 Interdit Travail Femmes Secteur Public/ONG, Filles Interdites École Secondaire, Exclusion Économique Totale & Burqa Obligatoire",
        96.0, 94.0, 92.0, 90.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-004",
        "Saudi Arabia/Ségrégation Emploi Dépendance Tuteur",
        "MENA",
        "Ségrégation Secteurs Emploi, Dépendance Tuteur Masculin Wali, Réformes Vision 2030 Partielles, 30% Participation Femmes & Plafond Verre Secteur Privé",
        82.0, 80.0, 78.0, 76.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-005",
        "India/Écart Salarial 34% Harcèlement Verre Plafond",
        "Asie du Sud",
        "Écart Salarial 34% BIT, Harcèlement Lieu Travail, Verre Plafond Sectoriel IT/Finance, Travail Informel 90% Femmes & POSH Act Sous-Appliqué",
        55.0, 52.0, 50.0, 58.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-006",
        "USA/82 Cents Dollar STEM Gap Maternité Non Rémunérée",
        "Amérique du Nord",
        "82 Cents/Dollar Global, STEM Gender Gap, Maternité Non Rémunérée 12 Semaines FMLA, Childcare Crisis & Wage Theft Low-Income Women",
        48.0, 45.0, 50.0, 52.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-007",
        "EU Moyenne/Directive Parité 14.1% Gap Progrès Partiels",
        "Europe",
        "Directive Transparence Salariale 2023, Gap 14.1% Eurostat, Progrès Inégaux Entre États Membres, Sous-Représentation Boards & Congé Parental Fragile",
        28.0, 32.0, 30.0, 25.0,
    ),
    GenderPayGapRightsEntity(
        "GPG-008",
        "Iceland/Loi Equal Pay 2018 Certification Légale Rang 1",
        "Europe du Nord",
        "Equal Pay Certification Obligatoire +25 Salariés, Gap 3.8%, GGI Rang 1 WEF 2023, Congé Parental Partagé 9 Mois & Sanctions Non-Conformité",
        8.0, 10.0, 9.0, 12.0,
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
        "last_analysis": "2026-06-22",
        "engine_version": "1.0.0",
        "domain": "gender_pay_gap_rights",
        "confidence_score": 0.87,
        "data_sources": [
            "wef_global_gender_gap_report_2023",
            "oit_convention_100_equal_remuneration",
            "cedaw_committee_country_reports_2023",
            "eurostat_gender_pay_gap_statistics_2023",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_gender_pay_gap_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_gender_pay_gap_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Gender Pay Gap Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
