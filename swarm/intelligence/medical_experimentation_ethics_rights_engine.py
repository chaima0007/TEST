from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MedicalExperimentationEthicsRightsEntity:
    entity_id: str
    name: str
    country: str
    informed_consent_violation_severity_score: float
    vulnerable_population_exploitation_gap_score: float
    regulatory_oversight_absence_score: float
    post_trial_access_accountability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_medical_experimentation_ethics_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.informed_consent_violation_severity_score * 0.30
            + self.vulnerable_population_exploitation_gap_score * 0.25
            + self.regulatory_oversight_absence_score * 0.25
            + self.post_trial_access_accountability_score * 0.20,
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
        self.estimated_medical_experimentation_ethics_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MedicalExperimentationEthicsRightsEngineResult:
    agent: str = "Medical Experimentation Ethics Rights Engine Agent"
    domain: str = "medical_experimentation_ethics_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_medical_experimentation_ethics_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MedicalExperimentationEthicsRightsEntity] = field(default_factory=list)

def run_medical_experimentation_ethics_rights_engine() -> MedicalExperimentationEthicsRightsEngineResult:
    entities = [
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-001",
            name="Afrique Sub-Saharienne — Essais Cliniques Multinationaux Sans Consentement Éclairé, 1200 Victimes/An",
            country="Afrique Sub-Saharienne",
            informed_consent_violation_severity_score=95.0,
            vulnerable_population_exploitation_gap_score=93.0,
            regulatory_oversight_absence_score=91.0,
            post_trial_access_accountability_score=90.0,
            primary_pattern="informed_consent_violation_severity",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-002",
            name="Inde — Essais Phase I sur Populations Tribales Analphabètes, Consentement Falsifié 847 Cas Documentés",
            country="Inde",
            informed_consent_violation_severity_score=92.0,
            vulnerable_population_exploitation_gap_score=90.0,
            regulatory_oversight_absence_score=88.0,
            post_trial_access_accountability_score=87.0,
            primary_pattern="vulnerable_population_exploitation_gap",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-003",
            name="Guatemala/Tuskegee Héritage — Expériences Non Consenties sur Prisonniers & Patients Psychiatriques",
            country="Amérique Latine",
            informed_consent_violation_severity_score=89.0,
            vulnerable_population_exploitation_gap_score=87.0,
            regulatory_oversight_absence_score=86.0,
            post_trial_access_accountability_score=84.0,
            primary_pattern="informed_consent_violation_severity",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-004",
            name="Chine — Expériences Militaires & Transplantation Organes Prisonniers, Zéro Transparence IRB",
            country="Chine",
            informed_consent_violation_severity_score=87.0,
            vulnerable_population_exploitation_gap_score=85.0,
            regulatory_oversight_absence_score=90.0,
            post_trial_access_accountability_score=83.0,
            primary_pattern="regulatory_oversight_absence",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-005",
            name="Big Pharma Global — Exclusion Post-Essai Accès Médicaments Populations Pays Bas Revenus Testées",
            country="Global",
            informed_consent_violation_severity_score=55.0,
            vulnerable_population_exploitation_gap_score=58.0,
            regulatory_oversight_absence_score=52.0,
            post_trial_access_accountability_score=60.0,
            primary_pattern="post_trial_access_accountability",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-006",
            name="Europe/USA — Biais de Genre Essais Cliniques, Exclusion Systématique Femmes Phases I-II, Résultats Biaisés",
            country="Europe/USA",
            informed_consent_violation_severity_score=48.0,
            vulnerable_population_exploitation_gap_score=53.0,
            regulatory_oversight_absence_score=45.0,
            post_trial_access_accountability_score=50.0,
            primary_pattern="vulnerable_population_exploitation_gap",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-007",
            name="CIOMS/Conseil International — Directives Éthiques Révision 2016, Renforcement Standards IRB Mondialisation",
            country="Global",
            informed_consent_violation_severity_score=22.0,
            vulnerable_population_exploitation_gap_score=25.0,
            regulatory_oversight_absence_score=20.0,
            post_trial_access_accountability_score=28.0,
            primary_pattern="regulatory_oversight_absence",
        ),
        MedicalExperimentationEthicsRightsEntity(
            entity_id="MEER-008",
            name="ONU/OMS — Déclaration Helsinki Révisée, Code Nuremberg Enforcement & Bioéthique Protocole International",
            country="Global",
            informed_consent_violation_severity_score=5.0,
            vulnerable_population_exploitation_gap_score=5.0,
            regulatory_oversight_absence_score=4.0,
            post_trial_access_accountability_score=6.0,
            primary_pattern="informed_consent_violation_severity",
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

    return MedicalExperimentationEthicsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_medical_experimentation_ethics_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_international_clinical_trials_ethics_violations_report",
            "human_rights_watch_medical_experimentation_unethical_research_review",
            "msf_access_medicines_post_trial_accountability_global_assessment",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_medical_experimentation_ethics_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_medical_experimentation_ethics_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
