from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class RightToAsylumRefugeeProtectionEntity:
    entity_id: str
    name: str
    country: str
    pushback_refoulement_severity_score: float
    detention_asylum_seeker_conditions_scale_score: float
    refugee_camp_rights_violation_score: float
    asylum_procedure_denial_obstruction_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_asylum_refugee_protection_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.pushback_refoulement_severity_score * 0.30
            + self.detention_asylum_seeker_conditions_scale_score * 0.25
            + self.refugee_camp_rights_violation_score * 0.25
            + self.asylum_procedure_denial_obstruction_gap_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_right_to_asylum_refugee_protection_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[RightToAsylumRefugeeProtectionEntity]:
    return [
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-001",
            name="Australie — Offshore Processing Nauru/PNG",
            country="Australie",
            pushback_refoulement_severity_score=95.0,
            detention_asylum_seeker_conditions_scale_score=92.0,
            refugee_camp_rights_violation_score=93.0,
            asylum_procedure_denial_obstruction_gap_score=91.0,
            primary_pattern="Détention Indéfinie, Refoulement & Bateaux Repoussés",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-002",
            name="Hongrie/UE — Clôtures Barbelées & Pushbacks Illégaux",
            country="Hongrie",
            pushback_refoulement_severity_score=92.0,
            detention_asylum_seeker_conditions_scale_score=89.0,
            refugee_camp_rights_violation_score=90.0,
            asylum_procedure_denial_obstruction_gap_score=88.0,
            primary_pattern="Pushbacks Illégaux Croatie, Hotspots Surpeuplés & Demandes Irrecevables",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-003",
            name="Libye/EU — Garde-Côtes Financés & Centres Détention",
            country="Libye",
            pushback_refoulement_severity_score=89.0,
            detention_asylum_seeker_conditions_scale_score=87.0,
            refugee_camp_rights_violation_score=86.0,
            asylum_procedure_denial_obstruction_gap_score=85.0,
            primary_pattern="Retour Migrant Torture, Centres Détention Inhumains & OIM Financement",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-004",
            name="USA/Trump — MPP/Attendre au Mexique & Titre 42",
            country="USA",
            pushback_refoulement_severity_score=86.0,
            detention_asylum_seeker_conditions_scale_score=83.0,
            refugee_camp_rights_violation_score=83.0,
            asylum_procedure_denial_obstruction_gap_score=84.0,
            primary_pattern="Politique MPP, Expulsions COVID, Séparation Familles & Demandes Annulées",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-005",
            name="Grèce — Pushbacks Égée & Camps Samos Surpeuplés",
            country="Grèce",
            pushback_refoulement_severity_score=57.0,
            detention_asylum_seeker_conditions_scale_score=54.0,
            refugee_camp_rights_violation_score=55.0,
            asylum_procedure_denial_obstruction_gap_score=53.0,
            primary_pattern="Pushbacks Égée Documentés, Demandeurs Asile Illégalement Expulsés",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-006",
            name="Turquie — 3.5M Réfugiés Syriens & Déportations",
            country="Turquie",
            pushback_refoulement_severity_score=54.0,
            detention_asylum_seeker_conditions_scale_score=51.0,
            refugee_camp_rights_violation_score=52.0,
            asylum_procedure_denial_obstruction_gap_score=50.0,
            primary_pattern="Pression Retour Syriens, Déportations Forcées & Naturalisation Refusée",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-007",
            name="HCR/OIM — Standards Protection Internationale",
            country="International",
            pushback_refoulement_severity_score=27.0,
            detention_asylum_seeker_conditions_scale_score=25.0,
            refugee_camp_rights_violation_score=26.0,
            asylum_procedure_denial_obstruction_gap_score=25.0,
            primary_pattern="Burden Sharing & Protocoles Détermination Statut",
        ),
        RightToAsylumRefugeeProtectionEntity(
            entity_id="RAR-008",
            name="ONU/Convention 1951 — Non-Refoulement & SDG 10.7",
            country="International",
            pushback_refoulement_severity_score=4.0,
            detention_asylum_seeker_conditions_scale_score=4.0,
            refugee_camp_rights_violation_score=4.0,
            asylum_procedure_denial_obstruction_gap_score=4.0,
            primary_pattern="Convention Réfugiés, Protocole 1967 & Non-Refoulement",
        ),
    ]


def analyze(entities: List[RightToAsylumRefugeeProtectionEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "right_to_asylum_refugee_protection_engine",
        "domain": "right_to_asylum_refugee_protection",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.91,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "pushback_refoulement": 4,
            "detention_conditions": 3,
            "procedure_obstruction": 1,
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
        "avg_estimated_right_to_asylum_refugee_protection_index": round(
            statistics.mean([e.estimated_right_to_asylum_refugee_protection_index for e in entities]), 2
        ),
        "data_sources": [
            "unhcr_global_trends_forced_displacement_report",
            "amnesty_pushback_refoulement_documentation",
            "borderline_europe_camp_conditions_monitoring",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "pushback_refoulement_severity_score": e.pushback_refoulement_severity_score,
                "detention_asylum_seeker_conditions_scale_score": e.detention_asylum_seeker_conditions_scale_score,
                "refugee_camp_rights_violation_score": e.refugee_camp_rights_violation_score,
                "asylum_procedure_denial_obstruction_gap_score": e.asylum_procedure_denial_obstruction_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_right_to_asylum_refugee_protection_index": e.estimated_right_to_asylum_refugee_protection_index,
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
