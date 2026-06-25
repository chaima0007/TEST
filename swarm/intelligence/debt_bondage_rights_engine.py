from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DebtBondageRightsEntity:
    entity_id: str
    name: str
    country: str
    bonded_labor_debt_coercion_severity_score: float
    migrant_debt_recruitment_exploitation_scale_score: float
    legal_protection_debt_bondage_absence_score: float
    corporate_supply_chain_debt_bondage_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_debt_bondage_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.bonded_labor_debt_coercion_severity_score * 0.30
            + self.migrant_debt_recruitment_exploitation_scale_score * 0.25
            + self.legal_protection_debt_bondage_absence_score * 0.25
            + self.corporate_supply_chain_debt_bondage_gap_score * 0.20,
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
        self.estimated_debt_bondage_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class DebtBondageRightsEngineResult:
    agent: str = "Debt Bondage Rights Engine Agent"
    domain: str = "debt_bondage_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_debt_bondage_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DebtBondageRightsEntity] = field(default_factory=list)

def run_debt_bondage_rights_engine() -> DebtBondageRightsEngineResult:
    entities = [
        DebtBondageRightsEntity(
            entity_id="DBR-001",
            name="Inde/Pakistan — 9M Travailleurs Liés Dette Briqueteries/Agricoles, Castes & Héritage Dette Inter-Générationnel",
            country="Inde/Pakistan",
            bonded_labor_debt_coercion_severity_score=96.0,
            migrant_debt_recruitment_exploitation_scale_score=93.0,
            legal_protection_debt_bondage_absence_score=94.0,
            corporate_supply_chain_debt_bondage_gap_score=92.0,
            primary_pattern="bonded_labor_debt_coercion_severity",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-002",
            name="Qatar/GCC — Kafala Sponsorship Passeports Confisqués, 2M Travailleurs Migrants, Frais Recrutement Illégaux",
            country="Qatar/GCC",
            bonded_labor_debt_coercion_severity_score=93.0,
            migrant_debt_recruitment_exploitation_scale_score=91.0,
            legal_protection_debt_bondage_absence_score=90.0,
            corporate_supply_chain_debt_bondage_gap_score=89.0,
            primary_pattern="migrant_debt_recruitment_exploitation_scale",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-003",
            name="Cambodge/Asie SE — Servitude Domestique Dette Agences, Usines Vêtements & Migrants Thaïlande Piégés",
            country="Cambodge/Asie SE",
            bonded_labor_debt_coercion_severity_score=90.0,
            migrant_debt_recruitment_exploitation_scale_score=88.0,
            legal_protection_debt_bondage_absence_score=87.0,
            corporate_supply_chain_debt_bondage_gap_score=86.0,
            primary_pattern="migrant_debt_recruitment_exploitation_scale",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-004",
            name="Bolivie/Pérou — Enganche Communautés Autochtones, Zafra Canne à Sucre & Dette Company Store",
            country="Bolivie/Pérou",
            bonded_labor_debt_coercion_severity_score=87.0,
            migrant_debt_recruitment_exploitation_scale_score=85.0,
            legal_protection_debt_bondage_absence_score=84.0,
            corporate_supply_chain_debt_bondage_gap_score=83.0,
            primary_pattern="bonded_labor_debt_coercion_severity",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-005",
            name="Golfe Arabe — Employées Maison Asie/Afrique, Frais Migration Excessifs & Contrats Substitués à l'Arrivée",
            country="Golfe Arabe",
            bonded_labor_debt_coercion_severity_score=56.0,
            migrant_debt_recruitment_exploitation_scale_score=54.0,
            legal_protection_debt_bondage_absence_score=53.0,
            corporate_supply_chain_debt_bondage_gap_score=52.0,
            primary_pattern="migrant_debt_recruitment_exploitation_scale",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-006",
            name="UK/Europe — Travailleurs Roumains Bulgares Agriculture, Gangmasters & Hébergement-Dette Employeurs",
            country="UK/Europe",
            bonded_labor_debt_coercion_severity_score=53.0,
            migrant_debt_recruitment_exploitation_scale_score=51.0,
            legal_protection_debt_bondage_absence_score=50.0,
            corporate_supply_chain_debt_bondage_gap_score=49.0,
            primary_pattern="bonded_labor_debt_coercion_severity",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-007",
            name="IJM/Anti-Slavery Int'l — Libération Travailleurs Liés, Litiges Judiciaires & Formation Policière",
            country="Global",
            bonded_labor_debt_coercion_severity_score=27.0,
            migrant_debt_recruitment_exploitation_scale_score=26.0,
            legal_protection_debt_bondage_absence_score=25.0,
            corporate_supply_chain_debt_bondage_gap_score=26.0,
            primary_pattern="bonded_labor_debt_coercion_severity",
        ),
        DebtBondageRightsEntity(
            entity_id="DBR-008",
            name="OIT/Protocol P029 — Protocole Travail Forcé 2014, Indicateurs Dette & SDG 8.7 Fin Esclavage Moderne",
            country="Global",
            bonded_labor_debt_coercion_severity_score=4.0,
            migrant_debt_recruitment_exploitation_scale_score=4.0,
            legal_protection_debt_bondage_absence_score=5.0,
            corporate_supply_chain_debt_bondage_gap_score=4.0,
            primary_pattern="legal_protection_debt_bondage_absence",
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

    return DebtBondageRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_debt_bondage_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_estimates_modern_slavery_forced_labour_debt_bondage",
            "ilo_protocol_p029_forced_labour_convention_2014",
            "anti_slavery_international_bonded_labour_south_asia_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_debt_bondage_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_debt_bondage_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
