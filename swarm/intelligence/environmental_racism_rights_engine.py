from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0a150a"
PREFIX = "ERR"
DOMAIN = "environmental_racism_rights"


@dataclass
class EnvironmentalRacismRightsEntity:
    entity_id: str
    name: str
    country: str
    toxic_exposure_score: float
    environmental_justice_denial_score: float
    community_displacement_score: float
    regulatory_capture_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_racism_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.toxic_exposure_score * 0.30
            + self.environmental_justice_denial_score * 0.25
            + self.community_displacement_score * 0.25
            + self.regulatory_capture_score * 0.20,
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
        self.estimated_environmental_racism_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class EnvironmentalRacismRightsEngineResult:
    agent: str = "Environmental Racism Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_racism_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalRacismRightsEntity] = field(default_factory=list)


def run_environmental_racism_rights_engine() -> EnvironmentalRacismRightsEngineResult:
    entities = [
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-001",
            name="Nigeria Delta Niger — Shell/TotalEnergies 50 Ans Pollution Pétrolière, Communautés Ogoni/Ijaw Empoisonnées, Aucune Réparation & Terres Détruites",
            country="Nigeria",
            toxic_exposure_score=90.0,
            environmental_justice_denial_score=88.0,
            community_displacement_score=87.0,
            regulatory_capture_score=82.0,
            primary_pattern="toxic_exposure",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-002",
            name="Flint Michigan USA — Crise Eau Plombée Communauté Noire, Scandale Gouvernemental Délibéré, Dommages Santé Permanents & Impunité Officielle",
            country="USA",
            toxic_exposure_score=87.0,
            environmental_justice_denial_score=85.0,
            community_displacement_score=84.0,
            regulatory_capture_score=79.0,
            primary_pattern="environmental_justice_denial",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-003",
            name="DRC Congo Cobalt Mining — Enfants Mineurs Exposés Métaux Lourds, Zéro Protection Santé, Déchets Mines Sans Traitement & Multinationales Impunies",
            country="DRC",
            toxic_exposure_score=84.0,
            environmental_justice_denial_score=82.0,
            community_displacement_score=81.0,
            regulatory_capture_score=76.0,
            primary_pattern="regulatory_capture",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-004",
            name="Bangladesh Tanneries Hazaribagh — Ouvriers Pauvres Exposés Chrome/Arsenic, Rivières Turikhal Totalement Polluées, Aucun Contrôle Gouvernemental & Exportation Cuir Europe",
            country="Bangladesh",
            toxic_exposure_score=81.0,
            environmental_justice_denial_score=79.0,
            community_displacement_score=78.0,
            regulatory_capture_score=73.0,
            primary_pattern="toxic_exposure",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-005",
            name="Brazil Amazonie Indigenes — Orpaillage Mercure Yanomami, Empoisonnement Rivières Territoriales, Garimpeiros Illégaux Protégés & Génocide Sanitaire Documenté",
            country="Brazil",
            toxic_exposure_score=60.0,
            environmental_justice_denial_score=58.0,
            community_displacement_score=57.0,
            regulatory_capture_score=52.0,
            primary_pattern="community_displacement",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-006",
            name="India Bhopal Legacy — Contamination Persistante Post-Catastrophe UCC, Nappe Phréatique Empoisonnée, Communautés Pauvres Sans Décontamination & Dow Chemical Impunie",
            country="India",
            toxic_exposure_score=57.0,
            environmental_justice_denial_score=55.0,
            community_displacement_score=54.0,
            regulatory_capture_score=49.0,
            primary_pattern="environmental_justice_denial",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-007",
            name="EU Environmental Justice — Réglementations REACH Partielles, Exceptions Industrielles Accordées, Inégalités Exposition Toxiques Persistantes & Lobbying Chimique Réussi",
            country="EU",
            toxic_exposure_score=35.0,
            environmental_justice_denial_score=33.0,
            community_displacement_score=32.0,
            regulatory_capture_score=27.0,
            primary_pattern="regulatory_capture",
        ),
        EnvironmentalRacismRightsEntity(
            entity_id="ERR-008",
            name="Costa Rica / Ecuador Green Rights — Droits Nature Constitutionnels, Justice Environnementale Avancée, Meilleure Pratique Mondiale & Modèle Législatif",
            country="Costa Rica/Ecuador",
            toxic_exposure_score=17.0,
            environmental_justice_denial_score=15.0,
            community_displacement_score=14.0,
            regulatory_capture_score=9.0,
            primary_pattern="environmental_justice_denial",
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

    return EnvironmentalRacismRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_racism_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unep_environmental_racism_global_assessment",
            "hrw_pollution_community_rights_violations",
            "amnesty_toxic_exposure_indigenous_peoples_report",
            "ejatlas_environmental_justice_cases_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_environmental_racism_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_racism_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
