from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NuclearTestingEnvironmentalRightsEntity:
    entity_id: str
    name: str
    country: str
    radioactive_contamination_civilian_exposure_score: float
    forced_displacement_indigenous_testing_score: float
    health_cancer_intergenerational_harm_score: float
    compensation_accountability_justice_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nuclear_testing_environmental_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.radioactive_contamination_civilian_exposure_score * 0.30
            + self.forced_displacement_indigenous_testing_score * 0.25
            + self.health_cancer_intergenerational_harm_score * 0.25
            + self.compensation_accountability_justice_gap_score * 0.20,
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
        self.estimated_nuclear_testing_environmental_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class NuclearTestingEnvironmentalRightsEngineResult:
    agent: str = "Nuclear Testing Environmental Rights Engine Agent"
    domain: str = "nuclear_testing_environmental_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_nuclear_testing_environmental_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NuclearTestingEnvironmentalRightsEntity] = field(default_factory=list)


def run_nuclear_testing_environmental_rights_engine() -> NuclearTestingEnvironmentalRightsEngineResult:
    entities = [
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-001",
            name="Kazakhstan/Semipalatinsk — 456 Tests Soviétiques 1949-1989, 1.5M Exposés, Cancers +70%, Polygon Documenté & ATOM Project 2010",
            country="Kazakhstan",
            radioactive_contamination_civilian_exposure_score=93.0,
            forced_displacement_indigenous_testing_score=88.0,
            health_cancer_intergenerational_harm_score=91.0,
            compensation_accountability_justice_gap_score=85.0,
            primary_pattern="radioactive_contamination_civilian_exposure",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-002",
            name="Polynésie Française/Mururoa — 193 Tests France 1966-1996, Tahiti Contamination Cachée, Veterans Cancer 2010 Loi Insuffisante & Moruroa e Tatou",
            country="France/Polynésie Française",
            radioactive_contamination_civilian_exposure_score=88.0,
            forced_displacement_indigenous_testing_score=82.0,
            health_cancer_intergenerational_harm_score=86.0,
            compensation_accountability_justice_gap_score=84.0,
            primary_pattern="health_cancer_intergenerational_harm",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-003",
            name="Marshall Islands/Bikini — USA 67 Tests 1946-1958, Castle Bravo 1954 = 1000x Hiroshima, Déplacement Permanent & Eau Radioactive",
            country="Marshall Islands",
            radioactive_contamination_civilian_exposure_score=91.0,
            forced_displacement_indigenous_testing_score=92.0,
            health_cancer_intergenerational_harm_score=89.0,
            compensation_accountability_justice_gap_score=87.0,
            primary_pattern="forced_displacement_indigenous_testing",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-004",
            name="Australie/Maralinga — UK 12 Tests 1956-1963, Anangu Déplacés Terres Ancestrales, Nettoyage Partiel 2000 & Cancers Vétérans",
            country="Australie",
            radioactive_contamination_civilian_exposure_score=84.0,
            forced_displacement_indigenous_testing_score=86.0,
            health_cancer_intergenerational_harm_score=82.0,
            compensation_accountability_justice_gap_score=80.0,
            primary_pattern="forced_displacement_indigenous_testing",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-005",
            name="USA/Nevada Test Site — 928 Tests, Shoshone Nation Terres Traités, Downwinders Utah/Nevada Cancers Thyroïde & RECA Compensations Limitées",
            country="USA",
            radioactive_contamination_civilian_exposure_score=57.0,
            forced_displacement_indigenous_testing_score=55.0,
            health_cancer_intergenerational_harm_score=58.0,
            compensation_accountability_justice_gap_score=56.0,
            primary_pattern="health_cancer_intergenerational_harm",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-006",
            name="Algérie/Reggane — France 17 Tests 1960-1966 Sahara, Soldats Algériens Exposés Sans Protection & Secret Militaire Maintenu",
            country="Algérie",
            radioactive_contamination_civilian_exposure_score=54.0,
            forced_displacement_indigenous_testing_score=50.0,
            health_cancer_intergenerational_harm_score=53.0,
            compensation_accountability_justice_gap_score=58.0,
            primary_pattern="compensation_accountability_justice_gap",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-007",
            name="Inde/Pakistan — Tests 1998 Pokhran/Chagai, Populations Rurales Rajasthan/Balochistan Sans Information & Monitoring Insuffisant",
            country="Inde/Pakistan",
            radioactive_contamination_civilian_exposure_score=32.0,
            forced_displacement_indigenous_testing_score=28.0,
            health_cancer_intergenerational_harm_score=30.0,
            compensation_accountability_justice_gap_score=35.0,
            primary_pattern="compensation_accountability_justice_gap",
        ),
        NuclearTestingEnvironmentalRightsEntity(
            entity_id="NTER-008",
            name="Nouvelle-Zélande/Politique — Traité Rarotonga 1985, Zone Dénucléarisée Pacifique, Non-Prolifération Actif & Modèle Régional",
            country="Nouvelle-Zélande",
            radioactive_contamination_civilian_exposure_score=8.0,
            forced_displacement_indigenous_testing_score=6.0,
            health_cancer_intergenerational_harm_score=7.0,
            compensation_accountability_justice_gap_score=10.0,
            primary_pattern="radioactive_contamination_civilian_exposure",
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

    return NuclearTestingEnvironmentalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_nuclear_testing_environmental_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icrc_nuclear_weapons_humanitarian_law_2023",
            "un_special_rapporteur_toxic_substances_nuclear_2023",
            "ippnw_nuclear_testing_health_effects_2023",
            "ican_humanitarian_impact_nuclear_testing_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_nuclear_testing_environmental_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_nuclear_testing_environmental_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
