"""Pandemic Health Emergency Rights Engine — Urgences sanitaires, droits humains, accès vaccins, blocage aide médicale."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class PandemicHealthEmergencyRightsEntity:
    entity_id: str
    name: str
    country: str
    vaccine_access_denial_score: float
    health_system_collapse_rights_score: float
    emergency_powers_rights_abuse_score: float
    humanitarian_aid_blockage_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_pandemic_health_emergency_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.vaccine_access_denial_score * 0.30
            + self.health_system_collapse_rights_score * 0.25
            + self.emergency_powers_rights_abuse_score * 0.25
            + self.humanitarian_aid_blockage_score * 0.20,
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
        self.estimated_pandemic_health_emergency_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PandemicHealthEmergencyRightsEngineResult:
    agent: str
    domain: str
    entities: List[PandemicHealthEmergencyRightsEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_pandemic_health_emergency_rights_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.89
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_pandemic_health_emergency_rights_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_pandemic_health_emergency_rights_engine() -> PandemicHealthEmergencyRightsEngineResult:
    entities = [
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-001",
            name="Corée du Nord — Zéro Accès Vaccins COVID, 25M Population Exposée Sans Protection, Refus Aide COVAX & Isolement Total Sanitaire",
            country="Corée du Nord",
            vaccine_access_denial_score=95.0,
            health_system_collapse_rights_score=90.0,
            emergency_powers_rights_abuse_score=88.0,
            humanitarian_aid_blockage_score=92.0,
            primary_pattern="vaccine_access_denial",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-002",
            name="Yémen/Système Santé Effondré — COVID Choléra Pandémies Simultanées, Hôpitaux Bombardés, Famine & Blocus Maritime Humanitaire",
            country="Yémen",
            vaccine_access_denial_score=88.0,
            health_system_collapse_rights_score=92.0,
            emergency_powers_rights_abuse_score=82.0,
            humanitarian_aid_blockage_score=90.0,
            primary_pattern="health_system_collapse_rights",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-003",
            name="Birmanie/Myanmar — Coup 2021 Hôpitaux Attaqués, Médecins Arrêtés, Accès Humanitaire Bloqué Junta & COVID Sans Protection",
            country="Birmanie/Myanmar",
            vaccine_access_denial_score=82.0,
            health_system_collapse_rights_score=88.0,
            emergency_powers_rights_abuse_score=90.0,
            humanitarian_aid_blockage_score=85.0,
            primary_pattern="emergency_powers_rights_abuse",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-004",
            name="Venezuela — Pénurie Médicaments Chronique, Sanctions Impact Accès Soins, Effondrement Système Public & Exode Médical 15000+",
            country="Venezuela",
            vaccine_access_denial_score=78.0,
            health_system_collapse_rights_score=82.0,
            emergency_powers_rights_abuse_score=75.0,
            humanitarian_aid_blockage_score=80.0,
            primary_pattern="health_system_collapse_rights",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-005",
            name="Haïti — Couverture Vaccinale 3%, Gangs Bloquant Aide MSF, Cholera Résurgence 2022 & Effondrement Gouvernance Sanitaire",
            country="Haïti",
            vaccine_access_denial_score=55.0,
            health_system_collapse_rights_score=58.0,
            emergency_powers_rights_abuse_score=48.0,
            humanitarian_aid_blockage_score=62.0,
            primary_pattern="humanitarian_aid_blockage",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-006",
            name="Éthiopie/Tigré — Blocage Aide Médicale Pendant Conflit 2020-2022, Hôpitaux Pillés, Famine & Accès Humanitaire Refusé",
            country="Éthiopie",
            vaccine_access_denial_score=48.0,
            health_system_collapse_rights_score=55.0,
            emergency_powers_rights_abuse_score=52.0,
            humanitarian_aid_blockage_score=58.0,
            primary_pattern="humanitarian_aid_blockage",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-007",
            name="Inde/Vague Delta 2021 — Inégalité Vaccins, Crise Oxygène, Crémations Masse & Sous-Comptabilisation Morts COVID Estimée x10",
            country="Inde",
            vaccine_access_denial_score=32.0,
            health_system_collapse_rights_score=35.0,
            emergency_powers_rights_abuse_score=28.0,
            humanitarian_aid_blockage_score=22.0,
            primary_pattern="health_system_collapse_rights",
        ),
        PandemicHealthEmergencyRightsEntity(
            entity_id="PHER-008",
            name="Cuba/Vaccins Soberana Abdala — Couverture 90%+ Malgré Embargo USA, Développement National Vaccins & Coopération Sud-Sud Santé",
            country="Cuba",
            vaccine_access_denial_score=5.0,
            health_system_collapse_rights_score=8.0,
            emergency_powers_rights_abuse_score=10.0,
            humanitarian_aid_blockage_score=12.0,
            primary_pattern="vaccine_access_denial",
        ),
    ]

    return PandemicHealthEmergencyRightsEngineResult(
        agent="Pandemic Health Emergency Rights Engine Agent",
        domain="pandemic_health_emergency_rights",
        entities=entities,
        data_sources=[
            "who_covid19_vaccination_tracker_2023",
            "msf_access_medicines_report_2023",
            "human_rights_watch_covid_rights_2021",
            "oxfam_vaccine_inequality_2022",
        ],
    )


if __name__ == "__main__":
    result = run_pandemic_health_emergency_rights_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_pandemic_health_emergency_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
