#!/usr/bin/env python3
"""Wave 174 — Biometric Border Surveillance Migration Engine — Caelum Partners SPRL"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BiometricBorderEntity:
    entity_id: str
    name: str
    country: str
    pushback_violence_scale: float
    biometric_overreach: float
    detention_condition_severity: float
    legal_protection_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_border_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.pushback_violence_scale * 0.30
            + self.biometric_overreach * 0.25
            + self.detention_condition_severity * 0.25
            + self.legal_protection_gap * 0.20,
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
        self.estimated_border_rights_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> dict:
    entities = [
        BiometricBorderEntity(
            entity_id="BBM-001",
            name="Libye / Gardes-Côtes",
            country="Libye",
            pushback_violence_scale=95,
            biometric_overreach=88,
            detention_condition_severity=92,
            legal_protection_gap=86,
        ),
        BiometricBorderEntity(
            entity_id="BBM-002",
            name="Grèce / Pushbacks Égée",
            country="Grèce",
            pushback_violence_scale=86,
            biometric_overreach=80,
            detention_condition_severity=82,
            legal_protection_gap=78,
        ),
        BiometricBorderEntity(
            entity_id="BBM-003",
            name="USA / CBP Frontière Sud",
            country="États-Unis",
            pushback_violence_scale=80,
            biometric_overreach=78,
            detention_condition_severity=77,
            legal_protection_gap=76,
        ),
        BiometricBorderEntity(
            entity_id="BBM-004",
            name="Turquie / Frontière Syrie-Iran",
            country="Turquie",
            pushback_violence_scale=77,
            biometric_overreach=72,
            detention_condition_severity=74,
            legal_protection_gap=70,
        ),
        BiometricBorderEntity(
            entity_id="BBM-005",
            name="Hongrie / Clôture Serbie",
            country="Hongrie",
            pushback_violence_scale=56,
            biometric_overreach=52,
            detention_condition_severity=54,
            legal_protection_gap=48,
        ),
        BiometricBorderEntity(
            entity_id="BBM-006",
            name="Australie / Offshore Processing",
            country="Australie",
            pushback_violence_scale=48,
            biometric_overreach=46,
            detention_condition_severity=50,
            legal_protection_gap=42,
        ),
        BiometricBorderEntity(
            entity_id="BBM-007",
            name="Canada / Safe Third Country",
            country="Canada",
            pushback_violence_scale=28,
            biometric_overreach=26,
            detention_condition_severity=27,
            legal_protection_gap=26,
        ),
        BiometricBorderEntity(
            entity_id="BBM-008",
            name="Allemagne / Système EUAA",
            country="Allemagne",
            pushback_violence_scale=8,
            biometric_overreach=7,
            detention_condition_severity=9,
            legal_protection_gap=8,
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
        "domain": "biometric_border_surveillance_migration",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "pushback_violence_scale": e.pushback_violence_scale,
                "biometric_overreach": e.biometric_overreach,
                "detention_condition_severity": e.detention_condition_severity,
                "legal_protection_gap": e.legal_protection_gap,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_border_rights_index": e.estimated_border_rights_index,
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
