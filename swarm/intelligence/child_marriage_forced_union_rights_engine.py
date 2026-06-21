from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ChildMarriageForcedUnionRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_union_prevalence_score: float
    legal_age_protection_gap_score: float
    consent_coercion_violence_score: float
    accountability_enforcement_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_marriage_forced_union_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_union_prevalence_score * 0.30
            + self.legal_age_protection_gap_score * 0.25
            + self.consent_coercion_violence_score * 0.25
            + self.accountability_enforcement_score * 0.20,
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
        self.estimated_child_marriage_forced_union_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

@dataclass
class ChildMarriageForcedUnionRightsEngineResult:
    agent: str = "Child Marriage Forced Union Rights Engine Agent"
    domain: str = "child_marriage_forced_union_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_child_marriage_forced_union_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildMarriageForcedUnionRightsEntity] = field(default_factory=list)

def run_child_marriage_forced_union_rights_engine() -> ChildMarriageForcedUnionRightsEngineResult:
    entities = [
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-001",
            name="Niger — Mariages Forcés Dès 9 Ans, Wali Imposé & Absence Totale Consentement Féminin",
            country="Afrique de l'Ouest",
            forced_union_prevalence_score=96.0,
            legal_age_protection_gap_score=93.0,
            consent_coercion_violence_score=95.0,
            accountability_enforcement_score=91.0,
            primary_pattern="forced_union_prevalence",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-002",
            name="Tchad — 52% Filles Mariées Avant 15 Ans, Dot Élevée & Pression Familiale Extrême",
            country="Afrique Centrale",
            forced_union_prevalence_score=90.0,
            legal_age_protection_gap_score=88.0,
            consent_coercion_violence_score=86.0,
            accountability_enforcement_score=85.0,
            primary_pattern="legal_age_protection_gap",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-003",
            name="Bangladesh — Exception Légale «Cas Spéciaux», Mariages Forcés Sans Âge Minimum",
            country="Asie du Sud",
            forced_union_prevalence_score=84.0,
            legal_age_protection_gap_score=90.0,
            consent_coercion_violence_score=80.0,
            accountability_enforcement_score=82.0,
            primary_pattern="legal_age_protection_gap",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-004",
            name="Yemen — Conflit & Mariages Précoces Forcés, Réfugiées IDPs & Effondrement Protection",
            country="Moyen-Orient",
            forced_union_prevalence_score=82.0,
            legal_age_protection_gap_score=80.0,
            consent_coercion_violence_score=85.0,
            accountability_enforcement_score=78.0,
            primary_pattern="consent_coercion_violence",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-005",
            name="Pakistan — Mariage Coutumier Vani/Swara, Filles Échangées pour Résolution Conflits Tribaux",
            country="Asie du Sud",
            forced_union_prevalence_score=58.0,
            legal_age_protection_gap_score=55.0,
            consent_coercion_violence_score=60.0,
            accountability_enforcement_score=50.0,
            primary_pattern="consent_coercion_violence",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-006",
            name="Turquie — Mariages Religieux Non-Civils d'Enfants, Zones Rurales & Impunité Familles",
            country="Europe/Asie",
            forced_union_prevalence_score=48.0,
            legal_age_protection_gap_score=50.0,
            consent_coercion_violence_score=45.0,
            accountability_enforcement_score=52.0,
            primary_pattern="accountability_enforcement",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-007",
            name="UNICEF/Girls Not Brides — Coalition Mondiale 1800 ONG, Plaidoyer & Législation Protectrice",
            country="Global",
            forced_union_prevalence_score=25.0,
            legal_age_protection_gap_score=22.0,
            consent_coercion_violence_score=28.0,
            accountability_enforcement_score=30.0,
            primary_pattern="accountability_enforcement",
        ),
        ChildMarriageForcedUnionRightsEntity(
            entity_id="CMFU-008",
            name="ONU/CEDAW Comité — Art.16 Consentement Libre Mariage, Recommandations Générales & Suivi États",
            country="Global",
            forced_union_prevalence_score=5.0,
            legal_age_protection_gap_score=8.0,
            consent_coercion_violence_score=6.0,
            accountability_enforcement_score=10.0,
            primary_pattern="legal_age_protection_gap",
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

    return ChildMarriageForcedUnionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_marriage_forced_union_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_child_marriage_global_database_2025",
            "girls_not_brides_forced_union_country_profiles",
            "human_rights_watch_no_place_for_children_report",
            "unhcr_child_protection_forced_displacement_data",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_child_marriage_forced_union_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_marriage_forced_union_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
