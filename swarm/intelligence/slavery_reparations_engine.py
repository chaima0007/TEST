from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SlaveryReparationsEntity:
    entity_id: str
    name: str
    country: str
    historical_atrocity_scale_score: float
    intergenerational_harm_persistence_score: float
    restitution_refusal_entrenchment_score: float
    institutional_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_slavery_reparations_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.historical_atrocity_scale_score * 0.30
            + self.intergenerational_harm_persistence_score * 0.25
            + self.restitution_refusal_entrenchment_score * 0.25
            + self.institutional_accountability_gap_score * 0.20,
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
        self.estimated_slavery_reparations_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SlaveryReparationsEngineResult:
    agent: str = "Slavery Reparations Engine Agent"
    domain: str = "slavery_reparations"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_slavery_reparations_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SlaveryReparationsEntity] = field(default_factory=list)

def run_slavery_reparations_engine() -> SlaveryReparationsEngineResult:
    entities = [
        SlaveryReparationsEntity(
            entity_id="SR-001",
            name="USA — 246 Ans Esclavage, 4M Afro-Américains, HR40 Bloqué 35 Ans & Écart Richesse 10:1",
            country="Amérique du Nord",
            historical_atrocity_scale_score=95.0,
            intergenerational_harm_persistence_score=95.0,
            restitution_refusal_entrenchment_score=92.0,
            institutional_accountability_gap_score=90.0,
            primary_pattern="restitution_refusal_entrenchment",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-002",
            name="UK/Caraïbes — CARICOM 14 Nations, £20M Indemnités Propriétaires 1833 & Zéro Réparation Descendants",
            country="Caraïbes",
            historical_atrocity_scale_score=92.0,
            intergenerational_harm_persistence_score=90.0,
            restitution_refusal_entrenchment_score=92.0,
            institutional_accountability_gap_score=88.0,
            primary_pattern="restitution_refusal_entrenchment",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-003",
            name="France/Haïti — Dette Odieuse 90M Francs 1825, 21 Milliards USD Modernes & Appauvrissement Durable",
            country="Caraïbes",
            historical_atrocity_scale_score=90.0,
            intergenerational_harm_persistence_score=88.0,
            restitution_refusal_entrenchment_score=88.0,
            institutional_accountability_gap_score=88.0,
            primary_pattern="historical_atrocity_scale",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-004",
            name="Brésil — 3.8M Esclaves Africains, 13 Mai 1888 Tardif, Inégalités Raciales Structurelles & Refus Etat",
            country="Amérique Latine",
            historical_atrocity_scale_score=88.0,
            intergenerational_harm_persistence_score=85.0,
            restitution_refusal_entrenchment_score=85.0,
            institutional_accountability_gap_score=82.0,
            primary_pattern="intergenerational_harm_persistence",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-005",
            name="Portugal — Premier Négrier Européen, 5.8M Africains Déportés & Aucun Mécanisme Réparation",
            country="Europe",
            historical_atrocity_scale_score=55.0,
            intergenerational_harm_persistence_score=52.0,
            restitution_refusal_entrenchment_score=55.0,
            institutional_accountability_gap_score=52.0,
            primary_pattern="institutional_accountability_gap",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-006",
            name="Pays-Bas — NiNsee Fermé 2012, Excuses 2022 Sans Réparation & WIC Commerce Triangle",
            country="Europe",
            historical_atrocity_scale_score=50.0,
            intergenerational_harm_persistence_score=48.0,
            restitution_refusal_entrenchment_score=52.0,
            institutional_accountability_gap_score=48.0,
            primary_pattern="restitution_refusal_entrenchment",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-007",
            name="CARICOM/Commission Réparations — Plan 10 Points, Dialogue Diplomatique & Standards Réparatoires",
            country="Global",
            historical_atrocity_scale_score=22.0,
            intergenerational_harm_persistence_score=28.0,
            restitution_refusal_entrenchment_score=25.0,
            institutional_accountability_gap_score=30.0,
            primary_pattern="institutional_accountability_gap",
        ),
        SlaveryReparationsEntity(
            entity_id="SR-008",
            name="ONU/DDPA — Durban 2001, Reconnaissance Esclavage Crime Humanité & Cadre Réparatoire International",
            country="Global",
            historical_atrocity_scale_score=4.0,
            intergenerational_harm_persistence_score=5.0,
            restitution_refusal_entrenchment_score=3.0,
            institutional_accountability_gap_score=6.0,
            primary_pattern="institutional_accountability_gap",
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

    return SlaveryReparationsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_slavery_reparations_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "caricom_reparations_commission_ten_point_plan_report",
            "un_durban_declaration_programme_action_slavery_heritage",
            "thomas_craemer_slavery_reparations_economic_quantification_study",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_slavery_reparations_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_slavery_reparations_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
