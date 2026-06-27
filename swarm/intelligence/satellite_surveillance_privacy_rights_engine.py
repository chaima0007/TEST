#!/usr/bin/env python3
from dataclasses import dataclass, field
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Surveillance de masse par satellite & collecte de données
    sub2: float  # Violations du droit à la vie privée & ciblage de populations
    sub3: float  # Absence de cadre légal & supervision démocratique
    sub4: float  # Recours & protection des droits des personnes surveillées
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20) * 10, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_index = round(self.composite_score / 100 * 10, 2)


def run_satellite_surveillance_privacy_rights_analysis():
    entities = [
        EntityScore(
            entity_id="sspr_001",
            name="Chine — BeiDou & surveillance Xinjiang/Tibet par satellite",
            sub1=9.8, sub2=9.7, sub3=9.9, sub4=9.6
        ),
        EntityScore(
            entity_id="sspr_002",
            name="NSA/GCHQ — Programme PRISM & surveillance globale (Five Eyes)",
            sub1=9.4, sub2=9.0, sub3=9.2, sub4=8.8
        ),
        EntityScore(
            entity_id="sspr_003",
            name="Russie — SORM & surveillance satellites Krasukha ciblée",
            sub1=9.1, sub2=8.8, sub3=9.3, sub4=8.5
        ),
        EntityScore(
            entity_id="sspr_004",
            name="Israël — Technologie Pegasus & ciblage satellite journalistes",
            sub1=8.6, sub2=9.2, sub3=8.4, sub4=9.0
        ),
        EntityScore(
            entity_id="sspr_005",
            name="Inde — NETRA & surveillance satellitaire minorités",
            sub1=5.6, sub2=5.4, sub3=5.8, sub4=5.2
        ),
        EntityScore(
            entity_id="sspr_006",
            name="Émirats Arabes Unis — Karma & espionnage régional",
            sub1=5.0, sub2=5.5, sub3=5.2, sub4=4.8
        ),
        EntityScore(
            entity_id="sspr_007",
            name="Brésil — Surveillance contestataires Amazon & MST",
            sub1=3.8, sub2=3.5, sub3=4.0, sub4=3.2
        ),
        EntityScore(
            entity_id="sspr_008",
            name="UE — GDPR & Parlement européen résolution surveillance",
            sub1=1.5, sub2=1.3, sub3=1.8, sub4=1.0
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_mass_surveillance": e.sub1,
            "sub2_privacy_rights_violations": e.sub2,
            "sub3_no_legal_oversight": e.sub3,
            "sub4_redress_protection": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_satellite_surveillance_index": e.estimated_index,
        })

    results.sort(key=lambda x: x["composite_score"], reverse=True)

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "satellite_surveillance_privacy_rights_engine",
        "wave": 146,
        "domain": "Surveillance satellitaire & droits à la vie privée",
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    print(f"\n--- VALIDATION ---")
    print(f"avg_composite : {avg_composite}")
    print(f"Distribution  : {distribution}")
    for r in results:
        print(f"  [{r['risk_level']:8s}] {r['composite_score']:5.2f}  {r['name']}")

    assert distribution.get("critique", 0) == 4, f"Attendu 4 critique, obtenu {distribution.get('critique', 0)}"
    assert distribution.get("élevé", 0) == 2, f"Attendu 2 élevé, obtenu {distribution.get('élevé', 0)}"
    assert distribution.get("modéré", 0) == 1, f"Attendu 1 modéré, obtenu {distribution.get('modéré', 0)}"
    assert distribution.get("faible", 0) == 1, f"Attendu 1 faible, obtenu {distribution.get('faible', 0)}"
    assert 58 <= avg_composite <= 68, f"avg_composite hors plage [58-68]: {avg_composite}"
    print("✓ Toutes les assertions passent.")


if __name__ == "__main__":
    run_satellite_surveillance_privacy_rights_analysis()
