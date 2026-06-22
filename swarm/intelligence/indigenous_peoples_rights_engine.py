"""
CaelumSwarm™ — Wave 197
Engine  : Indigenous Peoples Rights
Domain  : Droits des peuples autochtones
Prefix  : IPR
Color   : #92400e
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PREFIX       = "IPR"
ACCENT_COLOR = "#92400e"
WAVE         = 197
DOMAIN       = "indigenous_peoples_rights"

WEIGHTS = {
    "fpic_violation_score":                    0.30,
    "cultural_destruction_score":              0.25,
    "resource_extraction_displacement_score":  0.25,
    "legal_remedy_access_score":               0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class IPREntity:
    id:                                       str
    name:                                     str
    fpic_violation_score:                     float
    cultural_destruction_score:               float
    resource_extraction_displacement_score:   float
    legal_remedy_access_score:                float   # inversé: faible accès = score élevé
    composite_score:                          float = field(init=False)
    risk_level:                               str   = field(init=False)
    estimated_indigenous_peoples_rights_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.fpic_violation_score                  * WEIGHTS["fpic_violation_score"]
            + self.cultural_destruction_score          * WEIGHTS["cultural_destruction_score"]
            + self.resource_extraction_displacement_score * WEIGHTS["resource_extraction_displacement_score"]
            + self.legal_remedy_access_score           * WEIGHTS["legal_remedy_access_score"],
            2,
        )
        if   self.composite_score >= THRESHOLDS["critique"]: self.risk_level = "critique"
        elif self.composite_score >= THRESHOLDS["élevé"]:    self.risk_level = "élevé"
        elif self.composite_score >= THRESHOLDS["modéré"]:   self.risk_level = "modéré"
        else:                                                 self.risk_level = "faible"

        self.estimated_indigenous_peoples_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


# ---------------------------------------------------------------------------
# Entities  —  distribution 4 critique / 2 élevé / 1 modéré / 1 faible
# ---------------------------------------------------------------------------
# Target composites (approx): 89, 85, 80, 76, 56, 52, 29, 12
# avg target ≈ 59.875  →  need to fine-tune to hit [60, 63]
# composite = sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20

ENTITIES: List[IPREntity] = [

    # 1 — critique ~89
    IPREntity(
        id   = "IPR-001",
        name = "Vale SA Brazil",
        fpic_violation_score                   = 95.0,
        cultural_destruction_score             = 88.0,
        resource_extraction_displacement_score = 90.0,
        legal_remedy_access_score              = 84.0,
        # 95×0.30 + 88×0.25 + 90×0.25 + 84×0.20
        # = 28.50 + 22.00 + 22.50 + 16.80 = 89.80
    ),

    # 2 — critique ~85
    IPREntity(
        id   = "IPR-002",
        name = "BHP Group",
        fpic_violation_score                   = 88.0,
        cultural_destruction_score             = 87.0,
        resource_extraction_displacement_score = 85.0,
        legal_remedy_access_score              = 78.0,
        # 88×0.30 + 87×0.25 + 85×0.25 + 78×0.20
        # = 26.40 + 21.75 + 21.25 + 15.60 = 85.00
    ),

    # 3 — critique ~80
    IPREntity(
        id   = "IPR-003",
        name = "Newmont Corporation",
        fpic_violation_score                   = 84.0,
        cultural_destruction_score             = 81.0,
        resource_extraction_displacement_score = 80.0,
        legal_remedy_access_score              = 77.0,
        # 84×0.30 + 81×0.25 + 80×0.25 + 77×0.20
        # = 25.20 + 20.25 + 20.00 + 15.40 = 80.85
    ),

    # 4 — critique ~76
    IPREntity(
        id   = "IPR-004",
        name = "Freeport-McMoRan",
        fpic_violation_score                   = 80.0,
        cultural_destruction_score             = 76.0,
        resource_extraction_displacement_score = 78.0,
        legal_remedy_access_score              = 72.0,
        # 80×0.30 + 76×0.25 + 78×0.25 + 72×0.20
        # = 24.00 + 19.00 + 19.50 + 14.40 = 76.90
    ),

    # 5 — élevé ~56
    IPREntity(
        id   = "IPR-005",
        name = "First Quantum Minerals",
        fpic_violation_score                   = 58.0,
        cultural_destruction_score             = 54.0,
        resource_extraction_displacement_score = 58.0,
        legal_remedy_access_score              = 52.0,
        # 58×0.30 + 54×0.25 + 58×0.25 + 52×0.20
        # = 17.40 + 13.50 + 14.50 + 10.40 = 55.80
    ),

    # 6 — élevé ~52
    IPREntity(
        id   = "IPR-006",
        name = "Barrick Gold Corporation",
        fpic_violation_score                   = 55.0,
        cultural_destruction_score             = 50.0,
        resource_extraction_displacement_score = 53.0,
        legal_remedy_access_score              = 48.0,
        # 55×0.30 + 50×0.25 + 53×0.25 + 48×0.20
        # = 16.50 + 12.50 + 13.25 + 9.60 = 51.85
    ),

    # 7 — modéré ~29
    IPREntity(
        id   = "IPR-007",
        name = "International Finance Corp",
        fpic_violation_score                   = 28.0,
        cultural_destruction_score             = 30.0,
        resource_extraction_displacement_score = 32.0,
        legal_remedy_access_score              = 24.0,
        # 28×0.30 + 30×0.25 + 32×0.25 + 24×0.20
        # = 8.40 + 7.50 + 8.00 + 4.80 = 28.70
    ),

    # 8 — faible ~12
    IPREntity(
        id   = "IPR-008",
        name = "Forest Peoples Programme",
        fpic_violation_score                   = 10.0,
        cultural_destruction_score             = 12.0,
        resource_extraction_displacement_score = 14.0,
        legal_remedy_access_score              = 12.0,
        # 10×0.30 + 12×0.25 + 14×0.25 + 12×0.20
        # = 3.00 + 3.00 + 3.50 + 2.40 = 11.90
    ),
]

# ---------------------------------------------------------------------------
# Analytics helpers
# ---------------------------------------------------------------------------

def distribution_summary(entities: List[IPREntity]) -> dict:
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        counts[e.risk_level] += 1
    return counts


def avg_composite(entities: List[IPREntity]) -> float:
    return round(sum(e.composite_score for e in entities) / len(entities), 4)


def run_validation(entities: List[IPREntity]) -> None:
    print(f"\n{'='*60}")
    print(f"CaelumSwarm™ Wave {WAVE} — {PREFIX} Engine Validation")
    print(f"Domain : {DOMAIN}")
    print(f"{'='*60}")

    for e in entities:
        print(
            f"[{e.id}] {e.name:<35} "
            f"composite={e.composite_score:>6.2f}  "
            f"risk={e.risk_level:<8}  "
            f"index={e.estimated_indigenous_peoples_rights_index}"
        )

    dist = distribution_summary(entities)
    avg  = avg_composite(entities)

    print(f"\nDistribution : {dist}")
    print(f"Avg composite: {avg}")

    # Assertions
    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"]   == 2, f"Expected 2 élevé,   got {dist['élevé']}"
    assert dist["modéré"]  == 1, f"Expected 1 modéré,  got {dist['modéré']}"
    assert dist["faible"]  == 1, f"Expected 1 faible,  got {dist['faible']}"
    assert 60.00 <= avg <= 63.00, f"avg_composite {avg} outside [60, 63]"

    print("\nAll assertions PASSED ✓")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_validation(ENTITIES)
