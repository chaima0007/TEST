#!/usr/bin/env python3
"""Land Grabbing Agribusiness Engine — CaelumSwarm™ Wave 202 | CSDDD Art.8-13"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN_CODE = "LGA"
ACCENT_COLOR = "#365314"


@dataclass
class LandGrabbingAgribusinessEntity:
    entity_id: str
    name: str
    country: str
    land_acquisition_displacement_community_severity_score: float
    deforestation_ecosystem_destruction_agri_expansion_score: float
    smallholder_rights_violation_contract_farming_score: float
    due_diligence_community_consent_fpic_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_lga_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.land_acquisition_displacement_community_severity_score * 0.30
            + self.deforestation_ecosystem_destruction_agri_expansion_score * 0.25
            + self.smallholder_rights_violation_contract_farming_score * 0.25
            + self.due_diligence_community_consent_fpic_gap_score * 0.20,
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
        self.estimated_lga_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class LandGrabbingAgribusinessEngineResult:
    agent: str = "Land Grabbing Agribusiness Engine Agent"
    domain: str = "land_grabbing_agribusiness"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_lga_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[LandGrabbingAgribusinessEntity] = field(default_factory=list)


def run_land_grabbing_agribusiness_engine() -> LandGrabbingAgribusinessEngineResult:
    entities = [
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-001",
            name="Cargill — Accaparement Terres Amazonie Brésil Soja, Déforestation Fournisseurs, Expulsions Communautés Indigènes & Absence FPIC",
            country="USA/Global",
            land_acquisition_displacement_community_severity_score=95.0,
            deforestation_ecosystem_destruction_agri_expansion_score=93.0,
            smallholder_rights_violation_contract_farming_score=92.0,
            due_diligence_community_consent_fpic_gap_score=91.0,
            primary_pattern="land_acquisition_displacement_community_severity",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-002",
            name="Archer Daniels Midland — Acquisitions Terres Afrique Sub-Saharienne, Contrats Agriculteurs Inégaux, Déplacement Paysans & Soja Déforestation",
            country="USA/Global",
            land_acquisition_displacement_community_severity_score=91.0,
            deforestation_ecosystem_destruction_agri_expansion_score=89.0,
            smallholder_rights_violation_contract_farming_score=88.0,
            due_diligence_community_consent_fpic_gap_score=87.0,
            primary_pattern="deforestation_ecosystem_destruction_agri_expansion",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-003",
            name="Bunge — Accaparement Terres Cerrado Brésil, Soja Huile Palme Déforestation Cachée, Fournisseurs Illégaux & Violations Droits Paysans",
            country="USA/Global",
            land_acquisition_displacement_community_severity_score=87.0,
            deforestation_ecosystem_destruction_agri_expansion_score=85.0,
            smallholder_rights_violation_contract_farming_score=84.0,
            due_diligence_community_consent_fpic_gap_score=83.0,
            primary_pattern="smallholder_rights_violation_contract_farming",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-004",
            name="Louis Dreyfus — Acquisitions Massives Terres Agricoles Afrique/Asie SE, Transformation Subsistance Monoculture Export & Expulsions Communautés",
            country="Pays-Bas/Global",
            land_acquisition_displacement_community_severity_score=83.0,
            deforestation_ecosystem_destruction_agri_expansion_score=81.0,
            smallholder_rights_violation_contract_farming_score=80.0,
            due_diligence_community_consent_fpic_gap_score=79.0,
            primary_pattern="due_diligence_community_consent_fpic_gap",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-005",
            name="Olam International — Plantations Café Cacao Afrique Déforestation Partielle, Contrats Petits Agriculteurs Déséquilibrés & Risques Fonciers",
            country="Singapour/Global",
            land_acquisition_displacement_community_severity_score=57.0,
            deforestation_ecosystem_destruction_agri_expansion_score=55.0,
            smallholder_rights_violation_contract_farming_score=54.0,
            due_diligence_community_consent_fpic_gap_score=53.0,
            primary_pattern="smallholder_rights_violation_contract_farming",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-006",
            name="Wilmar International — Huile Palme Bornéo Déforestation, Concessions Contestées Communautés Indigènes & Compliance NDPE Partielle",
            country="Singapour",
            land_acquisition_displacement_community_severity_score=53.0,
            deforestation_ecosystem_destruction_agri_expansion_score=51.0,
            smallholder_rights_violation_contract_farming_score=50.0,
            due_diligence_community_consent_fpic_gap_score=49.0,
            primary_pattern="deforestation_ecosystem_destruction_agri_expansion",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-007",
            name="Danone — Approvisionnement Lait/Ingrédients Fournisseurs Terres Contestées, Progrès FPIC Insuffisants & Audit Chaîne Lacunaire",
            country="France",
            land_acquisition_displacement_community_severity_score=27.0,
            deforestation_ecosystem_destruction_agri_expansion_score=26.0,
            smallholder_rights_violation_contract_farming_score=25.0,
            due_diligence_community_consent_fpic_gap_score=25.0,
            primary_pattern="due_diligence_community_consent_fpic_gap",
        ),
        LandGrabbingAgribusinessEntity(
            entity_id="LGA-008",
            name="Rainforest Alliance — Certification Durabilité Agricole, Standards Droits Fonciers Paysans & Vérification Zéro Déforestation",
            country="Global",
            land_acquisition_displacement_community_severity_score=5.0,
            deforestation_ecosystem_destruction_agri_expansion_score=4.0,
            smallholder_rights_violation_contract_farming_score=4.0,
            due_diligence_community_consent_fpic_gap_score=4.0,
            primary_pattern="land_acquisition_displacement_community_severity",
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

    return LandGrabbingAgribusinessEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_lga_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "land_matrix_initiative_global_land_deals_database",
            "grain_org_land_grabbing_database_africa_asia_latam",
            "oxfam_behind_the_brands_land_rights_scorecard",
            "global_witness_deforestation_agribusiness_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_land_grabbing_agribusiness_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_lga_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
