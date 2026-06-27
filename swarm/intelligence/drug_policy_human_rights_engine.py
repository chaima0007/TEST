from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DrugPolicyHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_scale_score: float
    extrajudicial_killings_score: float
    treatment_access_denial_score: float
    racial_marginalization_bias_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_drug_policy_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_scale_score * 0.30
            + self.extrajudicial_killings_score * 0.25
            + self.treatment_access_denial_score * 0.25
            + self.racial_marginalization_bias_score * 0.20,
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
        self.estimated_drug_policy_human_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DrugPolicyHumanRightsEngineResult:
    agent: str = "Drug Policy Human Rights Engine Agent"
    domain: str = "drug_policy_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_drug_policy_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DrugPolicyHumanRightsEntity] = field(default_factory=list)

def run_drug_policy_human_rights_engine() -> DrugPolicyHumanRightsEngineResult:
    entities = [
        DrugPolicyHumanRightsEntity(
            entity_id="DP-001",
            name="Philippines/Duterte — 30 000 Tués Guerre Drogues, Exécutions Extrajudiciaires Policières",
            country="Asie du Sud-Est",
            criminalization_scale_score=92.0,
            extrajudicial_killings_score=98.0,
            treatment_access_denial_score=85.0,
            racial_marginalization_bias_score=88.0,
            primary_pattern="extrajudicial_killings",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-002",
            name="Indonésie/Thaïlande — Peine de Mort Drogues, Zéro Tolérance & Milliers Emprisonnés",
            country="Asie du Sud-Est",
            criminalization_scale_score=85.0,
            extrajudicial_killings_score=88.0,
            treatment_access_denial_score=82.0,
            racial_marginalization_bias_score=80.0,
            primary_pattern="criminalization_scale",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-003",
            name="USA — Mass Incarceration, War on Drugs, Biais Racial & Prison Industrial Complex",
            country="Amérique du Nord",
            criminalization_scale_score=78.0,
            extrajudicial_killings_score=72.0,
            treatment_access_denial_score=80.0,
            racial_marginalization_bias_score=92.0,
            primary_pattern="racial_marginalization_bias",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-004",
            name="Russie — Peine Sévère Héroïne, Refus Substitution Méthadone & Prohibition Harm Reduction",
            country="Europe de l'Est",
            criminalization_scale_score=80.0,
            extrajudicial_killings_score=75.0,
            treatment_access_denial_score=88.0,
            racial_marginalization_bias_score=70.0,
            primary_pattern="treatment_access_denial",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-005",
            name="Amérique Latine/Mexique — Cartels, Militarisation & Victimes Civils Guerre Drogues",
            country="Amérique Latine",
            criminalization_scale_score=55.0,
            extrajudicial_killings_score=58.0,
            treatment_access_denial_score=52.0,
            racial_marginalization_bias_score=50.0,
            primary_pattern="extrajudicial_killings",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-006",
            name="Afrique/Ghana — Criminalisation Usage Personnel, Absence Harm Reduction & Emprisonnement",
            country="Afrique Sub-Saharienne",
            criminalization_scale_score=50.0,
            extrajudicial_killings_score=45.0,
            treatment_access_denial_score=55.0,
            racial_marginalization_bias_score=52.0,
            primary_pattern="criminalization_scale",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-007",
            name="Portugal/UE — Modèle Décriminalisation, Harm Reduction & Résistance Politique Mondiale",
            country="Europe",
            criminalization_scale_score=22.0,
            extrajudicial_killings_score=20.0,
            treatment_access_denial_score=28.0,
            racial_marginalization_bias_score=30.0,
            primary_pattern="treatment_access_denial",
        ),
        DrugPolicyHumanRightsEntity(
            entity_id="DP-008",
            name="ONU/ONUDC/OMS — Conventions Drogues 1961-1988, Harm Reduction Recommandée & Réforme",
            country="Global",
            criminalization_scale_score=4.0,
            extrajudicial_killings_score=5.0,
            treatment_access_denial_score=3.0,
            racial_marginalization_bias_score=6.0,
            primary_pattern="racial_marginalization_bias",
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

    return DrugPolicyHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_drug_policy_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "human_rights_watch_killing_the_future_drug_war_report",
            "unodc_world_drug_report_annual_statistics_trends",
            "idpc_international_drug_policy_consortium_shadow_report_ungass",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_drug_policy_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_drug_policy_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
