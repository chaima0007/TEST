from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StatelessnessRightsEntity:
    entity_id: str
    name: str
    country: str
    statelessness_legal_vulnerability_severity_score: float
    documentation_citizenship_denial_scale_score: float
    stateless_detention_expulsion_risk_score: float
    reduced_social_rights_access_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_statelessness_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.statelessness_legal_vulnerability_severity_score * 0.30
            + self.documentation_citizenship_denial_scale_score * 0.25
            + self.stateless_detention_expulsion_risk_score * 0.25
            + self.reduced_social_rights_access_barrier_score * 0.20,
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
        self.estimated_statelessness_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class StatelessnessRightsEngineResult:
    agent: str = "Statelessness Rights Engine Agent"
    domain: str = "statelessness_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_statelessness_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessnessRightsEntity] = field(default_factory=list)

def run_statelessness_rights_engine() -> StatelessnessRightsEngineResult:
    entities = [
        StatelessnessRightsEntity(
            entity_id="STL-001",
            name="Rohingya/Myanmar — 600 000 Apatrides, Génocide Reconnu ICJ 2019, Cambodge/Thaïlande Refoulements & Camps UNHCR",
            country="Myanmar",
            statelessness_legal_vulnerability_severity_score=95.0,
            documentation_citizenship_denial_scale_score=93.0,
            stateless_detention_expulsion_risk_score=92.0,
            reduced_social_rights_access_barrier_score=92.0,
            primary_pattern="statelessness_legal_vulnerability_severity",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-002",
            name="Apatrides Golfe/Bidoun — Kuwait/UAE 100 000 Bidoun Sans Nationalité, Zéro Droit Légal & Arrestations Arbitraires",
            country="Kuwait",
            statelessness_legal_vulnerability_severity_score=92.0,
            documentation_citizenship_denial_scale_score=90.0,
            stateless_detention_expulsion_risk_score=89.0,
            reduced_social_rights_access_barrier_score=89.0,
            primary_pattern="documentation_citizenship_denial_scale",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-003",
            name="Syrie/Conflit — 1M Nés Hors Registres Guerre, Déplacés Apatrides Région & Bureaucratie Accès Documents",
            country="Syrie",
            statelessness_legal_vulnerability_severity_score=89.0,
            documentation_citizenship_denial_scale_score=87.0,
            stateless_detention_expulsion_risk_score=86.0,
            reduced_social_rights_access_barrier_score=84.0,
            primary_pattern="documentation_citizenship_denial_scale",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-004",
            name="Afrique Subsaharienne — Communautés Nomades Kenya/Éthiopie, Migrations Sans Documents & Discrimination Ethnique",
            country="Kenya",
            statelessness_legal_vulnerability_severity_score=86.0,
            documentation_citizenship_denial_scale_score=84.0,
            stateless_detention_expulsion_risk_score=83.0,
            reduced_social_rights_access_barrier_score=83.0,
            primary_pattern="statelessness_legal_vulnerability_severity",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-005",
            name="Europe/Roms — 12 000 Apatrides Roms Balkans, Non-Enregistrement Naissance & Discrimination Accès Droits",
            country="Balkans",
            statelessness_legal_vulnerability_severity_score=56.0,
            documentation_citizenship_denial_scale_score=54.0,
            stateless_detention_expulsion_risk_score=53.0,
            reduced_social_rights_access_barrier_score=52.0,
            primary_pattern="documentation_citizenship_denial_scale",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-006",
            name="Haïtiens Dominicains — Décision TC168/13 Rétroactive, 200 000 Dénaturalisés & Expulsions Sans Procédure",
            country="République Dominicaine",
            statelessness_legal_vulnerability_severity_score=53.0,
            documentation_citizenship_denial_scale_score=51.0,
            stateless_detention_expulsion_risk_score=51.0,
            reduced_social_rights_access_barrier_score=50.0,
            primary_pattern="stateless_detention_expulsion_risk",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-007",
            name="UNHCR/IBelong — Campagne #IBelong Fin Apatridie 2024, Plans Action & Enregistrements Naissances",
            country="Global",
            statelessness_legal_vulnerability_severity_score=27.0,
            documentation_citizenship_denial_scale_score=26.0,
            stateless_detention_expulsion_risk_score=25.0,
            reduced_social_rights_access_barrier_score=26.0,
            primary_pattern="reduced_social_rights_access_barrier",
        ),
        StatelessnessRightsEntity(
            entity_id="STL-008",
            name="ONU/Convention 1954 — Convention Statut Apatrides 1954/1961, Mécanismes Identification & SDG 16.9 Identité Légale",
            country="Global",
            statelessness_legal_vulnerability_severity_score=4.0,
            documentation_citizenship_denial_scale_score=4.0,
            stateless_detention_expulsion_risk_score=4.0,
            reduced_social_rights_access_barrier_score=5.0,
            primary_pattern="reduced_social_rights_access_barrier",
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

    return StatelessnessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_statelessness_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_ibelong_statelessness_campaign_report",
            "human_rights_watch_stateless_bidoun_gulf_report",
            "amnesty_international_rohingya_statelessness_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_statelessness_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_statelessness_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
