from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class BusinessHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    supply_chain_abuse_scale_score: float
    corporate_impunity_score: float
    remedy_access_denial_score: float
    regulatory_framework_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_business_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.supply_chain_abuse_scale_score * 0.30
            + self.corporate_impunity_score * 0.25
            + self.remedy_access_denial_score * 0.25
            + self.regulatory_framework_gap_score * 0.20,
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
        self.estimated_business_human_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class BusinessHumanRightsEngineResult:
    agent: str = "Business Human Rights Engine Agent"
    domain: str = "business_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_business_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BusinessHumanRightsEntity] = field(default_factory=list)

def run_business_human_rights_engine() -> BusinessHumanRightsEngineResult:
    entities = [
        BusinessHumanRightsEntity(
            entity_id="BHR-001",
            name="Fast Fashion/Rana Plaza — H&M/Zara/Primark, Travail Forcé Bangladesh & Impunité Totale",
            country="Global/Asie du Sud",
            supply_chain_abuse_scale_score=92.0,
            corporate_impunity_score=88.0,
            remedy_access_denial_score=90.0,
            regulatory_framework_gap_score=85.0,
            primary_pattern="supply_chain_abuse_scale",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-002",
            name="Tech/Minerais — Apple/Tesla/Samsung, Cobalt Enfants Congo & Chaînes Approvisionnement Opaques",
            country="Global/Afrique",
            supply_chain_abuse_scale_score=88.0,
            corporate_impunity_score=90.0,
            remedy_access_denial_score=85.0,
            regulatory_framework_gap_score=82.0,
            primary_pattern="corporate_impunity",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-003",
            name="Agro-industrie/Palmier à Huile — Déforestation, Expulsion Peuples Indigènes & Travail Servile",
            country="Asie du Sud-Est/Amérique Latine",
            supply_chain_abuse_scale_score=85.0,
            corporate_impunity_score=82.0,
            remedy_access_denial_score=88.0,
            regulatory_framework_gap_score=80.0,
            primary_pattern="remedy_access_denial",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-004",
            name="Pétrole/Gaz — Shell Niger Delta, TotalEnergies Ouganda EACOP & Pollution Sans Réparation",
            country="Afrique Sub-Saharienne",
            supply_chain_abuse_scale_score=80.0,
            corporate_impunity_score=85.0,
            remedy_access_denial_score=82.0,
            regulatory_framework_gap_score=78.0,
            primary_pattern="corporate_impunity",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-005",
            name="UE — Directive Devoir de Vigilance (CSDDD), Loi Française Vigilance & Application Partielle",
            country="Europe",
            supply_chain_abuse_scale_score=52.0,
            corporate_impunity_score=55.0,
            remedy_access_denial_score=58.0,
            regulatory_framework_gap_score=50.0,
            primary_pattern="regulatory_framework_gap",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-006",
            name="USA — Uyghur Forced Labor Prevention Act, FCPA & Lacunes Juridictionnelles Extraterritoriales",
            country="Amérique du Nord",
            supply_chain_abuse_scale_score=48.0,
            corporate_impunity_score=52.0,
            remedy_access_denial_score=55.0,
            regulatory_framework_gap_score=50.0,
            primary_pattern="regulatory_framework_gap",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-007",
            name="ONU — Principes Directeurs Ruggie, Traité Contraignant Entreprises & Droits Humains",
            country="Global",
            supply_chain_abuse_scale_score=22.0,
            corporate_impunity_score=28.0,
            remedy_access_denial_score=30.0,
            regulatory_framework_gap_score=25.0,
            primary_pattern="supply_chain_abuse_scale",
        ),
        BusinessHumanRightsEntity(
            entity_id="BHR-008",
            name="OIT/OCDE — Conventions Travail, Principes Directeurs Multinationales & Mécanismes PCN",
            country="Global",
            supply_chain_abuse_scale_score=4.0,
            corporate_impunity_score=5.0,
            remedy_access_denial_score=3.0,
            regulatory_framework_gap_score=6.0,
            primary_pattern="remedy_access_denial",
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

    return BusinessHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_business_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "business_human_rights_resource_centre_corporate_accountability_database",
            "un_working_group_business_human_rights_annual_report",
            "oecd_guidelines_multinational_enterprises_due_diligence_guidance",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_business_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_business_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
