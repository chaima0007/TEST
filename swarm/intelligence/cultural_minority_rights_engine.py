from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class CulturalMinorityRightsEntity:
    entity_id: str
    name: str
    country: str
    cultural_assimilation_forced_erasure_severity_score: float
    language_suppression_minority_discrimination_scale_score: float
    cultural_heritage_destruction_desecration_score: float
    minority_cultural_participation_exclusion_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_cultural_minority_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.cultural_assimilation_forced_erasure_severity_score * 0.30
            + self.language_suppression_minority_discrimination_scale_score * 0.25
            + self.cultural_heritage_destruction_desecration_score * 0.25
            + self.minority_cultural_participation_exclusion_gap_score * 0.20,
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
        self.estimated_cultural_minority_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class CulturalMinorityRightsEngineResult:
    agent: str = "Cultural Minority Rights Engine Agent"
    domain: str = "cultural_minority_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_cultural_minority_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[CulturalMinorityRightsEntity] = field(default_factory=list)

def run_cultural_minority_rights_engine() -> CulturalMinorityRightsEngineResult:
    entities = [
        CulturalMinorityRightsEntity(
            entity_id="CMR-001",
            name="Ouïghours/Chine — Camps Rééducation, Destruction Mosquées/Cimetières, Langue Interdite Écoles & Assimilation Forcée",
            country="Chine",
            cultural_assimilation_forced_erasure_severity_score=95.0,
            language_suppression_minority_discrimination_scale_score=93.0,
            cultural_heritage_destruction_desecration_score=92.0,
            minority_cultural_participation_exclusion_gap_score=91.0,
            primary_pattern="cultural_assimilation_forced_erasure_severity",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-002",
            name="Tibétains/Chine — Bouddhisme Contrôlé État, Réincarnation Politisée, Langue Supprimée & Exil Dalaï-Lama",
            country="Chine",
            cultural_assimilation_forced_erasure_severity_score=92.0,
            language_suppression_minority_discrimination_scale_score=89.0,
            cultural_heritage_destruction_desecration_score=88.0,
            minority_cultural_participation_exclusion_gap_score=90.0,
            primary_pattern="language_suppression_minority_discrimination_scale",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-003",
            name="Peuples Autochtones Amazonie — Chamans Assassinés, Rituels Interdits, Langues Mourantes & Évangélisation Forcée",
            country="Brésil/Amazonie",
            cultural_assimilation_forced_erasure_severity_score=89.0,
            language_suppression_minority_discrimination_scale_score=86.0,
            cultural_heritage_destruction_desecration_score=86.0,
            minority_cultural_participation_exclusion_gap_score=86.0,
            primary_pattern="cultural_heritage_destruction_desecration",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-004",
            name="Roms Europe — Ségrégation Culturelle, Stérilisations Forcées Histoire, Discrimination Fêtes & Identité Criminalisée",
            country="Europe",
            cultural_assimilation_forced_erasure_severity_score=86.0,
            language_suppression_minority_discrimination_scale_score=83.0,
            cultural_heritage_destruction_desecration_score=82.0,
            minority_cultural_participation_exclusion_gap_score=84.0,
            primary_pattern="minority_cultural_participation_exclusion_gap",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-005",
            name="Kurdes/Turquie — Langue Kurde Limitée Médias/Éducation, Musique Interdite Périodes, Noms Changés de Force",
            country="Turquie",
            cultural_assimilation_forced_erasure_severity_score=57.0,
            language_suppression_minority_discrimination_scale_score=54.0,
            cultural_heritage_destruction_desecration_score=53.0,
            minority_cultural_participation_exclusion_gap_score=55.0,
            primary_pattern="language_suppression_minority_discrimination_scale",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-006",
            name="Bretons/Occitans/Langues Régionales Europe — Standardisation Nationale, Langues Mourantes, Transmission Intergénération Brisée",
            country="Europe",
            cultural_assimilation_forced_erasure_severity_score=54.0,
            language_suppression_minority_discrimination_scale_score=51.0,
            cultural_heritage_destruction_desecration_score=50.0,
            minority_cultural_participation_exclusion_gap_score=52.0,
            primary_pattern="language_suppression_minority_discrimination_scale",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-007",
            name="UNESCO Convention Diversité Culturelle — 2005 Convention, Patrimoine Immatériel & Soutien Expressions Minoritaires",
            country="Global",
            cultural_assimilation_forced_erasure_severity_score=28.0,
            language_suppression_minority_discrimination_scale_score=26.0,
            cultural_heritage_destruction_desecration_score=27.0,
            minority_cultural_participation_exclusion_gap_score=27.0,
            primary_pattern="cultural_heritage_destruction_desecration",
        ),
        CulturalMinorityRightsEntity(
            entity_id="CMR-008",
            name="ONU/DRIP 2007 — Déclaration Droits Peuples Autochtones, Participation Culturelle & SDG 11.4 Patrimoine Inclusif",
            country="Global",
            cultural_assimilation_forced_erasure_severity_score=4.0,
            language_suppression_minority_discrimination_scale_score=4.0,
            cultural_heritage_destruction_desecration_score=5.0,
            minority_cultural_participation_exclusion_gap_score=4.0,
            primary_pattern="minority_cultural_participation_exclusion_gap",
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

    return CulturalMinorityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_cultural_minority_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_declaration_rights_indigenous_peoples_drip2007",
            "unesco_cultural_diversity_convention_2005_reports",
            "minority_rights_group_international_world_directory",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_cultural_minority_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_cultural_minority_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
