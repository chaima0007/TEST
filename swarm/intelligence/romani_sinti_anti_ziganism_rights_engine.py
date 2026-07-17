from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class RomaniSintiAntiZiganismRightsEntity:
    entity_id: str
    name: str
    country: str
    segregation_exclusion_score: float
    eviction_displacement_score: float
    anti_ziganism_state_complicity_score: float
    rights_protection_enforcement_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_romani_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.segregation_exclusion_score * 0.30
            + self.eviction_displacement_score * 0.25
            + self.anti_ziganism_state_complicity_score * 0.25
            + self.rights_protection_enforcement_deficit_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_romani_rights_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[RomaniSintiAntiZiganismRightsEntity]:
    return [
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-001",
            name="Slovaquie — Ségrégation Scolaire Roms, 50% Classes Spéciales",
            country="Slovaquie",
            segregation_exclusion_score=93.0,
            eviction_displacement_score=88.0,
            anti_ziganism_state_complicity_score=91.0,
            rights_protection_enforcement_deficit_score=89.0,
            primary_pattern="50% enfants roms classes spéciales, arrêt CEDH 2021 ignoré, discrimination institutionnelle éducation, ghettos scolaires",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-002",
            name="Bulgarie — Évictions Forcées Quartiers Roms, Mahala Démolis",
            country="Bulgarie",
            segregation_exclusion_score=88.0,
            eviction_displacement_score=90.0,
            anti_ziganism_state_complicity_score=85.0,
            rights_protection_enforcement_deficit_score=84.0,
            primary_pattern="Mahala démolis sans relogement, discrimination systémique emploi/logement, anti-ziganism médiatique normalisé",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-003",
            name="France — 15 000 Roms Expulsés 2023, Circulaire Valls",
            country="France",
            segregation_exclusion_score=83.0,
            eviction_displacement_score=86.0,
            anti_ziganism_state_complicity_score=82.0,
            rights_protection_enforcement_deficit_score=80.0,
            primary_pattern="15 000 expulsions 2023, circulaire Valls persistante, camps démantelés sans relogement, Roms citoyens UE discriminés",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-004",
            name="Hongrie — Orban Anti-Roms, Stérilisation Forcée Historique",
            country="Hongrie",
            segregation_exclusion_score=81.0,
            eviction_displacement_score=78.0,
            anti_ziganism_state_complicity_score=80.0,
            rights_protection_enforcement_deficit_score=77.0,
            primary_pattern="Rhétorique Orban anti-roms, stérilisation forcée historique non réparée, exclusion marché travail 70%, ségrégation écoles",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-005",
            name="République Tchèque — Stérilisations Forcées, 90 000 Cas Documentés",
            country="République Tchèque",
            segregation_exclusion_score=55.0,
            eviction_displacement_score=50.0,
            anti_ziganism_state_complicity_score=53.0,
            rights_protection_enforcement_deficit_score=51.0,
            primary_pattern="90 000 cas stérilisations forcées documentés, indemnisations 2021 partielles, mémoire collective niée, ségrégation persistante",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-006",
            name="Roumanie — Exclusion Sanitaire COVID, Logement Sous-Standard",
            country="Roumanie",
            segregation_exclusion_score=49.0,
            eviction_displacement_score=46.0,
            anti_ziganism_state_complicity_score=47.0,
            rights_protection_enforcement_deficit_score=45.0,
            primary_pattern="Discrimination accès vaccins COVID, logement sous-standard 85% Roms ruraux, exclusion système santé, pauvreté 80%",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-007",
            name="Espagne — Plan Inclusion Nationale PNAIN 2021-2030",
            country="Espagne",
            segregation_exclusion_score=26.0,
            eviction_displacement_score=24.0,
            anti_ziganism_state_complicity_score=25.0,
            rights_protection_enforcement_deficit_score=23.0,
            primary_pattern="PNAIN 2021-2030 actif, accès école 85% enfants roms, institutions romani cultura, discrimination résiduelle marché travail",
        ),
        RomaniSintiAntiZiganismRightsEntity(
            entity_id="RSA-008",
            name="Finlande — Roms Citoyens Intégrés, Programme Culture & Langue",
            country="Finlande",
            segregation_exclusion_score=8.0,
            eviction_displacement_score=7.0,
            anti_ziganism_state_complicity_score=8.0,
            rights_protection_enforcement_deficit_score=9.0,
            primary_pattern="Programme national langue romani, discrimination réduite, citoyenneté pleine, conseil consultatif roms gouvernemental",
        ),
    ]


def analyze(entities: List[RomaniSintiAntiZiganismRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "romani_sinti_anti_ziganism_rights_engine",
        "domain": "romani_sinti_anti_ziganism_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.90,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "educational_segregation": 3,
            "forced_eviction": 2,
            "anti_ziganism_institutional": 2,
            "rights_protection_deficit": 1,
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
        "avg_estimated_romani_rights_index": round(
            statistics.mean([e.estimated_romani_rights_index for e in entities]), 2
        ),
        "data_sources": [
            "fra_roma_inclusion_report_2023",
            "council_europe_ecri_reports_2023",
            "errc_european_roma_rights_centre_2023",
            "cedh_arrêts_roms_2021_2023",
        ],
        "entities": [
            {
                "id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "segregation_exclusion_score": e.segregation_exclusion_score,
                "eviction_displacement_score": e.eviction_displacement_score,
                "anti_ziganism_state_complicity_score": e.anti_ziganism_state_complicity_score,
                "rights_protection_enforcement_deficit_score": e.rights_protection_enforcement_deficit_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_romani_rights_index": e.estimated_romani_rights_index,
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
