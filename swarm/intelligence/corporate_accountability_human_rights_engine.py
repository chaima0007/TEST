from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CorporateAccountabilityHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    supply_chain_forced_labor_complicity_severity_score: float
    environmental_destruction_community_displacement_scale_score: float
    corporate_impunity_legal_accountability_gap_score: float
    human_rights_due_diligence_failure_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_corporate_accountability_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.supply_chain_forced_labor_complicity_severity_score * 0.30
            + self.environmental_destruction_community_displacement_scale_score * 0.25
            + self.corporate_impunity_legal_accountability_gap_score * 0.25
            + self.human_rights_due_diligence_failure_deficit_gap_score * 0.20,
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
        self.estimated_corporate_accountability_human_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CorporateAccountabilityHumanRightsEngineResult:
    agent: str = "Corporate Accountability Human Rights Engine Agent"
    domain: str = "corporate_accountability_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_corporate_accountability_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CorporateAccountabilityHumanRightsEntity] = field(default_factory=list)

def run_corporate_accountability_human_rights_engine() -> CorporateAccountabilityHumanRightsEngineResult:
    entities = [
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-001",
            name="Shell/Nigeria — Delta Niger Pollution 50 Ans, Ogoni 9 Pendus 1995, Droits Eau Détruits & Aucune Réparation Judiciaire",
            country="Nigeria",
            supply_chain_forced_labor_complicity_severity_score=95.0,
            environmental_destruction_community_displacement_scale_score=96.0,
            corporate_impunity_legal_accountability_gap_score=93.0,
            human_rights_due_diligence_failure_deficit_gap_score=94.0,
            primary_pattern="environmental_destruction_community_displacement_scale",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-002",
            name="Apple/Foxconn — Suicides Ouvriers Chine 2010, Filets Anti-Suicide, Travail Enfant Cobalt RDC & Conditions 12h/Jour",
            country="Chine",
            supply_chain_forced_labor_complicity_severity_score=92.0,
            environmental_destruction_community_displacement_scale_score=90.0,
            corporate_impunity_legal_accountability_gap_score=93.0,
            human_rights_due_diligence_failure_deficit_gap_score=89.0,
            primary_pattern="supply_chain_forced_labor_complicity_severity",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-003",
            name="Nestlé/Cacao — Travail Enfant Côte d'Ivoire 1.5M, Cacao Certifié Mensonger, Poursuites USA Rejetées & Chaîne Opaque",
            country="Côte d'Ivoire",
            supply_chain_forced_labor_complicity_severity_score=88.0,
            environmental_destruction_community_displacement_scale_score=87.0,
            corporate_impunity_legal_accountability_gap_score=89.0,
            human_rights_due_diligence_failure_deficit_gap_score=86.0,
            primary_pattern="corporate_impunity_legal_accountability_gap",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-004",
            name="BP/Deepwater — Marée Noire 2010 Golfe Mexique, Pêcheurs Ruinés, Compensations Insuffisantes & Lobbying Déréglementation",
            country="USA",
            supply_chain_forced_labor_complicity_severity_score=84.0,
            environmental_destruction_community_displacement_scale_score=85.0,
            corporate_impunity_legal_accountability_gap_score=82.0,
            human_rights_due_diligence_failure_deficit_gap_score=83.0,
            primary_pattern="environmental_destruction_community_displacement_scale",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-005",
            name="Amazon/Entrepôts — Blessures 2× Industrie, Surveillance Algorithmes, Syndicalistes Licenciés & Conditions Chaleur Létale",
            country="USA",
            supply_chain_forced_labor_complicity_severity_score=56.0,
            environmental_destruction_community_displacement_scale_score=54.0,
            corporate_impunity_legal_accountability_gap_score=55.0,
            human_rights_due_diligence_failure_deficit_gap_score=57.0,
            primary_pattern="human_rights_due_diligence_failure_deficit_gap",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-006",
            name="Volkswagen/Dieselgate — Émissions Frauduleuses, Santé Communautés Autoroutes, Amendes Sans Prison & Victimes Non Indemnisées",
            country="Allemagne",
            supply_chain_forced_labor_complicity_severity_score=53.0,
            environmental_destruction_community_displacement_scale_score=51.0,
            corporate_impunity_legal_accountability_gap_score=54.0,
            human_rights_due_diligence_failure_deficit_gap_score=52.0,
            primary_pattern="corporate_impunity_legal_accountability_gap",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-007",
            name="UNGP/OCDE — Principes Directeurs ONU Entreprises Droits Humains, Lignes OCDE, Devoir Vigilance France & CSDDD EU",
            country="Global",
            supply_chain_forced_labor_complicity_severity_score=27.0,
            environmental_destruction_community_displacement_scale_score=26.0,
            corporate_impunity_legal_accountability_gap_score=28.0,
            human_rights_due_diligence_failure_deficit_gap_score=25.0,
            primary_pattern="human_rights_due_diligence_failure_deficit_gap",
        ),
        CorporateAccountabilityHumanRightsEntity(
            entity_id="CAH-008",
            name="ISO/GRI — ISO 26000 RSE, GRI Standards Rapportage, B-Corp Certification & Initiative Reporting Mondial",
            country="Global",
            supply_chain_forced_labor_complicity_severity_score=4.0,
            environmental_destruction_community_displacement_scale_score=4.0,
            corporate_impunity_legal_accountability_gap_score=4.0,
            human_rights_due_diligence_failure_deficit_gap_score=4.0,
            primary_pattern="supply_chain_forced_labor_complicity_severity",
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

    return CorporateAccountabilityHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_corporate_accountability_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_guiding_principles_business_human_rights",
            "corporate_accountability_lab_supply_chain_report",
            "amnesty_international_corporate_complicity_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_corporate_accountability_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_corporate_accountability_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
