"""
CaelumSwarm™ — Wave 221
Engine  : Statelessness Rights
Domain  : Apatridie & droits des personnes sans nationalité
Prefix  : SRE
Color   : #f59e0b
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PREFIX       = "SRE"
ACCENT_COLOR = "#f59e0b"
WAVE         = 221
DOMAIN       = "statelessness_rights"

WEIGHTS = {
    "citizenship_denial_score":          0.30,
    "legal_identity_gap_score":          0.25,
    "stateless_detention_score":         0.25,
    "generational_statelessness_score":  0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class SREEntity:
    entity_id:                          str
    name:                               str
    country:                            str
    citizenship_denial_score:           float
    legal_identity_gap_score:           float
    stateless_detention_score:          float
    generational_statelessness_score:   float
    primary_pattern:                    str = ""
    last_updated:                       str = "2026-06-22"
    composite_score:                    float = field(init=False)
    risk_level:                         str   = field(init=False)
    estimated_statelessness_rights_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.citizenship_denial_score         * WEIGHTS["citizenship_denial_score"]
            + self.legal_identity_gap_score       * WEIGHTS["legal_identity_gap_score"]
            + self.stateless_detention_score      * WEIGHTS["stateless_detention_score"]
            + self.generational_statelessness_score * WEIGHTS["generational_statelessness_score"],
            2,
        )
        if   self.composite_score >= THRESHOLDS["critique"]: self.risk_level = "critique"
        elif self.composite_score >= THRESHOLDS["élevé"]:    self.risk_level = "élevé"
        elif self.composite_score >= THRESHOLDS["modéré"]:   self.risk_level = "modéré"
        else:                                                 self.risk_level = "faible"

        self.estimated_statelessness_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


# ---------------------------------------------------------------------------
# Entities  —  distribution 4 critique / 2 élevé / 1 modéré / 1 faible
# ---------------------------------------------------------------------------
# Target composites (approx): 96, 91, 86, 80, 57, 47, 32, 11
# avg target = (96+91+86+80+57+47+32+11)/8 = 500/8 = 62.50  → inside [60, 63]
# composite = citizenship×0.30 + legal_id×0.25 + detention×0.25 + generational×0.20

ENTITIES: List[SREEntity] = [

    # 1 — critique ~96
    SREEntity(
        entity_id = "SRE-001",
        name      = "Myanmar — Rohingya 900 000 Apatrides, NCA 1982 Dénie Nationalité & Camps Cox's Bazar Bangladesh",
        country   = "Myanmar",
        citizenship_denial_score          = 99.0,
        legal_identity_gap_score          = 96.0,
        stateless_detention_score         = 95.0,
        generational_statelessness_score  = 93.0,
        primary_pattern = "Exclusion légale systématique, génocide ICJ 2019, transmission apatridie sur 3 générations",
        # 99×0.30 + 96×0.25 + 95×0.25 + 93×0.20
        # = 29.70 + 24.00 + 23.75 + 18.60 = 96.05
    ),

    # 2 — critique ~91
    SREEntity(
        entity_id = "SRE-002",
        name      = "Koweït — Bidun 100 000 Résidents Sans Nationalité Depuis 1961 & Zéro Droits Civils",
        country   = "Koweït",
        citizenship_denial_score          = 95.0,
        legal_identity_gap_score          = 91.0,
        stateless_detention_score         = 90.0,
        generational_statelessness_score  = 88.0,
        primary_pattern = "Résidents de longue date exclus au moment de l'indépendance, héritage statut apatride",
        # 95×0.30 + 91×0.25 + 90×0.25 + 88×0.20
        # = 28.50 + 22.75 + 22.50 + 17.60 = 91.35
    ),

    # 3 — critique ~86
    SREEntity(
        entity_id = "SRE-003",
        name      = "République Dominicaine — Dénationalisation Haïtiens TC 168-13, 210 000 Apatrides Rétroactifs",
        country   = "République Dominicaine",
        citizenship_denial_score          = 90.0,
        legal_identity_gap_score          = 85.0,
        stateless_detention_score         = 84.0,
        generational_statelessness_score  = 82.0,
        primary_pattern = "Dénationalisation rétroactive, expulsions sans procédure légale, enfants nés sur territoire exclus",
        # 90×0.30 + 85×0.25 + 84×0.25 + 82×0.20
        # = 27.00 + 21.25 + 21.00 + 16.40 = 85.65
    ),

    # 4 — critique ~80
    SREEntity(
        entity_id = "SRE-004",
        name      = "Côte d'Ivoire — 700 000 Apatrides Post-Conflit, Communautés Nordistes Sans Documents Officiels",
        country   = "Côte d'Ivoire",
        citizenship_denial_score          = 82.0,
        legal_identity_gap_score          = 80.0,
        stateless_detention_score         = 78.0,
        generational_statelessness_score  = 80.0,
        primary_pattern = "Crise ivoirité, exclusion identitaire nord vs sud, enfants non enregistrés à la naissance",
        # 82×0.30 + 80×0.25 + 78×0.25 + 80×0.20
        # = 24.60 + 20.00 + 19.50 + 16.00 = 80.10
    ),

    # 5 — élevé ~57
    SREEntity(
        entity_id = "SRE-005",
        name      = "Thaïlande — 480 000 Highlanders Sans Nationalité, Enfants Nés Apatrides & Risque Traite",
        country   = "Thaïlande",
        citizenship_denial_score          = 60.0,
        legal_identity_gap_score          = 57.0,
        stateless_detention_score         = 55.0,
        generational_statelessness_score  = 56.0,
        primary_pattern = "Tribus montagnardes exclues, accès refusé santé et éducation, transmission apatridie aux enfants",
        # 60×0.30 + 57×0.25 + 55×0.25 + 56×0.20
        # = 18.00 + 14.25 + 13.75 + 11.20 = 57.20
    ),

    # 6 — élevé ~47
    SREEntity(
        entity_id = "SRE-006",
        name      = "Lettonie — 200 000 Non-Citoyens Post-URSS, Russophones Sans Passeport UE & Droits Limités",
        country   = "Lettonie",
        citizenship_denial_score          = 48.0,
        legal_identity_gap_score          = 46.0,
        stateless_detention_score         = 46.0,
        generational_statelessness_score  = 48.0,
        primary_pattern = "Statut non-citoyen spécifique, résidents de longue date exclus de la citoyenneté post-indépendance",
        # 48×0.30 + 46×0.25 + 46×0.25 + 48×0.20
        # = 14.40 + 11.50 + 11.50 + 9.60 = 47.00
    ),

    # 7 — modéré ~32
    SREEntity(
        entity_id = "SRE-007",
        name      = "Syrie — Exil Masse & Perte Documentation, 5M Réfugiés Sans Accès Registre Civil Détruit",
        country   = "Syrie",
        citizenship_denial_score          = 30.0,
        legal_identity_gap_score          = 35.0,
        stateless_detention_score         = 33.0,
        generational_statelessness_score  = 28.0,
        primary_pattern = "Destruction registres civils, enfants exil non enregistrés, risque apatridie de facto croissant",
        # 30×0.30 + 35×0.25 + 33×0.25 + 28×0.20
        # = 9.00 + 8.75 + 8.25 + 5.60 = 31.60
    ),

    # 8 — faible ~11
    SREEntity(
        entity_id = "SRE-008",
        name      = "UNHCR — Programme #IBelong 2014-2024, Réduction Apatridie 500 000 Personnes Naturalisées",
        country   = "International",
        citizenship_denial_score          = 10.0,
        legal_identity_gap_score          = 12.0,
        stateless_detention_score         = 11.0,
        generational_statelessness_score  = 10.0,
        primary_pattern = "Meilleure pratique internationale, campagnes naturalisation, coopération états membres",
        # 10×0.30 + 12×0.25 + 11×0.25 + 10×0.20
        # = 3.00 + 3.00 + 2.75 + 2.00 = 10.75
    ),
]

# ---------------------------------------------------------------------------
# Analytics helpers
# ---------------------------------------------------------------------------

def distribution_summary(entities: List[SREEntity]) -> dict:
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        counts[e.risk_level] += 1
    return counts


def avg_composite(entities: List[SREEntity]) -> float:
    return round(sum(e.composite_score for e in entities) / len(entities), 4)


def run_validation(entities: List[SREEntity]) -> None:
    print(f"\n{'='*60}")
    print(f"CaelumSwarm™ Wave {WAVE} — {PREFIX} Engine Validation")
    print(f"Domain : {DOMAIN}")
    print(f"{'='*60}")

    for e in entities:
        print(
            f"[{e.entity_id}] {e.name[:45]:<45} "
            f"composite={e.composite_score:>6.2f}  "
            f"risk={e.risk_level:<8}  "
            f"index={e.estimated_statelessness_rights_index}"
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
