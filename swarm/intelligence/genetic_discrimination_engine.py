from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class GeneticDiscriminationEntity:
    entity_id: str
    name: str
    country: str
    insurance_genetic_exclusion_severity_score: float
    employment_dna_testing_coercion_scale_score: float
    predictive_data_consent_absence_score: float
    legal_protection_genetic_privacy_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_genetic_discrimination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.insurance_genetic_exclusion_severity_score * 0.30
            + self.employment_dna_testing_coercion_scale_score * 0.25
            + self.predictive_data_consent_absence_score * 0.25
            + self.legal_protection_genetic_privacy_gap_score * 0.20,
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
        self.estimated_genetic_discrimination_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class GeneticDiscriminationEngineResult:
    agent: str = "Genetic Discrimination Engine Agent"
    domain: str = "genetic_discrimination"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_genetic_discrimination_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[GeneticDiscriminationEntity] = field(default_factory=list)

def run_genetic_discrimination_engine() -> GeneticDiscriminationEngineResult:
    entities = [
        GeneticDiscriminationEntity(
            entity_id="GDI-001",
            name="Chine — Base ADN Ethnique Ouïghours, Biobanque Forcée & Prédiction Crimes Génétique",
            country="Asie de l'Est",
            insurance_genetic_exclusion_severity_score=88.0,
            employment_dna_testing_coercion_scale_score=95.0,
            predictive_data_consent_absence_score=95.0,
            legal_protection_genetic_privacy_gap_score=95.0,
            primary_pattern="predictive_data_consent_absence",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-002",
            name="USA — GINA Gaps Assurance Vie/Invalidité, 23andMe Data Breach & Employeurs ADN",
            country="Amérique du Nord",
            insurance_genetic_exclusion_severity_score=92.0,
            employment_dna_testing_coercion_scale_score=88.0,
            predictive_data_consent_absence_score=90.0,
            legal_protection_genetic_privacy_gap_score=88.0,
            primary_pattern="insurance_genetic_exclusion_severity",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-003",
            name="Inde — Tests ADN Castes Pureté, Assurances ADN Non Régulées & 0 Loi Génomique",
            country="Asie du Sud",
            insurance_genetic_exclusion_severity_score=88.0,
            employment_dna_testing_coercion_scale_score=85.0,
            predictive_data_consent_absence_score=88.0,
            legal_protection_genetic_privacy_gap_score=92.0,
            primary_pattern="legal_protection_genetic_privacy_gap",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-004",
            name="UK/Europe — Assureurs ADN BRCA1/BRCA2, Underwriting Génétique & Code Concordat Insuffisant",
            country="Europe",
            insurance_genetic_exclusion_severity_score=88.0,
            employment_dna_testing_coercion_scale_score=82.0,
            predictive_data_consent_absence_score=85.0,
            legal_protection_genetic_privacy_gap_score=85.0,
            primary_pattern="insurance_genetic_exclusion_severity",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-005",
            name="Australie — Pas de Loi Fédérale Discrimination Génétique, Assureurs Autorisés ADN",
            country="Océanie",
            insurance_genetic_exclusion_severity_score=55.0,
            employment_dna_testing_coercion_scale_score=50.0,
            predictive_data_consent_absence_score=52.0,
            legal_protection_genetic_privacy_gap_score=55.0,
            primary_pattern="legal_protection_genetic_privacy_gap",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-006",
            name="Moyen-Orient/Gulf — Tests ADN Mariage Consanguinité, Refus Embauche & Zéro RGPD",
            country="Moyen-Orient",
            insurance_genetic_exclusion_severity_score=52.0,
            employment_dna_testing_coercion_scale_score=55.0,
            predictive_data_consent_absence_score=55.0,
            legal_protection_genetic_privacy_gap_score=50.0,
            primary_pattern="employment_dna_testing_coercion_scale",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-007",
            name="Genome Privacy Alliance/ACLU — GINA Réforme, Consentement Génomique & Droits Biobanques",
            country="Global",
            insurance_genetic_exclusion_severity_score=22.0,
            employment_dna_testing_coercion_scale_score=28.0,
            predictive_data_consent_absence_score=25.0,
            legal_protection_genetic_privacy_gap_score=30.0,
            primary_pattern="predictive_data_consent_absence",
        ),
        GeneticDiscriminationEntity(
            entity_id="GDI-008",
            name="UNESCO — Déclaration Génome Humain Patrimoine Humanité 1997, OCDE Biobanques & OMS",
            country="Global",
            insurance_genetic_exclusion_severity_score=4.0,
            employment_dna_testing_coercion_scale_score=5.0,
            predictive_data_consent_absence_score=3.0,
            legal_protection_genetic_privacy_gap_score=6.0,
            primary_pattern="employment_dna_testing_coercion_scale",
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

    return GeneticDiscriminationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_genetic_discrimination_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "aclu_genetic_discrimination_gina_gaps_insurance_employment_report",
            "unesco_human_genome_heritage_declaration_1997_bioethics_update",
            "nature_genetics_biobank_consent_privacy_discrimination_global_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_genetic_discrimination_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_genetic_discrimination_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
