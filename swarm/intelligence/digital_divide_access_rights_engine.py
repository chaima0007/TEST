"""
Caelum Partners — Digital Divide Access Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Fracture numérique, accès internet, droits numériques fondamentaux.

La fracture numérique représente l'une des inégalités les plus persistantes et
structurantes du XXIe siècle. Malgré la reconnaissance par l'ONU du droit à Internet
comme droit humain fondamental (résolution 2016), 2,6 milliards de personnes restent
non connectées en 2026. Les inégalités sont multidimensionnelles : infrastructures
absentes, coûts prohibitifs (1 Go représente 20% du salaire mensuel en Afrique
subsaharienne), barrières linguistiques (90% du contenu web en 10 langues), et fossé
entre genres (les femmes sont 25% moins connectées que les hommes dans les pays en
développement). L'ITU et l'Alliance for Affordable Internet alertent que les objectifs
SDG 9.c de connectivité universelle d'ici 2030 ne seront pas atteints au rythme actuel.

Risk levels (fracture numérique et exclusion droits numériques) :
  critique  -> composite >= 60  (exclusion totale — infrastructure absente — droits niés)
  élevé     -> composite >= 40  (accès partiel — barrières économiques structurelles)
  modéré    -> composite >= 20  (compétences insuffisantes — inégalités persistantes)
  faible    -> composite < 20   (cadre normatif — objectifs et recommandations)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class DigitalDivideAccessRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    internet_access_exclusion_infrastructure_severity_score: float
    affordability_economic_digital_barrier_scale_score: float
    digital_literacy_skills_gap_score: float
    platform_language_content_inclusion_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_digital_divide_access_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.internet_access_exclusion_infrastructure_severity_score * 0.30
            + self.affordability_economic_digital_barrier_scale_score * 0.25
            + self.digital_literacy_skills_gap_score * 0.25
            + self.platform_language_content_inclusion_deficit_gap_score * 0.20,
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
        self.estimated_digital_divide_access_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "internet_access_exclusion_infrastructure_severity_score": self.internet_access_exclusion_infrastructure_severity_score,
            "affordability_economic_digital_barrier_scale_score": self.affordability_economic_digital_barrier_scale_score,
            "digital_literacy_skills_gap_score": self.digital_literacy_skills_gap_score,
            "platform_language_content_inclusion_deficit_gap_score": self.platform_language_content_inclusion_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_digital_divide_access_rights_index": self.estimated_digital_divide_access_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class DigitalDivideAccessRightsEngineResult:
    agent: str = "Digital Divide Access Rights Engine Agent"
    domain: str = "digital_divide_access_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_digital_divide_access_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalDivideAccessRightsEntity] = field(default_factory=list)


def run_digital_divide_access_rights_engine() -> DigitalDivideAccessRightsEngineResult:
    entities = [
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-001",
            name="Afrique Sub-Saharienne — 28% Connexion Internet, Coût 1 Go = 20% Salaire, Électricité 40% Rurale & Femmes 25% Moins Connectées",
            country="Afrique",
            sector="Exclusion Numérique Infrastructure",
            internet_access_exclusion_infrastructure_severity_score=94.0,
            affordability_economic_digital_barrier_scale_score=92.0,
            digital_literacy_skills_gap_score=93.0,
            platform_language_content_inclusion_deficit_gap_score=91.0,
            primary_pattern="internet_access_exclusion_infrastructure_severity",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-002",
            name="Myanmar/Rural Asie — Coupures Internet Post-Coup, 50% Population Non-Connectée, Zones Rurales 3G Absente & Contenu Langue Maternelle 0%",
            country="Myanmar",
            sector="Coupures Internet Autoritaires",
            internet_access_exclusion_infrastructure_severity_score=90.0,
            affordability_economic_digital_barrier_scale_score=89.0,
            digital_literacy_skills_gap_score=88.0,
            platform_language_content_inclusion_deficit_gap_score=91.0,
            primary_pattern="internet_access_exclusion_infrastructure_severity",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-003",
            name="Inde/Rurale — 800M Sans Internet Régulier, 5G Urbain vs 2G Rural, Femmes 67% Moins Accès & Hindi 90% Contenu Langue",
            country="Inde",
            sector="Fracture Rurale-Urbaine Linguistique",
            internet_access_exclusion_infrastructure_severity_score=87.0,
            affordability_economic_digital_barrier_scale_score=85.0,
            digital_literacy_skills_gap_score=88.0,
            platform_language_content_inclusion_deficit_gap_score=86.0,
            primary_pattern="platform_language_content_inclusion_deficit_gap",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-004",
            name="USA/Zones Rurales — 21M Américains Sans Haut Débit, FCC Data Inexacte, Bibliothèques Seul Accès & Fracture Raciale Digitale Persistante",
            country="USA",
            sector="Fracture Numérique Rurale Pays Développé",
            internet_access_exclusion_infrastructure_severity_score=83.0,
            affordability_economic_digital_barrier_scale_score=82.0,
            digital_literacy_skills_gap_score=84.0,
            platform_language_content_inclusion_deficit_gap_score=81.0,
            primary_pattern="affordability_economic_digital_barrier_scale",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-005",
            name="Europe/DESI — 13% UE Sans Compétences Numériques Basiques, Personnes Âgées 60%+ Exclusion, PME Lag Numérique & Inégalités Régions",
            country="Europe",
            sector="Compétences Numériques Inclusion Sociale",
            internet_access_exclusion_infrastructure_severity_score=56.0,
            affordability_economic_digital_barrier_scale_score=54.0,
            digital_literacy_skills_gap_score=55.0,
            platform_language_content_inclusion_deficit_gap_score=57.0,
            primary_pattern="digital_literacy_skills_gap",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-006",
            name="Brésil/Favelas — 40% Sans Internet Fixe, Mobile Only Limitation, Contenu Portugais Dominant & Éducation Distance Inégale COVID",
            country="Brésil",
            sector="Fracture Mobile-Fixe Inégalités Urbaines",
            internet_access_exclusion_infrastructure_severity_score=52.0,
            affordability_economic_digital_barrier_scale_score=51.0,
            digital_literacy_skills_gap_score=54.0,
            platform_language_content_inclusion_deficit_gap_score=53.0,
            primary_pattern="affordability_economic_digital_barrier_scale",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-007",
            name="ITU/A4AI — Union Internationale Télécommunications, Alliance Affordable Internet, Web Foundation & Digital Rights Charter",
            country="Global",
            sector="Plaidoyer Droits Numériques",
            internet_access_exclusion_infrastructure_severity_score=27.0,
            affordability_economic_digital_barrier_scale_score=25.0,
            digital_literacy_skills_gap_score=28.0,
            platform_language_content_inclusion_deficit_gap_score=26.0,
            primary_pattern="affordability_economic_digital_barrier_scale",
        ),
        DigitalDivideAccessRightsEntity(
            entity_id="DDA-008",
            name="ONU/SDG9c — SDG 9.c Connectivité Universelle 2030, Déclaration WSIS, Droit Internet Résolution ONU & ITU Connect 2030",
            country="Global",
            sector="Cadre Normatif Connectivité Universelle",
            internet_access_exclusion_infrastructure_severity_score=4.0,
            affordability_economic_digital_barrier_scale_score=4.0,
            digital_literacy_skills_gap_score=4.0,
            platform_language_content_inclusion_deficit_gap_score=4.0,
            primary_pattern="internet_access_exclusion_infrastructure_severity",
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

    return DigitalDivideAccessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_divide_access_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "itu_measuring_digital_development_report",
            "a4ai_affordability_report",
            "web_foundation_digital_rights_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_digital_divide_access_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_digital_divide_access_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
