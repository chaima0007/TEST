from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DrugPolicyCriminalizationRightsEntity:
    entity_id: str
    name: str
    country: str
    death_penalty_drug_offenses_score: float
    mass_imprisonment_minor_drug_offenses_score: float
    extrajudicial_killings_war_on_drugs_score: float
    treatment_harm_reduction_access_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_drug_policy_criminalization_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.death_penalty_drug_offenses_score * 0.30
            + self.mass_imprisonment_minor_drug_offenses_score * 0.25
            + self.extrajudicial_killings_war_on_drugs_score * 0.25
            + self.treatment_harm_reduction_access_denial_score * 0.20,
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
        self.estimated_drug_policy_criminalization_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DrugPolicyCriminalizationRightsEngineResult:
    agent: str = "Drug Policy Criminalization Rights Engine Agent"
    domain: str = "drug_policy_criminalization_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_drug_policy_criminalization_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DrugPolicyCriminalizationRightsEntity] = field(default_factory=list)


def run_drug_policy_criminalization_rights_engine() -> DrugPolicyCriminalizationRightsEngineResult:
    entities = [
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-001",
            name="Philippines/Duterte — 6000+ EJK War on Drugs 2016-2022, Pauvres Ciblés, ICC Enquête Ouverte, Caloocan Police",
            country="Philippines",
            death_penalty_drug_offenses_score=90.0,
            mass_imprisonment_minor_drug_offenses_score=88.0,
            extrajudicial_killings_war_on_drugs_score=97.0,
            treatment_harm_reduction_access_denial_score=91.0,
            primary_pattern="extrajudicial_killings_war_on_drugs",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-002",
            name="Singapour — Peine de Mort Trafic depuis 1975, Pendaisons 2022-2023, Nagaenthran Dharmalingam, Amnesty Condamne",
            country="Singapour",
            death_penalty_drug_offenses_score=97.0,
            mass_imprisonment_minor_drug_offenses_score=82.0,
            extrajudicial_killings_war_on_drugs_score=60.0,
            treatment_harm_reduction_access_denial_score=88.0,
            primary_pattern="death_penalty_drug_offenses",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-003",
            name="Iran — 70%+ Exécutions pour Drogues, 2018 Loi Réforme Partielle Insuffisante, Kurdes Surreprésentés",
            country="Iran",
            death_penalty_drug_offenses_score=95.0,
            mass_imprisonment_minor_drug_offenses_score=87.0,
            extrajudicial_killings_war_on_drugs_score=78.0,
            treatment_harm_reduction_access_denial_score=85.0,
            primary_pattern="death_penalty_drug_offenses",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-004",
            name="Chine/Compulsory Treatment — 2000+ Centres Détox Forcée Ankang, Travail Forcé Toxicomanes, 300K Détenus",
            country="Chine",
            death_penalty_drug_offenses_score=80.0,
            mass_imprisonment_minor_drug_offenses_score=92.0,
            extrajudicial_killings_war_on_drugs_score=72.0,
            treatment_harm_reduction_access_denial_score=93.0,
            primary_pattern="mass_imprisonment_minor_drug_offenses",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-005",
            name="Russie — Zéro Thérapie Substitution, Harm Reduction Criminalisée, VIH/SIDA Épidémie PWID, 3M Dépendants Sans Aide",
            country="Russie",
            death_penalty_drug_offenses_score=52.0,
            mass_imprisonment_minor_drug_offenses_score=60.0,
            extrajudicial_killings_war_on_drugs_score=44.0,
            treatment_harm_reduction_access_denial_score=65.0,
            primary_pattern="treatment_harm_reduction_access_denial",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-006",
            name="USA/War on Drugs — Mass Incarceration 40% Crimes Drogues, Disparités Raciales 3:1, Overdoses Record 2022, Réforme Partielle",
            country="USA",
            death_penalty_drug_offenses_score=38.0,
            mass_imprisonment_minor_drug_offenses_score=62.0,
            extrajudicial_killings_war_on_drugs_score=55.0,
            treatment_harm_reduction_access_denial_score=48.0,
            primary_pattern="mass_imprisonment_minor_drug_offenses",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-007",
            name="Portugal/Dépénalisation — depuis 2001 Usage Décriminalisé, Traitement Obligatoire Possible, VIH -95%, Modèle Mondial",
            country="Portugal",
            death_penalty_drug_offenses_score=25.0,
            mass_imprisonment_minor_drug_offenses_score=28.0,
            extrajudicial_killings_war_on_drugs_score=20.0,
            treatment_harm_reduction_access_denial_score=22.0,
            primary_pattern="death_penalty_drug_offenses",
        ),
        DrugPolicyCriminalizationRightsEntity(
            entity_id="DPC-008",
            name="Pays-Bas/Pragmatisme — Gedoogbeleid Cannabis, Harm Reduction Trimbos, Methadon Légal, Trafic Toujours Criminel",
            country="Pays-Bas",
            death_penalty_drug_offenses_score=8.0,
            mass_imprisonment_minor_drug_offenses_score=12.0,
            extrajudicial_killings_war_on_drugs_score=5.0,
            treatment_harm_reduction_access_denial_score=9.0,
            primary_pattern="mass_imprisonment_minor_drug_offenses",
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

    return DrugPolicyCriminalizationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_drug_policy_criminalization_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "harm_reduction_international_drug_policy_2023",
            "human_rights_watch_drug_policy_rights_2023",
            "idpc_drug_policy_guide_2023",
            "amnesty_international_death_penalty_drugs_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_drug_policy_criminalization_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_drug_policy_criminalization_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
