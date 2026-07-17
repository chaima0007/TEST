from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#475569"


@dataclass
class SolitaryConfinementRightsEntity:
    entity_id: str
    name: str
    country: str
    prolonged_isolation_score: float
    psychological_torture_score: float
    judicial_oversight_absence_score: float
    vulnerable_population_isolation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_solitary_confinement_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.prolonged_isolation_score * 0.30
            + self.psychological_torture_score * 0.25
            + self.judicial_oversight_absence_score * 0.25
            + self.vulnerable_population_isolation_score * 0.20,
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
        self.estimated_solitary_confinement_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class SolitaryConfinementRightsEngineResult:
    agent: str = "Solitary Confinement Rights Engine Agent"
    domain: str = "solitary_confinement_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_solitary_confinement_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SolitaryConfinementRightsEntity] = field(default_factory=list)


def run_solitary_confinement_rights_engine() -> SolitaryConfinementRightsEngineResult:
    entities = [
        SolitaryConfinementRightsEntity(
            entity_id="SCO-001",
            name="USA — 80 000+ En Isolement/Jour, Plus Grand Nombre Mondial, SHU Super-Max, Décennies Sans Limite",
            country="USA",
            prolonged_isolation_score=94.0,
            psychological_torture_score=92.0,
            judicial_oversight_absence_score=86.0,
            vulnerable_population_isolation_score=90.0,
            primary_pattern="prolonged_isolation_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-002",
            name="Corée du Nord — Cellules Isolement Camp 14/25, Obscurité Totale, Torture Psychologique, Documentation Shin Dong-hyuk",
            country="Corée du Nord",
            prolonged_isolation_score=96.0,
            psychological_torture_score=97.0,
            judicial_oversight_absence_score=98.0,
            vulnerable_population_isolation_score=94.0,
            primary_pattern="judicial_oversight_absence_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-003",
            name="Israël — Facility 1391, Isolement Secret Sans Accès Avocat, Palestiniens Détenus, Centre Fantôme",
            country="Israël",
            prolonged_isolation_score=82.0,
            psychological_torture_score=86.0,
            judicial_oversight_absence_score=90.0,
            vulnerable_population_isolation_score=84.0,
            primary_pattern="judicial_oversight_absence_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-004",
            name="Turquie — F-Type Isolation Cellulaire, Prisonniers Politiques Post-2016 Gülen/Kurdes, Durée Indéterminée",
            country="Turquie",
            prolonged_isolation_score=78.0,
            psychological_torture_score=80.0,
            judicial_oversight_absence_score=76.0,
            vulnerable_population_isolation_score=74.0,
            primary_pattern="psychological_torture_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-005",
            name="France — QI Quartiers d'Isolement, Durée Illimitée, Abus Documentés CGLPL Contrôleur Général",
            country="France",
            prolonged_isolation_score=54.0,
            psychological_torture_score=52.0,
            judicial_oversight_absence_score=50.0,
            vulnerable_population_isolation_score=48.0,
            primary_pattern="prolonged_isolation_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-006",
            name="Mexique — CEFERESO Isolement Total, Politiques/Narcos/Journalistes, Conditions Inhumaines Documentées",
            country="Mexique",
            prolonged_isolation_score=56.0,
            psychological_torture_score=54.0,
            judicial_oversight_absence_score=58.0,
            vulnerable_population_isolation_score=52.0,
            primary_pattern="judicial_oversight_absence_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-007",
            name="UK — CSC Close Supervision Centre, Isolement Prolongé, Rapports Inspectorat HM Prisons Inquiétants",
            country="UK",
            prolonged_isolation_score=34.0,
            psychological_torture_score=30.0,
            judicial_oversight_absence_score=26.0,
            vulnerable_population_isolation_score=28.0,
            primary_pattern="prolonged_isolation_score",
        ),
        SolitaryConfinementRightsEntity(
            entity_id="SCO-008",
            name="Norvège — Isolement Max 4 Semaines Légalement, Meilleure Pratique Internationale, Mandela Rules Modèle",
            country="Norvège",
            prolonged_isolation_score=8.0,
            psychological_torture_score=6.0,
            judicial_oversight_absence_score=5.0,
            vulnerable_population_isolation_score=7.0,
            primary_pattern="prolonged_isolation_score",
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

    return SolitaryConfinementRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_solitary_confinement_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_nelson_mandela_rules_smc_2015",
            "un_special_rapporteur_torture_solitary_confinement",
            "aclu_solitary_watch_annual_report_2024",
            "hrw_solitary_confinement_global_documentation",
            "amnesty_isolation_torture_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_solitary_confinement_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
