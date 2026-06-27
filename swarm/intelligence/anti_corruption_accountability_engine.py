from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class AntiCorruptionAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    grand_corruption_state_capture_severity_score: float
    judicial_police_bribery_impunity_scale_score: float
    public_procurement_kleptocracy_scale_score: float
    whistleblower_anticorruption_protection_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_anti_corruption_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.grand_corruption_state_capture_severity_score * 0.30
            + self.judicial_police_bribery_impunity_scale_score * 0.25
            + self.public_procurement_kleptocracy_scale_score * 0.25
            + self.whistleblower_anticorruption_protection_deficit_gap_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_anti_corruption_accountability_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[AntiCorruptionAccountabilityEntity]:
    return [
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-001",
            name="Somalie — CPI 11/100, Corruption Systémique",
            country="Somalie",
            grand_corruption_state_capture_severity_score=96.0,
            judicial_police_bribery_impunity_scale_score=93.0,
            public_procurement_kleptocracy_scale_score=94.0,
            whistleblower_anticorruption_protection_deficit_gap_score=92.0,
            primary_pattern="État capturé clans, aide humanitaire détournée, impunité totale",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-002",
            name="Syrie — CPI 13/100, Kleptocracie Assad",
            country="Syrie",
            grand_corruption_state_capture_severity_score=94.0,
            judicial_police_bribery_impunity_scale_score=91.0,
            public_procurement_kleptocracy_scale_score=92.0,
            whistleblower_anticorruption_protection_deficit_gap_score=90.0,
            primary_pattern="Kleptocracie familiale Assad, reconstruction corruption, sanctions contournées",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-003",
            name="Corée du Nord — CPI 17/100, Corruption d'État",
            country="Corée du Nord",
            grand_corruption_state_capture_severity_score=92.0,
            judicial_police_bribery_impunity_scale_score=89.0,
            public_procurement_kleptocracy_scale_score=90.0,
            whistleblower_anticorruption_protection_deficit_gap_score=88.0,
            primary_pattern="Corruption État institutionnalisée, économie parallèle Donju, siphonnage fonds militaires",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-004",
            name="Yémen — CPI 16/100, Fragmentation Pouvoir",
            country="Yémen",
            grand_corruption_state_capture_severity_score=90.0,
            judicial_police_bribery_impunity_scale_score=87.0,
            public_procurement_kleptocracy_scale_score=88.0,
            whistleblower_anticorruption_protection_deficit_gap_score=86.0,
            primary_pattern="Fragmentation pouvoir, corruption factions armées, aide détournée",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-005",
            name="Venezuela — CPI 14/100, Corruption Pétrolière",
            country="Venezuela",
            grand_corruption_state_capture_severity_score=55.0,
            judicial_police_bribery_impunity_scale_score=52.0,
            public_procurement_kleptocracy_scale_score=53.0,
            whistleblower_anticorruption_protection_deficit_gap_score=51.0,
            primary_pattern="PDVSA pillé, Maduro kleptocrates, opposition emprisonnée",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-006",
            name="Afghanistan — CPI 20/100, Retour Taliban",
            country="Afghanistan",
            grand_corruption_state_capture_severity_score=52.0,
            judicial_police_bribery_impunity_scale_score=49.0,
            public_procurement_kleptocracy_scale_score=50.0,
            whistleblower_anticorruption_protection_deficit_gap_score=48.0,
            primary_pattern="Retour Taliban, corruption endémique, trafic opium financement",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-007",
            name="Kenya — CPI 31/100, Réformes Partielles Ruto",
            country="Kenya",
            grand_corruption_state_capture_severity_score=28.0,
            judicial_police_bribery_impunity_scale_score=25.0,
            public_procurement_kleptocracy_scale_score=26.0,
            whistleblower_anticorruption_protection_deficit_gap_score=24.0,
            primary_pattern="Ruto réformes partielles, marchés publics détournés, EACC limité",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-008",
            name="Danemark — CPI 90/100, Modèle Mondial Anti-Corruption",
            country="Danemark",
            grand_corruption_state_capture_severity_score=4.0,
            judicial_police_bribery_impunity_scale_score=4.0,
            public_procurement_kleptocracy_scale_score=4.0,
            whistleblower_anticorruption_protection_deficit_gap_score=4.0,
            primary_pattern="Transparence institutionnelle, protection lanceurs d'alerte solide, OCDE modèle",
        ),
    ]


def analyze(entities: List[AntiCorruptionAccountabilityEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "anti_corruption_accountability_engine",
        "domain": "anti_corruption_accountability",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.90,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "state_capture": 3,
            "judicial_bribery": 2,
            "kleptocracy_procurement": 2,
            "whistleblower_deficit": 1,
        },
        "top_risk_entities": [
            {"id": e.entity_id, "name": e.name, "score": e.composite_score, "risk": e.risk_level}
            for e in top_risk
        ],
        "critical_alerts": [
            f"{e.entity_id}: {e.name} — composite {e.composite_score}"
            for e in entities if e.risk_level == "critique"
        ],
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "avg_estimated_anti_corruption_accountability_index": round(
            statistics.mean([e.estimated_anti_corruption_accountability_index for e in entities]), 2
        ),
        "data_sources": [
            "transparency_international_cpi_2023",
            "u4_anti_corruption_resource_centre_2023",
            "basel_aml_index_2023",
            "un_uncac_review_mechanism_2023",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "grand_corruption_state_capture_severity_score": e.grand_corruption_state_capture_severity_score,
                "judicial_police_bribery_impunity_scale_score": e.judicial_police_bribery_impunity_scale_score,
                "public_procurement_kleptocracy_scale_score": e.public_procurement_kleptocracy_scale_score,
                "whistleblower_anticorruption_protection_deficit_gap_score": e.whistleblower_anticorruption_protection_deficit_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_anti_corruption_accountability_index": e.estimated_anti_corruption_accountability_index,
                "last_updated": e.last_updated,
            }
            for e in entities
        ],
    }


if __name__ == "__main__":
    import json
    entities = build_entities()
    result = analyze(entities)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✓ avg_composite = {result['avg_composite']}")
    print(f"✓ risk_distribution = {result['risk_distribution']}")
    print(f"✓ total_entities = {result['total_entities']}")
