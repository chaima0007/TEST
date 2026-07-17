from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateLossDamageEntity:
    entity_id: str
    name: str
    country: str
    economic_loss_scale_score: float
    cultural_territorial_loss_score: float
    compensation_mechanism_absence_score: float
    historical_emitter_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_loss_damage_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.economic_loss_scale_score * 0.30
            + self.cultural_territorial_loss_score * 0.25
            + self.compensation_mechanism_absence_score * 0.25
            + self.historical_emitter_impunity_score * 0.20,
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
        self.estimated_climate_loss_damage_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ClimateLossDamageEngineResult:
    agent: str = "Climate Loss & Damage Engine Agent"
    domain: str = "climate_loss_damage"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_climate_loss_damage_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateLossDamageEntity] = field(default_factory=list)

def run_climate_loss_damage_engine() -> ClimateLossDamageEngineResult:
    entities = [
        ClimateLossDamageEntity(
            entity_id="LD-001",
            name="Tuvalu/Kiribati — Submersion Territoriale, Identité Nationale Perdue & Déni Compensation Historique",
            country="Océanie",
            economic_loss_scale_score=88.0,
            cultural_territorial_loss_score=95.0,
            compensation_mechanism_absence_score=90.0,
            historical_emitter_impunity_score=85.0,
            primary_pattern="cultural_territorial_loss",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-002",
            name="Bangladesh — Inondations 1/3 Territoire, 20M Déplacés Cyclones & Pertes Économiques Annuelles",
            country="Asie du Sud",
            economic_loss_scale_score=92.0,
            cultural_territorial_loss_score=80.0,
            compensation_mechanism_absence_score=88.0,
            historical_emitter_impunity_score=82.0,
            primary_pattern="economic_loss_scale",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-003",
            name="Sahel/Afrique — Désertification, Conflits Éleveurs-Agriculteurs & Famine Amplifiée Climat",
            country="Afrique Sub-Saharienne",
            economic_loss_scale_score=85.0,
            cultural_territorial_loss_score=82.0,
            compensation_mechanism_absence_score=88.0,
            historical_emitter_impunity_score=80.0,
            primary_pattern="compensation_mechanism_absence",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-004",
            name="AOSIS/Petits États Insulaires — Perte Souveraineté, Coraux Morts & Fonds L&D Insuffisant COP28",
            country="Global/Océanie",
            economic_loss_scale_score=78.0,
            cultural_territorial_loss_score=90.0,
            compensation_mechanism_absence_score=82.0,
            historical_emitter_impunity_score=78.0,
            primary_pattern="cultural_territorial_loss",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-005",
            name="Amérique Latine/Glaciers — Disparition Glaciers Andes, Sécheresse Eau & Migrations Rurales",
            country="Amérique Latine",
            economic_loss_scale_score=52.0,
            cultural_territorial_loss_score=55.0,
            compensation_mechanism_absence_score=58.0,
            historical_emitter_impunity_score=50.0,
            primary_pattern="compensation_mechanism_absence",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-006",
            name="Asie du Sud-Est/Typhons — Dommages Cyclones Philippines/Vietnam & Reconstruction Sans Aide",
            country="Asie du Sud-Est",
            economic_loss_scale_score=50.0,
            cultural_territorial_loss_score=52.0,
            compensation_mechanism_absence_score=55.0,
            historical_emitter_impunity_score=48.0,
            primary_pattern="historical_emitter_impunity",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-007",
            name="COP27-28/Fonds L&D — Accord Sharm el-Sheikh, Fonds Mondial & Contributions Volontaires Insuffisantes",
            country="Global",
            economic_loss_scale_score=22.0,
            cultural_territorial_loss_score=28.0,
            compensation_mechanism_absence_score=30.0,
            historical_emitter_impunity_score=25.0,
            primary_pattern="economic_loss_scale",
        ),
        ClimateLossDamageEntity(
            entity_id="LD-008",
            name="ONU/CCNUCC — Mécanisme Santiago, Article 8 Accord Paris & Réseau Knowledge Santiago",
            country="Global",
            economic_loss_scale_score=4.0,
            cultural_territorial_loss_score=5.0,
            compensation_mechanism_absence_score=3.0,
            historical_emitter_impunity_score=6.0,
            primary_pattern="historical_emitter_impunity",
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

    return ClimateLossDamageEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_loss_damage_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "loss_damage_collaboration_global_climate_vulnerability_report",
            "v20_vulnerable_twenty_group_climate_vulnerable_forum_annual_report",
            "unfccc_santiago_network_loss_damage_technical_assistance_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_climate_loss_damage_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_loss_damage_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
