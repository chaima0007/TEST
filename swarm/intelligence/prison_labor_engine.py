from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonLaborEntity:
    entity_id: str
    name: str
    country: str
    forced_labor_scale_score: float
    below_minimum_wage_score: float
    coercion_punishment_score: float
    legal_protection_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_labor_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_labor_scale_score * 0.30
            + self.below_minimum_wage_score * 0.25
            + self.coercion_punishment_score * 0.25
            + self.legal_protection_absence_score * 0.20,
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
        self.estimated_prison_labor_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonLaborEngineResult:
    agent: str = "Prison Labor Engine Agent"
    domain: str = "prison_labor"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_prison_labor_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonLaborEntity] = field(default_factory=list)

def run_prison_labor_engine() -> PrisonLaborEngineResult:
    entities = [
        PrisonLaborEntity(
            entity_id="PL-001",
            name="USA — 1.2M Prisonniers Travaillant, Clause 13e Amendement & Corporations Prison-Industrie",
            country="Amérique du Nord",
            forced_labor_scale_score=92.0,
            below_minimum_wage_score=95.0,
            coercion_punishment_score=88.0,
            legal_protection_absence_score=90.0,
            primary_pattern="legal_protection_absence",
        ),
        PrisonLaborEntity(
            entity_id="PL-002",
            name="Chine/Laogai — 1.2M Détenus Ouïghours, Système Laogai & Travail Forcé Politique",
            country="Asie du Nord-Est",
            forced_labor_scale_score=90.0,
            below_minimum_wage_score=92.0,
            coercion_punishment_score=95.0,
            legal_protection_absence_score=88.0,
            primary_pattern="coercion_punishment",
        ),
        PrisonLaborEntity(
            entity_id="PL-003",
            name="Corée du Nord — Kwan-li-so, Colonies Pénitentiaires & Production Export Forcé",
            country="Asie du Nord-Est",
            forced_labor_scale_score=90.0,
            below_minimum_wage_score=88.0,
            coercion_punishment_score=92.0,
            legal_protection_absence_score=85.0,
            primary_pattern="below_minimum_wage",
        ),
        PrisonLaborEntity(
            entity_id="PL-004",
            name="Russie — Colonies Pénitentiaires IK, Travail Forcé État & Entreprises Russes Contrats",
            country="Europe de l'Est",
            forced_labor_scale_score=82.0,
            below_minimum_wage_score=78.0,
            coercion_punishment_score=85.0,
            legal_protection_absence_score=80.0,
            primary_pattern="forced_labor_scale",
        ),
        PrisonLaborEntity(
            entity_id="PL-005",
            name="Thaïlande/Myanmar — Migrants Détenus, Centres Rétention & Travail Forcé Non Payé",
            country="Asie du Sud-Est",
            forced_labor_scale_score=52.0,
            below_minimum_wage_score=55.0,
            coercion_punishment_score=58.0,
            legal_protection_absence_score=50.0,
            primary_pattern="forced_labor_scale",
        ),
        PrisonLaborEntity(
            entity_id="PL-006",
            name="Brésil/Mexique — Travail Carcéral Sous-Payé, Maquiladoras Prison & Réductions Peine",
            country="Amérique Latine",
            forced_labor_scale_score=48.0,
            below_minimum_wage_score=52.0,
            coercion_punishment_score=55.0,
            legal_protection_absence_score=50.0,
            primary_pattern="below_minimum_wage",
        ),
        PrisonLaborEntity(
            entity_id="PL-007",
            name="UE — Travail Carcéral Légalisé, Rémunération Inégale & Standards Minimum Disparates",
            country="Europe",
            forced_labor_scale_score=22.0,
            below_minimum_wage_score=30.0,
            coercion_punishment_score=28.0,
            legal_protection_absence_score=32.0,
            primary_pattern="legal_protection_absence",
        ),
        PrisonLaborEntity(
            entity_id="PL-008",
            name="ONU/OIT/OPCAT — Convention 29, Mécanismes Nationaux Prévention & Standards Travail Détenu",
            country="Global",
            forced_labor_scale_score=4.0,
            below_minimum_wage_score=5.0,
            coercion_punishment_score=3.0,
            legal_protection_absence_score=6.0,
            primary_pattern="coercion_punishment",
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

    return PrisonLaborEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_labor_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "american_civil_liberties_union_captive_labor_exploitation_prison_industries_report",
            "ilo_hard_to_see_harder_to_count_survey_guidelines_forced_labour_prisons",
            "un_subcommittee_prevention_torture_annual_report_detention_labor",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_labor_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_labor_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
