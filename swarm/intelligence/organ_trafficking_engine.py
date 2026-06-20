from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class OrganTraffickingEntity:
    entity_id: str
    name: str
    country: str
    forced_organ_extraction_scale_score: float
    transplant_tourism_infrastructure_score: float
    donor_coercion_vulnerability_score: float
    prosecution_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_organ_trafficking_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_organ_extraction_scale_score * 0.30
            + self.transplant_tourism_infrastructure_score * 0.25
            + self.donor_coercion_vulnerability_score * 0.25
            + self.prosecution_accountability_gap_score * 0.20,
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
        self.estimated_organ_trafficking_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class OrganTraffickingEngineResult:
    agent: str = "Organ Trafficking Engine Agent"
    domain: str = "organ_trafficking"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.82
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_organ_trafficking_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OrganTraffickingEntity] = field(default_factory=list)

def run_organ_trafficking_engine() -> OrganTraffickingEngineResult:
    entities = [
        OrganTraffickingEntity(
            entity_id="OT-001",
            name="Chine — Prélèvements Forcés Prisonniers Conscience, Falun Gong/Ouïghours & Industrie Transplants",
            country="Asie du Nord-Est",
            forced_organ_extraction_scale_score=95.0,
            transplant_tourism_infrastructure_score=92.0,
            donor_coercion_vulnerability_score=90.0,
            prosecution_accountability_gap_score=92.0,
            primary_pattern="forced_organ_extraction_scale",
        ),
        OrganTraffickingEntity(
            entity_id="OT-002",
            name="Pakistan — Marché Reins Ruraux Pauvres, Chirurgiens Complices & Trafic Migratoire Lié",
            country="Asie du Sud",
            forced_organ_extraction_scale_score=82.0,
            transplant_tourism_infrastructure_score=85.0,
            donor_coercion_vulnerability_score=88.0,
            prosecution_accountability_gap_score=80.0,
            primary_pattern="donor_coercion_vulnerability",
        ),
        OrganTraffickingEntity(
            entity_id="OT-003",
            name="Égypte/Afrique du Nord — Réfugiés Soudanais/Érythréens Vendant Organes & Cliniques Clandestines",
            country="Afrique du Nord",
            forced_organ_extraction_scale_score=80.0,
            transplant_tourism_infrastructure_score=78.0,
            donor_coercion_vulnerability_score=85.0,
            prosecution_accountability_gap_score=82.0,
            primary_pattern="donor_coercion_vulnerability",
        ),
        OrganTraffickingEntity(
            entity_id="OT-004",
            name="Kosovo/Balkans — Affaire Medicus, Prisonniers Serbes Organes Volés & Impunité Partielle",
            country="Europe du Sud-Est",
            forced_organ_extraction_scale_score=78.0,
            transplant_tourism_infrastructure_score=75.0,
            donor_coercion_vulnerability_score=80.0,
            prosecution_accountability_gap_score=85.0,
            primary_pattern="prosecution_accountability_gap",
        ),
        OrganTraffickingEntity(
            entity_id="OT-005",
            name="Inde — Tourisme Transplants Rein, Loi THOA Mal Appliquée & Trafic États Ruraux",
            country="Asie du Sud",
            forced_organ_extraction_scale_score=52.0,
            transplant_tourism_infrastructure_score=55.0,
            donor_coercion_vulnerability_score=58.0,
            prosecution_accountability_gap_score=50.0,
            primary_pattern="transplant_tourism_infrastructure",
        ),
        OrganTraffickingEntity(
            entity_id="OT-006",
            name="Israël/Patients Riches — Tourisme Transplants Vers Pakistan/Roumanie & Cadre Légal Insuffisant",
            country="Moyen-Orient/Europe",
            forced_organ_extraction_scale_score=48.0,
            transplant_tourism_infrastructure_score=52.0,
            donor_coercion_vulnerability_score=45.0,
            prosecution_accountability_gap_score=55.0,
            primary_pattern="prosecution_accountability_gap",
        ),
        OrganTraffickingEntity(
            entity_id="OT-007",
            name="Déclaration Istanbul — Coalition Anti-Tourisme Transplant, Réformes & Suivi International",
            country="Global",
            forced_organ_extraction_scale_score=22.0,
            transplant_tourism_infrastructure_score=25.0,
            donor_coercion_vulnerability_score=28.0,
            prosecution_accountability_gap_score=30.0,
            primary_pattern="forced_organ_extraction_scale",
        ),
        OrganTraffickingEntity(
            entity_id="OT-008",
            name="ONU/ONUDC — Protocole Palermo Organes, Rapport Trafic Êtres Humains & Standards Médicaux",
            country="Global",
            forced_organ_extraction_scale_score=4.0,
            transplant_tourism_infrastructure_score=5.0,
            donor_coercion_vulnerability_score=3.0,
            prosecution_accountability_gap_score=6.0,
            primary_pattern="transplant_tourism_infrastructure",
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

    return OrganTraffickingEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_organ_trafficking_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "david_matas_david_kilgour_bloody_harvest_organ_harvesting_china_report",
            "declaration_istanbul_custodian_group_organ_trafficking_transplant_tourism",
            "unodc_global_report_trafficking_persons_organ_removal_chapter",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_organ_trafficking_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_organ_trafficking_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
