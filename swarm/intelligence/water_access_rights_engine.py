"""
CaelumSwarm™ — Wave 197
Engine  : Water Access Rights
Domain  : Accès à l'eau potable et droits humains
Prefix  : WAR
Color   : #0ea5e9
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PREFIX       = "WAR"
ACCENT_COLOR = "#0ea5e9"
WAVE         = 197
DOMAIN       = "water_access_rights"

WEIGHTS = {
    "water_privatization_harm_score": 0.30,
    "water_pollution_score":          0.25,
    "access_denial_marginalized_score": 0.25,
    "conservation_failure_score":     0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class WAREntity:
    id:                                str
    name:                              str
    water_privatization_harm_score:    float
    water_pollution_score:             float
    access_denial_marginalized_score:  float
    conservation_failure_score:        float
    composite_score:                   float = field(init=False)
    risk_level:                        str   = field(init=False)
    estimated_water_access_rights_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.water_privatization_harm_score * WEIGHTS["water_privatization_harm_score"]
            + self.water_pollution_score        * WEIGHTS["water_pollution_score"]
            + self.access_denial_marginalized_score * WEIGHTS["access_denial_marginalized_score"]
            + self.conservation_failure_score   * WEIGHTS["conservation_failure_score"],
            2,
        )
        if   self.composite_score >= THRESHOLDS["critique"]: self.risk_level = "critique"
        elif self.composite_score >= THRESHOLDS["élevé"]:    self.risk_level = "élevé"
        elif self.composite_score >= THRESHOLDS["modéré"]:   self.risk_level = "modéré"
        else:                                                 self.risk_level = "faible"

        self.estimated_water_access_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


# ---------------------------------------------------------------------------
# Entities  —  distribution 4 critique / 2 élevé / 1 modéré / 1 faible
# ---------------------------------------------------------------------------
# Target composites (approx): 88, 84, 81, 77, 57, 53, 28, 13
# avg target ≈ 60.25  →  inside [60, 63]
# composite = sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20

ENTITIES: List[WAREntity] = [

    # 1 — critique ~88
    WAREntity(
        id   = "WAR-001",
        name = "Nestlé Waters",
        water_privatization_harm_score   = 95.0,
        water_pollution_score            = 82.0,
        access_denial_marginalized_score = 90.0,
        conservation_failure_score       = 84.0,
        # 95×0.30 + 82×0.25 + 90×0.25 + 84×0.20
        # = 28.50 + 20.50 + 22.50 + 16.80 = 88.30
    ),

    # 2 — critique ~84
    WAREntity(
        id   = "WAR-002",
        name = "Suez Water Technologies",
        water_privatization_harm_score   = 90.0,
        water_pollution_score            = 78.0,
        access_denial_marginalized_score = 86.0,
        conservation_failure_score       = 80.0,
        # 90×0.30 + 78×0.25 + 86×0.25 + 80×0.20
        # = 27.00 + 19.50 + 21.50 + 16.00 = 84.00
    ),

    # 3 — critique ~81
    WAREntity(
        id   = "WAR-003",
        name = "Veolia Water",
        water_privatization_harm_score   = 85.0,
        water_pollution_score            = 79.0,
        access_denial_marginalized_score = 80.0,
        conservation_failure_score       = 78.0,
        # 85×0.30 + 79×0.25 + 80×0.25 + 78×0.20
        # = 25.50 + 19.75 + 20.00 + 15.60 = 80.85
    ),

    # 4 — critique ~77
    WAREntity(
        id   = "WAR-004",
        name = "POSCO Holdings",
        water_privatization_harm_score   = 72.0,
        water_pollution_score            = 85.0,
        access_denial_marginalized_score = 78.0,
        conservation_failure_score       = 74.0,
        # 72×0.30 + 85×0.25 + 78×0.25 + 74×0.20
        # = 21.60 + 21.25 + 19.50 + 14.80 = 77.15
    ),

    # 5 — élevé ~57
    WAREntity(
        id   = "WAR-005",
        name = "Coca-Cola Company",
        water_privatization_harm_score   = 58.0,
        water_pollution_score            = 54.0,
        access_denial_marginalized_score = 60.0,
        conservation_failure_score       = 55.0,
        # 58×0.30 + 54×0.25 + 60×0.25 + 55×0.20
        # = 17.40 + 13.50 + 15.00 + 11.00 = 56.90
    ),

    # 6 — élevé ~53
    WAREntity(
        id   = "WAR-006",
        name = "PepsiCo Inc",
        water_privatization_harm_score   = 53.0,
        water_pollution_score            = 50.0,
        access_denial_marginalized_score = 56.0,
        conservation_failure_score       = 51.0,
        # 53×0.30 + 50×0.25 + 56×0.25 + 51×0.20
        # = 15.90 + 12.50 + 14.00 + 10.20 = 52.60
    ),

    # 7 — modéré ~28
    WAREntity(
        id   = "WAR-007",
        name = "Thames Water",
        water_privatization_harm_score   = 30.0,
        water_pollution_score            = 32.0,
        access_denial_marginalized_score = 22.0,
        conservation_failure_score       = 28.0,
        # 30×0.30 + 32×0.25 + 22×0.25 + 28×0.20
        # = 9.00 + 8.00 + 5.50 + 5.60 = 28.10
    ),

    # 8 — faible ~13
    WAREntity(
        id   = "WAR-008",
        name = "Xylem Inc",
        water_privatization_harm_score   = 10.0,
        water_pollution_score            = 12.0,
        access_denial_marginalized_score = 15.0,
        conservation_failure_score       = 14.0,
        # 10×0.30 + 12×0.25 + 15×0.25 + 14×0.20
        # = 3.00 + 3.00 + 3.75 + 2.80 = 12.55
    ),
]

# ---------------------------------------------------------------------------
# Analytics helpers
# ---------------------------------------------------------------------------

def distribution_summary(entities: List[WAREntity]) -> dict:
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        counts[e.risk_level] += 1
    return counts


def avg_composite(entities: List[WAREntity]) -> float:
    return round(sum(e.composite_score for e in entities) / len(entities), 4)


def run_validation(entities: List[WAREntity]) -> None:
    print(f"\n{'='*60}")
    print(f"CaelumSwarm™ Wave {WAVE} — {PREFIX} Engine Validation")
    print(f"Domain : {DOMAIN}")
    print(f"{'='*60}")

    for e in entities:
        print(
            f"[{e.id}] {e.name:<35} "
            f"composite={e.composite_score:>6.2f}  "
            f"risk={e.risk_level:<8}  "
            f"index={e.estimated_water_access_rights_index}"
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
