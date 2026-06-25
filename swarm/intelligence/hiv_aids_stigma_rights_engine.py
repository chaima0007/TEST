from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HivAidsStigmaRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_disclosure_score: float
    healthcare_discrimination_refusal_score: float
    employment_housing_exclusion_score: float
    family_community_rejection_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_hiv_aids_stigma_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_disclosure_score * 0.30
            + self.healthcare_discrimination_refusal_score * 0.25
            + self.employment_housing_exclusion_score * 0.25
            + self.family_community_rejection_score * 0.20,
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
        self.estimated_hiv_aids_stigma_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class HivAidsStigmaRightsEngineResult:
    agent: str = "HIV AIDS Stigma Rights Engine Agent"
    domain: str = "hiv_aids_stigma_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_hiv_aids_stigma_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HivAidsStigmaRightsEntity] = field(default_factory=list)


def run_hiv_aids_stigma_rights_engine() -> HivAidsStigmaRightsEngineResult:
    entities = [
        HivAidsStigmaRightsEntity(
            entity_id="HA-001",
            name="Russie — 134 Lois Criminalisant Transmission, 1,2M Séropositifs Ignorés & Refus ARV pour Étrangers",
            country="Europe de l'Est",
            criminalization_disclosure_score=95.0,
            healthcare_discrimination_refusal_score=92.0,
            employment_housing_exclusion_score=90.0,
            family_community_rejection_score=88.0,
            primary_pattern="criminalization_disclosure",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-002",
            name="Ouganda/Tanzanie — Loi Anti-Homosexualité + VIH, Peine Mort Proposition & Exode ONG Santé 2023",
            country="Afrique de l'Est",
            criminalization_disclosure_score=92.0,
            healthcare_discrimination_refusal_score=88.0,
            employment_housing_exclusion_score=88.0,
            family_community_rejection_score=90.0,
            primary_pattern="criminalization_disclosure",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-003",
            name="Nigeria/Sénégal — Criminalisation Relations Même Sexe + VIH, Refus Soins Hôpitaux Publics & Lapidation Menaces",
            country="Afrique de l'Ouest",
            criminalization_disclosure_score=90.0,
            healthcare_discrimination_refusal_score=92.0,
            employment_housing_exclusion_score=85.0,
            family_community_rejection_score=88.0,
            primary_pattern="healthcare_discrimination_refusal",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-004",
            name="Inde/Asie du Sud — Discrimination Soins 60% Séropositifs Rapportée, Licenciement Emploi & Exclusion Logement",
            country="Asie du Sud",
            criminalization_disclosure_score=75.0,
            healthcare_discrimination_refusal_score=80.0,
            employment_housing_exclusion_score=82.0,
            family_community_rejection_score=78.0,
            primary_pattern="employment_housing_exclusion",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-005",
            name="Caraïbes/Jamaïque — Buggery Laws Actives, VIH HSH Non Traités & Méfiance Système Santé Profonde",
            country="Caraïbes",
            criminalization_disclosure_score=55.0,
            healthcare_discrimination_refusal_score=58.0,
            employment_housing_exclusion_score=52.0,
            family_community_rejection_score=55.0,
            primary_pattern="criminalization_disclosure",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-006",
            name="Chine/Asie de l'Est — Fichage Séropositifs, Tests Emploi Obligatoires Illégaux & Stigmate Familles Rurales",
            country="Asie de l'Est",
            criminalization_disclosure_score=48.0,
            healthcare_discrimination_refusal_score=50.0,
            employment_housing_exclusion_score=52.0,
            family_community_rejection_score=48.0,
            primary_pattern="employment_housing_exclusion",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-007",
            name="UNAIDS/MSF — Programme ARV 39M Sous Traitement, Réduction Stigmate Communautaire & U=U Campaign",
            country="Global",
            criminalization_disclosure_score=22.0,
            healthcare_discrimination_refusal_score=20.0,
            employment_housing_exclusion_score=25.0,
            family_community_rejection_score=20.0,
            primary_pattern="healthcare_discrimination_refusal",
        ),
        HivAidsStigmaRightsEntity(
            entity_id="HA-008",
            name="ONU/ONUSIDA — Stratégie 95-95-95, Objectif Fin SIDA 2030 & Déclaration Politique Non-Discrimination",
            country="Global",
            criminalization_disclosure_score=5.0,
            healthcare_discrimination_refusal_score=4.0,
            employment_housing_exclusion_score=6.0,
            family_community_rejection_score=5.0,
            primary_pattern="criminalization_disclosure",
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

    return HivAidsStigmaRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_hiv_aids_stigma_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unaids_global_aids_update_2023_stigma_discrimination_chapter",
            "human_rights_watch_hiv_criminalization_laws_global_audit_2022",
            "amnesty_international_rights_not_crimes_hiv_decriminalization_report",
            "people_living_hiv_stigma_index_global_survey_gipa_2022",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_hiv_aids_stigma_rights_engine()
    dist = result.risk_distribution
    avg = result.avg_composite
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Risk distribution: {dist}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
    print(f"avg_composite : {avg:.2f}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")
