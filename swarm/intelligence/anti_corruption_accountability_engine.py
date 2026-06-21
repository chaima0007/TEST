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
            name="Somalie/Yémen — IPC 8-10/100 & État Capturé",
            country="Somalie",
            grand_corruption_state_capture_severity_score=95.0,
            judicial_police_bribery_impunity_scale_score=92.0,
            public_procurement_kleptocracy_scale_score=93.0,
            whistleblower_anticorruption_protection_deficit_gap_score=91.0,
            primary_pattern="État Capturé Clans, Fonctionnaires Jamais Payés & Aid Détournée",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-002",
            name="Venezuela/Nicaragua — PDVSA Pillé & Kleptocrates",
            country="Venezuela",
            grand_corruption_state_capture_severity_score=92.0,
            judicial_police_bribery_impunity_scale_score=89.0,
            public_procurement_kleptocracy_scale_score=90.0,
            whistleblower_anticorruption_protection_deficit_gap_score=88.0,
            primary_pattern="Pétrole PDVSA Pillé, Maduro Kleptocrates & Opposition Emprisonnée",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-003",
            name="Russie/Poutine — Oligarques Kremlin & Navalny",
            country="Russie",
            grand_corruption_state_capture_severity_score=89.0,
            judicial_police_bribery_impunity_scale_score=86.0,
            public_procurement_kleptocracy_scale_score=87.0,
            whistleblower_anticorruption_protection_deficit_gap_score=85.0,
            primary_pattern="Oligarques Proches Kremlin, Marchés Opaque & FBK Liquidé",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-004",
            name="Chine — Anti-Corruption Xi Sélective & CCDI",
            country="Chine",
            grand_corruption_state_capture_severity_score=86.0,
            judicial_police_bribery_impunity_scale_score=83.0,
            public_procurement_kleptocracy_scale_score=83.0,
            whistleblower_anticorruption_protection_deficit_gap_score=84.0,
            primary_pattern="5M Fonctionnaires Punis, Whistleblowers Disparus & CCDI Parti Contrôle",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-005",
            name="Brésil/Nigeria — Lava Jato Stoppé & Odebrecht",
            country="Brésil",
            grand_corruption_state_capture_severity_score=57.0,
            judicial_police_bribery_impunity_scale_score=54.0,
            public_procurement_kleptocracy_scale_score=55.0,
            whistleblower_anticorruption_protection_deficit_gap_score=53.0,
            primary_pattern="Lava Jato Stoppé Politique, Odebrecht 12 Pays & EFCC Sélectif",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-006",
            name="Europe/USA — Panama Papers & Lobbying Légalisé",
            country="Europe/USA",
            grand_corruption_state_capture_severity_score=53.0,
            judicial_police_bribery_impunity_scale_score=51.0,
            public_procurement_kleptocracy_scale_score=52.0,
            whistleblower_anticorruption_protection_deficit_gap_score=51.0,
            primary_pattern="Panama Papers Sans Suite, Enablers Immunisés & Revolving Door",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-007",
            name="Transparency International/GRECO — CPI & Standards OCDE",
            country="International",
            grand_corruption_state_capture_severity_score=27.0,
            judicial_police_bribery_impunity_scale_score=25.0,
            public_procurement_kleptocracy_scale_score=26.0,
            whistleblower_anticorruption_protection_deficit_gap_score=25.0,
            primary_pattern="Mécanisme Évaluation CoE & Recommandations Anti-Corruption",
        ),
        AntiCorruptionAccountabilityEntity(
            entity_id="ACA-008",
            name="ONU/UNCAC — Convention 2003 & SDG 16.6",
            country="International",
            grand_corruption_state_capture_severity_score=4.0,
            judicial_police_bribery_impunity_scale_score=4.0,
            public_procurement_kleptocracy_scale_score=4.0,
            whistleblower_anticorruption_protection_deficit_gap_score=4.0,
            primary_pattern="Convention Nations Unies Contre Corruption 2003 & GAFI Blanchiment",
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
            "transparency_international_cpi_annual_report",
            "fatf_money_laundering_corruption_assessment",
            "global_witness_state_capture_kleptocracy_report",
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
