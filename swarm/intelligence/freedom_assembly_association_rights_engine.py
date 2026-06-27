from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FreedomAssemblyAssociationRightsEntity:
    entity_id: str
    name: str
    country: str
    protest_crackdown_violence_severity_score: float
    union_suppression_labor_rights_scale_score: float
    civil_society_ngo_criminalization_score: float
    assembly_permit_restriction_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_freedom_assembly_association_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.protest_crackdown_violence_severity_score * 0.30
            + self.union_suppression_labor_rights_scale_score * 0.25
            + self.civil_society_ngo_criminalization_score * 0.25
            + self.assembly_permit_restriction_deficit_gap_score * 0.20,
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
        self.estimated_freedom_assembly_association_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class FreedomAssemblyAssociationRightsEngineResult:
    agent: str = "Freedom of Assembly Association Rights Engine Agent"
    domain: str = "freedom_assembly_association_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_freedom_assembly_association_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FreedomAssemblyAssociationRightsEntity] = field(default_factory=list)

def run_freedom_assembly_association_rights_engine() -> FreedomAssemblyAssociationRightsEngineResult:
    entities = [
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-001",
            name="Chine/Tiananmen Héritage — Hong Kong NSL 2019, Interdiction Totale Assemblée & Syndicats Contrôlés",
            country="Asie du Nord-Est",
            protest_crackdown_violence_severity_score=95.0,
            union_suppression_labor_rights_scale_score=92.0,
            civil_society_ngo_criminalization_score=94.0,
            assembly_permit_restriction_deficit_gap_score=96.0,
            primary_pattern="assembly_permit_restriction_deficit_gap",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-002",
            name="Biélorussie/Loukachenko 2020 — 35k Manifestants Arrêtés, Syndicats Interdits & ONG Liquidées",
            country="Europe de l'Est",
            protest_crackdown_violence_severity_score=92.0,
            union_suppression_labor_rights_scale_score=90.0,
            civil_society_ngo_criminalization_score=92.0,
            assembly_permit_restriction_deficit_gap_score=88.0,
            primary_pattern="protest_crackdown_violence_severity",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-003",
            name="Iran/Mahsa Amini — 500 Morts Manifestations 2022, Répression Syndicale & Criminalisation Société Civile",
            country="Moyen-Orient",
            protest_crackdown_violence_severity_score=90.0,
            union_suppression_labor_rights_scale_score=88.0,
            civil_society_ngo_criminalization_score=90.0,
            assembly_permit_restriction_deficit_gap_score=85.0,
            primary_pattern="civil_society_ngo_criminalization",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-004",
            name="Myanmar/Tatmadaw Coup — Syndicats Interdits, Manifestants Tués & Société Civile Clandestine",
            country="Asie du Sud-Est",
            protest_crackdown_violence_severity_score=88.0,
            union_suppression_labor_rights_scale_score=92.0,
            civil_society_ngo_criminalization_score=88.0,
            assembly_permit_restriction_deficit_gap_score=90.0,
            primary_pattern="union_suppression_labor_rights_scale",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-005",
            name="Russie/Anti-Guerre — 16k Manifestants Arrêtés 2022, Loi Discrédit Armée & ONG Agents Étrangers",
            country="Europe de l'Est",
            protest_crackdown_violence_severity_score=58.0,
            union_suppression_labor_rights_scale_score=52.0,
            civil_society_ngo_criminalization_score=62.0,
            assembly_permit_restriction_deficit_gap_score=55.0,
            primary_pattern="civil_society_ngo_criminalization",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-006",
            name="Thaïlande/Lèse-Majesté — Jeunesse Pro-Démocratie Arrêtée, Restriction Assemblée & Syndicats Limités",
            country="Asie du Sud-Est",
            protest_crackdown_violence_severity_score=48.0,
            union_suppression_labor_rights_scale_score=55.0,
            civil_society_ngo_criminalization_score=50.0,
            assembly_permit_restriction_deficit_gap_score=58.0,
            primary_pattern="assembly_permit_restriction_deficit_gap",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-007",
            name="CIVICUS/FIDH Monitor — Espace Civique Rétrécissant, Rapports Annuels Assemblée Pacifique",
            country="Global",
            protest_crackdown_violence_severity_score=24.0,
            union_suppression_labor_rights_scale_score=28.0,
            civil_society_ngo_criminalization_score=22.0,
            assembly_permit_restriction_deficit_gap_score=26.0,
            primary_pattern="union_suppression_labor_rights_scale",
        ),
        FreedomAssemblyAssociationRightsEntity(
            entity_id="FAAR-008",
            name="ONU/PIDCP Art.21-22 — Droit Réunion & Association, Rapporteur Spécial Libertés Fondamentales",
            country="Global",
            protest_crackdown_violence_severity_score=5.0,
            union_suppression_labor_rights_scale_score=6.0,
            civil_society_ngo_criminalization_score=4.0,
            assembly_permit_restriction_deficit_gap_score=8.0,
            primary_pattern="protest_crackdown_violence_severity",
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

    return FreedomAssemblyAssociationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_freedom_assembly_association_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "civicus_monitor_annual_report_civic_space_freedom_assembly_association",
            "un_special_rapporteur_rights_peaceful_assembly_freedom_association_reports",
            "amnesty_international_human_rights_watch_protest_crackdown_global_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_freedom_assembly_association_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_freedom_assembly_association_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
