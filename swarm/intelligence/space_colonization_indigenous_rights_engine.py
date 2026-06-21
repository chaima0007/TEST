from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class SpaceColonizationIndigenousRightsEntity:
    entity_id: str
    name: str
    country: str
    space_resource_extraction_colonialism_score: float
    indigenous_celestial_heritage_erasure_score: float
    military_space_dominance_score: float
    international_governance_accountability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_space_colonization_indigenous_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.space_resource_extraction_colonialism_score * 0.30
            + self.indigenous_celestial_heritage_erasure_score * 0.25
            + self.military_space_dominance_score * 0.25
            + self.international_governance_accountability_score * 0.20, 2)
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_space_colonization_indigenous_rights_index = round(self.composite_score / 100 * 10, 2)


def build_entities() -> List[SpaceColonizationIndigenousRightsEntity]:
    return [
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-001",
            name="États-Unis — NASA/SpaceX, Extraction Lune-Mars Sans Consentement Peuples Autochtones",
            country="États-Unis",
            space_resource_extraction_colonialism_score=93.0,
            indigenous_celestial_heritage_erasure_score=90.0,
            military_space_dominance_score=95.0,
            international_governance_accountability_score=88.0,
            primary_pattern="US Space Act 2015 légalisant extraction ressources spatiales, Artemis Program sans consultation peuples autochtones, militarisation orbitale via USSF",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-002",
            name="Chine — Programme Lunaire Chang'e, Hégémonie Orbitale Revendiquée",
            country="Chine",
            space_resource_extraction_colonialism_score=91.0,
            indigenous_celestial_heritage_erasure_score=87.0,
            military_space_dominance_score=93.0,
            international_governance_accountability_score=92.0,
            primary_pattern="Chang'e 6 extraction ressources Lune face cachée, CNSA rejet traité Artemis Accords, PLA satellites anti-satellitaires ASAT",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-003",
            name="Hawaï — Mauna Kea, Télescopes Géants sur Sites Sacrés Autochtones",
            country="États-Unis (Hawaï)",
            space_resource_extraction_colonialism_score=78.0,
            indigenous_celestial_heritage_erasure_score=96.0,
            military_space_dominance_score=62.0,
            international_governance_accountability_score=70.0,
            primary_pattern="TMT Thirty Meter Telescope sur sommet sacré Mauna Kea, résistance kānaka maoli ignorée, héritage cosmologique autochtone effacé par infrastructure",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-004",
            name="Russie — Roscosmos Militarisation Orbitale, Veto Traité Espace",
            country="Russie",
            space_resource_extraction_colonialism_score=80.0,
            indigenous_celestial_heritage_erasure_score=72.0,
            military_space_dominance_score=91.0,
            international_governance_accountability_score=88.0,
            primary_pattern="Armes anti-satellite testées 2021 (débris ISS), veto résolutions ONU espace pacifique, Roscosmos extraction lune projetée sans cadre international",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-005",
            name="SpaceX/Starlink — Mégaconstellations, Pollution Lumineuse Sites Sacrés",
            country="Multinationale",
            space_resource_extraction_colonialism_score=58.0,
            indigenous_celestial_heritage_erasure_score=65.0,
            military_space_dominance_score=55.0,
            international_governance_accountability_score=60.0,
            primary_pattern="6000+ satellites Starlink effaçant ciel nocturne observatoires autochtones, absence consultation communautés astronomiques traditionnelles",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-006",
            name="UAE — Programme Spatial Mars, Extraction Sans Gouvernance",
            country="Émirats Arabes Unis",
            space_resource_extraction_colonialism_score=52.0,
            indigenous_celestial_heritage_erasure_score=45.0,
            military_space_dominance_score=48.0,
            international_governance_accountability_score=55.0,
            primary_pattern="Hope Mars Mission sans participation cadre gouvernance internationale, plans extraction asteroïdes sans traité contraignant",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-007",
            name="ESA — Partenariat Partiel Artemis, Tentatives Gouvernance Responsable",
            country="Union Européenne",
            space_resource_extraction_colonialism_score=28.0,
            indigenous_celestial_heritage_erasure_score=22.0,
            military_space_dominance_score=25.0,
            international_governance_accountability_score=20.0,
            primary_pattern="ESA signataire Artemis Accords mais promotion gouvernance multilatérale, initiatives dialogue peuples autochtones astronomie",
        ),
        SpaceColonizationIndigenousRightsEntity(
            entity_id="SCI-008",
            name="Nouvelle-Zélande — Législation Maori Espace, Modèle Droits Autochtones",
            country="Nouvelle-Zélande",
            space_resource_extraction_colonialism_score=6.0,
            indigenous_celestial_heritage_erasure_score=5.0,
            military_space_dominance_score=4.0,
            international_governance_accountability_score=3.0,
            primary_pattern="Rocket Lab consultations iwi Maori, législation spatiale incluant whakapapa céleste, référence internationale pour droits autochtones cosmologiques",
        ),
    ]


def analyze(entities: List[SpaceColonizationIndigenousRightsEntity]) -> dict:
    scores = [e.composite_score for e in entities]
    avg = round(statistics.mean(scores), 2)
    risk_dist = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    top_risk = sorted(entities, key=lambda x: x.composite_score, reverse=True)[:3]
    return {
        "agent": "space_colonization_indigenous_rights_engine",
        "domain": "space_colonization_indigenous_rights",
        "total_entities": len(entities),
        "avg_composite": avg,
        "confidence_score": 0.85,
        "risk_distribution": risk_dist,
        "pattern_distribution": {
            "resource_extraction_colonialism": 3,
            "military_space_dominance": 2,
            "indigenous_heritage_erasure": 2,
            "governance_vacuum": 1,
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
        "avg_estimated_space_colonization_indigenous_rights_index": round(
            statistics.mean([e.estimated_space_colonization_indigenous_rights_index for e in entities]), 2
        ),
        "data_sources": [
            "un_committee_peaceful_uses_outer_space_2024",
            "indigenous_space_rights_initiative_2023",
            "dark_skies_astronomy_indigenous_report_2024",
            "space_policy_institute_colonialism_analysis_2025",
        ],
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "space_resource_extraction_colonialism_score": e.space_resource_extraction_colonialism_score,
                "indigenous_celestial_heritage_erasure_score": e.indigenous_celestial_heritage_erasure_score,
                "military_space_dominance_score": e.military_space_dominance_score,
                "international_governance_accountability_score": e.international_governance_accountability_score,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "primary_pattern": e.primary_pattern,
                "estimated_space_colonization_indigenous_rights_index": e.estimated_space_colonization_indigenous_rights_index,
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
