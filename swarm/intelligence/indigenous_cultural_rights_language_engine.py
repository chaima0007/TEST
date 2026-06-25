"""
Caelum Partners — Indigenous Cultural Rights & Language Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droits culturels autochtones et langues : extinction linguistique, assimilation, sites sacrés, transmission.

Les peuples autochtones du monde — estimés à 476 millions de personnes dans 90 pays —
sont les gardiens de 80 % de la biodiversité mondiale et détenteurs de langues, savoirs
et systèmes culturels uniques. La Déclaration des Nations Unies sur les droits des peuples
autochtones (DNUDPA, 2007) reconnaît leur droit à la culture, la langue, l'éducation et
la protection de leurs sites sacrés. Pourtant, l'érosion culturelle reste massive.

Parmi les 7 000 langues du monde, 40 % sont menacées d'extinction — dont la grande majorité
sont des langues autochtones. En Australie, les politiques de l'État colonial ont conduit
à la disparition de centaines de langues et à la dislocation culturelle des générations
volées (Stolen Generations). Au Canada, les pensionnats autochtones ont détruit des
transmissions culturelles pour des générations. Au Brésil, l'Amazonie abrite 270 langues
autochtones dont beaucoup comptent moins de 100 locuteurs.

La pression d'assimilation culturelle — que ce soit par les politiques éducatives,
l'extractivisme sur les terres ancestrales ou la destruction des sites sacrés — constitue
une forme de génocide culturel documentée par les organes de traités de l'ONU.

Risk levels (extinction langue, assimilation, protection sites sacrés, transmission culturelle) :
  critique  -> composite >= 60  (érosion culturelle systémique — langues mourantes, sites détruits)
  élevé     -> composite >= 40  (risque élevé — pression assimilation active, transmission menacée)
  modéré    -> composite >= 20  (revitalisation partielle — politiques mitigées, progrès inégaux)
  faible    -> composite < 20   (pluralisme constitutionnel — droits reconnus et appliqués)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class IndigenousCulturalRightsLanguageEntity:
    entity_id: str
    name: str
    country: str
    context: str
    sub1_language_extinction_risk: float
    sub2_cultural_assimilation_pressure: float
    sub3_sacred_sites_protection: float
    sub4_cultural_transmission: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_cultural_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.sub1_language_extinction_risk * 0.30
            + self.sub2_cultural_assimilation_pressure * 0.25
            + self.sub3_sacred_sites_protection * 0.25
            + self.sub4_cultural_transmission * 0.20,
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
        self.estimated_cultural_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "context": self.context,
            "composite_score": self.composite_score,
            "sub1_language_extinction_risk": self.sub1_language_extinction_risk,
            "sub2_cultural_assimilation_pressure": self.sub2_cultural_assimilation_pressure,
            "sub3_sacred_sites_protection": self.sub3_sacred_sites_protection,
            "sub4_cultural_transmission": self.sub4_cultural_transmission,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_cultural_rights_index": self.estimated_cultural_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class IndigenousCulturalRightsLanguageEngineResult:
    agent: str = "Indigenous Cultural Rights & Language Engine Agent"
    domain: str = "indigenous_cultural_rights_language"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_cultural_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousCulturalRightsLanguageEntity] = field(default_factory=list)


def run_indigenous_cultural_rights_language_engine() -> IndigenousCulturalRightsLanguageEngineResult:
    entities = [
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-001",
            name="Australie (Stolen Generations legacy — 250 langues disparues, 13 survivantes en danger)",
            country="Australie",
            context="Colonisation britannique — peuples aborigènes et insulaires du détroit de Torres",
            sub1_language_extinction_risk=85.0,
            sub2_cultural_assimilation_pressure=83.0,
            sub3_sacred_sites_protection=80.0,
            sub4_cultural_transmission=78.0,
            primary_pattern="sub1_language_extinction_risk",
            key_signals=[
                "Stolen Generations : 100 000+ enfants enlevés 1910-1970",
                "250 langues aborigènes disparues depuis colonisation",
                "Sites sacrés détruits légalement (Mine Rio Tinto Juukan Gorge 2020)",
                "Taux survie langues : <10% des 250 langues pré-contact",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-002",
            name="Canada (pensionnats legacy — 150 000 enfants, 1 000+ langues premières en déclin)",
            country="Canada",
            context="Colonisation britannique/française — 634 Premières Nations, Métis, Inuit",
            sub1_language_extinction_risk=80.0,
            sub2_cultural_assimilation_pressure=78.0,
            sub3_sacred_sites_protection=76.0,
            sub4_cultural_transmission=74.0,
            primary_pattern="sub2_cultural_assimilation_pressure",
            key_signals=[
                "Pensionnats indiens : 150 000 enfants, 3 000+ décès documentés",
                "Rapport Vérité et Réconciliation 2015 : 94 appels à l'action",
                "60% des langues autochtones canadiennes en danger critique",
                "Tombes anonymes découvertes depuis 2021 — traumatisme national",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-003",
            name="USA (langues amérindiennes mourantes — 175 langues, 20 locuteurs natifs en moyenne)",
            country="États-Unis",
            context="Décolonisation incomplète — 574 nations reconnues fédéralement",
            sub1_language_extinction_risk=77.0,
            sub2_cultural_assimilation_pressure=75.0,
            sub3_sacred_sites_protection=73.0,
            sub4_cultural_transmission=72.0,
            primary_pattern="sub1_language_extinction_risk",
            key_signals=[
                "175 langues amérindiennes encore parlées sur 300+ originelles",
                "80% des langues restantes : moins de 100 locuteurs natifs",
                "Loi NAGPRA sous-appliquée — rapatriement restes ancestraux lent",
                "Standing Rock 2016 : droits culturels vs pipeline Dakota Access",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-004",
            name="Brésil (Amazonie — 270 langues autochtones menacées, déforestation sites sacrés)",
            country="Brésil",
            context="Amazonie — 305 peuples autochtones, terres ancestrales sous pression extractiviste",
            sub1_language_extinction_risk=72.0,
            sub2_cultural_assimilation_pressure=70.0,
            sub3_sacred_sites_protection=68.0,
            sub4_cultural_transmission=67.0,
            primary_pattern="sub1_language_extinction_risk",
            key_signals=[
                "270 langues autochtones — 40% avec moins de 100 locuteurs",
                "Garimpos illégaux détruisent terres Yanomami et sites sacrés",
                "FUNAI affaiblie — protection juridique territoriale insuffisante",
                "Peuples non-contactés menacés par avancée déforestation",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-005",
            name="Mexique (52 langues autochtones — discrimination structurelle et urbanisation)",
            country="Mexique",
            context="Mésoamérique — 68 groupes ethnolinguistiques, 7,4 M locuteurs",
            sub1_language_extinction_risk=56.0,
            sub2_cultural_assimilation_pressure=54.0,
            sub3_sacred_sites_protection=52.0,
            sub4_cultural_transmission=53.0,
            primary_pattern="sub1_language_extinction_risk",
            key_signals=[
                "52 groupes linguistiques, dont plusieurs en danger immédiat",
                "INALI crée 2003 mais financement insuffisant",
                "Discrimination linguistique systémique dans éducation et justice",
                "Train Maya : projets infra dégradent sites archéologiques sacrés",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-006",
            name="Guatemala (Maya — discrimination institutionnelle, 22 langues, accès justice limité)",
            country="Guatemala",
            context="Mésoamérique — 43% population maya, 22 langues mayas vivantes",
            sub1_language_extinction_risk=47.0,
            sub2_cultural_assimilation_pressure=46.0,
            sub3_sacred_sites_protection=44.0,
            sub4_cultural_transmission=46.0,
            primary_pattern="sub2_cultural_assimilation_pressure",
            key_signals=[
                "22 langues mayas — ALMG protège mais ressources insuffisantes",
                "Génocide Maya 1981-83 : traumatisme culturel multigénérationnel",
                "Éducation bilingue interculturelle sous-financée",
                "Sites cérémoniels mayas spoliés par projets miniers",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-007",
            name="Nouvelle-Zélande (revitalisation Māori — Te Reo en renaissance, cadre biculturel)",
            country="Nouvelle-Zélande",
            context="Pacifique — Traité de Waitangi, 15% population Māori",
            sub1_language_extinction_risk=28.0,
            sub2_cultural_assimilation_pressure=26.0,
            sub3_sacred_sites_protection=27.0,
            sub4_cultural_transmission=25.0,
            primary_pattern="sub1_language_extinction_risk",
            key_signals=[
                "Te Reo Māori langue officielle depuis 1987",
                "Kura Kaupapa : écoles d'immersion māori en expansion",
                "Tribunal Waitangi : recours pour violations culturelles",
                "157 000 locuteurs Te Reo (recensement 2018) — en hausse",
            ],
        ),
        IndigenousCulturalRightsLanguageEntity(
            entity_id="ICR-008",
            name="Bolivie (plurinationalité constitutionnelle — 36 nations reconnues, langues co-officielles)",
            country="Bolivie",
            context="Andes-Amazonie — État plurinational, 36 peuples autochtones constitutionnellement reconnus",
            sub1_language_extinction_risk=14.0,
            sub2_cultural_assimilation_pressure=13.0,
            sub3_sacred_sites_protection=15.0,
            sub4_cultural_transmission=14.0,
            primary_pattern="sub3_sacred_sites_protection",
            key_signals=[
                "Constitution 2009 : 36 nations autochtones reconnues, 37 langues co-officielles",
                "Quechua et Aymara : millions de locuteurs, enseignement obligatoire",
                "Evo Morales : premier président autochtone (Aymara), 2006-2019",
                "Loi TIPNIS protège territoire indigène amazonie bolivienne",
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
        f"{e.name.split('(')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return IndigenousCulturalRightsLanguageEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_cultural_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_permanent_forum_indigenous_peoples_state_of_world_2023",
            "ethnologue_endangered_languages_global_database",
            "cultural_survival_indigenous_rights_country_reports",
            "iwgia_indigenous_world_2024_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_indigenous_cultural_rights_language_engine()
    print(f"=== Indigenous Cultural Rights & Language Engine — Wave 161 ===")
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_cultural_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: composite={e.composite_score} [{e.risk_level}] | index={e.estimated_cultural_rights_index}")
    print()
    assert result.risk_distribution.get("critique", 0) == 4, f"ERREUR: critique={result.risk_distribution.get('critique',0)} (attendu 4)"
    assert result.risk_distribution.get("élevé", 0) == 2, f"ERREUR: élevé={result.risk_distribution.get('élevé',0)} (attendu 2)"
    assert result.risk_distribution.get("modéré", 0) == 1, f"ERREUR: modéré={result.risk_distribution.get('modéré',0)} (attendu 1)"
    assert result.risk_distribution.get("faible", 0) == 1, f"ERREUR: faible={result.risk_distribution.get('faible',0)} (attendu 1)"
    print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
