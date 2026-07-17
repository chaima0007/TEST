from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CounterTerrorismRightsViolationsEntity:
    entity_id: str
    name: str
    country: str
    antiterrorism_law_political_misuse_severity_score: float
    secret_detention_torture_rendition_scale_score: float
    mass_surveillance_privacy_violation_score: float
    fair_trial_rights_suspension_terrorism_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_counter_terrorism_rights_violations_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.antiterrorism_law_political_misuse_severity_score * 0.30
            + self.secret_detention_torture_rendition_scale_score * 0.25
            + self.mass_surveillance_privacy_violation_score * 0.25
            + self.fair_trial_rights_suspension_terrorism_deficit_gap_score * 0.20,
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
        self.estimated_counter_terrorism_rights_violations_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CounterTerrorismRightsViolationsEngineResult:
    agent: str = "Counter Terrorism Rights Violations Engine Agent"
    domain: str = "counter_terrorism_rights_violations"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_counter_terrorism_rights_violations_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CounterTerrorismRightsViolationsEntity] = field(default_factory=list)

def run_counter_terrorism_rights_violations_engine() -> CounterTerrorismRightsViolationsEngineResult:
    entities = [
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-001",
            name="Chine/Xinjiang — Lois CTR Uyghurs, 1M Internés Camps Rééducation, Algorithmes Prédictifs & Famille Étrangère Détenue",
            country="Chine",
            antiterrorism_law_political_misuse_severity_score=96.0,
            secret_detention_torture_rendition_scale_score=94.0,
            mass_surveillance_privacy_violation_score=95.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=93.0,
            primary_pattern="antiterrorism_law_political_misuse_severity",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-002",
            name="USA/GWOT — Guantanamo 700+ Détenus, Renditions CIA 50 Pays, NSA PRISM Surveillance & Torture Memos Légalisée",
            country="USA",
            antiterrorism_law_political_misuse_severity_score=91.0,
            secret_detention_torture_rendition_scale_score=93.0,
            mass_surveillance_privacy_violation_score=89.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=92.0,
            primary_pattern="secret_detention_torture_rendition_scale",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-003",
            name="Égypte/Sissi — Loi CTR 2015 ONG Criminalisées, 60k Prisonniers, Tribunaux Militaires Civils & Avocats Détenus",
            country="Égypte",
            antiterrorism_law_political_misuse_severity_score=88.0,
            secret_detention_torture_rendition_scale_score=86.0,
            mass_surveillance_privacy_violation_score=87.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=85.0,
            primary_pattern="antiterrorism_law_political_misuse_severity",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-004",
            name="France/SILT — État Urgence Permanent, Assignations Résidence Militants, DGSI Surveillance Mosquées & Critiques Perquisitions",
            country="France",
            antiterrorism_law_political_misuse_severity_score=84.0,
            secret_detention_torture_rendition_scale_score=82.0,
            mass_surveillance_privacy_violation_score=86.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=83.0,
            primary_pattern="mass_surveillance_privacy_violation",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-005",
            name="Russie/Extrémisme — Loi Extrémisme Témoins Jéhovah Bannis, Novichok Navalny, FSB Provocateurs & Mosquées Surveillées",
            country="Russie",
            antiterrorism_law_political_misuse_severity_score=56.0,
            secret_detention_torture_rendition_scale_score=54.0,
            mass_surveillance_privacy_violation_score=55.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=53.0,
            primary_pattern="antiterrorism_law_political_misuse_severity",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-006",
            name="UK/Schedule 7 — Arrêtés Frontières Journalistes, Prevent Programme Écoles, GCHQ Surveillance Masse & Loi OSA Lanceurs Alertes",
            country="UK",
            antiterrorism_law_political_misuse_severity_score=52.0,
            secret_detention_torture_rendition_scale_score=51.0,
            mass_surveillance_privacy_violation_score=54.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=50.0,
            primary_pattern="fair_trial_rights_suspension_terrorism_deficit_gap",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-007",
            name="ICJ/Airwaves — Mémo Johannesburg CTR Droits, Rapporteur Spécial Droits Humains CTR & Standards Helsinki",
            country="Global",
            antiterrorism_law_political_misuse_severity_score=27.0,
            secret_detention_torture_rendition_scale_score=26.0,
            mass_surveillance_privacy_violation_score=28.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=25.0,
            primary_pattern="fair_trial_rights_suspension_terrorism_deficit_gap",
        ),
        CounterTerrorismRightsViolationsEntity(
            entity_id="CTR-008",
            name="ONU/Résolutions — Résolution 1373 CTR 2001, Stratégie Mondiale CTR ONU, Rapporteur Spécial & Standards Droits Fondamentaux",
            country="Global",
            antiterrorism_law_political_misuse_severity_score=4.0,
            secret_detention_torture_rendition_scale_score=4.0,
            mass_surveillance_privacy_violation_score=4.0,
            fair_trial_rights_suspension_terrorism_deficit_gap_score=4.0,
            primary_pattern="antiterrorism_law_political_misuse_severity",
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

    return CounterTerrorismRightsViolationsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_counter_terrorism_rights_violations_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_counter_terrorism_rights",
            "aclu_global_war_terror_accountability_report",
            "human_rights_watch_antiterrorism_law_misuse",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_counter_terrorism_rights_violations_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_counter_terrorism_rights_violations_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
