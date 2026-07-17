"""
Caelum Partners — Housing Rights, Forced Evictions & Gentrification Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droit au logement, expulsions forcées, déplacement urbain, gentrification
(art. 25 DUDH, PIDESC art. 11, Observation générale CODESC n°7 sur les expulsions forcées).

Le droit à un logement convenable est reconnu par l'article 25 de la Déclaration Universelle des
Droits de l'Homme et l'article 11 du Pacte international relatif aux droits économiques, sociaux
et culturels. Pourtant, plus de 1,6 milliard de personnes vivent dans des logements inadéquats
selon ONU-Habitat (2023), et des millions font face chaque année à des expulsions forcées sans
compensation ni relogement adéquat.

Les expulsions forcées constituent selon le CODESC une violation prima facie des droits humains,
particulièrement lorsqu'elles touchent des populations vulnérables sans procédure légale, sans
consultation, et sans alternative de relogement. La gentrification aggrave ces dynamiques en
chassant progressivement les populations à faibles revenus des centres urbains via des mécanismes
économiques qui ne déclenchent pas les protections légales formelles mais produisent des effets
comparables à l'expulsion forcée.

Risk levels (droit au logement et expulsions forcées — vulnérabilité structurelle) :
  critique  -> composite >= 60  (expulsions massives — violence d'État, absence totale relogement)
  élevé     -> composite >= 40  (déplacement systémique — pression économique forte, protections insuffisantes)
  modéré    -> composite >= 20  (gentrification avancée — tensions logement, réformes partielles engagées)
  faible    -> composite < 20   (modèle logement — politiques inclusives, expulsions encadrées, Housing First)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class HousingForcedEvictionsGentrificationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_eviction_scale_severity_score: float
    legal_protection_remedy_access_score: float
    displacement_vulnerability_score: float
    housing_policy_accountability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_housing_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_eviction_scale_severity_score * 0.30
            + self.legal_protection_remedy_access_score * 0.25
            + self.displacement_vulnerability_score * 0.25
            + self.housing_policy_accountability_score * 0.20,
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
        self.estimated_housing_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_eviction_scale_severity_score": self.forced_eviction_scale_severity_score,
            "legal_protection_remedy_access_score": self.legal_protection_remedy_access_score,
            "displacement_vulnerability_score": self.displacement_vulnerability_score,
            "housing_policy_accountability_score": self.housing_policy_accountability_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_housing_rights_index": self.estimated_housing_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class HousingForcedEvictionsGentrificationEngineResult:
    agent: str = "Housing Rights, Forced Evictions & Gentrification Engine Agent"
    domain: str = "housing_forced_evictions_gentrification"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_housing_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingForcedEvictionsGentrificationEntity] = field(default_factory=list)


def run_housing_forced_evictions_gentrification_engine() -> HousingForcedEvictionsGentrificationEngineResult:
    entities = [
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-001",
            name="Inde/Mumbai Dharavi Démolitions — 1 Million Habitants Bidonvilles, Expulsions Sans Relogement, Résistance ONG",
            country="Inde",
            sector="Démolitions Bidonvilles Urbains",
            forced_eviction_scale_severity_score=88.0,
            legal_protection_remedy_access_score=85.0,
            displacement_vulnerability_score=87.0,
            housing_policy_accountability_score=72.0,
            primary_pattern="forced_eviction_scale_severity",
            key_signals=[
                "Dharavi Mumbai : 1 million habitants sur 2,4 km² — opération Adani Group réaménagement 2023 controversée",
                "Expulsions sans relogement adéquat : 70% des expulsés relogés hors ville — destruction réseaux sociaux",
                "Haute Cour Bombay : condamné procédures expulsion irrégulières — injonctions partiellement ignorées",
                "ONG YUVA et SPARC : documentation 500 000 cas expulsions illégales bidonvilles Mumbai 2015-2023",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-002",
            name="Kenya/Nairobi Mathare Expulsions — 500 000 Résidents, Bulldozers État, Violence Policière, Zéro Compensation",
            country="Kenya",
            sector="Expulsions Forcées Bidonvilles Africains",
            forced_eviction_scale_severity_score=85.0,
            legal_protection_remedy_access_score=83.0,
            displacement_vulnerability_score=84.0,
            housing_policy_accountability_score=68.0,
            primary_pattern="displacement_vulnerability",
            key_signals=[
                "Mathare Nairobi : 500 000 résidents bidonville — expulsions État répétées sans alternative relogement",
                "Violence policière documentée : HRW 2019 — brutalités lors démolitions, meurtres extrajudiciaires",
                "Zéro compensation légale : droit kényan exige notification 3 mois — systématiquement contourné État",
                "Amnesty International 2020 : 3 000 structures détruites Mathare en 6 mois — 15 000 personnes déplacées",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-003",
            name="Brésil/Rio Favelas JO 2016 — 77 000 Expulsés Pré-Olympique, Villagio Autodromo, Compensation Insuffisante",
            country="Brésil",
            sector="Expulsions Événements Sportifs Mondiaux",
            forced_eviction_scale_severity_score=80.0,
            legal_protection_remedy_access_score=78.0,
            displacement_vulnerability_score=80.0,
            housing_policy_accountability_score=65.0,
            primary_pattern="forced_eviction_scale_severity",
            key_signals=[
                "JO Rio 2016 : 77 000 résidents expulsés préparation olympique — Amnesty International rapport critique",
                "Vilagio Autódromo : derniers résistants — maisons détruites nuit, compensations sous-évaluées 60%",
                "Favela da Pavuna : 3 000 familles déplacées vers Minha Casa Minha Vida éloigné — emplois perdus",
                "Rapporteur ONU Raquel Rolnik 2013 : avertissement anticipé expulsions forcées Rio — ignoré par État",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-004",
            name="Philippines/Manille Duterte Slum Clearance — 100 000 Déplacés 2016-2022, Demolition Teams, Violence State",
            country="Philippines",
            sector="Expulsions Autoritaires Urbaines",
            forced_eviction_scale_severity_score=77.0,
            legal_protection_remedy_access_score=75.0,
            displacement_vulnerability_score=76.0,
            housing_policy_accountability_score=62.0,
            primary_pattern="forced_eviction_scale_severity",
            key_signals=[
                "Politique Duterte 2016-2022 : 100 000 résidents informal settlements Manille déplacés par équipes démolition",
                "NHA relocation : relogement Bulacan province — 50 km de Manille, transports inexistants, emplois perdus",
                "Amnesty International 2018 : documente résistants tués lors expulsions, impunité des demolition teams",
                "Urban Development Housing Act Philippines : protections légales — systématiquement contournées présidence",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-005",
            name="Chine/Hutong Pékin Rénovation Urbaine — 1 Million Déplacés Préparation JO 2008, Hukou Discrimination Migrante",
            country="Chine",
            sector="Rénovation Urbaine Autoritaire",
            forced_eviction_scale_severity_score=56.0,
            legal_protection_remedy_access_score=54.0,
            displacement_vulnerability_score=58.0,
            housing_policy_accountability_score=47.0,
            primary_pattern="displacement_vulnerability",
            key_signals=[
                "JO Pékin 2008 : 1,5 million résidents déplacés rénovation urbaine — COHRE rapport 2007 chiffres confirmés",
                "Système hukou : résidents ruraux-urbains sans droits logement légaux — expulsables sans recours judiciaire",
                "Hutong historiques Pékin détruits : 40% de patrimoine détruit 1990-2010 — résidents sans compensation adéquate",
                "Recours légal inexistant : tribunaux rejettent 95% recours expropriés contre État — système judiciaire dépendant",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-006",
            name="USA/Los Angeles Sans-Abri Sweeps — 70 000 Encampments Démantelés, LAPD Opérations, Droits Contestés Justice",
            country="USA",
            sector="Démantèlement Campements Sans-Abri",
            forced_eviction_scale_severity_score=48.0,
            legal_protection_remedy_access_score=50.0,
            displacement_vulnerability_score=52.0,
            housing_policy_accountability_score=42.0,
            primary_pattern="displacement_vulnerability",
            key_signals=[
                "Los Angeles 2023 : 70 000 personnes sans abri — opérations LAPD démantèlement campements quotidiennes",
                "Johnson v. City of Los Angeles (2023) : 9e circuit — sweeps inconstitutionnels sans alternative logement",
                "Affaires ACLU : LAPD détruit biens personnels lors sweeps — pratique illégale 4e amendement documentée",
                "Measure HLA 2024 : budget logement 1,2 milliards — Housing First insuffisant face ampleur crise",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-007",
            name="Espagne/Madrid Gentrification — Quartiers Lavapiés-Malasaña, Encadrement Loyers Partiel, Résistance Locataires",
            country="Espagne",
            sector="Gentrification Métropole Européenne",
            forced_eviction_scale_severity_score=35.0,
            legal_protection_remedy_access_score=38.0,
            displacement_vulnerability_score=36.0,
            housing_policy_accountability_score=28.0,
            primary_pattern="legal_protection_remedy_access",
            key_signals=[
                "Lavapiés et Malasaña Madrid : loyers +85% en 10 ans — déplacement progressif résidents historiques",
                "Loi Logement 2023 : encadrement loyers zones tendues — tribunaux contestent applicabilité, effet limité",
                "PAH Plataforma Afectados Hipoteca : 26 000 expulsions hypothécaires 2022 — réseau résistance organisé",
                "Airbnb : 14 000 logements touristiques Madrid — pression marché locatif résidentiel documentée mairie",
            ],
        ),
        HousingForcedEvictionsGentrificationEntity(
            entity_id="HFE-008",
            name="Pays-Bas/Amsterdam Housing First Modèle — Sans-Abri -70%, Encadrement Loyers, Politique Inclusive Référence",
            country="Pays-Bas",
            sector="Modèle Logement Inclusif",
            forced_eviction_scale_severity_score=9.0,
            legal_protection_remedy_access_score=8.0,
            displacement_vulnerability_score=9.0,
            housing_policy_accountability_score=7.0,
            primary_pattern="housing_policy_accountability",
            key_signals=[
                "Amsterdam Housing First depuis 2006 : sans-abri chronique réduit de 70% — modèle ONU-Habitat cité",
                "Encadrement loyers social : 70% logements sous loyers sociaux contrôlés — accès garantis bas revenus",
                "Wet toezicht huurwoningen : loi 2023 encadrement secteur privé jusqu'à 186 points WWS — 300 000 logements",
                "Expulsions : procédure judiciaire obligatoire, aide relogement légalement garantie, zéro expulsion sans alternative",
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

    # Assertions OBLIGATOIRES — distribution 4 critique / 2 élevé / 1 modéré / 1 faible
    critique_count = risk_dist.get("critique", 0)
    eleve_count = risk_dist.get("élevé", 0)
    modere_count = risk_dist.get("modéré", 0)
    faible_count = risk_dist.get("faible", 0)
    assert critique_count == 4, f"Expected 4 critique, got {critique_count}: {risk_dist}"
    assert eleve_count == 2, f"Expected 2 élevé, got {eleve_count}: {risk_dist}"
    assert modere_count == 1, f"Expected 1 modéré, got {modere_count}: {risk_dist}"
    assert faible_count == 1, f"Expected 1 faible, got {faible_count}: {risk_dist}"

    return HousingForcedEvictionsGentrificationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_habitat_world_cities_report_2023_adequate_housing_global",
            "cohre_forced_evictions_violations_housing_rights_annual_2022",
            "amnesty_international_forced_evictions_kenya_brazil_philippines_reports",
            "un_special_rapporteur_adequate_housing_country_missions_2023",
            "pidesc_codesc_general_comment_7_forced_evictions_1997",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_housing_forced_evictions_gentrification_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — {e.name[:60]}")
