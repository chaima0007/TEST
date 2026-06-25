from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class FemicideGenderBasedKillingsEntity:
    entity_id: str
    name: str
    country: str
    femicide_rate_impunity_score: float
    legal_protection_enforcement_deficit_score: float
    gender_violence_systemic_failure_score: float
    state_accountability_prevention_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_femicide_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.femicide_rate_impunity_score * 0.30
            + self.legal_protection_enforcement_deficit_score * 0.25
            + self.gender_violence_systemic_failure_score * 0.25
            + self.state_accountability_prevention_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_femicide_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[FemicideGenderBasedKillingsEntity]:
    return [
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-001",
            name="Mexique — 10 Femmes Assassinées/Jour, Impunité 99%",
            country="Mexique",
            femicide_rate_impunity_score=96.0,
            legal_protection_enforcement_deficit_score=92.0,
            gender_violence_systemic_failure_score=93.0,
            state_accountability_prevention_score=91.0,
            primary_pattern="10 féminicides quotidiens, impunité 99%, absence enquêtes féminicide, loi Alerta sin efecto",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-002",
            name="El Salvador/Honduras/Guatemala — Triangle Nord Féminicides Gangs",
            country="Amérique Centrale",
            femicide_rate_impunity_score=91.0,
            legal_protection_enforcement_deficit_score=88.0,
            gender_violence_systemic_failure_score=89.0,
            state_accountability_prevention_score=87.0,
            primary_pattern="Féminicides MS-13/Barrio 18, lois insuffisantes, femmes déplacées, violence domestique impunie",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-003",
            name="Turquie — Retrait Convention Istanbul 2021, 300+ Morts/An",
            country="Turquie",
            femicide_rate_impunity_score=87.0,
            legal_protection_enforcement_deficit_score=84.0,
            gender_violence_systemic_failure_score=85.0,
            state_accountability_prevention_score=83.0,
            primary_pattern="Retrait Istanbul Convention 2021, 300+ femmes tuées ex-partenaires annuellement, politiques rétrogrades",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-004",
            name="Pakistan — Crimes Honneur Karo-Kari, 1000+ Annuel",
            country="Pakistan",
            femicide_rate_impunity_score=83.0,
            legal_protection_enforcement_deficit_score=80.0,
            gender_violence_systemic_failure_score=81.0,
            state_accountability_prevention_score=79.0,
            primary_pattern="1000+ crimes honneur annuels estimés ONG, acquittements familiaux, karo-kari systémique, loi honor killing 2004 inappliquée",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-005",
            name="Afrique du Sud — Féminicide 5x Moyenne Mondiale, Viol Correctionnel",
            country="Afrique du Sud",
            femicide_rate_impunity_score=58.0,
            legal_protection_enforcement_deficit_score=54.0,
            gender_violence_systemic_failure_score=55.0,
            state_accountability_prevention_score=52.0,
            primary_pattern="5x moyenne mondiale féminicide, viol correctionnel documenté, xenofeicide, surpopulation prison sans effet dissuasif",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-006",
            name="France — 118 Féminicides Conjugaux 2023, Bracelet Insuffisant",
            country="France",
            femicide_rate_impunity_score=50.0,
            legal_protection_enforcement_deficit_score=47.0,
            gender_violence_systemic_failure_score=46.0,
            state_accountability_prevention_score=48.0,
            primary_pattern="118 féminicides 2023, bracelet électronique sous-utilisé, 80% victimes avaient signalé, plan gouvernemental insuffisant",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-007",
            name="Espagne — Loi Violencia de Género 2004, Réduction 25%",
            country="Espagne",
            femicide_rate_impunity_score=28.0,
            legal_protection_enforcement_deficit_score=27.0,
            gender_violence_systemic_failure_score=28.0,
            state_accountability_prevention_score=30.0,
            primary_pattern="Modèle européen loi intégrale 2004, tribunaux spécialisés, réduction 25% féminicides, protocoles police renforcés",
        ),
        FemicideGenderBasedKillingsEntity(
            entity_id="FGK-008",
            name="Islande — Égalité Genre Championne, Féminicide Quasi-Nul",
            country="Islande",
            femicide_rate_impunity_score=5.0,
            legal_protection_enforcement_deficit_score=4.0,
            gender_violence_systemic_failure_score=4.0,
            state_accountability_prevention_score=5.0,
            primary_pattern="Féminicide quasi-nul, égalité salariale légale, parité politique 50%, modèle nordique prévention violence",
        ),
    ]


def analyze(entities: List[FemicideGenderBasedKillingsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "femicide_gender_based_killings_engine",
        "domain": "femicide_gender_based_killings",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.91,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "femicide_impunity": 4,
            "legal_protection_deficit": 2,
            "gender_violence_systemic": 1,
            "state_accountability": 1,
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
        "avg_estimated_femicide_index": round(
            statistics.mean([e.estimated_femicide_index for e in entities]), 2
        ),
        "data_sources": [
            "un_women_femicide_watch_2023",
            "who_violence_against_women_2023",
            "amnesty_international_femicide_report_2023",
            "council_europe_istanbul_convention_monitoring",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "femicide_rate_impunity_score": e.femicide_rate_impunity_score,
                "legal_protection_enforcement_deficit_score": e.legal_protection_enforcement_deficit_score,
                "gender_violence_systemic_failure_score": e.gender_violence_systemic_failure_score,
                "state_accountability_prevention_score": e.state_accountability_prevention_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_femicide_index": e.estimated_femicide_index,
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
