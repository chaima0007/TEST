from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DisabilityRightsEntity:
    entity_id: str
    name: str
    country: str
    institutionalization_forced_score: float
    accessibility_infrastructure_failure_score: float
    legal_capacity_deprivation_score: float
    crpd_implementation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.institutionalization_forced_score * 0.30
            + self.accessibility_infrastructure_failure_score * 0.25
            + self.legal_capacity_deprivation_score * 0.25
            + self.crpd_implementation_gap_score * 0.20,
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
        self.estimated_disability_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DisabilityRightsEngineResult:
    agent: str = "Disability Rights Engine Agent"
    domain: str = "disability_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_disability_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DisabilityRightsEntity] = field(default_factory=list)

def run_disability_rights_engine() -> DisabilityRightsEngineResult:
    entities = [
        DisabilityRightsEntity(
            entity_id="DR-001",
            name="Russie/Europe Est — Internats Psychiatriques, Tutelle Abusive & Isolement Institutionnel Massif",
            country="Europe de l'Est",
            institutionalization_forced_score=92.0,
            accessibility_infrastructure_failure_score=88.0,
            legal_capacity_deprivation_score=90.0,
            crpd_implementation_gap_score=88.0,
            primary_pattern="institutionalization_forced",
        ),
        DisabilityRightsEntity(
            entity_id="DR-002",
            name="Chine — Système Hukou Exclus Handicap, Internats Forcés & Stérilisations Non Consenties",
            country="Asie du Nord-Est",
            institutionalization_forced_score=88.0,
            accessibility_infrastructure_failure_score=85.0,
            legal_capacity_deprivation_score=88.0,
            crpd_implementation_gap_score=85.0,
            primary_pattern="legal_capacity_deprivation",
        ),
        DisabilityRightsEntity(
            entity_id="DR-003",
            name="Afrique Sub-Saharienne — Exorcismes/Guérisseurs, Abandon Famille, Exclusion Éducation & Pauvreté",
            country="Afrique Sub-Saharienne",
            institutionalization_forced_score=85.0,
            accessibility_infrastructure_failure_score=88.0,
            legal_capacity_deprivation_score=80.0,
            crpd_implementation_gap_score=85.0,
            primary_pattern="accessibility_infrastructure_failure",
        ),
        DisabilityRightsEntity(
            entity_id="DR-004",
            name="Inde — Loi Personnes Handicap 2016 Non Appliquée, Stigmatisation Mentale & Institutions Vétustes",
            country="Asie du Sud",
            institutionalization_forced_score=80.0,
            accessibility_infrastructure_failure_score=82.0,
            legal_capacity_deprivation_score=78.0,
            crpd_implementation_gap_score=82.0,
            primary_pattern="accessibility_infrastructure_failure",
        ),
        DisabilityRightsEntity(
            entity_id="DR-005",
            name="USA — ADA Gaps, Prisons Personnes Handicap Mental, Pauvreté & Inégalités Accès Soins",
            country="Amérique du Nord",
            institutionalization_forced_score=52.0,
            accessibility_infrastructure_failure_score=50.0,
            legal_capacity_deprivation_score=55.0,
            crpd_implementation_gap_score=58.0,
            primary_pattern="crpd_implementation_gap",
        ),
        DisabilityRightsEntity(
            entity_id="DR-006",
            name="UE/Désinstitutionnalisation — Fonds Structurels Mal Utilisés, Progrès Inégaux & CDPH Violations",
            country="Europe",
            institutionalization_forced_score=48.0,
            accessibility_infrastructure_failure_score=45.0,
            legal_capacity_deprivation_score=52.0,
            crpd_implementation_gap_score=50.0,
            primary_pattern="crpd_implementation_gap",
        ),
        DisabilityRightsEntity(
            entity_id="DR-007",
            name="IDA/Inclusion International — Alliance Mondiale, Désinstitutionnalisation & Vie Indépendante",
            country="Global",
            institutionalization_forced_score=22.0,
            accessibility_infrastructure_failure_score=25.0,
            legal_capacity_deprivation_score=28.0,
            crpd_implementation_gap_score=30.0,
            primary_pattern="institutionalization_forced",
        ),
        DisabilityRightsEntity(
            entity_id="DR-008",
            name="ONU/CDPH — Convention Droits Personnes Handicapées 2006, Comité & Protocole Facultatif",
            country="Global",
            institutionalization_forced_score=4.0,
            accessibility_infrastructure_failure_score=5.0,
            legal_capacity_deprivation_score=3.0,
            crpd_implementation_gap_score=6.0,
            primary_pattern="legal_capacity_deprivation",
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

    return DisabilityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disability_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "human_rights_watch_disability_institutionalization_global_report",
            "mental_disability_rights_international_global_report",
            "un_crpd_committee_state_party_reviews_concluding_observations",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_disability_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_disability_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
