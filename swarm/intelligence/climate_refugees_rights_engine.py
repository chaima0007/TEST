from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN = "climate_refugees_rights"
PREFIX = "CRR"
ACCENT_COLOR = "#0a1628"


@dataclass
class ClimateRefugeesRightsEntity:
    entity_id: str
    name: str
    country: str
    climate_displacement_exposure_score: float
    legal_protection_gap_score: float
    adaptation_resources_denial_score: float
    international_responsibility_evasion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_refugees_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.climate_displacement_exposure_score * 0.30
            + self.legal_protection_gap_score * 0.25
            + self.adaptation_resources_denial_score * 0.25
            + self.international_responsibility_evasion_score * 0.20,
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
        self.estimated_climate_refugees_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ClimateRefugeesRightsEngineResult:
    agent: str = "Climate Refugees Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_climate_refugees_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateRefugeesRightsEntity] = field(default_factory=list)


def run_climate_refugees_rights_engine() -> ClimateRefugeesRightsEngineResult:
    entities = [
        ClimateRefugeesRightsEntity(
            entity_id="CRR-001",
            name="Bangladesh — 18 Millions Déplacés d'ici 2050, Delta du Gange Submergé, Aucun Statut Légal Réfugié Climatique & Migration Forcée Urbaine",
            country="Bangladesh",
            climate_displacement_exposure_score=92.0,
            legal_protection_gap_score=90.0,
            adaptation_resources_denial_score=88.0,
            international_responsibility_evasion_score=87.0,
            primary_pattern="climate_displacement_exposure",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-002",
            name="Îles du Pacifique/Tuvalu — Disparition Imminente sous les Eaux, Souveraineté Nationale Menacée, Relocalisations Forcées Fiji & Reconnaissance Juridique Inexistante",
            country="Tuvalu/Kiribati",
            climate_displacement_exposure_score=88.0,
            legal_protection_gap_score=86.0,
            adaptation_resources_denial_score=85.0,
            international_responsibility_evasion_score=84.0,
            primary_pattern="legal_protection_gap",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-003",
            name="Somalie — Sécheresses Répétées & Inondations Combinées, 3,8M PDI, Famine Climatique & Conflits Ressources Eau Agropastorale",
            country="Somalie",
            climate_displacement_exposure_score=85.0,
            legal_protection_gap_score=82.0,
            adaptation_resources_denial_score=80.0,
            international_responsibility_evasion_score=78.0,
            primary_pattern="adaptation_resources_denial",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-004",
            name="Soudan — Darfour Crisis Amplifiée par Désertification, Conflit Eau/Pâturages, 2M+ PDI Climatiques & Néant Réponse Internationale",
            country="Soudan",
            climate_displacement_exposure_score=80.0,
            legal_protection_gap_score=78.0,
            adaptation_resources_denial_score=76.0,
            international_responsibility_evasion_score=75.0,
            primary_pattern="international_responsibility_evasion",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-005",
            name="Mozambique — Cyclones Idai & Kenneth Destructions Massives, 700 000 Déplacés, Reconstruction Insuffisante & Financement Adaptation Promis Non Livré",
            country="Mozambique",
            climate_displacement_exposure_score=60.0,
            legal_protection_gap_score=57.0,
            adaptation_resources_denial_score=55.0,
            international_responsibility_evasion_score=53.0,
            primary_pattern="climate_displacement_exposure",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-006",
            name="Inde/Sundarbans — 4,5M Habitants Deltas Menacés, Salinisation Terres Agricoles, Migration vers Kolkata & Absence Politique Nationale Déplacés Climatiques",
            country="Inde",
            climate_displacement_exposure_score=57.0,
            legal_protection_gap_score=55.0,
            adaptation_resources_denial_score=53.0,
            international_responsibility_evasion_score=51.0,
            primary_pattern="legal_protection_gap",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-007",
            name="Indonésie — Relocalisation Capitale Jakarta vers Nusantara, 9M Habitants Menacés par Subsidence & Élévation Mer, Coût Social Déplacés Interne",
            country="Indonésie",
            climate_displacement_exposure_score=38.0,
            legal_protection_gap_score=36.0,
            adaptation_resources_denial_score=34.0,
            international_responsibility_evasion_score=32.0,
            primary_pattern="adaptation_resources_denial",
        ),
        ClimateRefugeesRightsEntity(
            entity_id="CRR-008",
            name="Nouvelle-Zélande — Pacific Access Category & Humanitarian Visa Climatique Pionnier, Accords Bilatéraux Îles Pacifique & Meilleure Pratique Régionale",
            country="Nouvelle-Zélande",
            climate_displacement_exposure_score=12.0,
            legal_protection_gap_score=10.0,
            adaptation_resources_denial_score=11.0,
            international_responsibility_evasion_score=10.0,
            primary_pattern="legal_protection_gap",
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

    return ClimateRefugeesRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_refugees_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_climate_displacement_global_report",
            "internal_displacement_monitoring_centre_idmc",
            "world_bank_groundswell_climate_migration_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_refugees_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_refugees_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
