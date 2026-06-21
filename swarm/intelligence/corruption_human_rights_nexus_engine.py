from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CorruptionHumanRightsNexusEntity:
    entity_id: str
    name: str
    country: str
    judicial_corruption_impunity_score: float
    police_corruption_rights_violations_score: float
    state_capture_oligarchy_rights_score: float
    anticorruption_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_corruption_human_rights_nexus_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.judicial_corruption_impunity_score * 0.30
            + self.police_corruption_rights_violations_score * 0.25
            + self.state_capture_oligarchy_rights_score * 0.25
            + self.anticorruption_accountability_gap_score * 0.20,
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
        self.estimated_corruption_human_rights_nexus_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CorruptionHumanRightsNexusEngineResult:
    agent: str = "Corruption Human Rights Nexus Engine Agent"
    domain: str = "corruption_human_rights_nexus"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_corruption_human_rights_nexus_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CorruptionHumanRightsNexusEntity] = field(default_factory=list)

def run_corruption_human_rights_nexus_engine() -> CorruptionHumanRightsNexusEngineResult:
    entities = [
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-001",
            name="Venezuela — État mafieux, corruption judiciaire totale & opposition emprisonnée par régime Maduro",
            country="Amérique du Sud",
            judicial_corruption_impunity_score=95.0,
            police_corruption_rights_violations_score=92.0,
            state_capture_oligarchy_rights_score=94.0,
            anticorruption_accountability_gap_score=93.0,
            primary_pattern="judicial_corruption_impunity",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-002",
            name="Syrie — corruption armée systémique, droits humains inexistants sous régimes corrompus Assad/factions",
            country="Moyen-Orient",
            judicial_corruption_impunity_score=93.0,
            police_corruption_rights_violations_score=91.0,
            state_capture_oligarchy_rights_score=92.0,
            anticorruption_accountability_gap_score=90.0,
            primary_pattern="state_capture_oligarchy_rights",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-003",
            name="Somalie — corruption État-milices, fonds humanitaires détournés, impunité totale AL-Shabaab",
            country="Afrique de l'Est",
            judicial_corruption_impunity_score=90.0,
            police_corruption_rights_violations_score=88.0,
            state_capture_oligarchy_rights_score=87.0,
            anticorruption_accountability_gap_score=89.0,
            primary_pattern="anticorruption_accountability_gap",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-004",
            name="Érythrée — État-prison, aucune transparence, droits inexistants, service militaire indéfini",
            country="Afrique de l'Est",
            judicial_corruption_impunity_score=88.0,
            police_corruption_rights_violations_score=87.0,
            state_capture_oligarchy_rights_score=90.0,
            anticorruption_accountability_gap_score=91.0,
            primary_pattern="state_capture_oligarchy_rights",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-005",
            name="Nigeria — police SARS corruption torture documentée, impunité systémique #EndSARS ignoré",
            country="Afrique de l'Ouest",
            judicial_corruption_impunity_score=50.0,
            police_corruption_rights_violations_score=58.0,
            state_capture_oligarchy_rights_score=45.0,
            anticorruption_accountability_gap_score=52.0,
            primary_pattern="police_corruption_rights_violations",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-006",
            name="Russie — État oligarchique, corruption judiciaire systémique, opposition éliminée par poison/prison",
            country="Europe de l'Est",
            judicial_corruption_impunity_score=55.0,
            police_corruption_rights_violations_score=48.0,
            state_capture_oligarchy_rights_score=58.0,
            anticorruption_accountability_gap_score=52.0,
            primary_pattern="state_capture_oligarchy_rights",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-007",
            name="Brésil — corruption policière documentée, améliorations partielles post-Lula, CGU actif",
            country="Amérique du Sud",
            judicial_corruption_impunity_score=32.0,
            police_corruption_rights_violations_score=38.0,
            state_capture_oligarchy_rights_score=28.0,
            anticorruption_accountability_gap_score=35.0,
            primary_pattern="police_corruption_rights_violations",
        ),
        CorruptionHumanRightsNexusEntity(
            entity_id="CHN-008",
            name="Danemark — indice corruption le plus bas mondial, protections solides, ombudsman indépendant",
            country="Europe du Nord",
            judicial_corruption_impunity_score=4.0,
            police_corruption_rights_violations_score=5.0,
            state_capture_oligarchy_rights_score=4.0,
            anticorruption_accountability_gap_score=3.0,
            primary_pattern="anticorruption_accountability_gap",
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

    return CorruptionHumanRightsNexusEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_corruption_human_rights_nexus_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "transparency_international_cpi_2023",
            "human_rights_watch_corruption_impunity_2023",
            "global_integrity_report_2023",
            "unodc_corruption_human_rights_nexus_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_corruption_human_rights_nexus_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_corruption_human_rights_nexus_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
