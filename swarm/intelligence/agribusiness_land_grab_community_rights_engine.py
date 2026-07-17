#!/usr/bin/env python3
"""Wave 174 — Agribusiness Land Grab Community Rights Engine — Caelum Partners SPRL"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LandGrabEntity:
    entity_id: str
    name: str
    country: str
    displacement_scale: float
    fpic_violation_severity: float
    violence_impunity_defenders: float
    corporate_accountability_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_land_grab_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.displacement_scale * 0.30
            + self.fpic_violation_severity * 0.25
            + self.violence_impunity_defenders * 0.25
            + self.corporate_accountability_gap * 0.20,
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
        self.estimated_land_grab_rights_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> dict:
    entities = [
        LandGrabEntity(
            entity_id="ALG-001",
            name="Indonésie / Palmier Kalimantan",
            country="Indonésie",
            displacement_scale=90,
            fpic_violation_severity=88,
            violence_impunity_defenders=87,
            corporate_accountability_gap=86,
        ),
        LandGrabEntity(
            entity_id="ALG-002",
            name="Cambodge / Sucre EBA",
            country="Cambodge",
            displacement_scale=86,
            fpic_violation_severity=84,
            violence_impunity_defenders=83,
            corporate_accountability_gap=82,
        ),
        LandGrabEntity(
            entity_id="ALG-003",
            name="Brésil / Soja Cerrado",
            country="Brésil",
            displacement_scale=82,
            fpic_violation_severity=78,
            violence_impunity_defenders=79,
            corporate_accountability_gap=76,
        ),
        LandGrabEntity(
            entity_id="ALG-004",
            name="Sierra Leone / Sucre Addax",
            country="Sierra Leone",
            displacement_scale=74,
            fpic_violation_severity=72,
            violence_impunity_defenders=71,
            corporate_accountability_gap=70,
        ),
        LandGrabEntity(
            entity_id="ALG-005",
            name="Philippines / Ananas Dole-Del Monte",
            country="Philippines",
            displacement_scale=56,
            fpic_violation_severity=52,
            violence_impunity_defenders=54,
            corporate_accountability_gap=48,
        ),
        LandGrabEntity(
            entity_id="ALG-006",
            name="Pérou / Palmier Amazonie",
            country="Pérou",
            displacement_scale=46,
            fpic_violation_severity=44,
            violence_impunity_defenders=46,
            corporate_accountability_gap=42,
        ),
        LandGrabEntity(
            entity_id="ALG-007",
            name="Colombie / Post-Accord Terres",
            country="Colombie",
            displacement_scale=28,
            fpic_violation_severity=27,
            violence_impunity_defenders=29,
            corporate_accountability_gap=26,
        ),
        LandGrabEntity(
            entity_id="ALG-008",
            name="Pays-Bas / Responsible Business",
            country="Pays-Bas",
            displacement_scale=7,
            fpic_violation_severity=6,
            violence_impunity_defenders=7,
            corporate_accountability_gap=8,
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
        "domain": "agribusiness_land_grab_community_rights",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "displacement_scale": e.displacement_scale,
                "fpic_violation_severity": e.fpic_violation_severity,
                "violence_impunity_defenders": e.violence_impunity_defenders,
                "corporate_accountability_gap": e.corporate_accountability_gap,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_land_grab_rights_index": e.estimated_land_grab_rights_index,
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
