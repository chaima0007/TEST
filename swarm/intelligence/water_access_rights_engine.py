"""
CaelumSwarm™ — Wave 221
Engine  : Water Access Rights
Domain  : Accès à l'eau potable & droits WASH
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
WAVE         = 221
DOMAIN       = "water_access_rights"

WEIGHTS = {
    "water_scarcity_score":              0.30,
    "sanitation_gap_score":              0.25,
    "water_privatization_score":         0.25,
    "climate_water_vulnerability_score": 0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class WAREntity:
    entity_id:                          str
    name:                               str
    country:                            str
    water_scarcity_score:               float
    sanitation_gap_score:               float
    water_privatization_score:          float
    climate_water_vulnerability_score:  float
    primary_pattern:                    str = ""
    last_updated:                       str = "2026-06-22"
    composite_score:                    float = field(init=False)
    risk_level:                         str   = field(init=False)
    estimated_water_access_rights_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.water_scarcity_score              * WEIGHTS["water_scarcity_score"]
            + self.sanitation_gap_score            * WEIGHTS["sanitation_gap_score"]
            + self.water_privatization_score       * WEIGHTS["water_privatization_score"]
            + self.climate_water_vulnerability_score * WEIGHTS["climate_water_vulnerability_score"],
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
# Target composites (approx): 96, 90, 84, 78, 56, 47, 31, 10
# avg target = (96+90+84+78+56+47+31+10)/8 = 492/8 = 61.50  → inside [60, 63]
# composite = water_scarcity×0.30 + sanitation_gap×0.25 + water_privatization×0.25 + climate_water×0.20

ENTITIES: List[WAREntity] = [

    # 1 — critique ~96
    WAREntity(
        entity_id = "WAR-001",
        name      = "Yémen — Guerre Détruisant 50% Infrastructures Eau, 21M Sans Accès Eau Potable & Épidémie Choléra",
        country   = "Yémen",
        water_scarcity_score             = 99.0,
        sanitation_gap_score             = 96.0,
        water_privatization_score        = 94.0,
        climate_water_vulnerability_score = 95.0,
        primary_pattern = "Bombardements infrastructures WASH, choléra 2,5M cas, aquifères surexploités avant guerre",
        # 99×0.30 + 96×0.25 + 94×0.25 + 95×0.20
        # = 29.70 + 24.00 + 23.50 + 19.00 = 96.20
    ),

    # 2 — critique ~90
    WAREntity(
        entity_id = "WAR-002",
        name      = "Éthiopie & Somalie — Sécheresses Horn of Africa, 40M Sans Accès Eau & Crise Humanitaire 2022-2026",
        country   = "Éthiopie/Somalie",
        water_scarcity_score             = 94.0,
        sanitation_gap_score             = 90.0,
        water_privatization_score        = 87.0,
        climate_water_vulnerability_score = 92.0,
        primary_pattern = "5 saisons sèches consécutives, déplacement 4M personnes, aquifères asséchés",
        # 94×0.30 + 90×0.25 + 87×0.25 + 92×0.20
        # = 28.20 + 22.50 + 21.75 + 18.40 = 90.85
    ),

    # 3 — critique ~84
    WAREntity(
        entity_id = "WAR-003",
        name      = "RDC — Kinshasa 15M Habitants, 70% Sans Eau Potable Fiable & Choléra Endémique Zones Rurales",
        country   = "République Démocratique du Congo",
        water_scarcity_score             = 88.0,
        sanitation_gap_score             = 84.0,
        water_privatization_score        = 80.0,
        climate_water_vulnerability_score = 82.0,
        primary_pattern = "Paradoxe eau: 52% ressources eau douce Afrique mais 70% population sans accès fiable",
        # 88×0.30 + 84×0.25 + 80×0.25 + 82×0.20
        # = 26.40 + 21.00 + 20.00 + 16.40 = 83.80
    ),

    # 4 — critique ~78
    WAREntity(
        entity_id = "WAR-004",
        name      = "Gaza & Palestine — Aquifère Côtier 97% Impropre, Eau Dessalée Rationnée 4L/Jour Par Personne",
        country   = "Palestine",
        water_scarcity_score             = 82.0,
        sanitation_gap_score             = 79.0,
        water_privatization_score        = 74.0,
        climate_water_vulnerability_score = 76.0,
        primary_pattern = "Destruction infrastructure eau par conflits, aquifère contaminé sel et nitrates, blocus pièces détachées",
        # 82×0.30 + 79×0.25 + 74×0.25 + 76×0.20
        # = 24.60 + 19.75 + 18.50 + 15.20 = 78.05
    ),

    # 5 — élevé ~56
    WAREntity(
        entity_id = "WAR-005",
        name      = "Inde — 163M Sans Eau Potable Fiable, Gestion Inter-États Conflictuelle & Pollution Industrielle",
        country   = "Inde",
        water_scarcity_score             = 59.0,
        sanitation_gap_score             = 55.0,
        water_privatization_score        = 54.0,
        climate_water_vulnerability_score = 57.0,
        primary_pattern = "Conflits inter-États Cauvery/Krishna, nappes phréatiques surexploitées, inégalités caste/eau",
        # 59×0.30 + 55×0.25 + 54×0.25 + 57×0.20
        # = 17.70 + 13.75 + 13.50 + 11.40 = 56.35
    ),

    # 6 — élevé ~47
    WAREntity(
        entity_id = "WAR-006",
        name      = "Brésil — Privatisation Sabesp & Rio Águas, Favelas & Communautés Périphériques Exclues Services",
        country   = "Brésil",
        water_scarcity_score             = 48.0,
        sanitation_gap_score             = 50.0,
        water_privatization_score        = 46.0,
        climate_water_vulnerability_score = 44.0,
        primary_pattern = "Privatisation services eau Sabesp, sécheresses São Paulo 2015-2021, quilombolas sans accès",
        # 48×0.30 + 50×0.25 + 46×0.25 + 44×0.20
        # = 14.40 + 12.50 + 11.50 + 8.80 = 47.20
    ),

    # 7 — modéré ~31
    WAREntity(
        entity_id = "WAR-007",
        name      = "USA — Crises Flint & Jackson Mississippi, Inégalités Raciales Accès Eau Potable Récurrentes",
        country   = "États-Unis",
        water_scarcity_score             = 30.0,
        sanitation_gap_score             = 28.0,
        water_privatization_score        = 35.0,
        climate_water_vulnerability_score = 32.0,
        primary_pattern = "Plomb dans eau Flint 2014-2019, Jackson sans eau 2022, infrastructures vieillissantes zones pauvres",
        # 30×0.30 + 28×0.25 + 35×0.25 + 32×0.20
        # = 9.00 + 7.00 + 8.75 + 6.40 = 31.15
    ),

    # 8 — faible ~10
    WAREntity(
        entity_id = "WAR-008",
        name      = "Islande, Suède & Finlande — WASH Universel Garanti, Eau Droit Constitutionnel & Qualité Exemplaire",
        country   = "Islande/Suède/Finlande",
        water_scarcity_score             = 8.0,
        sanitation_gap_score             = 10.0,
        water_privatization_score        = 12.0,
        climate_water_vulnerability_score = 9.0,
        primary_pattern = "Eau publique constitutionnellement protégée, 100% accès eau potable, tarification solidaire",
        # 8×0.30 + 10×0.25 + 12×0.25 + 9×0.20
        # = 2.40 + 2.50 + 3.00 + 1.80 = 9.70
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
            f"[{e.entity_id}] {e.name[:45]:<45} "
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
