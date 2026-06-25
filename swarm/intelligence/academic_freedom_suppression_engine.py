"""
CaelumSwarm™ — Wave 197
Engine  : Academic Freedom Suppression
Domain  : Suppression de la liberté académique
Prefix  : AFS
Color   : #7c3aed
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PREFIX       = "AFS"
ACCENT_COLOR = "#7c3aed"
WAVE         = 197
DOMAIN       = "academic_freedom_suppression"

WEIGHTS = {
    "researcher_imprisonment_score":               0.30,
    "curriculum_political_control_score":          0.25,
    "publication_censorship_score":                0.25,
    "international_collaboration_restriction_score": 0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class AFSEntity:
    id:                                              str
    name:                                            str
    researcher_imprisonment_score:                   float
    curriculum_political_control_score:              float
    publication_censorship_score:                    float
    international_collaboration_restriction_score:   float
    composite_score:                                 float = field(init=False)
    risk_level:                                      str   = field(init=False)
    estimated_academic_freedom_suppression_index:    float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.researcher_imprisonment_score              * WEIGHTS["researcher_imprisonment_score"]
            + self.curriculum_political_control_score       * WEIGHTS["curriculum_political_control_score"]
            + self.publication_censorship_score             * WEIGHTS["publication_censorship_score"]
            + self.international_collaboration_restriction_score * WEIGHTS["international_collaboration_restriction_score"],
            2,
        )
        if   self.composite_score >= THRESHOLDS["critique"]: self.risk_level = "critique"
        elif self.composite_score >= THRESHOLDS["élevé"]:    self.risk_level = "élevé"
        elif self.composite_score >= THRESHOLDS["modéré"]:   self.risk_level = "modéré"
        else:                                                 self.risk_level = "faible"

        self.estimated_academic_freedom_suppression_index = round(
            self.composite_score / 100 * 10, 2
        )


# ---------------------------------------------------------------------------
# Entities  —  distribution 4 critique / 2 élevé / 1 modéré / 1 faible
# ---------------------------------------------------------------------------
# Target composites (approx): 91, 85, 82, 76, 58, 54, 26, 11
# avg target ≈ 60.375  →  inside [60, 63]
# composite = sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20

ENTITIES: List[AFSEntity] = [

    # 1 — critique ~91
    AFSEntity(
        id   = "AFS-001",
        name = "Chinese Ministry of Education",
        researcher_imprisonment_score                  = 95.0,
        curriculum_political_control_score             = 92.0,
        publication_censorship_score                   = 90.0,
        international_collaboration_restriction_score  = 86.0,
        # 95×0.30 + 92×0.25 + 90×0.25 + 86×0.20
        # = 28.50 + 23.00 + 22.50 + 17.20 = 91.20
    ),

    # 2 — critique ~85
    AFSEntity(
        id   = "AFS-002",
        name = "Turkish Ministry of National Education",
        researcher_imprisonment_score                  = 90.0,
        curriculum_political_control_score             = 84.0,
        publication_censorship_score                   = 84.0,
        international_collaboration_restriction_score  = 80.0,
        # 90×0.30 + 84×0.25 + 84×0.25 + 80×0.20
        # = 27.00 + 21.00 + 21.00 + 16.00 = 85.00
    ),

    # 3 — critique ~82
    AFSEntity(
        id   = "AFS-003",
        name = "Iranian Ministry of Science",
        researcher_imprisonment_score                  = 88.0,
        curriculum_political_control_score             = 80.0,
        publication_censorship_score                   = 81.0,
        international_collaboration_restriction_score  = 77.0,
        # 88×0.30 + 80×0.25 + 81×0.25 + 77×0.20
        # = 26.40 + 20.00 + 20.25 + 15.40 = 82.05
    ),

    # 4 — critique ~76
    AFSEntity(
        id   = "AFS-004",
        name = "Saudi Ministry of Education",
        researcher_imprisonment_score                  = 74.0,
        curriculum_political_control_score             = 80.0,
        publication_censorship_score                   = 78.0,
        international_collaboration_restriction_score  = 70.0,
        # 74×0.30 + 80×0.25 + 78×0.25 + 70×0.20
        # = 22.20 + 20.00 + 19.50 + 14.00 = 75.70
    ),

    # 5 — élevé ~58
    AFSEntity(
        id   = "AFS-005",
        name = "Russian Federal Agency on Education",
        researcher_imprisonment_score                  = 60.0,
        curriculum_political_control_score             = 57.0,
        publication_censorship_score                   = 58.0,
        international_collaboration_restriction_score  = 56.0,
        # 60×0.30 + 57×0.25 + 58×0.25 + 56×0.20
        # = 18.00 + 14.25 + 14.50 + 11.20 = 57.95
    ),

    # 6 — élevé ~54
    AFSEntity(
        id   = "AFS-006",
        name = "Hungarian Government / Orbán Education Reforms",
        researcher_imprisonment_score                  = 52.0,
        curriculum_political_control_score             = 56.0,
        publication_censorship_score                   = 55.0,
        international_collaboration_restriction_score  = 52.0,
        # 52×0.30 + 56×0.25 + 55×0.25 + 52×0.20
        # = 15.60 + 14.00 + 13.75 + 10.40 = 53.75
    ),

    # 7 — modéré ~26
    AFSEntity(
        id   = "AFS-007",
        name = "UNESCO",
        researcher_imprisonment_score                  = 24.0,
        curriculum_political_control_score             = 28.0,
        publication_censorship_score                   = 26.0,
        international_collaboration_restriction_score  = 24.0,
        # 24×0.30 + 28×0.25 + 26×0.25 + 24×0.20
        # = 7.20 + 7.00 + 6.50 + 4.80 = 25.50
    ),

    # 8 — faible ~11
    AFSEntity(
        id   = "AFS-008",
        name = "Scholars at Risk Network",
        researcher_imprisonment_score                  = 10.0,
        curriculum_political_control_score             = 11.0,
        publication_censorship_score                   = 12.0,
        international_collaboration_restriction_score  = 10.0,
        # 10×0.30 + 11×0.25 + 12×0.25 + 10×0.20
        # = 3.00 + 2.75 + 3.00 + 2.00 = 10.75
    ),
]

# ---------------------------------------------------------------------------
# Analytics helpers
# ---------------------------------------------------------------------------

def distribution_summary(entities: List[AFSEntity]) -> dict:
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        counts[e.risk_level] += 1
    return counts


def avg_composite(entities: List[AFSEntity]) -> float:
    return round(sum(e.composite_score for e in entities) / len(entities), 4)


def run_validation(entities: List[AFSEntity]) -> None:
    print(f"\n{'='*60}")
    print(f"CaelumSwarm™ Wave {WAVE} — {PREFIX} Engine Validation")
    print(f"Domain : {DOMAIN}")
    print(f"{'='*60}")

    for e in entities:
        print(
            f"[{e.id}] {e.name:<45} "
            f"composite={e.composite_score:>6.2f}  "
            f"risk={e.risk_level:<8}  "
            f"index={e.estimated_academic_freedom_suppression_index}"
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
