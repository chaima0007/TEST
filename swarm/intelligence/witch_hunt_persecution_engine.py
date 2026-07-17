from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WitchHuntPersecutionEntity:
    entity_id: str
    name: str
    country: str
    accused_killings_violence_scale_score: float
    legal_protection_absence_score: float
    stigma_social_exclusion_severity_score: float
    children_women_targeting_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_witch_hunt_persecution_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.accused_killings_violence_scale_score * 0.30
            + self.legal_protection_absence_score * 0.25
            + self.stigma_social_exclusion_severity_score * 0.25
            + self.children_women_targeting_pattern_score * 0.20,
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
        self.estimated_witch_hunt_persecution_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class WitchHuntPersecutionEngineResult:
    agent: str = "Witch Hunt Persecution Engine Agent"
    domain: str = "witch_hunt_persecution"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_witch_hunt_persecution_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WitchHuntPersecutionEntity] = field(default_factory=list)

def run_witch_hunt_persecution_engine() -> WitchHuntPersecutionEngineResult:
    entities = [
        WitchHuntPersecutionEntity(
            entity_id="WH-001",
            name="Tanzanie — 10,000+ Meurtres Sorcellerie/Albinisme, Membres Prélevés Vivants & Commerce Rituels",
            country="Afrique de l'Est",
            accused_killings_violence_scale_score=95.0,
            legal_protection_absence_score=92.0,
            stigma_social_exclusion_severity_score=92.0,
            children_women_targeting_pattern_score=92.0,
            primary_pattern="accused_killings_violence_scale",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-002",
            name="Papouasie-Nouvelle-Guinée — Femmes Brûlées Vives Accusations Sorcellerie & Loi Abrogée 1971",
            country="Pacifique",
            accused_killings_violence_scale_score=90.0,
            legal_protection_absence_score=92.0,
            stigma_social_exclusion_severity_score=88.0,
            children_women_targeting_pattern_score=90.0,
            primary_pattern="legal_protection_absence",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-003",
            name="Inde — 2,500+ Meurtres Sorcellerie 2000-2016, Femmes Adivasi Jharkhand & Bihar Ciblées",
            country="Asie du Sud",
            accused_killings_violence_scale_score=88.0,
            legal_protection_absence_score=88.0,
            stigma_social_exclusion_severity_score=88.0,
            children_women_targeting_pattern_score=90.0,
            primary_pattern="children_women_targeting_pattern",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-004",
            name="RDC — 30,000 Enfants Accusés Sorcellerie Rue Kinshasa, Abandonnés & Violences Exorcisme",
            country="Afrique Centrale",
            accused_killings_violence_scale_score=85.0,
            legal_protection_absence_score=85.0,
            stigma_social_exclusion_severity_score=88.0,
            children_women_targeting_pattern_score=85.0,
            primary_pattern="children_women_targeting_pattern",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-005",
            name="Ghana — Witch Camps Gnani/Gambaga, 1,000+ Femmes Exilées à Vie Sans Procès & Retour Impossible",
            country="Afrique de l'Ouest",
            accused_killings_violence_scale_score=52.0,
            legal_protection_absence_score=55.0,
            stigma_social_exclusion_severity_score=55.0,
            children_women_targeting_pattern_score=52.0,
            primary_pattern="stigma_social_exclusion_severity",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-006",
            name="Éthiopie — Femmes Âgées Accusées Sorcellerie Villages Ruraux, Lynchages & Expulsions Communautaires",
            country="Afrique de l'Est",
            accused_killings_violence_scale_score=48.0,
            legal_protection_absence_score=52.0,
            stigma_social_exclusion_severity_score=50.0,
            children_women_targeting_pattern_score=50.0,
            primary_pattern="accused_killings_violence_scale",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-007",
            name="Stepping Stones Nigeria/ActionAid — Monitoring Sorcellerie Global, Plaidoyer Witch Camps & Données",
            country="Global",
            accused_killings_violence_scale_score=22.0,
            legal_protection_absence_score=28.0,
            stigma_social_exclusion_severity_score=25.0,
            children_women_targeting_pattern_score=30.0,
            primary_pattern="stigma_social_exclusion_severity",
        ),
        WitchHuntPersecutionEntity(
            entity_id="WH-008",
            name="ONU/Expert Indépendant — Rapport 2009 Pratiques Traditionnelles Néfastes & CEDAW Art.5",
            country="Global",
            accused_killings_violence_scale_score=4.0,
            legal_protection_absence_score=5.0,
            stigma_social_exclusion_severity_score=3.0,
            children_women_targeting_pattern_score=6.0,
            primary_pattern="legal_protection_absence",
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

    return WitchHuntPersecutionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_witch_hunt_persecution_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_independent_expert_report_harmful_traditional_practices_witchcraft",
            "actionaid_stepping_stones_witch_camp_monitoring_report",
            "hrw_accused_killed_witch_hunt_persecution_africa_pacific",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_witch_hunt_persecution_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_witch_hunt_persecution_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
