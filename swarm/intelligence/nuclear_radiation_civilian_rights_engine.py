from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NuclearRadiationCivilianRightsEntity:
    entity_id: str
    name: str
    country: str
    nuclear_testing_civilian_contamination_severity_score: float
    reactor_accident_compensation_denial_scale_score: float
    nuclear_waste_indigenous_land_disposal_score: float
    radiation_information_transparency_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nuclear_radiation_civilian_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.nuclear_testing_civilian_contamination_severity_score * 0.30
            + self.reactor_accident_compensation_denial_scale_score * 0.25
            + self.nuclear_waste_indigenous_land_disposal_score * 0.25
            + self.radiation_information_transparency_deficit_gap_score * 0.20,
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
        self.estimated_nuclear_radiation_civilian_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class NuclearRadiationCivilianRightsEngineResult:
    agent: str = "Nuclear Radiation Civilian Rights Engine Agent"
    domain: str = "nuclear_radiation_civilian_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_nuclear_radiation_civilian_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NuclearRadiationCivilianRightsEntity] = field(default_factory=list)


def run_nuclear_radiation_civilian_rights_engine() -> NuclearRadiationCivilianRightsEngineResult:
    entities = [
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-001",
            name="France/Polynésie — 193 Essais Nucléaires Polynésie, Vétérans Irradiés Non Indemnisés, Cancers Cachés & Dépollution Refusée",
            country="France/Polynésie",
            nuclear_testing_civilian_contamination_severity_score=95.0,
            reactor_accident_compensation_denial_scale_score=93.0,
            nuclear_waste_indigenous_land_disposal_score=93.0,
            radiation_information_transparency_deficit_gap_score=91.0,
            primary_pattern="nuclear_testing_civilian_contamination_severity",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-002",
            name="USA/Marshall Islands — Bikini Atoll 67 Tests, Populations Déplacées Non Retournables, Castle Bravo & Fonds Compensation Épuisé",
            country="USA/Marshall Islands",
            nuclear_testing_civilian_contamination_severity_score=92.0,
            reactor_accident_compensation_denial_scale_score=90.0,
            nuclear_waste_indigenous_land_disposal_score=90.0,
            radiation_information_transparency_deficit_gap_score=88.0,
            primary_pattern="nuclear_waste_indigenous_land_disposal",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-003",
            name="URSS/Kazakhstan — Semipalatinsk 456 Essais, 1.5M Exposés, Maladies Génération & Dépollution Insuffisante Post-URSS",
            country="Kazakhstan",
            nuclear_testing_civilian_contamination_severity_score=89.0,
            reactor_accident_compensation_denial_scale_score=87.0,
            nuclear_waste_indigenous_land_disposal_score=87.0,
            radiation_information_transparency_deficit_gap_score=85.0,
            primary_pattern="nuclear_testing_civilian_contamination_severity",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-004",
            name="Japon/Fukushima — Évacuations Forcées 154 000, Compensation Tepco Insuffisante, Eaux Traitées Pacifique & Zones Exclusion",
            country="Japon",
            nuclear_testing_civilian_contamination_severity_score=86.0,
            reactor_accident_compensation_denial_scale_score=84.0,
            nuclear_waste_indigenous_land_disposal_score=84.0,
            radiation_information_transparency_deficit_gap_score=82.0,
            primary_pattern="reactor_accident_compensation_denial_scale",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-005",
            name="Inde/Pakistan — Tests Pokhran/Chagai Sans TICE, Mines Uranium Travailleurs Exposés, Prolifération & Sans Traité Interdiction",
            country="Inde/Pakistan",
            nuclear_testing_civilian_contamination_severity_score=57.0,
            reactor_accident_compensation_denial_scale_score=55.0,
            nuclear_waste_indigenous_land_disposal_score=55.0,
            radiation_information_transparency_deficit_gap_score=53.0,
            primary_pattern="radiation_information_transparency_deficit_gap",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-006",
            name="Australie — Essais Maralinga Aborigènes Exposés, Décontamination Incomplète, Veterans Irradiés & Uranium Mines Kakadu",
            country="Australie",
            nuclear_testing_civilian_contamination_severity_score=54.0,
            reactor_accident_compensation_denial_scale_score=52.0,
            nuclear_waste_indigenous_land_disposal_score=52.0,
            radiation_information_transparency_deficit_gap_score=50.0,
            primary_pattern="nuclear_waste_indigenous_land_disposal",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-007",
            name="AIEA/IPPNW — Normes Radioprotection, Médecins Prevention Guerre Nucléaire & Traité Interdiction Armes Nucléaires 2017",
            country="Global",
            nuclear_testing_civilian_contamination_severity_score=27.0,
            reactor_accident_compensation_denial_scale_score=26.0,
            nuclear_waste_indigenous_land_disposal_score=26.0,
            radiation_information_transparency_deficit_gap_score=25.0,
            primary_pattern="nuclear_testing_civilian_contamination_severity",
        ),
        NuclearRadiationCivilianRightsEntity(
            entity_id="NRC-008",
            name="ONU/TNP — Traité Non-Prolifération, TICE Moratoire, Article VI Désarmement & SDG 16 Paix Justice",
            country="Global",
            nuclear_testing_civilian_contamination_severity_score=5.0,
            reactor_accident_compensation_denial_scale_score=4.0,
            nuclear_waste_indigenous_land_disposal_score=4.0,
            radiation_information_transparency_deficit_gap_score=4.0,
            primary_pattern="radiation_information_transparency_deficit_gap",
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

    return NuclearRadiationCivilianRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_nuclear_radiation_civilian_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "greenpeace_nuclear_testing_contamination_report",
            "ippnw_nuclear_weapons_humanitarian_impact_study",
            "iaea_radiation_protection_standards_review",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_nuclear_radiation_civilian_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_nuclear_radiation_civilian_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
