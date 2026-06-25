from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SocialProtectionPovertyRightsEntity:
    entity_id: str
    name: str
    country: str
    extreme_poverty_social_security_gap_score: float
    austerity_welfare_cuts_rights_impact_score: float
    informal_economy_worker_exclusion_score: float
    healthcare_education_access_poverty_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_social_protection_poverty_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.extreme_poverty_social_security_gap_score * 0.30
            + self.austerity_welfare_cuts_rights_impact_score * 0.25
            + self.informal_economy_worker_exclusion_score * 0.25
            + self.healthcare_education_access_poverty_score * 0.20,
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
        self.estimated_social_protection_poverty_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SocialProtectionPovertyRightsEngineResult:
    agent: str = "Social Protection Poverty Rights Engine Agent"
    domain: str = "social_protection_poverty_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_social_protection_poverty_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SocialProtectionPovertyRightsEntity] = field(default_factory=list)


def run_social_protection_poverty_rights_engine() -> SocialProtectionPovertyRightsEngineResult:
    entities = [
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-001",
            name="RDC/Congo — 73% Sous Seuil Pauvreté Extrême, Aucun Filet Sécurité National, Conflit Détruit Services & 40M Insécurité Alimentaire",
            country="RDC",
            extreme_poverty_social_security_gap_score=95.0,
            austerity_welfare_cuts_rights_impact_score=91.0,
            informal_economy_worker_exclusion_score=93.0,
            healthcare_education_access_poverty_score=92.0,
            primary_pattern="extreme_poverty_social_security_gap",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-002",
            name="Venezuela — Hyperinflation 2018-2023, 96% Pauvreté ENCOVI, 7M Exilés, Retraites = Cents & Hôpitaux Sans Médicaments",
            country="Venezuela",
            extreme_poverty_social_security_gap_score=92.0,
            austerity_welfare_cuts_rights_impact_score=90.0,
            informal_economy_worker_exclusion_score=88.0,
            healthcare_education_access_poverty_score=91.0,
            primary_pattern="extreme_poverty_social_security_gap",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-003",
            name="Haïti — 60% Extrême Pauvreté, Gangs Contrôlent Distribution Aide, 0 Protection Chômage, Choléra Récurrent & État Absent",
            country="Haïti",
            extreme_poverty_social_security_gap_score=90.0,
            austerity_welfare_cuts_rights_impact_score=87.0,
            informal_economy_worker_exclusion_score=91.0,
            healthcare_education_access_poverty_score=89.0,
            primary_pattern="informal_economy_worker_exclusion",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-004",
            name="Yémen/Guerre — 21M Aide Humanitaire Dépendants, Économie Effondrée, Fonctionnaires Sans Salaire 7 Ans & Nutrition Enfants -3%",
            country="Yémen",
            extreme_poverty_social_security_gap_score=88.0,
            austerity_welfare_cuts_rights_impact_score=86.0,
            informal_economy_worker_exclusion_score=85.0,
            healthcare_education_access_poverty_score=90.0,
            primary_pattern="healthcare_education_access_poverty",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-005",
            name="Inde/Informel — 90% Économie Informelle = 400M Sans Protections, MGNREGA Insuffisant & COVID Effacement Millions",
            country="Inde",
            extreme_poverty_social_security_gap_score=57.0,
            austerity_welfare_cuts_rights_impact_score=54.0,
            informal_economy_worker_exclusion_score=60.0,
            healthcare_education_access_poverty_score=55.0,
            primary_pattern="informal_economy_worker_exclusion",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-006",
            name="Nigeria — 133M Pauvreté Multidimensionnelle, Subventions Carburant Supprimées 2023, Naira Dévaluation & NSIP Ciblage Inefficace",
            country="Nigeria",
            extreme_poverty_social_security_gap_score=55.0,
            austerity_welfare_cuts_rights_impact_score=58.0,
            informal_economy_worker_exclusion_score=57.0,
            healthcare_education_access_poverty_score=56.0,
            primary_pattern="austerity_welfare_cuts_rights_impact",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-007",
            name="Grèce/Austérité — Troïka 2010-2018, Retraites -40%, Chômage 27%, SYRIZA Retour Partiel État Social & Récupération Inégale",
            country="Grèce",
            extreme_poverty_social_security_gap_score=32.0,
            austerity_welfare_cuts_rights_impact_score=38.0,
            informal_economy_worker_exclusion_score=30.0,
            healthcare_education_access_poverty_score=28.0,
            primary_pattern="austerity_welfare_cuts_rights_impact",
        ),
        SocialProtectionPovertyRightsEntity(
            entity_id="SPPR-008",
            name="Danemark/Welfare State — Folkepension Universel, Dagpenge 90% Salaire, Sundhedskort Gratuit & Gini 0.28 Le Plus Bas Monde",
            country="Danemark",
            extreme_poverty_social_security_gap_score=6.0,
            austerity_welfare_cuts_rights_impact_score=5.0,
            informal_economy_worker_exclusion_score=5.0,
            healthcare_education_access_poverty_score=4.0,
            primary_pattern="extreme_poverty_social_security_gap",
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

    return SocialProtectionPovertyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_social_protection_poverty_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_world_social_protection_report_2022_2023",
            "world_bank_poverty_social_protection_2023",
            "un_special_rapporteur_extreme_poverty_2023",
            "oxfam_inequality_report_social_protection_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_social_protection_poverty_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_social_protection_poverty_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
