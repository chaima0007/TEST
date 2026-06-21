from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonConditionsDetentionRightsEntity:
    entity_id: str
    name: str
    country: str
    torture_ill_treatment_detention_severity_score: float
    overcrowding_inhumane_conditions_scale_score: float
    solitary_confinement_isolation_abuse_score: float
    prison_healthcare_legal_access_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_conditions_detention_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.torture_ill_treatment_detention_severity_score * 0.30
            + self.overcrowding_inhumane_conditions_scale_score * 0.25
            + self.solitary_confinement_isolation_abuse_score * 0.25
            + self.prison_healthcare_legal_access_deficit_gap_score * 0.20,
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
        self.estimated_prison_conditions_detention_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonConditionsDetentionRightsEngineResult:
    agent: str = "Prison Conditions Detention Rights Engine Agent"
    domain: str = "prison_conditions_detention_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_prison_conditions_detention_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonConditionsDetentionRightsEntity] = field(default_factory=list)

def run_prison_conditions_detention_rights_engine() -> PrisonConditionsDetentionRightsEngineResult:
    entities = [
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-001",
            name="Philippines/Guerre Drogues — Prisons 800% Capacité, Torture Systématique & Morts en Détention",
            country="Asie du Sud-Est",
            torture_ill_treatment_detention_severity_score=92.0,
            overcrowding_inhumane_conditions_scale_score=95.0,
            solitary_confinement_isolation_abuse_score=85.0,
            prison_healthcare_legal_access_deficit_gap_score=90.0,
            primary_pattern="overcrowding_inhumane_conditions_scale",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-002",
            name="Libye/Prisons Milices — Torture Généralisée, Détention Arbitraire & Absence Contrôle Judiciaire",
            country="Afrique du Nord",
            torture_ill_treatment_detention_severity_score=95.0,
            overcrowding_inhumane_conditions_scale_score=88.0,
            solitary_confinement_isolation_abuse_score=90.0,
            prison_healthcare_legal_access_deficit_gap_score=92.0,
            primary_pattern="torture_ill_treatment_detention_severity",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-003",
            name="Égypte/Prisons Politiques — Tortures Al-Aqrab, Isolement Prolongé & Détention Sans Procès",
            country="Afrique du Nord",
            torture_ill_treatment_detention_severity_score=90.0,
            overcrowding_inhumane_conditions_scale_score=85.0,
            solitary_confinement_isolation_abuse_score=92.0,
            prison_healthcare_legal_access_deficit_gap_score=88.0,
            primary_pattern="solitary_confinement_isolation_abuse",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-004",
            name="El Salvador/Bukele Méga-Prison — 40k Détenus CECOT, Surpopulation Extrême & Droits Bafoués",
            country="Amérique Centrale",
            torture_ill_treatment_detention_severity_score=85.0,
            overcrowding_inhumane_conditions_scale_score=92.0,
            solitary_confinement_isolation_abuse_score=88.0,
            prison_healthcare_legal_access_deficit_gap_score=82.0,
            primary_pattern="overcrowding_inhumane_conditions_scale",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-005",
            name="USA/Comté Prisons — Surpopulation Chronique, Isolement & Accès Soins Mentaux Déficient",
            country="Amérique du Nord",
            torture_ill_treatment_detention_severity_score=52.0,
            overcrowding_inhumane_conditions_scale_score=58.0,
            solitary_confinement_isolation_abuse_score=62.0,
            prison_healthcare_legal_access_deficit_gap_score=55.0,
            primary_pattern="solitary_confinement_isolation_abuse",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-006",
            name="Russie/Colonies Pénales Arctique — Conditions Extrêmes, Privations & Travail Forcé Sibérie",
            country="Europe de l'Est",
            torture_ill_treatment_detention_severity_score=55.0,
            overcrowding_inhumane_conditions_scale_score=48.0,
            solitary_confinement_isolation_abuse_score=52.0,
            prison_healthcare_legal_access_deficit_gap_score=58.0,
            primary_pattern="prison_healthcare_legal_access_deficit_gap",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-007",
            name="CPT/APT — Comité Prévention Torture, Inspections & Mécanismes Nationaux Monitoring Détention",
            country="Global",
            torture_ill_treatment_detention_severity_score=25.0,
            overcrowding_inhumane_conditions_scale_score=22.0,
            solitary_confinement_isolation_abuse_score=20.0,
            prison_healthcare_legal_access_deficit_gap_score=28.0,
            primary_pattern="prison_healthcare_legal_access_deficit_gap",
        ),
        PrisonConditionsDetentionRightsEntity(
            entity_id="PCDR-008",
            name="ONU/Règles Nelson Mandela 2015 — Standards Minima Traitement Détenus & Réforme Pénitentiaire",
            country="Global",
            torture_ill_treatment_detention_severity_score=5.0,
            overcrowding_inhumane_conditions_scale_score=6.0,
            solitary_confinement_isolation_abuse_score=4.0,
            prison_healthcare_legal_access_deficit_gap_score=8.0,
            primary_pattern="torture_ill_treatment_detention_severity",
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

    return PrisonConditionsDetentionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_conditions_detention_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_torture_report_detention_conditions_global",
            "amnesty_international_cpt_annual_report_prison_overcrowding_ill_treatment",
            "un_standard_minimum_rules_treatment_prisoners_nelson_mandela_rules_2015",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_conditions_detention_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_conditions_detention_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
