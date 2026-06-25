from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AccessMedicineInequalityEntity:
    entity_id: str
    name: str
    country: str
    patent_barrier_essential_medicine_scale_score: float
    price_exclusion_low_income_severity_score: float
    generic_drug_access_suppression_score: float
    research_development_neglect_diseases_poor_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_access_medicine_inequality_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.patent_barrier_essential_medicine_scale_score * 0.30
            + self.price_exclusion_low_income_severity_score * 0.25
            + self.generic_drug_access_suppression_score * 0.25
            + self.research_development_neglect_diseases_poor_score * 0.20,
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
        self.estimated_access_medicine_inequality_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AccessMedicineInequalityEngineResult:
    agent: str = "Access Medicine Inequality Engine Agent"
    domain: str = "access_medicine_inequality"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_access_medicine_inequality_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AccessMedicineInequalityEntity] = field(default_factory=list)

def run_access_medicine_inequality_engine() -> AccessMedicineInequalityEngineResult:
    entities = [
        AccessMedicineInequalityEntity(
            entity_id="AMI-001",
            name="Afrique Sub-Saharienne — 50% Sans Médicaments OMS, Brevets ARV/TB Bloqués & Paludisme Non Traité",
            country="Afrique",
            patent_barrier_essential_medicine_scale_score=92.0,
            price_exclusion_low_income_severity_score=95.0,
            generic_drug_access_suppression_score=92.0,
            research_development_neglect_diseases_poor_score=92.0,
            primary_pattern="patent_barrier_essential_medicine_scale",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-002",
            name="USA — Insuline 900$/Mois vs 98$ Canada, Evergreening Brevets & 30M Sans Couverture",
            country="Amérique du Nord",
            patent_barrier_essential_medicine_scale_score=88.0,
            price_exclusion_low_income_severity_score=95.0,
            generic_drug_access_suppression_score=90.0,
            research_development_neglect_diseases_poor_score=85.0,
            primary_pattern="price_exclusion_low_income_severity",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-003",
            name="Inde — TRIPS-Plus Lobbying, Section 3d Contournée & Leishmaniose/Chagas Négligés 1Md Exposés",
            country="Asie du Sud",
            patent_barrier_essential_medicine_scale_score=90.0,
            price_exclusion_low_income_severity_score=85.0,
            generic_drug_access_suppression_score=92.0,
            research_development_neglect_diseases_poor_score=88.0,
            primary_pattern="generic_drug_access_suppression",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-004",
            name="Afrique Francophone/UEMOA — Doha Non Implémenté, Zéro Capacité Génériques & Dépendance Totale",
            country="Afrique de l'Ouest",
            patent_barrier_essential_medicine_scale_score=88.0,
            price_exclusion_low_income_severity_score=92.0,
            generic_drug_access_suppression_score=88.0,
            research_development_neglect_diseases_poor_score=85.0,
            primary_pattern="research_development_neglect_diseases_poor",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-005",
            name="Europe de l'Est — Médicaments Cancer Hors Portée, Roumanie/Bulgarie 40% Accès Restreint",
            country="Europe de l'Est",
            patent_barrier_essential_medicine_scale_score=50.0,
            price_exclusion_low_income_severity_score=55.0,
            generic_drug_access_suppression_score=52.0,
            research_development_neglect_diseases_poor_score=52.0,
            primary_pattern="price_exclusion_low_income_severity",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-006",
            name="Amérique Latine/APC-USA — Accords TRIPS-Plus Guatemala/Colombie, Brevets Cancer Inaccessibles",
            country="Amérique Latine",
            patent_barrier_essential_medicine_scale_score=50.0,
            price_exclusion_low_income_severity_score=52.0,
            generic_drug_access_suppression_score=55.0,
            research_development_neglect_diseases_poor_score=48.0,
            primary_pattern="patent_barrier_essential_medicine_scale",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-007",
            name="MSF/DNDi/Campagne Accès — Licences Obligatoires, Push Génériques & Médicaments Maladies Oubliées",
            country="Global",
            patent_barrier_essential_medicine_scale_score=22.0,
            price_exclusion_low_income_severity_score=28.0,
            generic_drug_access_suppression_score=25.0,
            research_development_neglect_diseases_poor_score=30.0,
            primary_pattern="generic_drug_access_suppression",
        ),
        AccessMedicineInequalityEntity(
            entity_id="AMI-008",
            name="OMS/ONU — Liste Médicaments Essentiels, Résolution TRIPS Doha 2001 & SDG 3.8 Couverture",
            country="Global",
            patent_barrier_essential_medicine_scale_score=4.0,
            price_exclusion_low_income_severity_score=5.0,
            generic_drug_access_suppression_score=3.0,
            research_development_neglect_diseases_poor_score=6.0,
            primary_pattern="research_development_neglect_diseases_poor",
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

    return AccessMedicineInequalityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_access_medicine_inequality_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "msf_access_campaign_essential_medicines_patent_barrier_report",
            "who_essential_medicines_list_trips_doha_declaration_review",
            "dndi_drugs_neglected_diseases_initiative_global_access_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_access_medicine_inequality_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_access_medicine_inequality_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
