from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonRehabilitationReentryRightsEntity:
    entity_id: str
    name: str
    country: str
    prison_overcrowding_inhumane_conditions_severity_score: float
    rehabilitation_education_program_absence_scale_score: float
    solitary_confinement_prolonged_use_score: float
    post_release_reintegration_support_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_rehabilitation_reentry_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.prison_overcrowding_inhumane_conditions_severity_score * 0.30
            + self.rehabilitation_education_program_absence_scale_score * 0.25
            + self.solitary_confinement_prolonged_use_score * 0.25
            + self.post_release_reintegration_support_deficit_gap_score * 0.20,
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
        self.estimated_prison_rehabilitation_reentry_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PrisonRehabilitationReentryRightsEngineResult:
    agent: str = "Prison Rehabilitation Reentry Rights Engine Agent"
    domain: str = "prison_rehabilitation_reentry_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_prison_rehabilitation_reentry_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonRehabilitationReentryRightsEntity] = field(default_factory=list)


def run_prison_rehabilitation_reentry_rights_engine() -> PrisonRehabilitationReentryRightsEngineResult:
    entities = [
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-001",
            name="USA — 2.3M Détenus #1 Monde, Solitary 80 000, Prison Privatisée Lobby, For-Profit & Three Strikes Perpétuité",
            country="USA",
            prison_overcrowding_inhumane_conditions_severity_score=95.0,
            rehabilitation_education_program_absence_scale_score=93.0,
            solitary_confinement_prolonged_use_score=92.0,
            post_release_reintegration_support_deficit_gap_score=91.0,
            primary_pattern="solitary_confinement_prolonged_use",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-002",
            name="Philippines — Prisons 500% Surpeuplées, 800 Détenus/Cellule 50 Places, Morts Chaleur & Guerre Drogue Détenus Abandonnés",
            country="Philippines",
            prison_overcrowding_inhumane_conditions_severity_score=92.0,
            rehabilitation_education_program_absence_scale_score=90.0,
            solitary_confinement_prolonged_use_score=89.0,
            post_release_reintegration_support_deficit_gap_score=88.0,
            primary_pattern="prison_overcrowding_inhumane_conditions_severity",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-003",
            name="Brésil — APAC vs Complexes Régimes, Massacres Pénitentiaires Carandiru, Factions Contrôlent Prisons & Réhab Absente",
            country="Brésil",
            prison_overcrowding_inhumane_conditions_severity_score=89.0,
            rehabilitation_education_program_absence_scale_score=87.0,
            solitary_confinement_prolonged_use_score=86.0,
            post_release_reintegration_support_deficit_gap_score=85.0,
            primary_pattern="rehabilitation_education_program_absence_scale",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-004",
            name="Russie/Belarus — Colonies Pénitentiaires Sibérie, Travail Forcé Prisonniers, Torture Systématique & IK-6 Navalny",
            country="Russie/Belarus",
            prison_overcrowding_inhumane_conditions_severity_score=86.0,
            rehabilitation_education_program_absence_scale_score=84.0,
            solitary_confinement_prolonged_use_score=83.0,
            post_release_reintegration_support_deficit_gap_score=82.0,
            primary_pattern="post_release_reintegration_support_deficit_gap",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-005",
            name="Afrique Sub-Saharienne — Prisons Coloniales Non Réformées, Détention Préventive 70%, Sans Procès Années & Maladies",
            country="Afrique Sub-Saharienne",
            prison_overcrowding_inhumane_conditions_severity_score=57.0,
            rehabilitation_education_program_absence_scale_score=55.0,
            solitary_confinement_prolonged_use_score=54.0,
            post_release_reintegration_support_deficit_gap_score=53.0,
            primary_pattern="prison_overcrowding_inhumane_conditions_severity",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-006",
            name="Europe — Récidive Manque Réhab France, UK Short Sentences Inefficaces, Norvège Modèle Non Copié & Détention Immigrants",
            country="Europe",
            prison_overcrowding_inhumane_conditions_severity_score=54.0,
            rehabilitation_education_program_absence_scale_score=52.0,
            solitary_confinement_prolonged_use_score=51.0,
            post_release_reintegration_support_deficit_gap_score=50.0,
            primary_pattern="rehabilitation_education_program_absence_scale",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-007",
            name="Penal Reform International/ICPA — Standards Mandela Rules, Réforme Pénitentiaire Globale, Réhab Evidence-Based & Monitoring",
            country="Global",
            prison_overcrowding_inhumane_conditions_severity_score=27.0,
            rehabilitation_education_program_absence_scale_score=26.0,
            solitary_confinement_prolonged_use_score=25.0,
            post_release_reintegration_support_deficit_gap_score=25.0,
            primary_pattern="rehabilitation_education_program_absence_scale",
        ),
        PrisonRehabilitationReentryRightsEntity(
            entity_id="PRR-008",
            name="ONU/Règles Mandela — Règles Minima Traitement Détenus, OPCAT Mécanismes & SDG 16.3 Justice Accès",
            country="Global",
            prison_overcrowding_inhumane_conditions_severity_score=5.0,
            rehabilitation_education_program_absence_scale_score=4.0,
            solitary_confinement_prolonged_use_score=4.0,
            post_release_reintegration_support_deficit_gap_score=4.0,
            primary_pattern="post_release_reintegration_support_deficit_gap",
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

    return PrisonRehabilitationReentryRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_rehabilitation_reentry_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "penal_reform_international_global_prison_trends",
            "un_mandela_rules_implementation_monitoring_report",
            "human_rights_watch_solitary_confinement_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_prison_rehabilitation_reentry_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_rehabilitation_reentry_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
