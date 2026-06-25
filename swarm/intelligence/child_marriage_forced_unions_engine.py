"""
Caelum Partners — Child Marriage Forced Unions Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Mariage d'enfants et unions forcées — mariage précoce, consentement forcé,
impact sur droits filles, accès éducation.

Le mariage d'enfants est une violation des droits humains reconnue par la CEDAW,
la Convention des droits de l'enfant et les ODD. Plus de 650 millions de femmes
vivant aujourd'hui ont été mariées avant l'âge de 18 ans. Chaque année, 12 millions
de filles supplémentaires sont mariées avant leur majorité — soit 33 000 par jour.

Le mariage d'enfants prive les filles de leur enfance, de leur éducation et de leur
autonomie. Il expose les jeunes épouses à des grossesses précoces et dangereuses —
principale cause de mortalité chez les adolescentes de 15-19 ans dans les pays à
revenu faible. Les exceptions religieuses et coutumières dans de nombreux systèmes
juridiques permettent à des lois formellement protectrices d'être contournées avec
la complicité des autorités locales. Les conflits armés, les crises climatiques et
les chocs économiques agissent comme accélérateurs du mariage d'enfants.

Risk levels (prévalence mariage enfants, lacunes légales, abandon scolaire, harm obstétrical) :
  critique  -> composite >= 60  (mariage enfants endémique — 40%+, impunité légale, crise systémique)
  élevé     -> composite >= 40  (prévalence élevée — 20-40%, lois insuffisantes, abandon scolaire massif)
  modéré    -> composite >= 20  (loopholes légaux persistants — exceptions coutumières non résolues)
  faible    -> composite < 20   (cadre protecteur — âge minimum absolu, programmes efficaces)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class ChildMarriageForcedUnionsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    child_marriage_prevalence_girls_score: float
    legal_minimum_age_enforcement_gap_score: float
    education_access_denial_dropout_score: float
    reproductive_coercion_maternal_harm_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_child_marriage_forced_unions_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.child_marriage_prevalence_girls_score * 0.30
            + self.legal_minimum_age_enforcement_gap_score * 0.25
            + self.education_access_denial_dropout_score * 0.25
            + self.reproductive_coercion_maternal_harm_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_child_marriage_forced_unions_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "child_marriage_prevalence_girls_score": self.child_marriage_prevalence_girls_score,
            "legal_minimum_age_enforcement_gap_score": self.legal_minimum_age_enforcement_gap_score,
            "education_access_denial_dropout_score": self.education_access_denial_dropout_score,
            "reproductive_coercion_maternal_harm_score": self.reproductive_coercion_maternal_harm_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_child_marriage_forced_unions_index": self.estimated_child_marriage_forced_unions_index,
            "last_updated": self.last_updated,
        }


@dataclass
class ChildMarriageForcedUnionsEngineResult:
    agent: str = "Child Marriage Forced Unions Engine Agent"
    domain: str = "child_marriage_forced_unions"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_child_marriage_forced_unions_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildMarriageForcedUnionsEntity] = field(default_factory=list)


def run_child_marriage_forced_unions_engine() -> ChildMarriageForcedUnionsEngineResult:
    entities = [
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-001",
            name="Niger — 76% Filles Mariées Avant 18 (Taux Mondial le Plus Élevé), Sécheresse Sahel Pousse Familles",
            country="Niger",
            sector="Mariage Enfants Endémique Sahel",
            child_marriage_prevalence_girls_score=97.0,
            legal_minimum_age_enforcement_gap_score=94.0,
            education_access_denial_dropout_score=93.0,
            reproductive_coercion_maternal_harm_score=91.0,
            primary_pattern="child_marriage_prevalence_girls",
            key_signals=[
                "76% filles mariées avant 18 ans — record mondial absolu",
                "28% mariées avant 15 ans",
                "Crise Sahel accélère mariages précoces comme stratégie survie",
                "Taux alphabétisation filles 11% — lié à abandon scolaire précoce",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-002",
            name="Bangladesh — 59% Avant 18, Lois Exceptions 'Cas Spéciaux', Surge Mariages COVID",
            country="Bangladesh",
            sector="Mariage Enfants & Lacunes Légales",
            child_marriage_prevalence_girls_score=92.0,
            legal_minimum_age_enforcement_gap_score=89.0,
            education_access_denial_dropout_score=87.0,
            reproductive_coercion_maternal_harm_score=85.0,
            primary_pattern="legal_minimum_age_enforcement_gap",
            key_signals=[
                "59% filles mariées avant 18 — 2e taux Asie du Sud",
                "Loi 2017 : exceptions sans limite d'âge minimum dans 'cas spéciaux'",
                "COVID : 13 000 mariages enfants supplémentaires estimés 2020",
                "Garçons portent pression dot sur famille fille",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-003",
            name="Mali — 52% Avant 18, Charia Locale, Conflit Armé Accélère Pratique, Camps IDP Vulnérables",
            country="Mali",
            sector="Mariage Enfants Conflit & Charia",
            child_marriage_prevalence_girls_score=87.0,
            legal_minimum_age_enforcement_gap_score=84.0,
            education_access_denial_dropout_score=83.0,
            reproductive_coercion_maternal_harm_score=81.0,
            primary_pattern="child_marriage_prevalence_girls",
            key_signals=[
                "52% filles mariées avant 18 ans",
                "Nord Mali sous contrôle groupes armés — mariages forcés documentés",
                "Fermeture écoles conflit IDP camps expose filles",
                "Code de la famille 2009 maintient exceptions coutumières",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-004",
            name="Yémen/Guerre — 32% Avant 15, Conflit Détruit Écoles, Familles Vendent Filles pour Survie",
            country="Yémen",
            sector="Mariage Enfants Conflit Armé Humanitaire",
            child_marriage_prevalence_girls_score=82.0,
            legal_minimum_age_enforcement_gap_score=79.0,
            education_access_denial_dropout_score=80.0,
            reproductive_coercion_maternal_harm_score=77.0,
            primary_pattern="education_access_denial_dropout",
            key_signals=[
                "32% filles mariées avant 15 ans — parmi les plus hauts au monde",
                "Conflit détruit 2 500+ écoles — filles premières retirées",
                "Mariages transactionnels dot-dowry pour survie économique",
                "Mortalité maternelle 385/100 000 liée grossesses adolescentes",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-005",
            name="Inde/États Ruraux — 23% National mais 40%+ Bihar/Rajasthan, Balika Vadhu Inefficace",
            country="Inde",
            sector="Mariage Enfants États Ruraux & Caste",
            child_marriage_prevalence_girls_score=55.0,
            legal_minimum_age_enforcement_gap_score=52.0,
            education_access_denial_dropout_score=53.0,
            reproductive_coercion_maternal_harm_score=50.0,
            primary_pattern="child_marriage_prevalence_girls",
            key_signals=[
                "23% national mais disparités massives état par état",
                "Bihar 40% et Rajasthan 35% mariages avant 18",
                "Programme Balika Vadhu impact limité rural",
                "Pression caste pour mariage intra-communautaire précoce",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-006",
            name="Éthiopie — 40% Avant 18, Communautés Pastorales, Programmes Girls Not Brides Impact Mitigé",
            country="Éthiopie",
            sector="Mariage Enfants Communautés Pastorales",
            child_marriage_prevalence_girls_score=50.0,
            legal_minimum_age_enforcement_gap_score=47.0,
            education_access_denial_dropout_score=48.0,
            reproductive_coercion_maternal_harm_score=45.0,
            primary_pattern="child_marriage_prevalence_girls",
            key_signals=[
                "40% filles mariées avant 18 ans",
                "Amhara 68% — région avec taux les plus élevés",
                "Communautés Afar et Somali : mariage avant 12 ans documenté",
                "Girls Not Brides partnership — progrès lents en zones rurales",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-007",
            name="USA — 17 États Encore sans Âge Minimum Absolu 2023, Loopholes Religieux/Judiciaires",
            country="USA",
            sector="Lacunes Légales Mariage Enfants Pays Développé",
            child_marriage_prevalence_girls_score=30.0,
            legal_minimum_age_enforcement_gap_score=34.0,
            education_access_denial_dropout_score=27.0,
            reproductive_coercion_maternal_harm_score=29.0,
            primary_pattern="legal_minimum_age_enforcement_gap",
            key_signals=[
                "17 États sans âge minimum absolu pour mariage en 2023",
                "Exceptions parentales et judiciaires contournent protections",
                "300 000+ enfants mariés USA 2000-2018 selon données CDC",
                "Lobbying religieux bloque réformes législatives dans plusieurs États",
            ],
        ),
        ChildMarriageForcedUnionsEntity(
            entity_id="CMF-008",
            name="Suède — Âge Minimum 18 Absolu depuis 2014, Programme Prévention Diaspora Efficace",
            country="Suède",
            sector="Cadre Référence Protection Mariage Enfants",
            child_marriage_prevalence_girls_score=5.0,
            legal_minimum_age_enforcement_gap_score=4.0,
            education_access_denial_dropout_score=6.0,
            reproductive_coercion_maternal_harm_score=4.0,
            primary_pattern="legal_minimum_age_enforcement_gap",
            key_signals=[
                "Âge minimum mariage 18 absolu — aucune exception depuis 2014",
                "Programme Länsstyrelsen prévention mariages forcés diaspora",
                "Non-reconnaissance mariages enfants étrangers depuis 2019",
                "Taux scolarisation filles 99% — corrélation protection forte",
            ],
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return ChildMarriageForcedUnionsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_marriage_forced_unions_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "girls_not_brides_global_data_2023",
            "unicef_child_marriage_data_2023",
            "icrw_child_marriage_atlas_2023",
            "human_rights_watch_child_marriage_reports_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_child_marriage_forced_unions_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_marriage_forced_unions_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
