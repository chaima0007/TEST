from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#1a1505"
PREFIX = "MWR"
DOMAIN = "migrant_worker_rights"


@dataclass
class MigrantWorkerRightsEntity:
    entity_id: str
    name: str
    country: str
    kafala_exploitation_score: float
    wage_theft_abuse_score: float
    freedom_movement_restriction_score: float
    social_protection_exclusion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_migrant_worker_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.kafala_exploitation_score * 0.30
            + self.wage_theft_abuse_score * 0.25
            + self.freedom_movement_restriction_score * 0.25
            + self.social_protection_exclusion_score * 0.20,
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
        self.estimated_migrant_worker_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MigrantWorkerRightsEngineResult:
    agent: str = "Migrant Worker Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_migrant_worker_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MigrantWorkerRightsEntity] = field(default_factory=list)


def run_migrant_worker_rights_engine() -> MigrantWorkerRightsEngineResult:
    entities = [
        MigrantWorkerRightsEntity(
            entity_id="MWR-001",
            name="Qatar FIFA 2022 — 6 500 Morts Documentés Travailleurs Asie, Kafala Systémique, Passeports Confisqués & Travail Forcé Infrastructures Mondial",
            country="Qatar",
            kafala_exploitation_score=90.0,
            wage_theft_abuse_score=88.0,
            freedom_movement_restriction_score=87.0,
            social_protection_exclusion_score=82.0,
            primary_pattern="kafala_exploitation",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-002",
            name="Saudi Arabia Domestic Workers — Kafala Sans Aucune Protection, Violences Domestiques Courantes, Aucun Recours Légal & Travailleurs Asie/Afrique Piégés",
            country="Saudi Arabia",
            kafala_exploitation_score=87.0,
            wage_theft_abuse_score=85.0,
            freedom_movement_restriction_score=84.0,
            social_protection_exclusion_score=79.0,
            primary_pattern="freedom_movement_restriction",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-003",
            name="UAE Construction Sector — Travailleurs Inde/Pakistan/Bangladesh, Debt Bondage Recrutement, Accidents Mortels Impunis & Chaleur Extrême Sans Protection",
            country="UAE",
            kafala_exploitation_score=84.0,
            wage_theft_abuse_score=82.0,
            freedom_movement_restriction_score=81.0,
            social_protection_exclusion_score=76.0,
            primary_pattern="wage_theft_abuse",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-004",
            name="Malaysia Plantation Palm Oil — Travailleurs Indonésiens/Bangladais, Travail Forcé Documenté RSPO, Logements Insalubres & Recrutement Frauduleux Systématique",
            country="Malaysia",
            kafala_exploitation_score=81.0,
            wage_theft_abuse_score=79.0,
            freedom_movement_restriction_score=78.0,
            social_protection_exclusion_score=73.0,
            primary_pattern="kafala_exploitation",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-005",
            name="USA Agricultural Migrants H-2A — Travailleurs Saisonniers Sans Sécurité Sociale, Logements Insalubres Contractuels, Rétorsions Syndicales & Dépendance Visa Employeur",
            country="USA",
            kafala_exploitation_score=60.0,
            wage_theft_abuse_score=58.0,
            freedom_movement_restriction_score=57.0,
            social_protection_exclusion_score=52.0,
            primary_pattern="social_protection_exclusion",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-006",
            name="France Travailleurs Détachés — Directive Détachement Massivement Contournée, Sous-Traitance En Cascade Exploitation, Salaires Non Respectés & Inspection Travail Débordée",
            country="France",
            kafala_exploitation_score=57.0,
            wage_theft_abuse_score=55.0,
            freedom_movement_restriction_score=54.0,
            social_protection_exclusion_score=49.0,
            primary_pattern="wage_theft_abuse",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-007",
            name="ILO Convention C189 Domestic Workers — Ratification Partielle 35 Pays Seulement, Lacunes Protection Persistantes, Meilleure Pratique Incomplète & Monitoring Faible",
            country="Global",
            kafala_exploitation_score=35.0,
            wage_theft_abuse_score=33.0,
            freedom_movement_restriction_score=32.0,
            social_protection_exclusion_score=27.0,
            primary_pattern="social_protection_exclusion",
        ),
        MigrantWorkerRightsEntity(
            entity_id="MWR-008",
            name="Philippines Overseas Workers Program — Protections Légales Minimales Codifiées, Ambassades Support OFW, Meilleure Pratique Relative & Rapatriement Actif",
            country="Philippines",
            kafala_exploitation_score=17.0,
            wage_theft_abuse_score=15.0,
            freedom_movement_restriction_score=14.0,
            social_protection_exclusion_score=9.0,
            primary_pattern="kafala_exploitation",
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

    return MigrantWorkerRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_migrant_worker_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_labour_migration_statistics_2025",
            "hrw_kafala_system_abuse_documentation",
            "amnesty_migrant_worker_exploitation_gulf_report",
            "ilo_forced_labour_supply_chains_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_migrant_worker_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_migrant_worker_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
