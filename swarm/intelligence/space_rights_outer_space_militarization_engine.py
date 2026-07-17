"""
Caelum Partners — Space Rights Outer Space Militarization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Militarisation espace, debris spatiaux, droits accès espace extra-atmosphérique.

La militarisation croissante de l'espace extra-atmosphérique constitue une menace existentielle
pour le bien commun de l'humanité. Le Traité de l'Espace de 1967 interdit les armes de
destruction massive en orbite mais ne couvre pas les armes antisatellites (ASAT) conventionnelles.
Les tests ASAT russes (2021, 1 500 débris) et chinois (2007, 3 000 débris) ont dramatiquement
augmenté le risque de syndrome de Kessler — une cascade de collisions qui pourrait rendre
l'orbite terrestre basse inutilisable pour des générations. Pendant ce temps, les méga-constellations
commerciales (Starlink 6 000+ satellites) exacerbent la congestion orbitale sans gouvernance adéquate.

Risk levels (militarisation espace et dégradation accès orbital) :
  critique  -> composite >= 60  (ASAT actifs — débris massifs — course armements orbitale)
  élevé     -> composite >= 40  (militarisation accélérée — gouvernance lacunaire)
  modéré    -> composite >= 20  (pression commerciale — congestion orbitale croissante)
  faible    -> composite < 20   (cadre normatif — traités et lignes directrices)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class SpaceRightsOuterSpaceMilitarizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    anti_satellite_weapons_debris_severity_score: float
    space_militarization_arms_race_scale_score: float
    space_debris_kessler_syndrome_risk_score: float
    outer_space_treaty_compliance_governance_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_space_rights_outer_space_militarization_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.anti_satellite_weapons_debris_severity_score * 0.30
            + self.space_militarization_arms_race_scale_score * 0.25
            + self.space_debris_kessler_syndrome_risk_score * 0.25
            + self.outer_space_treaty_compliance_governance_deficit_gap_score * 0.20,
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
        self.estimated_space_rights_outer_space_militarization_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "anti_satellite_weapons_debris_severity_score": self.anti_satellite_weapons_debris_severity_score,
            "space_militarization_arms_race_scale_score": self.space_militarization_arms_race_scale_score,
            "space_debris_kessler_syndrome_risk_score": self.space_debris_kessler_syndrome_risk_score,
            "outer_space_treaty_compliance_governance_deficit_gap_score": self.outer_space_treaty_compliance_governance_deficit_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_space_rights_outer_space_militarization_index": self.estimated_space_rights_outer_space_militarization_index,
            "last_updated": self.last_updated,
        }


@dataclass
class SpaceRightsOuterSpaceMilitarizationEngineResult:
    agent: str = "Space Rights Outer Space Militarization Engine Agent"
    domain: str = "space_rights_outer_space_militarization"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_space_rights_outer_space_militarization_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SpaceRightsOuterSpaceMilitarizationEntity] = field(default_factory=list)


def run_space_rights_outer_space_militarization_engine() -> SpaceRightsOuterSpaceMilitarizationEngineResult:
    entities = [
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-001",
            name="Russie — Test ASAT Nudol 2021 1 500 Débris, Orbital Bombardment System, Inspection Satellites Rapprochée & Armes Lasers Anti-Sat",
            country="Russie",
            sector="ASAT Débris Orbitaux",
            anti_satellite_weapons_debris_severity_score=94.0,
            space_militarization_arms_race_scale_score=92.0,
            space_debris_kessler_syndrome_risk_score=93.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=91.0,
            primary_pattern="anti_satellite_weapons_debris_severity",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-002",
            name="Chine — ASAT SC-19 Test 2007 3 000 Débris, Satellites Militaires 200+, Jamming GPS & Programme Espace Militaire Accéléré",
            country="Chine",
            sector="Programme Militaire Spatial",
            anti_satellite_weapons_debris_severity_score=90.0,
            space_militarization_arms_race_scale_score=89.0,
            space_debris_kessler_syndrome_risk_score=91.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=88.0,
            primary_pattern="space_militarization_arms_race_scale",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-003",
            name="USA/SpaceCom — US Space Force 2019, Starlink Usage Ukraine Militaire, X-37B Orbital, Co-Orbital ASAT & Contrôle Commercial Militarisé",
            country="USA",
            sector="Space Force Militarisation Commerciale",
            anti_satellite_weapons_debris_severity_score=87.0,
            space_militarization_arms_race_scale_score=86.0,
            space_debris_kessler_syndrome_risk_score=85.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=88.0,
            primary_pattern="space_militarization_arms_race_scale",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-004",
            name="Inde — Test ASAT Mission Shakti 2019 400+ Débris, DRDO Capacités Croissantes, Spatialisation Défense & Adhésion Partielle Traités",
            country="Inde",
            sector="ASAT Capacités Croissantes",
            anti_satellite_weapons_debris_severity_score=83.0,
            space_militarization_arms_race_scale_score=82.0,
            space_debris_kessler_syndrome_risk_score=84.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=81.0,
            primary_pattern="anti_satellite_weapons_debris_severity",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-005",
            name="Méga-Constellations — Starlink 6 000+ Satellites 42k Prévus, OneWeb Amazon Kuiper, Pollution Lumineuse Astronomie & Collision Risk 1% /An",
            country="Global",
            sector="Constellations Commerciales Congestion Orbitale",
            anti_satellite_weapons_debris_severity_score=56.0,
            space_militarization_arms_race_scale_score=54.0,
            space_debris_kessler_syndrome_risk_score=55.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=57.0,
            primary_pattern="space_debris_kessler_syndrome_risk",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-006",
            name="JAXA/ESA — Agences Civiles Pression Militarisée, Budget Défense Espace +30%, Clean Space Initiative & Nettoyage Débris Sous-Financé",
            country="Global",
            sector="Agences Civiles Transition Défense",
            anti_satellite_weapons_debris_severity_score=52.0,
            space_militarization_arms_race_scale_score=51.0,
            space_debris_kessler_syndrome_risk_score=54.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=53.0,
            primary_pattern="outer_space_treaty_compliance_governance_deficit_gap",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-007",
            name="UNOOSA/COPUOS — Committee Peaceful Uses Outer Space, Space Debris Mitigation Guidelines, LTS Guidelines & Registre ONU",
            country="Global",
            sector="Gouvernance Internationale Espace",
            anti_satellite_weapons_debris_severity_score=27.0,
            space_militarization_arms_race_scale_score=25.0,
            space_debris_kessler_syndrome_risk_score=28.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=26.0,
            primary_pattern="outer_space_treaty_compliance_governance_deficit_gap",
        ),
        SpaceRightsOuterSpaceMilitarizationEntity(
            entity_id="SRM-008",
            name="ONU/OST 1967 — Traité Espace Extra-Atmosphérique 1967, Traité Lune 1979, Convention Responsabilité & Régime Gouvernance Lacunaire",
            country="Global",
            sector="Cadre Normatif Traités Spatiaux",
            anti_satellite_weapons_debris_severity_score=4.0,
            space_militarization_arms_race_scale_score=4.0,
            space_debris_kessler_syndrome_risk_score=4.0,
            outer_space_treaty_compliance_governance_deficit_gap_score=4.0,
            primary_pattern="anti_satellite_weapons_debris_severity",
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

    return SpaceRightsOuterSpaceMilitarizationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_space_rights_outer_space_militarization_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unoosa_space_debris_environment_report",
            "secure_world_foundation_space_threat_assessment",
            "un_group_experts_outer_space_security",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_space_rights_outer_space_militarization_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_space_rights_outer_space_militarization_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
