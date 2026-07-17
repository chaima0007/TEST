"""
Forced Sterilization & Reproductive Coercion Engine — Wave 125
Domain: Stérilisation forcée et coercition reproductive
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
Weights: sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20
"""

from dataclasses import dataclass


@dataclass
class ForcedSterilizationReproductiveCoercionCase:
    case_id: str
    entity_name: str
    description: str
    forced_sterilization_state_coercion_score: float       # ×0.30
    reproductive_autonomy_violations_scale_score: float    # ×0.25
    informed_consent_medical_coercion_score: float         # ×0.25
    accountability_impunity_medical_perpetrators_score: float  # ×0.20

    @property
    def composite_score(self) -> float:
        return (
            self.forced_sterilization_state_coercion_score * 0.30
            + self.reproductive_autonomy_violations_scale_score * 0.25
            + self.informed_consent_medical_coercion_score * 0.25
            + self.accountability_impunity_medical_perpetrators_score * 0.20
        )

    @property
    def severity_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        elif s >= 40:
            return "élevé"
        elif s >= 20:
            return "modéré"
        else:
            return "faible"

    @property
    def estimated_forced_sterilization_reproductive_coercion_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)


CASES = [
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-001",
        entity_name="Chine/Ouïghours",
        description="Stérilisations Forcées 2017-2021 Xinjiang, DIU Imposés, Taux Natalité -84%, Rapport AP & Tribunal",
        forced_sterilization_state_coercion_score=97,
        reproductive_autonomy_violations_scale_score=93,
        informed_consent_medical_coercion_score=94,
        accountability_impunity_medical_perpetrators_score=91,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-002",
        entity_name="Inde/Campagnes",
        description="15 Décès Sterilization Camp Chattisgarh 2014, Quotas États, Femmes Rurales Ciblées, OMS Alerte",
        forced_sterilization_state_coercion_score=89,
        reproductive_autonomy_violations_scale_score=85,
        informed_consent_medical_coercion_score=86,
        accountability_impunity_medical_perpetrators_score=84,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-003",
        entity_name="USA/Prison",
        description="Stérilisations Femmes Incarcérées California 2014, 1977 Sterilization Amérindiens BIA, Impunité",
        forced_sterilization_state_coercion_score=86,
        reproductive_autonomy_violations_scale_score=82,
        informed_consent_medical_coercion_score=83,
        accountability_impunity_medical_perpetrators_score=81,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-004",
        entity_name="Pérou/Fujimori",
        description="300K Femmes Stérilisées 1996-2000 Programme AQV, Indiennes Rurales Ciblées, Procès 30 Ans Après",
        forced_sterilization_state_coercion_score=84,
        reproductive_autonomy_violations_scale_score=80,
        informed_consent_medical_coercion_score=81,
        accountability_impunity_medical_perpetrators_score=79,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-005",
        entity_name="Europe/Roms",
        description="Stérilisations Femmes Roms Tchèquie/Slovaquie, CEDH Condamnations 2011, Pratiques Persistantes",
        forced_sterilization_state_coercion_score=56,
        reproductive_autonomy_violations_scale_score=52,
        informed_consent_medical_coercion_score=53,
        accountability_impunity_medical_perpetrators_score=51,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-006",
        entity_name="Namibie/VIH",
        description="Femmes VIH+ Stérilisées Sans Consentement Hôpitaux, LRC Procès 2012, Réparations Insuffisantes",
        forced_sterilization_state_coercion_score=52,
        reproductive_autonomy_violations_scale_score=48,
        informed_consent_medical_coercion_score=49,
        accountability_impunity_medical_perpetrators_score=47,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-007",
        entity_name="ONU/OHCHR",
        description="Rapport 2014 Stérilisations Forcées Femmes Handicapées, Standards Médicaux Éthiques, Suivi Insuffisant",
        forced_sterilization_state_coercion_score=27,
        reproductive_autonomy_violations_scale_score=25,
        informed_consent_medical_coercion_score=24,
        accountability_impunity_medical_perpetrators_score=23,
    ),
    ForcedSterilizationReproductiveCoercionCase(
        case_id="FSRC-008",
        entity_name="Canada/Enquête",
        description="Commission 2022 Stérilisations Femmes Autochtones, Loi Jade Sangara 2023, Progrès Réels",
        forced_sterilization_state_coercion_score=6,
        reproductive_autonomy_violations_scale_score=5,
        informed_consent_medical_coercion_score=5,
        accountability_impunity_medical_perpetrators_score=4,
    ),
]


def run_engine():
    print("=" * 65)
    print("FORCED STERILIZATION & REPRODUCTIVE COERCION ENGINE — Wave 125")
    print("=" * 65)

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    total_composite = 0.0

    for case in CASES:
        composite = case.composite_score
        level = case.severity_level
        index = case.estimated_forced_sterilization_reproductive_coercion_index
        distribution[level] += 1
        total_composite += composite

        print(
            f"[{case.case_id}] {case.entity_name:<30} "
            f"composite={composite:.1f}  level={level:<8}  index={index}"
        )

    avg_composite = total_composite / len(CASES)
    print("-" * 65)
    print(f"avg_composite       : {avg_composite:.2f}")
    print(f"distribution        : {distribution}")
    print(
        f"expected distribution: "
        f"{{'critique': 4, 'élevé': 2, 'modéré': 1, 'faible': 1}}"
    )
    assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, (
        f"Distribution error: {distribution}"
    )
    assert 55 <= avg_composite <= 70, f"avg_composite out of range: {avg_composite}"
    print("✓ Distribution OK")
    print("✓ avg_composite in range [55, 70]")
    return avg_composite, distribution


if __name__ == "__main__":
    run_engine()
