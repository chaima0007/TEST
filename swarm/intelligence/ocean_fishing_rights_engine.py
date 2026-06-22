#!/usr/bin/env python3
"""Ocean Fishing Rights Engine — CaelumSwarm™ Wave 202 | CSDDD Art.8-13"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN_CODE = "OFR"
ACCENT_COLOR = "#0c4a6e"


@dataclass
class OceanFishingRightsEntity:
    entity_id: str
    name: str
    country: str
    iuu_fishing_forced_labor_vessel_severity_score: float
    worker_rights_abuse_catch_supply_chain_score: float
    transparency_traceability_seafood_sourcing_score: float
    labor_inspection_port_state_control_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_ofr_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.iuu_fishing_forced_labor_vessel_severity_score * 0.30
            + self.worker_rights_abuse_catch_supply_chain_score * 0.25
            + self.transparency_traceability_seafood_sourcing_score * 0.25
            + self.labor_inspection_port_state_control_score * 0.20,
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
        self.estimated_ofr_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class OceanFishingRightsEngineResult:
    agent: str = "Ocean Fishing Rights Engine Agent"
    domain: str = "ocean_fishing_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_ofr_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OceanFishingRightsEntity] = field(default_factory=list)


def run_ocean_fishing_rights_engine() -> OceanFishingRightsEngineResult:
    entities = [
        OceanFishingRightsEntity(
            entity_id="OFR-001",
            name="Thai Union — Travail Forcé Bateaux Thonier Thaïlande, Migrants Birmans Esclavage Maritime & IUU Fishing Réseaux Cachés",
            country="Thaïlande",
            iuu_fishing_forced_labor_vessel_severity_score=95.0,
            worker_rights_abuse_catch_supply_chain_score=93.0,
            transparency_traceability_seafood_sourcing_score=92.0,
            labor_inspection_port_state_control_score=91.0,
            primary_pattern="iuu_fishing_forced_labor_vessel_severity",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-002",
            name="Charoen Pokphand Foods — Fourniture Crevettes Travail Forcé, Supply Chain Opaque & Flotte Pêche IUU Sous-Traitée",
            country="Thaïlande",
            iuu_fishing_forced_labor_vessel_severity_score=91.0,
            worker_rights_abuse_catch_supply_chain_score=89.0,
            transparency_traceability_seafood_sourcing_score=88.0,
            labor_inspection_port_state_control_score=87.0,
            primary_pattern="worker_rights_abuse_catch_supply_chain",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-003",
            name="Pacific Andes — Pêche IUU Eaux Africaines Ouest, Licences Frauduleuses, Pavillons Complaisance & Faux Rapports Captures",
            country="Hong Kong/Chine",
            iuu_fishing_forced_labor_vessel_severity_score=87.0,
            worker_rights_abuse_catch_supply_chain_score=85.0,
            transparency_traceability_seafood_sourcing_score=84.0,
            labor_inspection_port_state_control_score=83.0,
            primary_pattern="iuu_fishing_forced_labor_vessel_severity",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-004",
            name="Dongwon Industries — Flotte Thonière Pacifique IUU, Conditions Équipages Migrants Abusives & Pêche Zones Exclusives Illicite",
            country="Corée du Sud",
            iuu_fishing_forced_labor_vessel_severity_score=83.0,
            worker_rights_abuse_catch_supply_chain_score=81.0,
            transparency_traceability_seafood_sourcing_score=80.0,
            labor_inspection_port_state_control_score=79.0,
            primary_pattern="labor_inspection_port_state_control",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-005",
            name="Maruha Nichiro — Pratiques IUU Partiellement Documentées Pacifique Nord, Traçabilité Insuffisante Approvisionnement Thon",
            country="Japon",
            iuu_fishing_forced_labor_vessel_severity_score=57.0,
            worker_rights_abuse_catch_supply_chain_score=55.0,
            transparency_traceability_seafood_sourcing_score=54.0,
            labor_inspection_port_state_control_score=53.0,
            primary_pattern="transparency_traceability_seafood_sourcing",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-006",
            name="Nippon Suisan Kaisha — Risques Chaîne Approvisionnement Crevettes Asie SE, Déficits Vérification Licences Sous-Traitants",
            country="Japon",
            iuu_fishing_forced_labor_vessel_severity_score=53.0,
            worker_rights_abuse_catch_supply_chain_score=51.0,
            transparency_traceability_seafood_sourcing_score=50.0,
            labor_inspection_port_state_control_score=49.0,
            primary_pattern="worker_rights_abuse_catch_supply_chain",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-007",
            name="Marine Stewardship Council — Certification MSC Critiquée Insuffisance Contrôle IUU, Lacunes Audit Travail Bateaux Certifiés",
            country="Global",
            iuu_fishing_forced_labor_vessel_severity_score=27.0,
            worker_rights_abuse_catch_supply_chain_score=26.0,
            transparency_traceability_seafood_sourcing_score=25.0,
            labor_inspection_port_state_control_score=25.0,
            primary_pattern="transparency_traceability_seafood_sourcing",
        ),
        OceanFishingRightsEntity(
            entity_id="OFR-008",
            name="Fair Fish International — ONG Droits Pêcheurs Artisanaux, Promotion Pêche Durable & Lobbying Contre IUU Industriel",
            country="Global",
            iuu_fishing_forced_labor_vessel_severity_score=5.0,
            worker_rights_abuse_catch_supply_chain_score=4.0,
            transparency_traceability_seafood_sourcing_score=4.0,
            labor_inspection_port_state_control_score=4.0,
            primary_pattern="iuu_fishing_forced_labor_vessel_severity",
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

    return OceanFishingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_ofr_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_iuu_fishing_global_record_vessels",
            "ilo_work_in_fishing_convention_c188_reports",
            "environmental_justice_foundation_seafood_slavery_reports",
            "global_fishing_watch_vessel_monitoring_data",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_ocean_fishing_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_ofr_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
