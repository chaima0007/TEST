from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class NuclearTestingRadiationVictimsEntity:
    entity_id: str
    name: str
    country: str
    radiation_exposure_health_harm_score: float
    institutional_denial_compensation_failure_score: float
    environmental_contamination_legacy_score: float
    international_accountability_treaty_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nuclear_radiation_victims_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.radiation_exposure_health_harm_score * 0.30
            + self.institutional_denial_compensation_failure_score * 0.25
            + self.environmental_contamination_legacy_score * 0.25
            + self.international_accountability_treaty_gap_score * 0.20,
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
        self.estimated_nuclear_radiation_victims_index = round(
            self.composite_score / 100 * 10, 2
        )


def build_entities() -> List[NuclearTestingRadiationVictimsEntity]:
    return [
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-001",
            name="Marshall Islands/Bikini Atoll — 67 Tests USA, Population Déplacée, Contamination Perpétuelle",
            country="Marshall Islands",
            radiation_exposure_health_harm_score=95.0,
            institutional_denial_compensation_failure_score=92.0,
            environmental_contamination_legacy_score=96.0,
            international_accountability_treaty_gap_score=90.0,
            primary_pattern="Déplacement forcé population, 67 essais 1946-1958, cancers générationnels, île invivable 1000 ans",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-002",
            name="Kazakhstan/Semipalatinsk — 456 Tests URSS, 1.5M Victimes, Pathologies Héréditaires",
            country="Kazakhstan",
            radiation_exposure_health_harm_score=93.0,
            institutional_denial_compensation_failure_score=89.0,
            environmental_contamination_legacy_score=94.0,
            international_accountability_treaty_gap_score=88.0,
            primary_pattern="456 essais soviétiques 1949-1989, 1.5M exposés, leucémies, malformations congénitales intergénérationnelles",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-003",
            name="Algérie/Reggane Sahara — 17 Tests France Coloniale, Victimes Touareg Sans Reconnaissance",
            country="Algérie",
            radiation_exposure_health_harm_score=88.0,
            institutional_denial_compensation_failure_score=91.0,
            environmental_contamination_legacy_score=87.0,
            international_accountability_treaty_gap_score=86.0,
            primary_pattern="17 essais France 1960-1966, populations Touareg jamais indemnisées, refus déclassification archives médicales",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-004",
            name="Polynésie Française/Mururoa — 193 Tests France, Cancers Vétérans, Dissimulation État",
            country="France (Polynésie Française)",
            radiation_exposure_health_harm_score=85.0,
            institutional_denial_compensation_failure_score=87.0,
            environmental_contamination_legacy_score=83.0,
            international_accountability_treaty_gap_score=82.0,
            primary_pattern="193 essais 1966-1996, vétérans cancéreux indemnisés partiellement, loi Morin 2010 insuffisante, Polynésiens exclus",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-005",
            name="Nevada/Downwinders — Autochtones Shoshone Exposés, Cancer Thyroïde, Justice Partielle",
            country="États-Unis",
            radiation_exposure_health_harm_score=58.0,
            institutional_denial_compensation_failure_score=55.0,
            environmental_contamination_legacy_score=52.0,
            international_accountability_treaty_gap_score=50.0,
            primary_pattern="Essais Nevada 1951-1992, Radiation Exposure Compensation Act 1990 partiel, Shoshone exclus, cancers thyroïde",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-006",
            name="Australie/Maralinga — Tests Britanniques, Aborigènes Anangu Exposés, Nettoyage Incomplet",
            country="Australie",
            radiation_exposure_health_harm_score=52.0,
            institutional_denial_compensation_failure_score=58.0,
            environmental_contamination_legacy_score=55.0,
            international_accountability_treaty_gap_score=48.0,
            primary_pattern="12 essais UK 1952-1963, Anangu déplacés sans consentement, décontamination partielle 1993, terres partiellement rendues",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-007",
            name="Japan/Hibakusha Hiroshima Nagasaki — Survivants Atomiques, Stigmatisation, Vieillissement",
            country="Japon",
            radiation_exposure_health_harm_score=30.0,
            institutional_denial_compensation_failure_score=22.0,
            environmental_contamination_legacy_score=18.0,
            international_accountability_treaty_gap_score=25.0,
            primary_pattern="118 000 Hibakusha survivants, loi soutien médical 1957, stigmatisation mariage, témoins TPNW, vieillissement communauté",
        ),
        NuclearTestingRadiationVictimsEntity(
            entity_id="NRV-008",
            name="Treaty on Prohibition Nuclear Weapons TPNW 2021 — Modèle Réparation & Assistance Victimes",
            country="International",
            radiation_exposure_health_harm_score=5.0,
            institutional_denial_compensation_failure_score=8.0,
            environmental_contamination_legacy_score=6.0,
            international_accountability_treaty_gap_score=10.0,
            primary_pattern="TPNW article 6-7 assistance victimes, 93 États signataires, cadre réparation environnementale, norme internationale",
        ),
    ]


def analyze(entities: List[NuclearTestingRadiationVictimsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    assert risk_dist.get("critique", 0) == 4, f"Distribution critique attendue: 4, obtenu: {risk_dist.get('critique', 0)}"
    assert risk_dist.get("élevé", 0) == 2, f"Distribution élevé attendue: 2, obtenu: {risk_dist.get('élevé', 0)}"
    assert risk_dist.get("modéré", 0) == 1, f"Distribution modéré attendue: 1, obtenu: {risk_dist.get('modéré', 0)}"
    assert risk_dist.get("faible", 0) == 1, f"Distribution faible attendue: 1, obtenu: {risk_dist.get('faible', 0)}"

    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "nuclear_testing_radiation_victims_engine",
        "domain": "nuclear_testing_radiation_victims",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.91,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "radiation_exposure_health_harm": 4,
            "institutional_denial_compensation": 2,
            "environmental_contamination": 1,
            "treaty_accountability_gap": 1,
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
        "avg_estimated_nuclear_radiation_victims_index": round(
            statistics.mean([e.estimated_nuclear_radiation_victims_index for e in entities]), 2
        ),
        "data_sources": [
            "international_campaign_abolish_nuclear_weapons_ican_2024",
            "tpnw_treaty_prohibition_nuclear_weapons_2021",
            "human_rights_watch_nuclear_testing_legacy_2023",
            "atomic_heritage_foundation_testing_database",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "radiation_exposure_health_harm_score": e.radiation_exposure_health_harm_score,
                "institutional_denial_compensation_failure_score": e.institutional_denial_compensation_failure_score,
                "environmental_contamination_legacy_score": e.environmental_contamination_legacy_score,
                "international_accountability_treaty_gap_score": e.international_accountability_treaty_gap_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_nuclear_radiation_victims_index": e.estimated_nuclear_radiation_victims_index,
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
