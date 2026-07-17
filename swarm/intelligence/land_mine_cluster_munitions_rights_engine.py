from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LandMineClusterMunitionsRightsEntity:
    entity_id: str
    name: str
    country: str
    active_landmine_civilian_casualty_severity_score: float
    cluster_munition_unexploded_ordnance_scale_score: float
    mine_ban_treaty_non_compliance_score: float
    victim_assistance_demining_funding_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_mine_cluster_munitions_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.active_landmine_civilian_casualty_severity_score * 0.30
            + self.cluster_munition_unexploded_ordnance_scale_score * 0.25
            + self.mine_ban_treaty_non_compliance_score * 0.25
            + self.victim_assistance_demining_funding_deficit_gap_score * 0.20,
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
        self.estimated_land_mine_cluster_munitions_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class LandMineClusterMunitionsRightsEngineResult:
    agent: str = "Land Mine Cluster Munitions Rights Engine Agent"
    domain: str = "land_mine_cluster_munitions_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_land_mine_cluster_munitions_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LandMineClusterMunitionsRightsEntity] = field(default_factory=list)

def run_land_mine_cluster_munitions_rights_engine() -> LandMineClusterMunitionsRightsEngineResult:
    entities = [
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-001",
            name="Afghanistan — 10M Mines Posées, 30+ Ans Contamination, 50 Victimes/Mois & HALO Trust Financement Insuffisant",
            country="Afghanistan",
            active_landmine_civilian_casualty_severity_score=95.0,
            cluster_munition_unexploded_ordnance_scale_score=93.0,
            mine_ban_treaty_non_compliance_score=92.0,
            victim_assistance_demining_funding_deficit_gap_score=94.0,
            primary_pattern="active_landmine_civilian_casualty_severity",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-002",
            name="Yemen — Coalition Sous-Munitions 2015-22, Cluster CBU-87 Civils, Zones Contaminées Portuaires & Financement Déminage Bloqué",
            country="Yemen",
            active_landmine_civilian_casualty_severity_score=91.0,
            cluster_munition_unexploded_ordnance_scale_score=92.0,
            mine_ban_treaty_non_compliance_score=88.0,
            victim_assistance_demining_funding_deficit_gap_score=90.0,
            primary_pattern="cluster_munition_unexploded_ordnance_scale",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-003",
            name="Myanmar — Mines Tatmadaw Minorités Ethniques, Chin/Karen Villages Minés, Non-Signataire Ottawa & Victimes Enfants",
            country="Myanmar",
            active_landmine_civilian_casualty_severity_score=87.0,
            cluster_munition_unexploded_ordnance_scale_score=85.0,
            mine_ban_treaty_non_compliance_score=88.0,
            victim_assistance_demining_funding_deficit_gap_score=86.0,
            primary_pattern="mine_ban_treaty_non_compliance",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-004",
            name="Ukraine/Russie — Mines POM-3 Russes 2022, Cluster MLRS Civils, Zones Résidentielles Contaminées & Déminage 100 Ans Estimé",
            country="Ukraine",
            active_landmine_civilian_casualty_severity_score=83.0,
            cluster_munition_unexploded_ordnance_scale_score=82.0,
            mine_ban_treaty_non_compliance_score=84.0,
            victim_assistance_demining_funding_deficit_gap_score=81.0,
            primary_pattern="cluster_munition_unexploded_ordnance_scale",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-005",
            name="Laos/Vietnam — Heritage Indochine Guerre, UXO Laos 30% Territoire 50 Ans, Agent Orange Victimes & Financement US Insuffisant",
            country="Laos",
            active_landmine_civilian_casualty_severity_score=56.0,
            cluster_munition_unexploded_ordnance_scale_score=54.0,
            mine_ban_treaty_non_compliance_score=55.0,
            victim_assistance_demining_funding_deficit_gap_score=57.0,
            primary_pattern="victim_assistance_demining_funding_deficit_gap",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-006",
            name="Colombie — FARC Mines Rurales, 2ème Mondial Victimes 2019-22, Accord Paix Déminage & Remine Post-Conflit",
            country="Colombie",
            active_landmine_civilian_casualty_severity_score=52.0,
            cluster_munition_unexploded_ordnance_scale_score=51.0,
            mine_ban_treaty_non_compliance_score=54.0,
            victim_assistance_demining_funding_deficit_gap_score=53.0,
            primary_pattern="active_landmine_civilian_casualty_severity",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-007",
            name="ICBL/GICHD — Campagne Internationale Mines, Geneva International Centre Déminage, Monitor Mines 2024 & Mécanisme Convention Ottawa",
            country="Global",
            active_landmine_civilian_casualty_severity_score=27.0,
            cluster_munition_unexploded_ordnance_scale_score=25.0,
            mine_ban_treaty_non_compliance_score=28.0,
            victim_assistance_demining_funding_deficit_gap_score=26.0,
            primary_pattern="victim_assistance_demining_funding_deficit_gap",
        ),
        LandMineClusterMunitionsRightsEntity(
            entity_id="LMC-008",
            name="ONU/Ottawa — Traité Ottawa 1997 163 États Parties, CCM Sous-Munitions 2008, Protocol V CCW & Mécanisme Revue Mise Oeuvre",
            country="Global",
            active_landmine_civilian_casualty_severity_score=4.0,
            cluster_munition_unexploded_ordnance_scale_score=4.0,
            mine_ban_treaty_non_compliance_score=4.0,
            victim_assistance_demining_funding_deficit_gap_score=4.0,
            primary_pattern="mine_ban_treaty_non_compliance",
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

    return LandMineClusterMunitionsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_land_mine_cluster_munitions_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icbl_landmine_monitor_report",
            "geneva_international_centre_demining_report",
            "human_rights_watch_cluster_munitions_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_land_mine_cluster_munitions_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_land_mine_cluster_munitions_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
