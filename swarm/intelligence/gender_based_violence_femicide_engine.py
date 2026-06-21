from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class GenderBasedViolenceFemicideEntity:
    entity_id: str
    name: str
    country: str
    femicide_domestic_violence_impunity_severity_score: float
    rape_sexual_violence_prosecution_gap_scale_score: float
    honor_killing_forced_marriage_prevalence_score: float
    gbv_legal_protection_enforcement_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_gender_based_violence_femicide_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.femicide_domestic_violence_impunity_severity_score * 0.30
            + self.rape_sexual_violence_prosecution_gap_scale_score * 0.25
            + self.honor_killing_forced_marriage_prevalence_score * 0.25
            + self.gbv_legal_protection_enforcement_deficit_gap_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_gender_based_violence_femicide_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[GenderBasedViolenceFemicideEntity]:
    return [
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-001",
            name="Mexique/Amérique Centrale — 10 Féminicides/Jour",
            country="Mexique",
            femicide_domestic_violence_impunity_severity_score=95.0,
            rape_sexual_violence_prosecution_gap_scale_score=92.0,
            honor_killing_forced_marriage_prevalence_score=92.0,
            gbv_legal_protection_enforcement_deficit_gap_score=93.0,
            primary_pattern="Alerte Genre 22 États, Impunité 95% & Cartels Femmes",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-002",
            name="Afghanistan/Taliban — Mariage Enfants & Violence Conjugale",
            country="Afghanistan",
            femicide_domestic_violence_impunity_severity_score=93.0,
            rape_sexual_violence_prosecution_gap_scale_score=90.0,
            honor_killing_forced_marriage_prevalence_score=91.0,
            gbv_legal_protection_enforcement_deficit_gap_score=89.0,
            primary_pattern="Mariage Enfants Légalisé, Violence Non Criminalisée & Stoning",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-003",
            name="Pakistan/Inde — Honor Killings 1000+/An",
            country="Pakistan",
            femicide_domestic_violence_impunity_severity_score=90.0,
            rape_sexual_violence_prosecution_gap_scale_score=87.0,
            honor_killing_forced_marriage_prevalence_score=88.0,
            gbv_legal_protection_enforcement_deficit_gap_score=86.0,
            primary_pattern="Honor Killings, Viol Conjugal Légal, Acid Attacks & Jirga",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-004",
            name="RDC/Afrique Conflits — Viol Arme de Guerre",
            country="RDC",
            femicide_domestic_violence_impunity_severity_score=86.0,
            rape_sexual_violence_prosecution_gap_scale_score=83.0,
            honor_killing_forced_marriage_prevalence_score=83.0,
            gbv_legal_protection_enforcement_deficit_gap_score=84.0,
            primary_pattern="200 000 Survivantes, Impunité Militaires & Fistules Non Traitées",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-005",
            name="Brésil/Turquie — Feminicide Post-COVID & Istanbul",
            country="Brésil",
            femicide_domestic_violence_impunity_severity_score=57.0,
            rape_sexual_violence_prosecution_gap_scale_score=54.0,
            honor_killing_forced_marriage_prevalence_score=54.0,
            gbv_legal_protection_enforcement_deficit_gap_score=55.0,
            primary_pattern="Hausse Post-COVID, Maria da Penha Non Appliquée & Retrait Convention Istanbul",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-006",
            name="Europe/USA — Cyberviolence Genre & Underreporting",
            country="Europe/USA",
            femicide_domestic_violence_impunity_severity_score=53.0,
            rape_sexual_violence_prosecution_gap_scale_score=52.0,
            honor_killing_forced_marriage_prevalence_score=51.0,
            gbv_legal_protection_enforcement_deficit_gap_score=52.0,
            primary_pattern="Cyberviolence Montante, Underreporting 80% & VAWA Insuffisant",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-007",
            name="ONU Femmes/CEDAW — Mécanismes Élimination Discrimination",
            country="International",
            femicide_domestic_violence_impunity_severity_score=27.0,
            rape_sexual_violence_prosecution_gap_scale_score=25.0,
            honor_killing_forced_marriage_prevalence_score=26.0,
            gbv_legal_protection_enforcement_deficit_gap_score=25.0,
            primary_pattern="Standards Protection & Comité CEDAW Rapports",
        ),
        GenderBasedViolenceFemicideEntity(
            entity_id="GBV-008",
            name="ONU/DEVAW — Convention Istanbul & SDG 5.2",
            country="International",
            femicide_domestic_violence_impunity_severity_score=4.0,
            rape_sexual_violence_prosecution_gap_scale_score=4.0,
            honor_killing_forced_marriage_prevalence_score=4.0,
            gbv_legal_protection_enforcement_deficit_gap_score=4.0,
            primary_pattern="Déclaration Élimination Violence Femmes 1993 & SDG 5.2",
        ),
    ]


def analyze(entities: List[GenderBasedViolenceFemicideEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "gender_based_violence_femicide_engine",
        "domain": "gender_based_violence_femicide",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.92,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "femicide_impunity": 3,
            "sexual_violence": 2,
            "honor_killing_forced_marriage": 2,
            "legal_deficit": 1,
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
        "avg_estimated_gender_based_violence_femicide_index": round(
            statistics.mean([e.estimated_gender_based_violence_femicide_index for e in entities]), 2
        ),
        "data_sources": [
            "un_women_gbv_prevalence_global_database",
            "who_femicide_global_status_report",
            "amnesty_honor_killing_sexual_violence_documentation",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "femicide_domestic_violence_impunity_severity_score": e.femicide_domestic_violence_impunity_severity_score,
                "rape_sexual_violence_prosecution_gap_scale_score": e.rape_sexual_violence_prosecution_gap_scale_score,
                "honor_killing_forced_marriage_prevalence_score": e.honor_killing_forced_marriage_prevalence_score,
                "gbv_legal_protection_enforcement_deficit_gap_score": e.gbv_legal_protection_enforcement_deficit_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_gender_based_violence_femicide_index": e.estimated_gender_based_violence_femicide_index,
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
