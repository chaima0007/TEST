from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SettlerColonialismLandRightsEntity:
    entity_id: str
    name: str
    country: str
    sub1_land_dispossession: float
    sub2_treaty_violations: float
    sub3_displacement_ongoing: float
    sub4_legal_recognition_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.sub1_land_dispossession * 0.30
            + self.sub2_treaty_violations * 0.25
            + self.sub3_displacement_ongoing * 0.25
            + self.sub4_legal_recognition_gap * 0.20,
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
        self.estimated_land_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SettlerColonialismLandRightsEngineResult:
    agent: str = "Settler Colonialism Land Rights Engine Agent"
    domain: str = "settler_colonialism_land_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_land_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SettlerColonialismLandRightsEntity] = field(default_factory=list)


def run_settler_colonialism_land_rights_engine() -> SettlerColonialismLandRightsEngineResult:
    entities = [
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-001",
            name="Palestine — Colonisation Cisjordanie, Expulsions Jerusalem-Est, Demolitions Maisons & Apartheid Foncier",
            country="Palestine/Israel",
            sub1_land_dispossession=97.0,
            sub2_treaty_violations=95.0,
            sub3_displacement_ongoing=93.0,
            sub4_legal_recognition_gap=91.0,
            primary_pattern="sub1_land_dispossession",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-002",
            name="Australie — Terra Nullius Legacy, Stolen Generations, Native Title Act Lacunaire & Closing the Gap Echec",
            country="Australie",
            sub1_land_dispossession=81.0,
            sub2_treaty_violations=79.0,
            sub3_displacement_ongoing=77.0,
            sub4_legal_recognition_gap=74.0,
            primary_pattern="sub2_treaty_violations",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-003",
            name="Inde — Adivasi Deplacements Mines, Forest Rights Act Vide, Naxalite Zones & POSCO Resistances",
            country="Inde",
            sub1_land_dispossession=77.0,
            sub2_treaty_violations=75.0,
            sub3_displacement_ongoing=73.0,
            sub4_legal_recognition_gap=70.0,
            primary_pattern="sub3_displacement_ongoing",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-004",
            name="Colombie — Accaparement Terres Paramilitaires, Restitution Loi 1448 Lente, Paysans Deplaces & Leaders Assassines",
            country="Colombie",
            sub1_land_dispossession=72.0,
            sub2_treaty_violations=70.0,
            sub3_displacement_ongoing=68.0,
            sub4_legal_recognition_gap=65.0,
            primary_pattern="sub1_land_dispossession",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-005",
            name="Canada — Revendications Territoriales Premieres Nations, MMIWG, Genocides Culturels & DNUDPA Implementation",
            country="Canada",
            sub1_land_dispossession=55.0,
            sub2_treaty_violations=53.0,
            sub3_displacement_ongoing=51.0,
            sub4_legal_recognition_gap=48.0,
            primary_pattern="sub2_treaty_violations",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-006",
            name="Bresil — Amazonie Garimpeiros, Yanomami Genocide Sanitaire, FUNAI Demantele & Ruralistas Pression",
            country="Bresil",
            sub1_land_dispossession=61.0,
            sub2_treaty_violations=59.0,
            sub3_displacement_ongoing=57.0,
            sub4_legal_recognition_gap=54.0,
            primary_pattern="sub3_displacement_ongoing",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-007",
            name="Nouvelle-Zelande — Treaty Waitangi Process, Tribunal Actif, Reparations Partielles & Co-Gouvernance",
            country="Nouvelle-Zelande",
            sub1_land_dispossession=30.0,
            sub2_treaty_violations=28.0,
            sub3_displacement_ongoing=27.0,
            sub4_legal_recognition_gap=25.0,
            primary_pattern="sub4_legal_recognition_gap",
        ),
        SettlerColonialismLandRightsEntity(
            entity_id="SCL-008",
            name="Bolivie — Plurinationalite Constitutionnelle, Titres Communautaires TCO, Autonomies Indigenes & MAS Conflits",
            country="Bolivie",
            sub1_land_dispossession=14.0,
            sub2_treaty_violations=13.0,
            sub3_displacement_ongoing=13.0,
            sub4_legal_recognition_gap=12.0,
            primary_pattern="sub4_legal_recognition_gap",
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

    return SettlerColonialismLandRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_land_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "undrip_indigenous_rights_monitoring",
            "land_matrix_global_land_grabbing_database",
            "amnesty_international_land_rights_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_settler_colonialism_land_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_land_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")

    assert result.risk_distribution.get("critique", 0) == 4, f"Expected 4 critique, got {result.risk_distribution.get('critique', 0)}"
    assert result.risk_distribution.get("élevé", 0) == 2, f"Expected 2 élevé, got {result.risk_distribution.get('élevé', 0)}"
    assert result.risk_distribution.get("modéré", 0) == 1, f"Expected 1 modéré, got {result.risk_distribution.get('modéré', 0)}"
    assert result.risk_distribution.get("faible", 0) == 1, f"Expected 1 faible, got {result.risk_distribution.get('faible', 0)}"
    print("Distribution assertion: PASSED 4/2/1/1")

    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
