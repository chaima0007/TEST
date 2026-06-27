from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ConflictMineralsEntity:
    entity_id: str
    name: str
    country: str
    armed_group_financing_scale_score: float
    supply_chain_due_diligence_failure_score: float
    civilian_exploitation_harm_score: float
    corporate_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_conflict_minerals_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.armed_group_financing_scale_score * 0.30
            + self.supply_chain_due_diligence_failure_score * 0.25
            + self.civilian_exploitation_harm_score * 0.25
            + self.corporate_accountability_gap_score * 0.20,
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
        self.estimated_conflict_minerals_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ConflictMineralsEngineResult:
    agent: str = "Conflict Minerals Engine Agent"
    domain: str = "conflict_minerals"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_conflict_minerals_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ConflictMineralsEntity] = field(default_factory=list)

def run_conflict_minerals_engine() -> ConflictMineralsEngineResult:
    entities = [
        ConflictMineralsEntity(
            entity_id="CM-001",
            name="RDC/3TG — Coltan Financement M23/FDLR, 200K Mineurs Artisanaux & Apple/Samsung Chaîne Opaque",
            country="Afrique Centrale",
            armed_group_financing_scale_score=95.0,
            supply_chain_due_diligence_failure_score=92.0,
            civilian_exploitation_harm_score=92.0,
            corporate_accountability_gap_score=90.0,
            primary_pattern="armed_group_financing_scale",
        ),
        ConflictMineralsEntity(
            entity_id="CM-002",
            name="RDC/Cobalt — 70% Réserves Mondiales, Glencore/Artisanal, 40K Enfants Mines & Tesla Due Diligence",
            country="Afrique Centrale",
            armed_group_financing_scale_score=90.0,
            supply_chain_due_diligence_failure_score=92.0,
            civilian_exploitation_harm_score=88.0,
            corporate_accountability_gap_score=88.0,
            primary_pattern="supply_chain_due_diligence_failure",
        ),
        ConflictMineralsEntity(
            entity_id="CM-003",
            name="Birmanie/Jade & Rubis — Armée Financement Coup État 2021, Kachin & Myanmar Gems Sanctionnées",
            country="Asie du Sud-Est",
            armed_group_financing_scale_score=88.0,
            supply_chain_due_diligence_failure_score=85.0,
            civilian_exploitation_harm_score=88.0,
            corporate_accountability_gap_score=85.0,
            primary_pattern="civilian_exploitation_harm",
        ),
        ConflictMineralsEntity(
            entity_id="CM-004",
            name="Mali/Or — Groupes Armés Jihadistes Taxation Mines, WAGENINGEN Rapport & Sanctions OFAC",
            country="Afrique de l'Ouest",
            armed_group_financing_scale_score=85.0,
            supply_chain_due_diligence_failure_score=85.0,
            civilian_exploitation_harm_score=82.0,
            corporate_accountability_gap_score=85.0,
            primary_pattern="corporate_accountability_gap",
        ),
        ConflictMineralsEntity(
            entity_id="CM-005",
            name="Rwanda — Coltan Ré-Export RDC, OCCRP Rapport Blanchiment Minéraux & Pression Diplomatique",
            country="Afrique de l'Est",
            armed_group_financing_scale_score=55.0,
            supply_chain_due_diligence_failure_score=52.0,
            civilian_exploitation_harm_score=52.0,
            corporate_accountability_gap_score=55.0,
            primary_pattern="supply_chain_due_diligence_failure",
        ),
        ConflictMineralsEntity(
            entity_id="CM-006",
            name="UE/Règlement Minerais Conflit 2021 & Dodd-Frank 1502 — Enforcement Lacunaire & Portée Limitée",
            country="Global",
            armed_group_financing_scale_score=50.0,
            supply_chain_due_diligence_failure_score=52.0,
            civilian_exploitation_harm_score=48.0,
            corporate_accountability_gap_score=52.0,
            primary_pattern="corporate_accountability_gap",
        ),
        ConflictMineralsEntity(
            entity_id="CM-007",
            name="Global Witness/IPIS — Cartographie Mines Conflit, Monitoring Chaînes Approvisionnement & Plaidoyer",
            country="Global",
            armed_group_financing_scale_score=22.0,
            supply_chain_due_diligence_failure_score=28.0,
            civilian_exploitation_harm_score=25.0,
            corporate_accountability_gap_score=30.0,
            primary_pattern="corporate_accountability_gap",
        ),
        ConflictMineralsEntity(
            entity_id="CM-008",
            name="ONU/GE RDC — Rapport Experts Groupe Sanctions, Résolution 1533 & Mécanisme Suivi Minerais",
            country="Global",
            armed_group_financing_scale_score=4.0,
            supply_chain_due_diligence_failure_score=5.0,
            civilian_exploitation_harm_score=3.0,
            corporate_accountability_gap_score=6.0,
            primary_pattern="armed_group_financing_scale",
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

    return ConflictMineralsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_conflict_minerals_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_group_experts_drc_conflict_minerals_sanctions_report",
            "global_witness_ipis_mining_conflict_supply_chain_database",
            "oecd_due_diligence_guidance_responsible_mineral_supply_chains",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_conflict_minerals_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_conflict_minerals_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
