from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EthnicMinorityRightsDiscriminationEntity:
    entity_id: str
    name: str
    country: str
    state_ethnic_persecution_violence_score: float
    legal_discrimination_citizenship_denial_score: float
    cultural_erasure_linguistic_rights_score: float
    minority_protection_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_ethnic_minority_rights_discrimination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_ethnic_persecution_violence_score * 0.30
            + self.legal_discrimination_citizenship_denial_score * 0.25
            + self.cultural_erasure_linguistic_rights_score * 0.25
            + self.minority_protection_enforcement_gap_score * 0.20,
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
        self.estimated_ethnic_minority_rights_discrimination_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class EthnicMinorityRightsDiscriminationEngineResult:
    agent: str = "Ethnic Minority Rights Discrimination Engine Agent"
    domain: str = "ethnic_minority_rights_discrimination"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_ethnic_minority_rights_discrimination_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EthnicMinorityRightsDiscriminationEntity] = field(default_factory=list)


def run_ethnic_minority_rights_discrimination_engine() -> EthnicMinorityRightsDiscriminationEngineResult:
    entities = [
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-001",
            name="Chine/Ouïghours — Génocide Culturel, Interdiction Langue, Destruction Mosquées & 1M+ Internés Camps Xinjiang",
            country="Chine",
            state_ethnic_persecution_violence_score=97.0,
            legal_discrimination_citizenship_denial_score=95.0,
            cultural_erasure_linguistic_rights_score=96.0,
            minority_protection_enforcement_gap_score=98.0,
            primary_pattern="cultural_erasure_linguistic_rights",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-002",
            name="Myanmar/Rohingya — Génocide 2017, Apatridie, 700K Réfugiés, Villages Brûlés & Tatmadaw Impuni",
            country="Myanmar",
            state_ethnic_persecution_violence_score=95.0,
            legal_discrimination_citizenship_denial_score=96.0,
            cultural_erasure_linguistic_rights_score=92.0,
            minority_protection_enforcement_gap_score=94.0,
            primary_pattern="legal_discrimination_citizenship_denial",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-003",
            name="Inde/Musulmans — CAA 2019 Discriminatoire, Lynchages Vache, Démolitions Maisons & Discours Haine Institutionnel",
            country="Inde",
            state_ethnic_persecution_violence_score=82.0,
            legal_discrimination_citizenship_denial_score=84.0,
            cultural_erasure_linguistic_rights_score=78.0,
            minority_protection_enforcement_gap_score=80.0,
            primary_pattern="legal_discrimination_citizenship_denial",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-004",
            name="Éthiopie/Tigréens — Blocus Alimentaire, Massacres Amhara, Déshumanisation & Crimes de Guerre 2020-2022",
            country="Éthiopie",
            state_ethnic_persecution_violence_score=88.0,
            legal_discrimination_citizenship_denial_score=76.0,
            cultural_erasure_linguistic_rights_score=72.0,
            minority_protection_enforcement_gap_score=85.0,
            primary_pattern="state_ethnic_persecution_violence",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-005",
            name="USA/Noirs — Violence Policière Systémique, Mass Incarceration, Redlining Hérité & Inégalités Structurelles",
            country="USA",
            state_ethnic_persecution_violence_score=57.0,
            legal_discrimination_citizenship_denial_score=52.0,
            cultural_erasure_linguistic_rights_score=45.0,
            minority_protection_enforcement_gap_score=55.0,
            primary_pattern="state_ethnic_persecution_violence",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-006",
            name="Russie/Tchétchènes & Peuples Autochtones — Russification Forcée, Langues Supprimées & Sibérie Sans Droits",
            country="Russie",
            state_ethnic_persecution_violence_score=62.0,
            legal_discrimination_citizenship_denial_score=58.0,
            cultural_erasure_linguistic_rights_score=65.0,
            minority_protection_enforcement_gap_score=48.0,
            primary_pattern="cultural_erasure_linguistic_rights",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-007",
            name="France/Roms — Expulsions Campements Systématiques, Discrimination Logement Emploi & Enfants Sans École",
            country="France",
            state_ethnic_persecution_violence_score=28.0,
            legal_discrimination_citizenship_denial_score=32.0,
            cultural_erasure_linguistic_rights_score=25.0,
            minority_protection_enforcement_gap_score=30.0,
            primary_pattern="minority_protection_enforcement_gap",
        ),
        EthnicMinorityRightsDiscriminationEntity(
            entity_id="EMR-008",
            name="Canada — Droits Constitutionnels, Commission Vérité Réconciliation, Progrès Réels mais Inégaux",
            country="Canada",
            state_ethnic_persecution_violence_score=12.0,
            legal_discrimination_citizenship_denial_score=10.0,
            cultural_erasure_linguistic_rights_score=15.0,
            minority_protection_enforcement_gap_score=14.0,
            primary_pattern="minority_protection_enforcement_gap",
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

    return EthnicMinorityRightsDiscriminationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_ethnic_minority_rights_discrimination_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "minority_rights_group_state_world_minorities_2023",
            "human_rights_watch_ethnic_discrimination_database",
            "un_special_rapporteur_minority_issues_2023",
            "amnesty_international_racial_discrimination_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_ethnic_minority_rights_discrimination_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_ethnic_minority_rights_discrimination_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
