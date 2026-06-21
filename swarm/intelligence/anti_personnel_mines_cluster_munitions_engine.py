from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AntiPersonnelMinesClusterMunitionsEntity:
    entity_id: str
    name: str
    country: str
    contamination_landmine_density: float
    civilian_victim_rate: float
    clearance_capacity_gap: float
    treaty_compliance_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mine_contamination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.contamination_landmine_density * 0.30
            + self.civilian_victim_rate * 0.25
            + self.clearance_capacity_gap * 0.25
            + self.treaty_compliance_gap * 0.20,
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
        self.estimated_mine_contamination_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AntiPersonnelMinesClusterMunitionsEngineResult:
    agent: str = "Anti-Personnel Mines Cluster Munitions Engine Agent"
    domain: str = "anti_personnel_mines_cluster_munitions"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_mine_contamination_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AntiPersonnelMinesClusterMunitionsEntity] = field(default_factory=list)

def run_anti_personnel_mines_cluster_munitions_engine() -> AntiPersonnelMinesClusterMunitionsEngineResult:
    entities = [
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-001",
            name="Afghanistan — 5.4M km2 contamines, 150+ victimes/an, plus grand parc mines mondial",
            country="Afghanistan",
            contamination_landmine_density=96.0,
            civilian_victim_rate=93.0,
            clearance_capacity_gap=94.0,
            treaty_compliance_gap=90.0,
            primary_pattern="contamination_landmine_density",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-002",
            name="Myanmar — Utilisation active mines anti-Rohingya et contexte coup 2021",
            country="Myanmar",
            contamination_landmine_density=88.0,
            civilian_victim_rate=86.0,
            clearance_capacity_gap=80.0,
            treaty_compliance_gap=92.0,
            primary_pattern="treaty_compliance_gap",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-003",
            name="Yemen — Guerre Houthis et coalition, cluster munitions interdites utilisees",
            country="Yemen",
            contamination_landmine_density=84.0,
            civilian_victim_rate=88.0,
            clearance_capacity_gap=78.0,
            treaty_compliance_gap=86.0,
            primary_pattern="civilian_victim_rate",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-004",
            name="Ukraine — Invasion russe 2022, contamination massive est et sud du pays",
            country="Ukraine",
            contamination_landmine_density=78.0,
            civilian_victim_rate=80.0,
            clearance_capacity_gap=72.0,
            treaty_compliance_gap=84.0,
            primary_pattern="treaty_compliance_gap",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-005",
            name="Cambodge — Heritage Khmer Rouge, deminage continu depuis 40 ans",
            country="Cambodge",
            contamination_landmine_density=56.0,
            civilian_victim_rate=52.0,
            clearance_capacity_gap=50.0,
            treaty_compliance_gap=44.0,
            primary_pattern="contamination_landmine_density",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-006",
            name="Colombie — Legacy FARC, mines artisanales zones rurales persistantes",
            country="Colombie",
            contamination_landmine_density=48.0,
            civilian_victim_rate=50.0,
            clearance_capacity_gap=46.0,
            treaty_compliance_gap=40.0,
            primary_pattern="civilian_victim_rate",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-007",
            name="Mozambique — Post-guerre civile, deminage avance mais contamination residuelle",
            country="Mozambique",
            contamination_landmine_density=26.0,
            civilian_victim_rate=22.0,
            clearance_capacity_gap=24.0,
            treaty_compliance_gap=18.0,
            primary_pattern="contamination_landmine_density",
        ),
        AntiPersonnelMinesClusterMunitionsEntity(
            entity_id="APM-008",
            name="Allemagne — Traite Ottawa signe, zero stock mines AP, modele de conformite",
            country="Allemagne",
            contamination_landmine_density=4.0,
            civilian_victim_rate=3.0,
            clearance_capacity_gap=5.0,
            treaty_compliance_gap=2.0,
            primary_pattern="clearance_capacity_gap",
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
        f"{e.entity_id}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return AntiPersonnelMinesClusterMunitionsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_mine_contamination_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "landmine_monitor_2024_annual_report",
            "icbl_cluster_munition_monitor_2024",
            "unmas_contamination_assessment_global_2023",
            "halo_trust_demining_progress_report_2024",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_anti_personnel_mines_cluster_munitions_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_mine_contamination_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — estimated_mine_contamination_index={e.estimated_mine_contamination_index}")
