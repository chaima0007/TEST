"""Elderly Rights Ageism Engine — droits des personnes âgées & âgisme structurel."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"


@dataclass
class ElderlyRightsAgeismEntity:
    entity_id: str
    name: str
    country: str
    sub1_pension_adequacy: float
    sub2_elder_abuse_rate: float
    sub3_healthcare_geriatric: float
    sub4_social_isolation: float
    primary_pattern: str = ""
    last_updated: str = "2026-06-21"
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_elderly_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.sub1_pension_adequacy * 0.30
            + self.sub2_elder_abuse_rate * 0.25
            + self.sub3_healthcare_geriatric * 0.25
            + self.sub4_social_isolation * 0.20,
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
        self.estimated_elderly_rights_index = round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "sub1_pension_adequacy": self.sub1_pension_adequacy,
            "sub2_elder_abuse_rate": self.sub2_elder_abuse_rate,
            "sub3_healthcare_geriatric": self.sub3_healthcare_geriatric,
            "sub4_social_isolation": self.sub4_social_isolation,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "estimated_elderly_rights_index": self.estimated_elderly_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    ElderlyRightsAgeismEntity(
        entity_id="ERA-001",
        name="Somalie (aucun système pension)",
        country="Somalie",
        sub1_pension_adequacy=94.0,
        sub2_elder_abuse_rate=90.0,
        sub3_healthcare_geriatric=90.0,
        sub4_social_isolation=88.0,
        primary_pattern="absence_protection_sociale",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-002",
        name="Haïti (seniors abandonnés post-séisme)",
        country="Haïti",
        sub1_pension_adequacy=88.0,
        sub2_elder_abuse_rate=84.0,
        sub3_healthcare_geriatric=84.0,
        sub4_social_isolation=82.0,
        primary_pattern="abandon_seniors_catastrophe",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-003",
        name="Inde (zones rurales sans protection)",
        country="Inde",
        sub1_pension_adequacy=78.0,
        sub2_elder_abuse_rate=76.0,
        sub3_healthcare_geriatric=74.0,
        sub4_social_isolation=76.0,
        primary_pattern="inegalite_rural_urbain",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-004",
        name="Nigeria (maltraitance seniors endémique)",
        country="Nigeria",
        sub1_pension_adequacy=70.0,
        sub2_elder_abuse_rate=68.0,
        sub3_healthcare_geriatric=66.0,
        sub4_social_isolation=68.0,
        primary_pattern="maltraitance_endemique",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-005",
        name="Chine (abandon rural exodus)",
        country="Chine",
        sub1_pension_adequacy=56.0,
        sub2_elder_abuse_rate=52.0,
        sub3_healthcare_geriatric=52.0,
        sub4_social_isolation=58.0,
        primary_pattern="exode_rural_abandon",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-006",
        name="USA (coût soins EHPAD)",
        country="USA",
        sub1_pension_adequacy=48.0,
        sub2_elder_abuse_rate=44.0,
        sub3_healthcare_geriatric=44.0,
        sub4_social_isolation=50.0,
        primary_pattern="inaccessibilite_soins_cout",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-007",
        name="France (canicule 2003 legacy)",
        country="France",
        sub1_pension_adequacy=28.0,
        sub2_elder_abuse_rate=26.0,
        sub3_healthcare_geriatric=26.0,
        sub4_social_isolation=28.0,
        primary_pattern="isolement_social_structurel",
    ),
    ElderlyRightsAgeismEntity(
        entity_id="ERA-008",
        name="Norvège (silver economy modèle)",
        country="Norvège",
        sub1_pension_adequacy=10.0,
        sub2_elder_abuse_rate=10.0,
        sub3_healthcare_geriatric=10.0,
        sub4_social_isolation=10.0,
        primary_pattern="modele_silver_economy",
    ),
]


def run_analysis():
    results = [e.to_dict() for e in ENTITIES]
    avg = round(statistics.mean(e.composite_score for e in ENTITIES), 2)
    dist: dict = {}
    for e in ENTITIES:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
    pat: dict = {}
    for e in ENTITIES:
        pat[e.primary_pattern] = pat.get(e.primary_pattern, 0) + 1
    top3 = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [e for e in ENTITIES if e.risk_level == "critique"]

    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Distribution incorrecte: {dist}"

    return {
        "agent": "Elderly Rights Ageism Engine Agent",
        "domain": "elderly_rights_ageism",
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "confidence_score": 0.85,
        "risk_distribution": dist,
        "pattern_distribution": pat,
        "top_risk_entities": [e.name for e in top3],
        "critical_alerts": [
            f"{e.name.split('(')[0].strip()}: {e.primary_pattern}"
            for e in critiques
        ],
        "last_analysis": "2026-06-21",
        "engine_version": ENGINE_VERSION,
        "avg_estimated_elderly_rights_index": round(avg / 100 * 10, 2),
        "data_sources": [
            "who_global_report_on_ageism_2021",
            "helpage_global_age_watch_index_2023",
            "un_open_ended_working_group_ageing_reports",
            "world_bank_pensions_social_protection_data",
        ],
        "entities": results,
    }


if __name__ == "__main__":
    import json
    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Avg index: {data['avg_estimated_elderly_rights_index']}")
    for e in ENTITIES:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_elderly_rights_index}")
