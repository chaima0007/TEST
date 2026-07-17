from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class ClimateRefugeeDisplacementRightsEntity:
    entity_id: str
    name: str
    country: str
    climate_displacement_scale_protection_gap_score: float
    statelessness_legal_limbo_climate_score: float
    adaptation_failure_forced_migration_score: float
    international_responsibility_sharing_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_refugee_displacement_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.climate_displacement_scale_protection_gap_score * 0.30
            + self.statelessness_legal_limbo_climate_score * 0.25
            + self.adaptation_failure_forced_migration_score * 0.25
            + self.international_responsibility_sharing_deficit_score * 0.20,
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
        self.estimated_climate_refugee_displacement_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ClimateRefugeeDisplacementRightsEngineResult:
    agent: str = "Climate Refugee Displacement Rights Engine Agent"
    domain: str = "climate_refugee_displacement_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_climate_refugee_displacement_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateRefugeeDisplacementRightsEntity] = field(default_factory=list)


def run_climate_refugee_displacement_rights_engine() -> ClimateRefugeeDisplacementRightsEngineResult:
    entities = [
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-001",
            name="Tuvalu/Submersion Totale 2050 — Traité Migration Fidji Unique Mondial, Citoyenneté Sans Territoire Concept Juridique Nouveau, 11K Habitants Bientôt Sans État & Aucun Cadre International Reconnu",
            country="Tuvalu",
            climate_displacement_scale_protection_gap_score=95.0,
            statelessness_legal_limbo_climate_score=92.0,
            adaptation_failure_forced_migration_score=90.0,
            international_responsibility_sharing_deficit_score=88.0,
            primary_pattern="disparition_etat_crise_statut_juridique",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-002",
            name="Bangladesh/Deltas Submergés — 20M Déplacés Internes Prévus 2050, Chars Insulaires Déjà Abandonnés, Bidonvilles Dhaka Surpeuplés Migrants Climatiques & Aucun Statut Légal Protection",
            country="Bangladesh",
            climate_displacement_scale_protection_gap_score=90.0,
            statelessness_legal_limbo_climate_score=85.0,
            adaptation_failure_forced_migration_score=88.0,
            international_responsibility_sharing_deficit_score=82.0,
            primary_pattern="deplacement_massif_sans_protection",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-003",
            name="Somalie/Sécheresse-Conflit Combinés — 3.8M Déplacés Internes, Éleveurs Nomades Sédentarisés Force, Cycles Famine Répétés Pluies Impossibles & Camps IDP Sans Perspectives Retour",
            country="Somalie",
            climate_displacement_scale_protection_gap_score=88.0,
            statelessness_legal_limbo_climate_score=78.0,
            adaptation_failure_forced_migration_score=90.0,
            international_responsibility_sharing_deficit_score=85.0,
            primary_pattern="deplacement_massif_sans_protection",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-004",
            name="Pakistan/Inondations 2022 Catastrophiques — 33M Affectés, 2M Maisons Détruites, Sindh 40% Submergé, Déplacés Retournés Zones Inondables Faute Alternatives & Aide Internationale Insuffisante",
            country="Pakistan",
            climate_displacement_scale_protection_gap_score=85.0,
            statelessness_legal_limbo_climate_score=72.0,
            adaptation_failure_forced_migration_score=82.0,
            international_responsibility_sharing_deficit_score=80.0,
            primary_pattern="catastrophe_climatique_deplacement_aigu",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-005",
            name="Éthiopie/Sécheresse Corne Afrique — 5.5M Déplacés Conflits+Climat Entremêlés, Pasteurs Oromo Contraints Sédentarisation, Décès Malnutrition Pic 2022-2023 & Aid Détournée Zones Conflit",
            country="Éthiopie",
            climate_displacement_scale_protection_gap_score=62.0,
            statelessness_legal_limbo_climate_score=50.0,
            adaptation_failure_forced_migration_score=55.0,
            international_responsibility_sharing_deficit_score=45.0,
            primary_pattern="deplacement_massif_sans_protection",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-006",
            name="Philippines/Typhons Récurrents — Haiyan 2013 4M Déplacés, Zones Danger Permanent Repeuplées Pauvreté, Manille Côtières Vulnérables 2050 & Politiques Relocalisation Forcée Droits Locataires Ignorés",
            country="Philippines",
            climate_displacement_scale_protection_gap_score=52.0,
            statelessness_legal_limbo_climate_score=45.0,
            adaptation_failure_forced_migration_score=50.0,
            international_responsibility_sharing_deficit_score=40.0,
            primary_pattern="catastrophe_climatique_deplacement_aigu",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-007",
            name="Pays-Bas/Adaptation Delta Works — Digues Modèles Mondial, Mais Aide Adaptation Sud Global Insuffisante, Politique Migration Climatique UE Absente & Shell Condamné Réductions CO2 Non Respectées",
            country="Pays-Bas",
            climate_displacement_scale_protection_gap_score=20.0,
            statelessness_legal_limbo_climate_score=25.0,
            adaptation_failure_forced_migration_score=18.0,
            international_responsibility_sharing_deficit_score=38.0,
            primary_pattern="echec_partage_responsabilite_internationale",
        ),
        ClimateRefugeeDisplacementRightsEntity(
            entity_id="CRDR-008",
            name="Australie/Îles Pacifique Partenaire — Pacific Australia Labour Mobility Visa Limité, Kiribati Négociations Lentes, Politique Migration Climatique Refus Formel & Émissions Charbon Contradictoires",
            country="Australie",
            climate_displacement_scale_protection_gap_score=8.0,
            statelessness_legal_limbo_climate_score=12.0,
            adaptation_failure_forced_migration_score=10.0,
            international_responsibility_sharing_deficit_score=25.0,
            primary_pattern="echec_partage_responsabilite_internationale",
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

    return ClimateRefugeeDisplacementRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_refugee_displacement_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "idmc_global_report_internal_displacement_2023",
            "unhcr_climate_change_displacement_report_2023",
            "platform_disaster_displacement_2023",
            "ipcc_sixth_assessment_report_displacement_chapter",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_refugee_displacement_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_climate_refugee_displacement_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_climate_refugee_displacement_rights_index}")
