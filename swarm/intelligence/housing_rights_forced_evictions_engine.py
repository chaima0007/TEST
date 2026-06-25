from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HousingRightsForcedEvictionsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_scale_violence_score: float
    homelessness_criminalization_neglect_score: float
    informal_settlement_security_tenure_gap_score: float
    housing_legal_protection_enforcement_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_housing_rights_forced_evictions_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_scale_violence_score * 0.30
            + self.homelessness_criminalization_neglect_score * 0.25
            + self.informal_settlement_security_tenure_gap_score * 0.25
            + self.housing_legal_protection_enforcement_score * 0.20,
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
        self.estimated_housing_rights_forced_evictions_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class HousingRightsForcedEvictionsEngineResult:
    agent: str = "Housing Rights Forced Evictions Engine Agent"
    domain: str = "housing_rights_forced_evictions"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_housing_rights_forced_evictions_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingRightsForcedEvictionsEntity] = field(default_factory=list)


def run_housing_rights_forced_evictions_engine() -> HousingRightsForcedEvictionsEngineResult:
    entities = [
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-001",
            name="Kenya/Kibera — 2.5M Bidonville Sans Eau Légal, Expulsions Gouvernementales Récurrentes & Foncier Sans Titre",
            country="Kenya",
            forced_eviction_scale_violence_score=88.0,
            homelessness_criminalization_neglect_score=84.0,
            informal_settlement_security_tenure_gap_score=92.0,
            housing_legal_protection_enforcement_score=86.0,
            primary_pattern="informal_settlement_security_tenure_gap",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-002",
            name="Bangladesh/Dhaka — 40% Population Bidonvilles, Déplacements Climatiques & Expulsions Violentes Développement",
            country="Bangladesh",
            forced_eviction_scale_violence_score=85.0,
            homelessness_criminalization_neglect_score=80.0,
            informal_settlement_security_tenure_gap_score=90.0,
            housing_legal_protection_enforcement_score=82.0,
            primary_pattern="informal_settlement_security_tenure_gap",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-003",
            name="Zimbabwe — Murambatsvina 2005 700K Sans Logement, Expulsions Persistantes Opposants & Bidonvilles Illégaux",
            country="Zimbabwe",
            forced_eviction_scale_violence_score=90.0,
            homelessness_criminalization_neglect_score=78.0,
            informal_settlement_security_tenure_gap_score=85.0,
            housing_legal_protection_enforcement_score=88.0,
            primary_pattern="forced_eviction_scale_violence",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-004",
            name="Philippines/Manille — Duterte Expulsions Forcées Infrastructures, Sans Relogement Adéquat & Défenseurs Menacés",
            country="Philippines",
            forced_eviction_scale_violence_score=82.0,
            homelessness_criminalization_neglect_score=76.0,
            informal_settlement_security_tenure_gap_score=80.0,
            housing_legal_protection_enforcement_score=84.0,
            primary_pattern="forced_eviction_scale_violence",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-005",
            name="Brésil/Favelas — UPP Violence Expulsions Mondial 2014/JO 2016, Trafic+Police & Titres Fonciers Niés",
            country="Brésil",
            forced_eviction_scale_violence_score=58.0,
            homelessness_criminalization_neglect_score=52.0,
            informal_settlement_security_tenure_gap_score=62.0,
            housing_legal_protection_enforcement_score=55.0,
            primary_pattern="informal_settlement_security_tenure_gap",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-006",
            name="USA/Sans-Abrisme — 600K Sans-Abri, Anti-Camping Laws, Expulsions Locataires & Manque Logement Abordable",
            country="USA",
            forced_eviction_scale_violence_score=48.0,
            homelessness_criminalization_neglect_score=62.0,
            informal_settlement_security_tenure_gap_score=45.0,
            housing_legal_protection_enforcement_score=50.0,
            primary_pattern="homelessness_criminalization_neglect",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-007",
            name="France — Loi DALO Partielle, 300K Mal-Logés, Squats Hivers Expulsions & Bidonvilles Roms Récurrents",
            country="France",
            forced_eviction_scale_violence_score=28.0,
            homelessness_criminalization_neglect_score=32.0,
            informal_settlement_security_tenure_gap_score=25.0,
            housing_legal_protection_enforcement_score=30.0,
            primary_pattern="homelessness_criminalization_neglect",
        ),
        HousingRightsForcedEvictionsEntity(
            entity_id="HRF-008",
            name="Autriche — Logement Social 60% Vienne, Wiener Wohnen Modèle & Taux Sans-Abrisme Très Bas",
            country="Autriche",
            forced_eviction_scale_violence_score=8.0,
            homelessness_criminalization_neglect_score=6.0,
            informal_settlement_security_tenure_gap_score=5.0,
            housing_legal_protection_enforcement_score=7.0,
            primary_pattern="housing_legal_protection_enforcement",
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

    return HousingRightsForcedEvictionsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_rights_forced_evictions_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_habitat_world_cities_report_2022",
            "cohre_forced_evictions_global_survey_2023",
            "feantsa_homeless_europe_report_2023",
            "human_rights_watch_housing_rights_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_housing_rights_forced_evictions_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_rights_forced_evictions_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
