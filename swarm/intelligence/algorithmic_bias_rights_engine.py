from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AlgorithmicBiasRightsEntity:
    entity_id: str
    name: str
    country: str
    employment_housing_algorithmic_exclusion_severity_score: float
    predictive_policing_racial_bias_scale_score: float
    judicial_algorithmic_sentencing_gap_score: float
    algorithmic_transparency_right_explanation_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_algorithmic_bias_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.employment_housing_algorithmic_exclusion_severity_score * 0.30
            + self.predictive_policing_racial_bias_scale_score * 0.25
            + self.judicial_algorithmic_sentencing_gap_score * 0.25
            + self.algorithmic_transparency_right_explanation_absence_score * 0.20,
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
        self.estimated_algorithmic_bias_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AlgorithmicBiasRightsEngineResult:
    agent: str = "Algorithmic Bias Rights Engine Agent"
    domain: str = "algorithmic_bias_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_algorithmic_bias_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AlgorithmicBiasRightsEntity] = field(default_factory=list)

def run_algorithmic_bias_rights_engine() -> AlgorithmicBiasRightsEngineResult:
    entities = [
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-001",
            name="USA/COMPAS — Récidivisme Biaisé Justice, Crédit Score Racial & Algorithmes RH Discriminatoires",
            country="Amérique du Nord",
            employment_housing_algorithmic_exclusion_severity_score=95.0,
            predictive_policing_racial_bias_scale_score=92.0,
            judicial_algorithmic_sentencing_gap_score=92.0,
            algorithmic_transparency_right_explanation_absence_score=92.0,
            primary_pattern="judicial_algorithmic_sentencing_gap",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-002",
            name="Chine — Score Social Emploi Ethnique, Algorithmes Surveillance Citoyens & Notation Comportement",
            country="Asie de l'Est",
            employment_housing_algorithmic_exclusion_severity_score=90.0,
            predictive_policing_racial_bias_scale_score=92.0,
            judicial_algorithmic_sentencing_gap_score=90.0,
            algorithmic_transparency_right_explanation_absence_score=88.0,
            primary_pattern="predictive_policing_racial_bias_scale",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-003",
            name="UK — PredPol Police Prédictive, Algorithmes DWP Prestations & Windrush Biais Systémique",
            country="Europe",
            employment_housing_algorithmic_exclusion_severity_score=88.0,
            predictive_policing_racial_bias_scale_score=88.0,
            judicial_algorithmic_sentencing_gap_score=88.0,
            algorithmic_transparency_right_explanation_absence_score=88.0,
            primary_pattern="employment_housing_algorithmic_exclusion_severity",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-004",
            name="Pays en Développement — FinTech Exclusion Crédit Mobile, Score Sans Historique & Biais Genre",
            country="Global Sud",
            employment_housing_algorithmic_exclusion_severity_score=85.0,
            predictive_policing_racial_bias_scale_score=85.0,
            judicial_algorithmic_sentencing_gap_score=88.0,
            algorithmic_transparency_right_explanation_absence_score=85.0,
            primary_pattern="employment_housing_algorithmic_exclusion_severity",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-005",
            name="UE — RGPD Art.22 Insuffisant, AI Act Lacunes Systèmes HRisk & Biais Recrutement Automatisé",
            country="Europe",
            employment_housing_algorithmic_exclusion_severity_score=52.0,
            predictive_policing_racial_bias_scale_score=55.0,
            judicial_algorithmic_sentencing_gap_score=52.0,
            algorithmic_transparency_right_explanation_absence_score=55.0,
            primary_pattern="algorithmic_transparency_right_explanation_absence",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-006",
            name="Amérique Latine — Algorithmes Police Prédictive, Score Pauvreté Géographique & Zéro Recours",
            country="Amérique Latine",
            employment_housing_algorithmic_exclusion_severity_score=50.0,
            predictive_policing_racial_bias_scale_score=52.0,
            judicial_algorithmic_sentencing_gap_score=52.0,
            algorithmic_transparency_right_explanation_absence_score=55.0,
            primary_pattern="predictive_policing_racial_bias_scale",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-007",
            name="Algorithmic Justice League/AI Now — Audit Biais, Fairness ML & Plaidoyer Réglementation IA",
            country="Global",
            employment_housing_algorithmic_exclusion_severity_score=22.0,
            predictive_policing_racial_bias_scale_score=28.0,
            judicial_algorithmic_sentencing_gap_score=25.0,
            algorithmic_transparency_right_explanation_absence_score=30.0,
            primary_pattern="algorithmic_transparency_right_explanation_absence",
        ),
        AlgorithmicBiasRightsEntity(
            entity_id="ABR-008",
            name="ONU/UNESCO — Recommandation IA 2021, RGPD Art.22, SDG 16 Justice & Droits Humains IA",
            country="Global",
            employment_housing_algorithmic_exclusion_severity_score=4.0,
            predictive_policing_racial_bias_scale_score=5.0,
            judicial_algorithmic_sentencing_gap_score=3.0,
            algorithmic_transparency_right_explanation_absence_score=6.0,
            primary_pattern="judicial_algorithmic_sentencing_gap",
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

    return AlgorithmicBiasRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_algorithmic_bias_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "algorithmic_justice_league_facial_recognition_bias_audit_report",
            "ai_now_institute_discriminatory_algorithms_employment_housing_study",
            "propublica_compas_recidivism_racial_bias_investigative_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_algorithmic_bias_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_algorithmic_bias_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
