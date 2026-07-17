#!/usr/bin/env python3
"""Wave 174 — ICC Universal Jurisdiction Impunity Engine — Caelum Partners SPRL"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ImpunityAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    crime_severity_documented: float
    icc_non_cooperation_level: float
    domestic_impunity_scale: float
    victim_justice_access_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_impunity_accountability_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.crime_severity_documented * 0.30
            + self.icc_non_cooperation_level * 0.25
            + self.domestic_impunity_scale * 0.25
            + self.victim_justice_access_gap * 0.20,
            2,
        )
        self.risk_level = (
            "critique"
            if self.composite_score >= 60
            else "élevé"
            if self.composite_score >= 40
            else "modéré"
            if self.composite_score >= 20
            else "faible"
        )
        self.estimated_impunity_accountability_index = round(
            self.composite_score / 100 * 10, 2
        )


def run_engine() -> dict:
    entities = [
        ImpunityAccountabilityEntity(
            entity_id="IUJ-001",
            name="Russie / Ukraine",
            country="Russie",
            crime_severity_documented=95,
            icc_non_cooperation_level=93,
            domestic_impunity_scale=92,
            victim_justice_access_gap=88,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-002",
            name="Myanmar / Tatmadaw Junta",
            country="Myanmar",
            crime_severity_documented=91,
            icc_non_cooperation_level=88,
            domestic_impunity_scale=90,
            victim_justice_access_gap=82,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-003",
            name="Israël-Palestine",
            country="Israël / Palestine",
            crime_severity_documented=87,
            icc_non_cooperation_level=84,
            domestic_impunity_scale=83,
            victim_justice_access_gap=82,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-004",
            name="Soudan / El-Béchir",
            country="Soudan",
            crime_severity_documented=78,
            icc_non_cooperation_level=77,
            domestic_impunity_scale=76,
            victim_justice_access_gap=72,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-005",
            name="Syrie / Assad",
            country="Syrie",
            crime_severity_documented=57,
            icc_non_cooperation_level=54,
            domestic_impunity_scale=55,
            victim_justice_access_gap=48,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-006",
            name="Venezuela / Maduro",
            country="Venezuela",
            crime_severity_documented=49,
            icc_non_cooperation_level=46,
            domestic_impunity_scale=48,
            victim_justice_access_gap=44,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-007",
            name="Espagne / UJ Pinochet-Ruanda",
            country="Espagne",
            crime_severity_documented=29,
            icc_non_cooperation_level=26,
            domestic_impunity_scale=28,
            victim_justice_access_gap=27,
        ),
        ImpunityAccountabilityEntity(
            entity_id="IUJ-008",
            name="Allemagne / UJ Syriens",
            country="Allemagne",
            crime_severity_documented=10,
            icc_non_cooperation_level=9,
            domestic_impunity_scale=10,
            victim_justice_access_gap=11,
        ),
    ]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        dist[e.risk_level] += 1

    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, (
        f"Distribution invalide: {dist}"
    )

    avg = round(sum(e.composite_score for e in entities) / len(entities), 2)

    return {
        "domain": "icc_universal_jurisdiction_impunity",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "crime_severity_documented": e.crime_severity_documented,
                "icc_non_cooperation_level": e.icc_non_cooperation_level,
                "domestic_impunity_scale": e.domestic_impunity_scale,
                "victim_justice_access_gap": e.victim_justice_access_gap,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_impunity_accountability_index": e.estimated_impunity_accountability_index,
            }
            for e in entities
        ],
        "avg_composite": avg,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    r = run_engine()
    print(f"Avg composite: {r['avg_composite']}")
    print(f"Risk distribution: {r['risk_distribution']}")
    for e_data in r["entities"]:
        print(
            f"  {e_data['entity_id']}: {e_data['composite_score']} [{e_data['risk_level']}] — {e_data['name']}"
        )
