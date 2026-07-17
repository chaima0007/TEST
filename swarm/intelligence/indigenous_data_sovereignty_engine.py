from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IndigenousDataSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    indigenous_data_extraction_commercialization_severity_score: float
    biometric_genomic_collection_without_consent_scale_score: float
    government_surveillance_indigenous_communities_score: float
    ocap_fpic_data_governance_exclusion_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_data_sovereignty_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.indigenous_data_extraction_commercialization_severity_score * 0.30
            + self.biometric_genomic_collection_without_consent_scale_score * 0.25
            + self.government_surveillance_indigenous_communities_score * 0.25
            + self.ocap_fpic_data_governance_exclusion_gap_score * 0.20,
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
        self.estimated_indigenous_data_sovereignty_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class IndigenousDataSovereigntyEngineResult:
    agent: str = "Indigenous Data Sovereignty Engine Agent"
    domain: str = "indigenous_data_sovereignty"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_data_sovereignty_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousDataSovereigntyEntity] = field(default_factory=list)

def run_indigenous_data_sovereignty_engine() -> IndigenousDataSovereigntyEngineResult:
    entities = [
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-001",
            name="USA — Havasupai Tribe Sang ADN Étude Maladie→Schizophrénie Sans Consentement, GenBank Données & NAGPRA Contournement",
            country="USA",
            indigenous_data_extraction_commercialization_severity_score=95.0,
            biometric_genomic_collection_without_consent_scale_score=93.0,
            government_surveillance_indigenous_communities_score=90.0,
            ocap_fpic_data_governance_exclusion_gap_score=92.0,
            primary_pattern="indigenous_data_extraction_commercialization_severity",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-002",
            name="Australie — Données Santé Communautés Autochtones Partagées Assureurs, Surveillance Drones NT & My Health Record Opt-Out Défaut",
            country="Australie",
            indigenous_data_extraction_commercialization_severity_score=92.0,
            biometric_genomic_collection_without_consent_scale_score=89.0,
            government_surveillance_indigenous_communities_score=91.0,
            ocap_fpic_data_governance_exclusion_gap_score=87.0,
            primary_pattern="government_surveillance_indigenous_communities",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-003",
            name="Canada — FNPOC Données Mal Stockées, Visages Autochtones Algorithmie Policière & Base ADN GRC Surreprésentée",
            country="Canada",
            indigenous_data_extraction_commercialization_severity_score=88.0,
            biometric_genomic_collection_without_consent_scale_score=87.0,
            government_surveillance_indigenous_communities_score=86.0,
            ocap_fpic_data_governance_exclusion_gap_score=85.0,
            primary_pattern="biometric_genomic_collection_without_consent_scale",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-004",
            name="Brésil/Amazonie — Cartographie Satellite Terres Garimpos Sans Consultation, Données Yanomami Partagées Agro-Business & FUNAI Surveillance",
            country="Brésil",
            indigenous_data_extraction_commercialization_severity_score=85.0,
            biometric_genomic_collection_without_consent_scale_score=83.0,
            government_surveillance_indigenous_communities_score=84.0,
            ocap_fpic_data_governance_exclusion_gap_score=82.0,
            primary_pattern="ocap_fpic_data_governance_exclusion_gap",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-005",
            name="Nouvelle-Zélande Māori — Données Whakapapa Utilisées Recherche Académique Sans Retour Communauté & Data Colonialism Héritage",
            country="Nouvelle-Zélande",
            indigenous_data_extraction_commercialization_severity_score=57.0,
            biometric_genomic_collection_without_consent_scale_score=54.0,
            government_surveillance_indigenous_communities_score=52.0,
            ocap_fpic_data_governance_exclusion_gap_score=55.0,
            primary_pattern="indigenous_data_extraction_commercialization_severity",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-006",
            name="Afrique Autochtones — Biopiraterie Données Génétiques San/Bushmen, Projets Génome Sans FPIC & Biotechs Brevets Traditionnels",
            country="Afrique",
            indigenous_data_extraction_commercialization_severity_score=54.0,
            biometric_genomic_collection_without_consent_scale_score=53.0,
            government_surveillance_indigenous_communities_score=50.0,
            ocap_fpic_data_governance_exclusion_gap_score=51.0,
            primary_pattern="biometric_genomic_collection_without_consent_scale",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-007",
            name="FNPOC/GIDA — First Nations Principes OCAP, Global Indigenous Data Alliance, Standards CARE & Protocoles Gouvernance",
            country="Global",
            indigenous_data_extraction_commercialization_severity_score=28.0,
            biometric_genomic_collection_without_consent_scale_score=26.0,
            government_surveillance_indigenous_communities_score=25.0,
            ocap_fpic_data_governance_exclusion_gap_score=27.0,
            primary_pattern="ocap_fpic_data_governance_exclusion_gap",
        ),
        IndigenousDataSovereigntyEntity(
            entity_id="IDS-008",
            name="ONU/DRIP Données — DRIP Art.11-13 Données Culturelles, CBD Nagoya Ressources Génétiques & SDG 17 Partenariat Données",
            country="Global",
            indigenous_data_extraction_commercialization_severity_score=4.0,
            biometric_genomic_collection_without_consent_scale_score=4.0,
            government_surveillance_indigenous_communities_score=4.0,
            ocap_fpic_data_governance_exclusion_gap_score=4.0,
            primary_pattern="indigenous_data_extraction_commercialization_severity",
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

    return IndigenousDataSovereigntyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_data_sovereignty_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_indigenous_data_alliance_care_principles",
            "first_nations_ocap_principles_report",
            "un_drip_cultural_data_rights_framework",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_indigenous_data_sovereignty_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_indigenous_data_sovereignty_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
