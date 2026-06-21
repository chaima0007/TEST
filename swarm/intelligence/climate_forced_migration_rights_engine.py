"""
Caelum Partners — Climate Forced Migration Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Déplacement climatique forcé, droit à la mobilité, apatridie climatique.

Le déplacement climatique forcé représente l'une des crises humanitaires et juridiques
les plus sous-traitées du XXIe siècle. La Banque mondiale estime que 216 millions de
personnes pourraient être contraintes à une migration interne due au changement climatique
d'ici 2050, principalement en Afrique subsaharienne, en Asie du Sud et en Amérique latine.

Contrairement aux réfugiés fuyant la persécution, les migrants climatiques ne bénéficient
d'aucun statut juridique reconnu dans le droit international. La Convention de Genève
de 1951 ne couvre pas le déplacement causé par les catastrophes climatiques ou la
dégradation environnementale. Cette lacune juridique laisse des dizaines de millions
de personnes sans protection, sans droit à la mobilité et sans accès aux mécanismes
de réparation pour les pertes et dommages subis.

Risk levels (déplacement climatique forcé et absence de protection juridique) :
  critique  -> composite >= 60  (déplacement massif — absence totale cadre légal clima-migrants)
  élevé     -> composite >= 40  (migration forcée active — politiques frontières répressives)
  modéré    -> composite >= 20  (plaidoyer insuffisant — cadre Genève inadapté)
  faible    -> composite < 20   (protection normative — rapports et recommandations)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class ClimateForcedMigrationRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    climate_displacement_severity_score: float
    legal_protection_climate_migrants_gap_score: float
    adaptation_finance_access_exclusion_score: float
    loss_damage_reparation_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_climate_forced_migration_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.climate_displacement_severity_score * 0.30
            + self.legal_protection_climate_migrants_gap_score * 0.25
            + self.adaptation_finance_access_exclusion_score * 0.25
            + self.loss_damage_reparation_absence_score * 0.20,
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
        self.estimated_climate_forced_migration_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "climate_displacement_severity_score": self.climate_displacement_severity_score,
            "legal_protection_climate_migrants_gap_score": self.legal_protection_climate_migrants_gap_score,
            "adaptation_finance_access_exclusion_score": self.adaptation_finance_access_exclusion_score,
            "loss_damage_reparation_absence_score": self.loss_damage_reparation_absence_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_climate_forced_migration_rights_index": self.estimated_climate_forced_migration_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class ClimateForcedMigrationRightsEngineResult:
    agent: str = "Climate Forced Migration Rights Engine Agent"
    domain: str = "climate_forced_migration_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_forced_migration_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateForcedMigrationRightsEntity] = field(default_factory=list)


def run_climate_forced_migration_rights_engine() -> ClimateForcedMigrationRightsEngineResult:
    entities = [
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-001",
            name="Bangladesh — 13M Déplacés Climatiques 2050, Cyclones & Montée Eaux, Zéro Statut Légal Clima-Migrants",
            country="Bangladesh",
            sector="Déplacement Climatique Côtier",
            climate_displacement_severity_score=96.0,
            legal_protection_climate_migrants_gap_score=94.0,
            adaptation_finance_access_exclusion_score=91.0,
            loss_damage_reparation_absence_score=92.0,
            primary_pattern="climate_displacement_severity",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-002",
            name="Pacifique/Tuvalu — Submersion Totale, COP Pertes & Dommages Insuffisant, Diaspora Sans Nationalité",
            country="Tuvalu/Pacifique",
            sector="Apatridie Climatique Insulaire",
            climate_displacement_severity_score=93.0,
            legal_protection_climate_migrants_gap_score=91.0,
            adaptation_finance_access_exclusion_score=88.0,
            loss_damage_reparation_absence_score=90.0,
            primary_pattern="loss_damage_reparation_absence",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-003",
            name="Sahel/Afrique Subsaharienne — Désertification 216M Déplacés 2050, Conflits Eau-Terre & Zéro Cadre Légal",
            country="Sahel",
            sector="Migration Climatique Continentale",
            climate_displacement_severity_score=91.0,
            legal_protection_climate_migrants_gap_score=88.0,
            adaptation_finance_access_exclusion_score=86.0,
            loss_damage_reparation_absence_score=87.0,
            primary_pattern="climate_displacement_severity",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-004",
            name="Asie du Sud-Est Côtière — Typhons, Deltas Inondés, Zéro Cadre Légal Migration Climatique",
            country="Asie du Sud-Est",
            sector="Déplacement Côtier Typhons",
            climate_displacement_severity_score=88.0,
            legal_protection_climate_migrants_gap_score=85.0,
            adaptation_finance_access_exclusion_score=83.0,
            loss_damage_reparation_absence_score=84.0,
            primary_pattern="legal_protection_climate_migrants_gap",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-005",
            name="Amérique Centrale — Sécheresse, Migrations Nord, Politiques Frontières Répressives & Droit Mobilité Nié",
            country="Amérique Centrale",
            sector="Migration Climatique Régionale",
            climate_displacement_severity_score=56.0,
            legal_protection_climate_migrants_gap_score=54.0,
            adaptation_finance_access_exclusion_score=51.0,
            loss_damage_reparation_absence_score=53.0,
            primary_pattern="legal_protection_climate_migrants_gap",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-006",
            name="Méditerranée/MENA — Chaleur Extrême, Conflits Eau, Migration Forcée Non Reconnue Légalement",
            country="MENA",
            sector="Migration Climatique MENA",
            climate_displacement_severity_score=54.0,
            legal_protection_climate_migrants_gap_score=51.0,
            adaptation_finance_access_exclusion_score=49.0,
            loss_damage_reparation_absence_score=50.0,
            primary_pattern="climate_displacement_severity",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-007",
            name="UNHCR/Climate Migrants Coalition — Plaidoyer Statut Clima-Migrants, Cadre Genève Insuffisant",
            country="Global",
            sector="Plaidoyer International",
            climate_displacement_severity_score=27.0,
            legal_protection_climate_migrants_gap_score=25.0,
            adaptation_finance_access_exclusion_score=26.0,
            loss_damage_reparation_absence_score=28.0,
            primary_pattern="legal_protection_climate_migrants_gap",
        ),
        ClimateForcedMigrationRightsEntity(
            entity_id="CFM-008",
            name="ONU/IPCC — Rapports AR6, Recommandations Adaptation & Accord Paris Article 8 Pertes & Dommages",
            country="Global",
            sector="Cadre Normatif International",
            climate_displacement_severity_score=5.0,
            legal_protection_climate_migrants_gap_score=4.0,
            adaptation_finance_access_exclusion_score=4.0,
            loss_damage_reparation_absence_score=3.0,
            primary_pattern="loss_damage_reparation_absence",
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

    return ClimateForcedMigrationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_forced_migration_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_climate_change_displacement_global_trends_report",
            "world_bank_groundswell_internal_climate_migration_report",
            "ipcc_ar6_impacts_adaptation_vulnerability_chapter_migration",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_forced_migration_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_forced_migration_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
