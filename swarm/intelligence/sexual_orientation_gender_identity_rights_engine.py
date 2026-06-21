from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SexualOrientationGenderIdentityRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_legal_penalty_severity_score: float
    state_sanctioned_violence_impunity_score: float
    social_discrimination_hate_crime_exposure_score: float
    legal_protection_recognition_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sogi_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_legal_penalty_severity_score * 0.30
            + self.state_sanctioned_violence_impunity_score * 0.25
            + self.social_discrimination_hate_crime_exposure_score * 0.25
            + self.legal_protection_recognition_gap_score * 0.20,
            2,
        )
        if self.composite_score >= 65:
            self.risk_level = "critique"
        elif self.composite_score >= 45:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_sogi_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class SexualOrientationGenderIdentityRightsEngineResult:
    agent: str = "Sexual Orientation Gender Identity Rights Engine Agent"
    domain: str = "sexual_orientation_gender_identity_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sogi_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexualOrientationGenderIdentityRightsEntity] = field(default_factory=list)


def run_sexual_orientation_gender_identity_rights_engine() -> SexualOrientationGenderIdentityRightsEngineResult:
    entities = [
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-001",
            name="Ouganda/Anti-Homosexuality Act 2023 Peine Mort — Aggravated Homosexuality, ONG Fermées, Exils Massifs",
            country="Ouganda",
            criminalization_legal_penalty_severity_score=97.0,
            state_sanctioned_violence_impunity_score=94.0,
            social_discrimination_hate_crime_exposure_score=95.0,
            legal_protection_recognition_gap_score=96.0,
            primary_pattern="criminalization_legal_penalty_severity",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-002",
            name="Iran/Exécutions LGBTQ+ Légales — 100-200 Exécutions Annuelles, Article 237 Code Pénal, Pendaisons Publiques",
            country="Iran",
            criminalization_legal_penalty_severity_score=95.0,
            state_sanctioned_violence_impunity_score=97.0,
            social_discrimination_hate_crime_exposure_score=93.0,
            legal_protection_recognition_gap_score=94.0,
            primary_pattern="state_sanctioned_violence_impunity",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-003",
            name="Russie/Loi Propagande LGBTQ Universelle — Interdiction Totale Toute Expression, Amendes & Arrestations ONG",
            country="Russie",
            criminalization_legal_penalty_severity_score=89.0,
            state_sanctioned_violence_impunity_score=87.0,
            social_discrimination_hate_crime_exposure_score=91.0,
            legal_protection_recognition_gap_score=92.0,
            primary_pattern="legal_protection_recognition_gap",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-004",
            name="Tchétchénie/Camps Disparitions — Camps Secrets Hommes Présumés Gay, Torture & Meurtres Familiaux Honte",
            country="Russie/Tchétchénie",
            criminalization_legal_penalty_severity_score=93.0,
            state_sanctioned_violence_impunity_score=96.0,
            social_discrimination_hate_crime_exposure_score=94.0,
            legal_protection_recognition_gap_score=91.0,
            primary_pattern="state_sanctioned_violence_impunity",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-005",
            name="Hongrie/Anti-Trans Loi Constitution — Interdiction Changement Sexe Légal 2020, Éducation LGBTQ Censurée",
            country="Hongrie",
            criminalization_legal_penalty_severity_score=55.0,
            state_sanctioned_violence_impunity_score=52.0,
            social_discrimination_hate_crime_exposure_score=58.0,
            legal_protection_recognition_gap_score=62.0,
            primary_pattern="legal_protection_recognition_gap",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-006",
            name="Jamaïque/Buggery Law Violence — 10 Ans Emprisonnement, Lynchages Communautaires, Fuites Vers Amérique",
            country="Jamaïque",
            criminalization_legal_penalty_severity_score=32.0,
            state_sanctioned_violence_impunity_score=28.0,
            social_discrimination_hate_crime_exposure_score=35.0,
            legal_protection_recognition_gap_score=30.0,
            primary_pattern="social_discrimination_hate_crime_exposure",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-007",
            name="Canada/Modèle Protection — Marriage Civil Equal 2005, Politique Trans-Inclusive, Conversion Therapy Ban",
            country="Canada",
            criminalization_legal_penalty_severity_score=6.0,
            state_sanctioned_violence_impunity_score=5.0,
            social_discrimination_hate_crime_exposure_score=8.0,
            legal_protection_recognition_gap_score=5.0,
            primary_pattern="criminalization_legal_penalty_severity",
        ),
        SexualOrientationGenderIdentityRightsEntity(
            entity_id="SGI-008",
            name="Taiwan/Mariage Égal Asie Modèle — Premier Pays Asie Mariage Same-Sex 2019, Protection Discrimination Emploi",
            country="Taiwan",
            criminalization_legal_penalty_severity_score=4.0,
            state_sanctioned_violence_impunity_score=3.0,
            social_discrimination_hate_crime_exposure_score=5.0,
            legal_protection_recognition_gap_score=4.0,
            primary_pattern="criminalization_legal_penalty_severity",
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

    dist = {"critique": risk_dist.get("critique", 0), "élevé": risk_dist.get("élevé", 0),
            "modéré": risk_dist.get("modéré", 0), "faible": risk_dist.get("faible", 0)}
    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"

    return SexualOrientationGenderIdentityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sogi_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilga_world_state_sponsored_homophobia_report_2023",
            "human_rights_watch_chechen_lgbtq_persecution_camps",
            "amnesty_international_iran_lgbtq_executions_criminalization",
            "outright_international_sogi_rights_global_tracker",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_sexual_orientation_gender_identity_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sogi_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
