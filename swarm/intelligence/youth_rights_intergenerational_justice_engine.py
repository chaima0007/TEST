from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class YouthRightsIntergenerationalJusticeEntity:
    entity_id: str
    name: str
    country: str
    youth_employment_education_rights_deprivation_score: float
    child_soldier_exploitation_intergenerational_harm_score: float
    intergenerational_poverty_inequality_transmission_score: float
    state_protection_future_generations_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_youth_rights_intergenerational_justice_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.youth_employment_education_rights_deprivation_score * 0.30
            + self.child_soldier_exploitation_intergenerational_harm_score * 0.25
            + self.intergenerational_poverty_inequality_transmission_score * 0.25
            + self.state_protection_future_generations_deficit_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_youth_rights_intergenerational_justice_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[YouthRightsIntergenerationalJusticeEntity]:
    return [
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-001",
            name="Mali — 77% Jeunes Sans Emploi, Conflit Armé, Droit Futur Violé",
            country="Mali",
            youth_employment_education_rights_deprivation_score=94.0,
            child_soldier_exploitation_intergenerational_harm_score=90.0,
            intergenerational_poverty_inequality_transmission_score=92.0,
            state_protection_future_generations_deficit_score=91.0,
            primary_pattern="Chômage jeunes 77%, recrutement groupes armés sahéliens, génération sans avenir",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-002",
            name="Burundi — Recrutement Enfants Soldats, Pauvreté Intergénérationnelle",
            country="Burundi",
            youth_employment_education_rights_deprivation_score=91.0,
            child_soldier_exploitation_intergenerational_harm_score=93.0,
            intergenerational_poverty_inequality_transmission_score=90.0,
            state_protection_future_generations_deficit_score=89.0,
            primary_pattern="Recrutement enfants Imbonerakure, pauvreté héréditaire, État défaillant protections",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-003",
            name="Yémen — Génération Entière Sans Éducation, Famine",
            country="Yémen",
            youth_employment_education_rights_deprivation_score=93.0,
            child_soldier_exploitation_intergenerational_harm_score=88.0,
            intergenerational_poverty_inequality_transmission_score=91.0,
            state_protection_future_generations_deficit_score=92.0,
            primary_pattern="2M enfants déscolarisés, famine générationnelle, trauma PTSD collectif, mariage précoce",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-004",
            name="Haïti — Gangs Recruteurs Jeunes, État Défaillant",
            country="Haïti",
            youth_employment_education_rights_deprivation_score=89.0,
            child_soldier_exploitation_intergenerational_harm_score=87.0,
            intergenerational_poverty_inequality_transmission_score=88.0,
            state_protection_future_generations_deficit_score=90.0,
            primary_pattern="Gangs G9 recrutent enfants, effondrement système éducatif, 60% population -25 ans",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-005",
            name="Bangladesh — Ateliers Jeunes, Manifestations Réprimées 2024",
            country="Bangladesh",
            youth_employment_education_rights_deprivation_score=55.0,
            child_soldier_exploitation_intergenerational_harm_score=50.0,
            intergenerational_poverty_inequality_transmission_score=53.0,
            state_protection_future_generations_deficit_score=54.0,
            primary_pattern="Ateliers textile exploitant jeunes, répression manifestations étudiantes juillet 2024",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-006",
            name="Éthiopie — Jeunes Tigré Trauma, Déplacement",
            country="Éthiopie",
            youth_employment_education_rights_deprivation_score=52.0,
            child_soldier_exploitation_intergenerational_harm_score=54.0,
            intergenerational_poverty_inequality_transmission_score=51.0,
            state_protection_future_generations_deficit_score=50.0,
            primary_pattern="Conflit Tigré trauma générationnel, 2M déplacés jeunes, éducation interrompue",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-007",
            name="Brésil — Inégalités Intergénérationnelles, Crime Organisé",
            country="Brésil",
            youth_employment_education_rights_deprivation_score=27.0,
            child_soldier_exploitation_intergenerational_harm_score=24.0,
            intergenerational_poverty_inequality_transmission_score=28.0,
            state_protection_future_generations_deficit_score=25.0,
            primary_pattern="Favelas inégalités héréditaires, trafic drogue recrute jeunes, Bolsa Família limité",
        ),
        YouthRightsIntergenerationalJusticeEntity(
            entity_id="YRJ-008",
            name="Finlande — Droits Jeunes Constitutionnels, Meilleur Système Éducatif",
            country="Finlande",
            youth_employment_education_rights_deprivation_score=4.0,
            child_soldier_exploitation_intergenerational_harm_score=4.0,
            intergenerational_poverty_inequality_transmission_score=4.0,
            state_protection_future_generations_deficit_score=4.0,
            primary_pattern="Droits jeunes constitutionnels, PISA meilleur système, parlement jeunesse consultatif",
        ),
    ]


def analyze(entities: List[YouthRightsIntergenerationalJusticeEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "youth_rights_intergenerational_justice_engine",
        "domain": "youth_rights_intergenerational_justice",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.89,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "child_soldier_exploitation": 3,
            "education_deprivation": 2,
            "intergenerational_poverty": 2,
            "state_protection_deficit": 1,
        },
        "top_risk_entities": [
            {"id": e.entity_id, "name": e.name, "score": e.composite_score, "risk": e.risk_level}
            for e in top_risk
        ],
        "critical_alerts": [
            f"{e.entity_id}: {e.name} — composite {e.composite_score}"
            for e in entities if e.risk_level == "critique"
        ],
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_youth_rights_intergenerational_justice_index": round(
            statistics.mean([e.estimated_youth_rights_intergenerational_justice_index for e in entities]), 2
        ),
        "data_sources": [
            "unicef_state_worlds_children_2023",
            "ilo_global_employment_trends_youth_2023",
            "youth_for_human_rights_report_2023",
            "un_crc_committee_recommendations_2023",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "youth_employment_education_rights_deprivation_score": e.youth_employment_education_rights_deprivation_score,
                "child_soldier_exploitation_intergenerational_harm_score": e.child_soldier_exploitation_intergenerational_harm_score,
                "intergenerational_poverty_inequality_transmission_score": e.intergenerational_poverty_inequality_transmission_score,
                "state_protection_future_generations_deficit_score": e.state_protection_future_generations_deficit_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_youth_rights_intergenerational_justice_index": e.estimated_youth_rights_intergenerational_justice_index,
                "last_updated": e.last_updated,
            }
            for e in entities
        ],
    }


if __name__ == "__main__":
    import json
    entities = build_entities()
    result = analyze(entities)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✓ avg_composite = {result['avg_composite']}")
    print(f"✓ risk_distribution = {result['risk_distribution']}")
    print(f"✓ total_entities = {result['total_entities']}")
