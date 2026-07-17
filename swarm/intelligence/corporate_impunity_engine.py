from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CorporateImpunityEntity:
    entity_id: str
    name: str
    country: str
    supply_chain_abuse_scale_score: float
    legal_jurisdiction_evasion_score: float
    environmental_social_harm_score: float
    accountability_remedy_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_corporate_impunity_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.supply_chain_abuse_scale_score * 0.30
            + self.legal_jurisdiction_evasion_score * 0.25
            + self.environmental_social_harm_score * 0.25
            + self.accountability_remedy_gap_score * 0.20,
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
        self.estimated_corporate_impunity_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CorporateImpunityEngineResult:
    agent: str = "Corporate Impunity Engine Agent"
    domain: str = "corporate_impunity"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_corporate_impunity_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CorporateImpunityEntity] = field(default_factory=list)

def run_corporate_impunity_engine() -> CorporateImpunityEngineResult:
    entities = [
        CorporateImpunityEntity(
            entity_id="CI-001",
            name="Extractives/Congo — Cobalt Apple/Tesla, Travail Enfants Mines & Chaînes Sans Traçabilité",
            country="Afrique Centrale",
            supply_chain_abuse_scale_score=95.0,
            legal_jurisdiction_evasion_score=88.0,
            environmental_social_harm_score=92.0,
            accountability_remedy_gap_score=92.0,
            primary_pattern="supply_chain_abuse_scale",
        ),
        CorporateImpunityEntity(
            entity_id="CI-002",
            name="Fast Fashion/Bangladesh — Rana Plaza 1134 Morts, Marques Non Poursuivies & Due Diligence Absente",
            country="Asie du Sud",
            supply_chain_abuse_scale_score=92.0,
            legal_jurisdiction_evasion_score=90.0,
            environmental_social_harm_score=85.0,
            accountability_remedy_gap_score=88.0,
            primary_pattern="accountability_remedy_gap",
        ),
        CorporateImpunityEntity(
            entity_id="CI-003",
            name="Big Oil/Nigeria — Shell Delta Ogoni, Marée Noires 50 Ans & Procès Hors Territoire",
            country="Afrique de l'Ouest",
            supply_chain_abuse_scale_score=88.0,
            legal_jurisdiction_evasion_score=85.0,
            environmental_social_harm_score=92.0,
            accountability_remedy_gap_score=85.0,
            primary_pattern="environmental_social_harm",
        ),
        CorporateImpunityEntity(
            entity_id="CI-004",
            name="Tech/Surveillance — NSO/Palantir Ventes Régimes, Export Contrôle Insuffisant & Complicité",
            country="Global",
            supply_chain_abuse_scale_score=82.0,
            legal_jurisdiction_evasion_score=88.0,
            environmental_social_harm_score=78.0,
            accountability_remedy_gap_score=85.0,
            primary_pattern="legal_jurisdiction_evasion",
        ),
        CorporateImpunityEntity(
            entity_id="CI-005",
            name="Agro-Industrie/Brésil — Déforestation Amazonie, Expulsions Peuples Indigènes & Soja/Élevage",
            country="Amérique Latine",
            supply_chain_abuse_scale_score=55.0,
            legal_jurisdiction_evasion_score=52.0,
            environmental_social_harm_score=58.0,
            accountability_remedy_gap_score=50.0,
            primary_pattern="environmental_social_harm",
        ),
        CorporateImpunityEntity(
            entity_id="CI-006",
            name="Finance/Paradis Fiscaux — Évasion Multinationales, Ressources États Appauvries & OCDE Lacunes",
            country="Global",
            supply_chain_abuse_scale_score=48.0,
            legal_jurisdiction_evasion_score=58.0,
            environmental_social_harm_score=45.0,
            accountability_remedy_gap_score=52.0,
            primary_pattern="legal_jurisdiction_evasion",
        ),
        CorporateImpunityEntity(
            entity_id="CI-007",
            name="OCCRP/Global Witness — Journalisme Enquête Corruption Corporate & Plaidoyer Due Diligence",
            country="Global",
            supply_chain_abuse_scale_score=22.0,
            legal_jurisdiction_evasion_score=28.0,
            environmental_social_harm_score=25.0,
            accountability_remedy_gap_score=30.0,
            primary_pattern="supply_chain_abuse_scale",
        ),
        CorporateImpunityEntity(
            entity_id="CI-008",
            name="ONU/Principes Directeurs Ruggie — Cadre Entreprises & Droits Humains 2011, Traité Négocié",
            country="Global",
            supply_chain_abuse_scale_score=4.0,
            legal_jurisdiction_evasion_score=5.0,
            environmental_social_harm_score=3.0,
            accountability_remedy_gap_score=6.0,
            primary_pattern="accountability_remedy_gap",
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

    return CorporateImpunityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_corporate_impunity_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "business_human_rights_resource_centre_corporate_abuse_tracker",
            "global_witness_corporate_accountability_annual_investigation_report",
            "un_working_group_business_human_rights_state_reports_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_corporate_impunity_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_corporate_impunity_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
