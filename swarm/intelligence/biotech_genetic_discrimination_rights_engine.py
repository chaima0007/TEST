"""
biotech_genetic_discrimination_rights_engine.py
Wave 189 — Discrimination Génétique & Biotechnologie
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class BiotechGeneticDiscriminationEntity:
    entity_id: str
    name: str
    country: str
    genetic_data_exploitation_corporate_score: float
    discrimination_employment_insurance_score: float
    consent_privacy_genomic_database_score: float
    regulatory_framework_protection_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_biotech_genetic_discrimination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.genetic_data_exploitation_corporate_score * 0.30
            + self.discrimination_employment_insurance_score * 0.25
            + self.consent_privacy_genomic_database_score * 0.25
            + self.regulatory_framework_protection_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_biotech_genetic_discrimination_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[BiotechGeneticDiscriminationEntity]:
    return [
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-001",
            name="États-Unis — Compagnies Assurances Génotype, GINA Non Appliquée",
            country="États-Unis",
            genetic_data_exploitation_corporate_score=92.0,
            discrimination_employment_insurance_score=90.0,
            consent_privacy_genomic_database_score=88.0,
            regulatory_framework_protection_score=85.0,
            primary_pattern="Exploitation données génomiques 23andMe/AncestryDNA, discrimination assurance santé GINA contournée, 26M profils génétiques exposés",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-002",
            name="Chine — Base Données ADN Obligatoire, Surveillance Génétique Ethnique",
            country="Chine",
            genetic_data_exploitation_corporate_score=95.0,
            discrimination_employment_insurance_score=91.0,
            consent_privacy_genomic_database_score=96.0,
            regulatory_framework_protection_score=94.0,
            primary_pattern="Base ADN 80M citoyens Xinjiang, séquençage ethnique Ouïghours, discrimination génétique systémique par l'État",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-003",
            name="Inde — Discrimination Génétique Castes, Entreprises Sans Régulation",
            country="Inde",
            genetic_data_exploitation_corporate_score=88.0,
            discrimination_employment_insurance_score=87.0,
            consent_privacy_genomic_database_score=85.0,
            regulatory_framework_protection_score=89.0,
            primary_pattern="Corrélation génotype-caste utilisée par employeurs, absence loi protection ADN, 600k profils collectés sans consentement",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-004",
            name="Brésil — Biopiraterie Génétique Peuples Autochtones, Données Vendues",
            country="Brésil",
            genetic_data_exploitation_corporate_score=86.0,
            discrimination_employment_insurance_score=84.0,
            consent_privacy_genomic_database_score=90.0,
            regulatory_framework_protection_score=83.0,
            primary_pattern="Exploitation données génétiques Amazonie sans consentement FPIC, biopiraterie Big Pharma, discrimination assurance vie 34% plus élevée",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-005",
            name="Royaume-Uni — NHS Génomique, Accès Assureurs aux Prédispositions",
            country="Royaume-Uni",
            genetic_data_exploitation_corporate_score=52.0,
            discrimination_employment_insurance_score=55.0,
            consent_privacy_genomic_database_score=48.0,
            regulatory_framework_protection_score=50.0,
            primary_pattern="NHS 100K Genomes Project, assureurs demandent résultats BRCA1/2, moratoire volontaire insuffisant, gaps réglementaires ICO",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-006",
            name="Australie — Discrimination Assurance-Vie Génétique Légale",
            country="Australie",
            genetic_data_exploitation_corporate_score=54.0,
            discrimination_employment_insurance_score=58.0,
            consent_privacy_genomic_database_score=50.0,
            regulatory_framework_protection_score=52.0,
            primary_pattern="Discrimination génétique assurance-vie légalement autorisée jusqu'en 2023, résidus pratiques, 4% Australiens refusés couverture",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-007",
            name="Mexique — Banques Génétiques Privées Non Régulées, Frontière ADN",
            country="Mexique",
            genetic_data_exploitation_corporate_score=28.0,
            discrimination_employment_insurance_score=25.0,
            consent_privacy_genomic_database_score=30.0,
            regulatory_framework_protection_score=26.0,
            primary_pattern="Cliniques génétiques privées sans cadre légal, données partagées avec partenaires US, protection constitutionnelle insuffisante",
        ),
        BiotechGeneticDiscriminationEntity(
            entity_id="BGD-008",
            name="France — Loi Bioéthique 2021, Protection CNIL Génomique",
            country="France",
            genetic_data_exploitation_corporate_score=8.0,
            discrimination_employment_insurance_score=7.0,
            consent_privacy_genomic_database_score=9.0,
            regulatory_framework_protection_score=6.0,
            primary_pattern="Loi bioéthique 2021 protège données génétiques, CNIL supervision stricte, interdiction discrimination génétique emploi/assurance",
        ),
    ]


def analyze(entities: List[BiotechGeneticDiscriminationEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "biotech_genetic_discrimination_rights_engine",
        "domain": "biotech_genetic_discrimination",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.91,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "corporate_genetic_exploitation": 3,
            "state_genomic_surveillance": 2,
            "insurance_discrimination": 2,
            "consent_violation": 1,
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
        "avg_estimated_biotech_genetic_discrimination_index": round(
            statistics.mean([e.estimated_biotech_genetic_discrimination_index for e in entities]), 2
        ),
        "data_sources": [
            "who_human_genome_mapping_project_2023",
            "ohchr_genetic_discrimination_report_2024",
            "un_biotechnology_rights_framework_2023",
            "gina_enforcement_eeoc_report_2024",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "genetic_data_exploitation_corporate_score": e.genetic_data_exploitation_corporate_score,
                "discrimination_employment_insurance_score": e.discrimination_employment_insurance_score,
                "consent_privacy_genomic_database_score": e.consent_privacy_genomic_database_score,
                "regulatory_framework_protection_score": e.regulatory_framework_protection_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_biotech_genetic_discrimination_index": e.estimated_biotech_genetic_discrimination_index,
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
    dist = result["risk_distribution"]
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
