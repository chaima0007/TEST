from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LeprosyAffectedRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_isolation_segregation_score: float
    legal_discrimination_exclusion_score: float
    healthcare_access_treatment_gap_score: float
    social_stigma_family_abandonment_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_leprosy_affected_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_isolation_segregation_score * 0.30
            + self.legal_discrimination_exclusion_score * 0.25
            + self.healthcare_access_treatment_gap_score * 0.25
            + self.social_stigma_family_abandonment_score * 0.20,
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
        self.estimated_leprosy_affected_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class LeprosyAffectedRightsEngineResult:
    agent: str = "Leprosy Affected Rights Engine Agent"
    domain: str = "leprosy_affected_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_leprosy_affected_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LeprosyAffectedRightsEntity] = field(default_factory=list)


def run_leprosy_affected_rights_engine() -> LeprosyAffectedRightsEngineResult:
    entities = [
        LeprosyAffectedRightsEntity(
            entity_id="LA-001",
            name="Inde — 700+ Lois Discriminatoires Actives, Colonies Léproseriums Isolées & 3,4M Cas Historiques Non Réhabilités",
            country="Asie du Sud",
            forced_isolation_segregation_score=92.0,
            legal_discrimination_exclusion_score=95.0,
            healthcare_access_treatment_gap_score=88.0,
            social_stigma_family_abandonment_score=90.0,
            primary_pattern="legal_discrimination_exclusion",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-002",
            name="Brésil — 33 000 Nouveaux Cas/An, Deuxième Pays Mondial & Stigmatisation Extrême en Amazonie Rurale",
            country="Amérique du Sud",
            forced_isolation_segregation_score=85.0,
            legal_discrimination_exclusion_score=82.0,
            healthcare_access_treatment_gap_score=88.0,
            social_stigma_family_abandonment_score=85.0,
            primary_pattern="healthcare_access_treatment_gap",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-003",
            name="Nigeria — Colonies Lépreux Actives, Ségrégation Communautaire & Déni Emploi/Mariage Systématique",
            country="Afrique de l'Ouest",
            forced_isolation_segregation_score=88.0,
            legal_discrimination_exclusion_score=82.0,
            healthcare_access_treatment_gap_score=85.0,
            social_stigma_family_abandonment_score=88.0,
            primary_pattern="forced_isolation_segregation",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-004",
            name="Éthiopie/Afrique de l'Est — Abandon Familial Documenté, Mendicité Forcée & Accès Traitement MDT Inexistant",
            country="Afrique de l'Est",
            forced_isolation_segregation_score=80.0,
            legal_discrimination_exclusion_score=78.0,
            healthcare_access_treatment_gap_score=90.0,
            social_stigma_family_abandonment_score=85.0,
            primary_pattern="healthcare_access_treatment_gap",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-005",
            name="Myanmar/Bangladesh — Zones Conflit + Lèpre, Rupture Chaîne Traitement MDT & Double Discrimination Réfugiés",
            country="Asie du Sud-Est",
            forced_isolation_segregation_score=55.0,
            legal_discrimination_exclusion_score=58.0,
            healthcare_access_treatment_gap_score=62.0,
            social_stigma_family_abandonment_score=55.0,
            primary_pattern="healthcare_access_treatment_gap",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-006",
            name="Indonésie — 18 000 Cas/An, Stigmate Religieux Islam/Chrétien & Réhabilitation Sociale Insuffisante",
            country="Asie du Sud-Est",
            forced_isolation_segregation_score=50.0,
            legal_discrimination_exclusion_score=48.0,
            healthcare_access_treatment_gap_score=45.0,
            social_stigma_family_abandonment_score=52.0,
            primary_pattern="social_stigma_family_abandonment",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-007",
            name="ILEP/Fondation Damien — Programme MDT Global, Réintégration 600 000 Patients/An & Plaidoyer OMS",
            country="Global",
            forced_isolation_segregation_score=22.0,
            legal_discrimination_exclusion_score=28.0,
            healthcare_access_treatment_gap_score=20.0,
            social_stigma_family_abandonment_score=25.0,
            primary_pattern="legal_discrimination_exclusion",
        ),
        LeprosyAffectedRightsEntity(
            entity_id="LA-008",
            name="OMS Stratégie 2021-2030 — Objectif Zéro Loi Discriminatoire, Diagnostic Précoce & Intégration Soins Primaires",
            country="Global",
            forced_isolation_segregation_score=5.0,
            legal_discrimination_exclusion_score=8.0,
            healthcare_access_treatment_gap_score=5.0,
            social_stigma_family_abandonment_score=7.0,
            primary_pattern="legal_discrimination_exclusion",
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

    return LeprosyAffectedRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_leprosy_affected_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_global_leprosy_programme_2021_2030_strategy",
            "ilep_international_federation_anti_leprosy_associations_reports",
            "india_national_leprosy_eradication_programme_discrimination_laws_audit",
            "human_rights_watch_leprosy_discrimination_india_2020",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_leprosy_affected_rights_engine()
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
