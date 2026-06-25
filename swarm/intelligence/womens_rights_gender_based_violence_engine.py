"""
Caelum Partners — Women's Rights Gender Based Violence Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droits des femmes et violences basées sur le genre (féminicides, MGF, mariage
forcé, discriminations légales, violence conjugale, dot/bride price).

Les violences basées sur le genre (VBG) constituent la violation des droits humains
la plus répandue au monde : l'OMS estime que 736 millions de femmes — soit une sur
trois — ont subi des violences physiques ou sexuelles. Ces violences ne sont pas
des phénomènes isolés mais des systèmes institutionnalisés soutenus par des lois
discriminatoires, une impunité judiciaire structurelle et des normes culturelles
qui traitent les femmes comme propriété.

En Afghanistan, les talibans ont instauré ce que l'ONU qualifie d'"apartheid de
genre" — seul système au monde qui interdit légalement aux femmes l'éducation,
le travail, la mobilité et l'espace public. En Somalie, la prévalence des
mutilations génitales féminines (98%) s'accompagne d'une absence totale de loi
pénalisant la pratique. En RDC, le viol est utilisé comme arme de guerre à une
échelle documentée comme "capitale mondiale du viol" par l'ONU.

Risk levels (féminicides, MGF, mariage forcé, discriminations légales) :
  critique  -> composite >= 60  (VBG systémique — apartheid genre, viol arme de guerre, MGF quasi-universelle)
  élevé     -> composite >= 40  (féminicides impunis — VBG documentée, discriminations légales persistantes)
  modéré    -> composite >= 20  (progrès légaux réels — féminicides persistants, lacunes application)
  faible    -> composite < 20   (modèle égalité genre — féminicides quasi-inexistants, MGF absente)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class WomensRightsGenderBasedViolenceEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    femicide_gender_violence_impunity_score: float
    fgm_forced_marriage_child_marriage_score: float
    legal_discrimination_women_rights_gap_score: float
    womens_protection_access_justice_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_womens_rights_gender_based_violence_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.femicide_gender_violence_impunity_score * 0.30
            + self.fgm_forced_marriage_child_marriage_score * 0.25
            + self.legal_discrimination_women_rights_gap_score * 0.25
            + self.womens_protection_access_justice_score * 0.20,
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
        self.estimated_womens_rights_gender_based_violence_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "femicide_gender_violence_impunity_score": self.femicide_gender_violence_impunity_score,
            "fgm_forced_marriage_child_marriage_score": self.fgm_forced_marriage_child_marriage_score,
            "legal_discrimination_women_rights_gap_score": self.legal_discrimination_women_rights_gap_score,
            "womens_protection_access_justice_score": self.womens_protection_access_justice_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_womens_rights_gender_based_violence_index": self.estimated_womens_rights_gender_based_violence_index,
            "last_updated": self.last_updated,
        }


@dataclass
class WomensRightsGenderBasedViolenceEngineResult:
    agent: str = "Women's Rights Gender Based Violence Engine Agent"
    domain: str = "womens_rights_gender_based_violence"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_womens_rights_gender_based_violence_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WomensRightsGenderBasedViolenceEntity] = field(default_factory=list)


def run_womens_rights_gender_based_violence_engine() -> WomensRightsGenderBasedViolenceEngineResult:
    entities = [
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-001",
            name="Afghanistan — Apartheid Genre Talibans, Exclusion Éducation/Travail/Espace Public & Peine Mort Adultère",
            country="Afghanistan",
            sector="Droits Femmes & Discrimination Légale Totale",
            femicide_gender_violence_impunity_score=97.0,
            fgm_forced_marriage_child_marriage_score=94.0,
            legal_discrimination_women_rights_gap_score=99.0,
            womens_protection_access_justice_score=98.0,
            primary_pattern="legal_discrimination_women_rights_gap",
            key_signals=[
                "apartheid de genre reconnu par ONU 2023",
                "interdiction éducation filles depuis 2021",
                "interdiction espace public sans mahram",
                "peine mort adultère appliquée",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-002",
            name="Somalie — MGF 98% Prévalence Sans Loi, Mariage Enfants 45% Avant 18 Ans & Viol Al-Shabaab",
            country="Somalie",
            sector="MGF & Mariage Enfants & Viol Conflit",
            femicide_gender_violence_impunity_score=94.0,
            fgm_forced_marriage_child_marriage_score=97.0,
            legal_discrimination_women_rights_gap_score=92.0,
            womens_protection_access_justice_score=93.0,
            primary_pattern="fgm_forced_marriage_child_marriage",
            key_signals=[
                "98% prévalence MGF — plus haute au monde",
                "pas de loi criminalisant MGF",
                "45% filles mariées avant 18 ans",
                "viol arme de guerre Al-Shabaab documenté",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-003",
            name="RD Congo — Viol Arme Guerre Systématique Est Congo, 400K+ Viols/An & Impunité Milices Femmes Stigmatisées",
            country="RD Congo",
            sector="Viol Conflit Armé & VBG Systémique",
            femicide_gender_violence_impunity_score=93.0,
            fgm_forced_marriage_child_marriage_score=89.0,
            legal_discrimination_women_rights_gap_score=90.0,
            womens_protection_access_justice_score=91.0,
            primary_pattern="femicide_gender_violence_impunity",
            key_signals=[
                "400 000+ viols/an documentés ONU MONUSCO",
                "viol arme de guerre M23/FDLR/ADF",
                "stigmatisation survivantes rejetées familles",
                "impunité quasi-totale milices armées",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-004",
            name="Yémen — Mariage Enfants 32% Avant 15 Ans, Violence Conflit Sur Femmes & Blocus Soins Maternels",
            country="Yémen",
            sector="Mariage Enfants & VBG Conflit",
            femicide_gender_violence_impunity_score=88.0,
            fgm_forced_marriage_child_marriage_score=86.0,
            legal_discrimination_women_rights_gap_score=87.0,
            womens_protection_access_justice_score=88.0,
            primary_pattern="fgm_forced_marriage_child_marriage",
            key_signals=[
                "32% filles mariées avant 15 ans",
                "blocus soins maternels mortalité élevée",
                "violence conflit cible femmes déplacées",
                "loi discriminatoire statut personnel",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-005",
            name="Inde — Féminicides Dot 7 000+/An, Viols Collectifs Impunis & MGF Dawoodi Bohra Crimes Honneur Haryana",
            country="Inde",
            sector="Féminicides & Violence Basée Genre",
            femicide_gender_violence_impunity_score=57.0,
            fgm_forced_marriage_child_marriage_score=54.0,
            legal_discrimination_women_rights_gap_score=52.0,
            womens_protection_access_justice_score=53.0,
            primary_pattern="femicide_gender_violence_impunity",
            key_signals=[
                "7 000+ meurtres dot annuels NCRB",
                "viols collectifs haute médiatisation — impunité",
                "MGF Dawoodi Bohra pratiquée clandestinement",
                "crimes honneur Haryana/Rajasthan tribunaux",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-006",
            name="Mexique — Féminicides 10/Jour, 95% Impunité, Cartels Violence Femmes & Protocole ALBA Insuffisant",
            country="Mexique",
            sector="Féminicides & Impunité Structurelle",
            femicide_gender_violence_impunity_score=55.0,
            fgm_forced_marriage_child_marriage_score=48.0,
            legal_discrimination_women_rights_gap_score=50.0,
            womens_protection_access_justice_score=54.0,
            primary_pattern="femicide_gender_violence_impunity",
            key_signals=[
                "10 féminicides/jour — 3 600+/an",
                "95% impunité féminicides SESNSP",
                "disparitions femmes Ciudad Juárez continue",
                "cartels violence sexuelle outil contrôle",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-007",
            name="France — 106 Féminicides 2023, Progrès Légaux Réels Bracelet Électronique & Persistance Violence Intra-Familiale",
            country="France",
            sector="Féminicides & Violence Conjugale",
            femicide_gender_violence_impunity_score=25.0,
            fgm_forced_marriage_child_marriage_score=20.0,
            legal_discrimination_women_rights_gap_score=22.0,
            womens_protection_access_justice_score=23.0,
            primary_pattern="femicide_gender_violence_impunity",
            key_signals=[
                "106 féminicides 2023 malgré progrès",
                "bracelet électronique auteurs mesure avancée",
                "MGF criminalisée quelques poursuites",
                "égalité légale acquise — application imparfaite",
            ],
        ),
        WomensRightsGenderBasedViolenceEntity(
            entity_id="WRG-008",
            name="Islande — Égalité Salariale Loi 2018, Pas de MGF, Féminicides Quasi-Inexistants & Modèle Nordique",
            country="Islande",
            sector="Égalité Genre & Droits Femmes",
            femicide_gender_violence_impunity_score=6.0,
            fgm_forced_marriage_child_marriage_score=4.0,
            legal_discrimination_women_rights_gap_score=5.0,
            womens_protection_access_justice_score=5.0,
            primary_pattern="womens_protection_access_justice",
            key_signals=[
                "loi égalité salariale obligation certification 2018",
                "zéro MGF pratiquée",
                "féminicides quasi-inexistants statistiques",
                "1er rang Global Gender Gap Index WEF",
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

    return WomensRightsGenderBasedViolenceEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_womens_rights_gender_based_violence_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_women_gender_based_violence_report_2023",
            "who_global_prevalence_violence_against_women_2021",
            "girls_not_brides_child_marriage_database_2023",
            "equality_now_womens_rights_global_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_womens_rights_gender_based_violence_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_womens_rights_gender_based_violence_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
