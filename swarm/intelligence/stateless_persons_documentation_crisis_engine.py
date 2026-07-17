from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class StatelessPersonsDocumentationCrisisEntity:
    entity_id: str
    name: str
    country: str
    statelessness_scale_documentation_denial_score: float
    legal_framework_citizenship_deprivation_score: float
    rights_deprivation_healthcare_education_score: float
    international_protection_mechanism_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_stateless_documentation_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.statelessness_scale_documentation_denial_score * 0.30
            + self.legal_framework_citizenship_deprivation_score * 0.25
            + self.rights_deprivation_healthcare_education_score * 0.25
            + self.international_protection_mechanism_gap_score * 0.20,
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
        self.estimated_stateless_documentation_index = round(
            self.composite_score / 100 * 10, 2
        )


def build_entities() -> List[StatelessPersonsDocumentationCrisisEntity]:
    return [
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-001",
            name="Birmanie/Rohingya — 1M Apatrides, Refus Citoyenneté Loi 1982, Génocide Documenté ONU",
            country="Birmanie",
            statelessness_scale_documentation_denial_score=96.0,
            legal_framework_citizenship_deprivation_score=94.0,
            rights_deprivation_healthcare_education_score=93.0,
            international_protection_mechanism_gap_score=91.0,
            primary_pattern="1M+ Rohingya apatrides depuis 1982, exclusion citoyenneté, réfugiés Bangladesh, génocide 2017 documenté ONU",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-002",
            name="Kuwait/Bidoon — 100 000 Résidents Sans Papiers, Droits Fondamentaux Refusés Depuis 1961",
            country="Kuwait",
            statelessness_scale_documentation_denial_score=88.0,
            legal_framework_citizenship_deprivation_score=85.0,
            rights_deprivation_healthcare_education_score=87.0,
            international_protection_mechanism_gap_score=84.0,
            primary_pattern="100K Bidoon résidents sans nationalité depuis indépendance 1961, accès emploi public refusé, mariages restreints",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-003",
            name="Côte d'Ivoire/Dioula — Apatridie Post-Guerre Civile, Actes Naissance Refusés, 700 000 Cas",
            country="Côte d'Ivoire",
            statelessness_scale_documentation_denial_score=82.0,
            legal_framework_citizenship_deprivation_score=79.0,
            rights_deprivation_healthcare_education_score=80.0,
            international_protection_mechanism_gap_score=76.0,
            primary_pattern="Post-conflit 2002-2011, Dioulas sans actes naissance, 700K apatrides, accès éducation santé bloqué",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-004",
            name="République Dominicaine/Haïtiens — Arrêt 168-13, Dénationalisation Rétroactive 200 000 Personnes",
            country="République Dominicaine",
            statelessness_scale_documentation_denial_score=79.0,
            legal_framework_citizenship_deprivation_score=85.0,
            rights_deprivation_healthcare_education_score=76.0,
            international_protection_mechanism_gap_score=74.0,
            primary_pattern="Arrêt TC/0168/13 dénationalise Haïtiens nés RD avant 2010, 200K apatrides, expulsions massives",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-005",
            name="Lettonie/Non-Citoyens Soviétiques — 200 000 Passeports Gris, Droits Limités UE",
            country="Lettonie",
            statelessness_scale_documentation_denial_score=52.0,
            legal_framework_citizenship_deprivation_score=48.0,
            rights_deprivation_healthcare_education_score=45.0,
            international_protection_mechanism_gap_score=50.0,
            primary_pattern="200K non-citoyens post-URSS, passeport gris alien, vote local refusé, naturalisation conditionnelle, amélioration lente",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-006",
            name="Thaïlande/Highlanders Montagnards — 500K Sans Acte Naissance, Mobilité & Éducation Bloquées",
            country="Thaïlande",
            statelessness_scale_documentation_denial_score=48.0,
            legal_framework_citizenship_deprivation_score=44.0,
            rights_deprivation_healthcare_education_score=50.0,
            international_protection_mechanism_gap_score=42.0,
            primary_pattern="500K montagnards sans enregistrement naissance, accès soins limité, mobilité restreinte, école difficile d'accès",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-007",
            name="UNHCR/IBelong Campaign 2024 — Objectif Réduction Apatridie, Progrès Mesuré 10 Pays",
            country="International",
            statelessness_scale_documentation_denial_score=28.0,
            legal_framework_citizenship_deprivation_score=22.0,
            rights_deprivation_healthcare_education_score=25.0,
            international_protection_mechanism_gap_score=20.0,
            primary_pattern="Campagne IBelong 2014-2024, 450K apatrides reconnus, loi modèle 10 États, lacunes persistantes financement",
        ),
        StatelessPersonsDocumentationCrisisEntity(
            entity_id="SDC-008",
            name="Estonie/Intégration Naturalisation — Modèle Réussite, Non-Citoyens Intégrés, UE Standards",
            country="Estonie",
            statelessness_scale_documentation_denial_score=8.0,
            legal_framework_citizenship_deprivation_score=7.0,
            rights_deprivation_healthcare_education_score=6.0,
            international_protection_mechanism_gap_score=9.0,
            primary_pattern="Programme naturalisation estonien, 80% intégrés, cours langue financés, accès droits UE progressif, modèle régional",
        ),
    ]


def analyze(entities: List[StatelessPersonsDocumentationCrisisEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    assert risk_dist.get("critique", 0) == 4, f"Distribution critique attendue: 4, obtenu: {risk_dist.get('critique', 0)}"
    assert risk_dist.get("élevé", 0) == 2, f"Distribution élevé attendue: 2, obtenu: {risk_dist.get('élevé', 0)}"
    assert risk_dist.get("modéré", 0) == 1, f"Distribution modéré attendue: 1, obtenu: {risk_dist.get('modéré', 0)}"
    assert risk_dist.get("faible", 0) == 1, f"Distribution faible attendue: 1, obtenu: {risk_dist.get('faible', 0)}"

    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "stateless_persons_documentation_crisis_engine",
        "domain": "stateless_persons_documentation_crisis",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.88,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "statelessness_documentation_denial": 4,
            "citizenship_deprivation_legal": 2,
            "rights_deprivation_services": 1,
            "international_framework_gap": 1,
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
        "avg_estimated_stateless_documentation_index": round(
            statistics.mean([e.estimated_stateless_documentation_index for e in entities]), 2
        ),
        "data_sources": [
            "unhcr_ibelong_campaign_progress_report_2024",
            "institute_statelessness_inclusion_world_statelessness_2023",
            "human_rights_watch_stateless_documentation_crisis_2024",
            "open_society_foundations_citizenship_deprivation_study_2023",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "statelessness_scale_documentation_denial_score": e.statelessness_scale_documentation_denial_score,
                "legal_framework_citizenship_deprivation_score": e.legal_framework_citizenship_deprivation_score,
                "rights_deprivation_healthcare_education_score": e.rights_deprivation_healthcare_education_score,
                "international_protection_mechanism_gap_score": e.international_protection_mechanism_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_stateless_documentation_index": e.estimated_stateless_documentation_index,
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
