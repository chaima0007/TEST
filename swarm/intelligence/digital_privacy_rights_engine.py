"""
CaelumSwarm™ — Wave 221
Engine  : Digital Privacy Rights
Domain  : Vie privée numérique & surveillance de masse
Prefix  : DPR
Color   : #8b5cf6
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PREFIX       = "DPR"
ACCENT_COLOR = "#8b5cf6"
WAVE         = 221
DOMAIN       = "digital_privacy_rights"

WEIGHTS = {
    "mass_surveillance_score":      0.30,
    "facial_recognition_score":     0.25,
    "data_rights_score":            0.25,
    "encryption_restriction_score": 0.20,
}

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class DPREntity:
    entity_id:                      str
    name:                           str
    country:                        str
    mass_surveillance_score:        float
    facial_recognition_score:       float
    data_rights_score:              float
    encryption_restriction_score:   float
    primary_pattern:                str = ""
    last_updated:                   str = "2026-06-22"
    composite_score:                float = field(init=False)
    risk_level:                     str   = field(init=False)
    estimated_digital_privacy_rights_index: float = field(init=False)

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.mass_surveillance_score       * WEIGHTS["mass_surveillance_score"]
            + self.facial_recognition_score    * WEIGHTS["facial_recognition_score"]
            + self.data_rights_score           * WEIGHTS["data_rights_score"]
            + self.encryption_restriction_score * WEIGHTS["encryption_restriction_score"],
            2,
        )
        if   self.composite_score >= THRESHOLDS["critique"]: self.risk_level = "critique"
        elif self.composite_score >= THRESHOLDS["élevé"]:    self.risk_level = "élevé"
        elif self.composite_score >= THRESHOLDS["modéré"]:   self.risk_level = "modéré"
        else:                                                 self.risk_level = "faible"

        self.estimated_digital_privacy_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


# ---------------------------------------------------------------------------
# Entities  —  distribution 4 critique / 2 élevé / 1 modéré / 1 faible
# ---------------------------------------------------------------------------
# Target composites (approx): 97, 94, 88, 80, 55, 48, 28, 12
# avg target = (97+94+88+80+55+48+28+12)/8 = 502/8 = 62.75  → inside [60, 63]
# composite = mass_surv×0.30 + facial_rec×0.25 + data_rights×0.25 + encryption×0.20

ENTITIES: List[DPREntity] = [

    # 1 — critique ~97
    DPREntity(
        entity_id = "DPR-001",
        name      = "Chine — SCS 1,4Mrd Personnes Notées, 700M Caméras IA & Surveillance Ouïghours Xinjiang Totale",
        country   = "Chine",
        mass_surveillance_score      = 99.0,
        facial_recognition_score     = 99.0,
        data_rights_score            = 97.0,
        encryption_restriction_score = 95.0,
        primary_pattern = "Système crédit social, reconnaissance faciale urbaine en temps réel, internement Ouïghours via IA",
        # 99×0.30 + 99×0.25 + 97×0.25 + 95×0.20
        # = 29.70 + 24.75 + 24.25 + 19.00 = 97.70
    ),

    # 2 — critique ~94
    DPREntity(
        entity_id = "DPR-002",
        name      = "Corée du Nord — Surveillance Totalitaire, Intranet Kwangmyong & Espionnage Citoyens Par Voisins",
        country   = "Corée du Nord",
        mass_surveillance_score      = 98.0,
        facial_recognition_score     = 84.0,
        data_rights_score            = 96.0,
        encryption_restriction_score = 97.0,
        primary_pattern = "Isolation digitale totale, intranet national, délateurs institutionnels, exécution pour contenu étranger",
        # 98×0.30 + 84×0.25 + 96×0.25 + 97×0.20
        # = 29.40 + 21.00 + 24.00 + 19.40 = 93.80
    ),

    # 3 — critique ~88
    DPREntity(
        entity_id = "DPR-003",
        name      = "Iran — FATA Cyber Police, Blocage VPN 99% & Surveillance IRIB Dissidents & Femmes Voilées",
        country   = "Iran",
        mass_surveillance_score      = 91.0,
        facial_recognition_score     = 87.0,
        data_rights_score            = 88.0,
        encryption_restriction_score = 86.0,
        primary_pattern = "Internet national isolé, arrestations VPN, reconnaissance faciale pour contrôle hijab depuis 2023",
        # 91×0.30 + 87×0.25 + 88×0.25 + 86×0.20
        # = 27.30 + 21.75 + 22.00 + 17.20 = 88.25
    ),

    # 4 — critique ~80
    DPREntity(
        entity_id = "DPR-004",
        name      = "Russie — Système SORM, Lois Yarovaya 2016 & RuNet Isolement Progressif Post-Invasion Ukraine",
        country   = "Russie",
        mass_surveillance_score      = 84.0,
        facial_recognition_score     = 80.0,
        data_rights_score            = 79.0,
        encryption_restriction_score = 77.0,
        primary_pattern = "SORM-3 interception obligatoire, filtrage DPI, arrestations VPN, blocage 300 000 sites",
        # 84×0.30 + 80×0.25 + 79×0.25 + 77×0.20
        # = 25.20 + 20.00 + 19.75 + 15.40 = 80.35
    ),

    # 5 — élevé ~55
    DPREntity(
        entity_id = "DPR-005",
        name      = "USA — NSA PRISM & XKeyscore, Section 702 FISA, Clearview AI 30Mrd Photos & Absence Loi Fédérale",
        country   = "États-Unis",
        mass_surveillance_score      = 57.0,
        facial_recognition_score     = 58.0,
        data_rights_score            = 52.0,
        encryption_restriction_score = 53.0,
        primary_pattern = "Surveillance NSA globale révélations Snowden, Clearview AI police, pas de loi fédérale vie privée",
        # 57×0.30 + 58×0.25 + 52×0.25 + 53×0.20
        # = 17.10 + 14.50 + 13.00 + 10.60 = 55.20
    ),

    # 6 — élevé ~48
    DPREntity(
        entity_id = "DPR-006",
        name      = "Inde — NATGRID 11 Bases Données, Aadhaar Biométrie 1,3Mrd Forcé & Coupures Internet 100+/An",
        country   = "Inde",
        mass_surveillance_score      = 50.0,
        facial_recognition_score     = 49.0,
        data_rights_score            = 46.0,
        encryption_restriction_score = 46.0,
        primary_pattern = "NATGRID interconnexion bases données, Aadhaar biométrie obligatoire, record coupures Internet mondial",
        # 50×0.30 + 49×0.25 + 46×0.25 + 46×0.20
        # = 15.00 + 12.25 + 11.50 + 9.20 = 47.95
    ),

    # 7 — modéré ~28
    DPREntity(
        entity_id = "DPR-007",
        name      = "Union Européenne — RGPD Protecteur Mais DSA/DMA Tensions, Frontex Biométrie & Débat Chiffrement",
        country   = "Union Européenne",
        mass_surveillance_score      = 26.0,
        facial_recognition_score     = 30.0,
        data_rights_score            = 22.0,
        encryption_restriction_score = 35.0,
        primary_pattern = "RGPD meilleur cadre mondial mais pressions Chat Control, Frontex biométrie migrants controversée",
        # 26×0.30 + 30×0.25 + 22×0.25 + 35×0.20
        # = 7.80 + 7.50 + 5.50 + 7.00 = 27.80
    ),

    # 8 — faible ~12
    DPREntity(
        entity_id = "DPR-008",
        name      = "Allemagne & Suisse — Protection Données Constitutionnelle, BVerfG Jurisprudence & Vie Privée Droit Fondamental",
        country   = "Allemagne/Suisse",
        mass_surveillance_score      = 11.0,
        facial_recognition_score     = 13.0,
        data_rights_score            = 10.0,
        encryption_restriction_score = 14.0,
        primary_pattern = "Mémoire Stasi intégrée loi, BVerfG arrêts fondateurs vie privée, chiffrement protégé constitutionnellement",
        # 11×0.30 + 13×0.25 + 10×0.25 + 14×0.20
        # = 3.30 + 3.25 + 2.50 + 2.80 = 11.85
    ),
]

# ---------------------------------------------------------------------------
# Analytics helpers
# ---------------------------------------------------------------------------

def distribution_summary(entities: List[DPREntity]) -> dict:
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        counts[e.risk_level] += 1
    return counts


def avg_composite(entities: List[DPREntity]) -> float:
    return round(sum(e.composite_score for e in entities) / len(entities), 4)


def run_validation(entities: List[DPREntity]) -> None:
    print(f"\n{'='*60}")
    print(f"CaelumSwarm™ Wave {WAVE} — {PREFIX} Engine Validation")
    print(f"Domain : {DOMAIN}")
    print(f"{'='*60}")

    for e in entities:
        print(
            f"[{e.entity_id}] {e.name[:45]:<45} "
            f"composite={e.composite_score:>6.2f}  "
            f"risk={e.risk_level:<8}  "
            f"index={e.estimated_digital_privacy_rights_index}"
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
