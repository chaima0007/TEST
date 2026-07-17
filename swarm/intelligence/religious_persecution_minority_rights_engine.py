from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ReligiousPersecutionMinorityRightsEntity:
    entity_id: str
    name: str
    country: str
    state_persecution_imprisonment_score: float
    legal_discrimination_blasphemy_laws_score: float
    mob_violence_communal_attacks_score: float
    religious_freedom_legal_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_religious_persecution_minority_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_persecution_imprisonment_score * 0.30
            + self.legal_discrimination_blasphemy_laws_score * 0.25
            + self.mob_violence_communal_attacks_score * 0.25
            + self.religious_freedom_legal_protection_gap_score * 0.20,
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
        self.estimated_religious_persecution_minority_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ReligiousPersecutionMinorityRightsEngineResult:
    agent: str = "Religious Persecution Minority Rights Engine Agent"
    domain: str = "religious_persecution_minority_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_religious_persecution_minority_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ReligiousPersecutionMinorityRightsEntity] = field(default_factory=list)

def run_religious_persecution_minority_rights_engine() -> ReligiousPersecutionMinorityRightsEngineResult:
    entities = [
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-001",
            name="Corée du Nord — religion totalement interdite, chrétiens envoyés camps travail, bibles punies de mort",
            country="Asie du Nord-Est",
            state_persecution_imprisonment_score=99.0,
            legal_discrimination_blasphemy_laws_score=98.0,
            mob_violence_communal_attacks_score=95.0,
            religious_freedom_legal_protection_gap_score=99.0,
            primary_pattern="state_persecution_imprisonment",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-002",
            name="Iran — Bahaïs persécutés systématiquement, conversion Islam peine de mort, clergé contrôle total",
            country="Moyen-Orient",
            state_persecution_imprisonment_score=92.0,
            legal_discrimination_blasphemy_laws_score=95.0,
            mob_violence_communal_attacks_score=82.0,
            religious_freedom_legal_protection_gap_score=93.0,
            primary_pattern="legal_discrimination_blasphemy_laws",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-003",
            name="Pakistan — Ahmadiyya déclarés non-musulmans par constitution, loi blasphème lynchages documentés",
            country="Asie du Sud",
            state_persecution_imprisonment_score=85.0,
            legal_discrimination_blasphemy_laws_score=93.0,
            mob_violence_communal_attacks_score=88.0,
            religious_freedom_legal_protection_gap_score=87.0,
            primary_pattern="legal_discrimination_blasphemy_laws",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-004",
            name="Chine — Ouïghours camps rééducation, Falun Gong persécuté, Tibétains bouddhistes réprimés",
            country="Asie du Nord-Est",
            state_persecution_imprisonment_score=90.0,
            legal_discrimination_blasphemy_laws_score=82.0,
            mob_violence_communal_attacks_score=78.0,
            religious_freedom_legal_protection_gap_score=88.0,
            primary_pattern="state_persecution_imprisonment",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-005",
            name="Inde — lois anti-conversion BJP, violences contre chrétiens et musulmans, nationalisme hindou montant",
            country="Asie du Sud",
            state_persecution_imprisonment_score=52.0,
            legal_discrimination_blasphemy_laws_score=58.0,
            mob_violence_communal_attacks_score=65.0,
            religious_freedom_legal_protection_gap_score=55.0,
            primary_pattern="mob_violence_communal_attacks",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-006",
            name="Nigeria — Boko Haram violence religieuse systémique, enlèvements chrétiens, impunité État nord",
            country="Afrique de l'Ouest",
            state_persecution_imprisonment_score=48.0,
            legal_discrimination_blasphemy_laws_score=50.0,
            mob_violence_communal_attacks_score=68.0,
            religious_freedom_legal_protection_gap_score=52.0,
            primary_pattern="mob_violence_communal_attacks",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-007",
            name="Russie — Témoins de Jéhovah interdits, organisations religieuses étrangères restreintes, contrôle FSB",
            country="Europe de l'Est",
            state_persecution_imprisonment_score=30.0,
            legal_discrimination_blasphemy_laws_score=35.0,
            mob_violence_communal_attacks_score=22.0,
            religious_freedom_legal_protection_gap_score=28.0,
            primary_pattern="legal_discrimination_blasphemy_laws",
        ),
        ReligiousPersecutionMinorityRightsEntity(
            entity_id="RPM-008",
            name="Allemagne — liberté religieuse constitutionnelle garantie, quelques cas discrimination mineure",
            country="Europe de l'Ouest",
            state_persecution_imprisonment_score=5.0,
            legal_discrimination_blasphemy_laws_score=6.0,
            mob_violence_communal_attacks_score=8.0,
            religious_freedom_legal_protection_gap_score=5.0,
            primary_pattern="mob_violence_communal_attacks",
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

    return ReligiousPersecutionMinorityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_religious_persecution_minority_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "open_doors_world_watch_list_2024",
            "us_commission_international_religious_freedom_2023",
            "pew_research_global_restrictions_religion_2023",
            "human_rights_watch_religious_persecution_database",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_religious_persecution_minority_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_religious_persecution_minority_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
