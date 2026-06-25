"""Refugees Asylum Seekers Rights Engine — Refoulement, pushbacks, systèmes asile effondrés, conditions camps, apatridie."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class RefugeesAsylumSeekersRightsEntity:
    entity_id: str
    name: str
    country: str
    refoulement_pushback_violence_score: float
    asylum_system_collapse_access_denial_score: float
    refugee_camp_conditions_dignity_violation_score: float
    stateless_refugee_integration_failure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_refugees_asylum_seekers_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.refoulement_pushback_violence_score * 0.30
            + self.asylum_system_collapse_access_denial_score * 0.25
            + self.refugee_camp_conditions_dignity_violation_score * 0.25
            + self.stateless_refugee_integration_failure_score * 0.20,
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
        self.estimated_refugees_asylum_seekers_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class RefugeesAsylumSeekersRightsEngineResult:
    agent: str
    domain: str
    entities: List[RefugeesAsylumSeekersRightsEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_refugees_asylum_seekers_rights_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.88
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_refugees_asylum_seekers_rights_index = round(
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


def run_refugees_asylum_seekers_rights_engine() -> RefugeesAsylumSeekersRightsEngineResult:
    entities = [
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-001",
            name="Libye/Centres Détention — Torture, Esclavage, Viols Systématiques, Pushbacks EU-Financés & Conditions Inhumaines Documentées",
            country="Libye",
            refoulement_pushback_violence_score=92.0,
            asylum_system_collapse_access_denial_score=90.0,
            refugee_camp_conditions_dignity_violation_score=88.0,
            stateless_refugee_integration_failure_score=85.0,
            primary_pattern="refugee_camp_conditions_dignity_violation",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-002",
            name="Grèce/Pushbacks Mer Égée — Refoulements Illégaux Documentés HRW, Moria Incendie, Noyades & Gardes-Côtes Violence",
            country="Grèce",
            refoulement_pushback_violence_score=85.0,
            asylum_system_collapse_access_denial_score=88.0,
            refugee_camp_conditions_dignity_violation_score=82.0,
            stateless_refugee_integration_failure_score=80.0,
            primary_pattern="refoulement_pushback_violence",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-003",
            name="USA/Title 42 Héritage — Expulsions Pandémie Sanitaire, Familles Séparées Frontière, MPP Rester Mexique & Héritage Politique",
            country="USA",
            refoulement_pushback_violence_score=80.0,
            asylum_system_collapse_access_denial_score=78.0,
            refugee_camp_conditions_dignity_violation_score=82.0,
            stateless_refugee_integration_failure_score=75.0,
            primary_pattern="asylum_system_collapse_access_denial",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-004",
            name="Turquie/Refoulement Syrien — 3.6M Réfugiés, Déportations Forcées Documentées, Violences Frontière & Pression Politique Retour",
            country="Turquie",
            refoulement_pushback_violence_score=82.0,
            asylum_system_collapse_access_denial_score=80.0,
            refugee_camp_conditions_dignity_violation_score=78.0,
            stateless_refugee_integration_failure_score=72.0,
            primary_pattern="refoulement_pushback_violence",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-005",
            name="Royaume-Uni/Rwanda Plan — Externalisation Asile Contestée, Cour Suprême Illégal 2023, Nouvelle Loi Contournement & Droits Menacés",
            country="Royaume-Uni",
            refoulement_pushback_violence_score=55.0,
            asylum_system_collapse_access_denial_score=58.0,
            refugee_camp_conditions_dignity_violation_score=52.0,
            stateless_refugee_integration_failure_score=50.0,
            primary_pattern="asylum_system_collapse_access_denial",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-006",
            name="Australie/Offshore Processing — Manus Nauru Détention Indéfinie, Trauma Documenté, Coût Exorbitant & Politique Dissuasion",
            country="Australie",
            refoulement_pushback_violence_score=50.0,
            asylum_system_collapse_access_denial_score=52.0,
            refugee_camp_conditions_dignity_violation_score=48.0,
            stateless_refugee_integration_failure_score=55.0,
            primary_pattern="refugee_camp_conditions_dignity_violation",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-007",
            name="Canada/Accord Tiers Pays Sûr — Accord USA-Canada Révisé 2023, Demandes Refusées Frontière, Systèmes Engorgés & Arriérés",
            country="Canada",
            refoulement_pushback_violence_score=25.0,
            asylum_system_collapse_access_denial_score=28.0,
            refugee_camp_conditions_dignity_violation_score=22.0,
            stateless_refugee_integration_failure_score=30.0,
            primary_pattern="asylum_system_collapse_access_denial",
        ),
        RefugeesAsylumSeekersRightsEntity(
            entity_id="RASR-008",
            name="Allemagne/Intégration Réfugiés — Programme Intégration Modèle, Cours Langue, Soutien Logement & Référence Accueil Europe",
            country="Allemagne",
            refoulement_pushback_violence_score=5.0,
            asylum_system_collapse_access_denial_score=6.0,
            refugee_camp_conditions_dignity_violation_score=4.0,
            stateless_refugee_integration_failure_score=8.0,
            primary_pattern="stateless_refugee_integration_failure",
        ),
    ]

    return RefugeesAsylumSeekersRightsEngineResult(
        agent="Refugees Asylum Seekers Rights Engine Agent",
        domain="refugees_asylum_seekers_rights",
        entities=entities,
        data_sources=[
            "unhcr_global_trends_2023",
            "human_rights_watch_refugee_rights_2023",
            "amnesty_international_refugee_crisis_report_2023",
            "borderline_europe_pushback_monitoring_2023",
        ],
    )


if __name__ == "__main__":
    result = run_refugees_asylum_seekers_rights_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_refugees_asylum_seekers_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
