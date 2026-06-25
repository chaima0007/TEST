"""
AI Surveillance & Biometric Rights Engine — Wave 125
Domain: Surveillance IA, biométrie et droits fondamentaux
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
Weights: sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20
"""

from dataclasses import dataclass


@dataclass
class AISurveillanceBiometricRightsCase:
    case_id: str
    entity_name: str
    description: str
    mass_facial_recognition_surveillance_score: float      # ×0.30
    predictive_policing_discrimination_score: float        # ×0.25
    biometric_data_exploitation_rights_score: float        # ×0.25
    algorithmic_accountability_gap_score: float            # ×0.20

    @property
    def composite_score(self) -> float:
        return (
            self.mass_facial_recognition_surveillance_score * 0.30
            + self.predictive_policing_discrimination_score * 0.25
            + self.biometric_data_exploitation_rights_score * 0.25
            + self.algorithmic_accountability_gap_score * 0.20
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
    def estimated_ai_surveillance_biometric_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)


CASES = [
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-001",
        entity_name="Chine/SCS",
        description="Système Crédit Social, 1.4Md Habitants Notés, 400M Caméras CCTV, Pénalités Sociales Dissidents",
        mass_facial_recognition_surveillance_score=97,
        predictive_policing_discrimination_score=92,
        biometric_data_exploitation_rights_score=94,
        algorithmic_accountability_gap_score=90,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-002",
        entity_name="Russie/SORM-3",
        description="Surveillance Internet SORM Totale, Reconnaissance Faciale Moscou 160K Caméras, Activistes Arrêtés",
        mass_facial_recognition_surveillance_score=89,
        predictive_policing_discrimination_score=86,
        biometric_data_exploitation_rights_score=84,
        algorithmic_accountability_gap_score=87,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-003",
        entity_name="Inde/Aadhaar",
        description="1.3Md Personnes Fichées, Exclusions Services Sans Biométrie, Fuites Données 2018, Cour Suprême",
        mass_facial_recognition_surveillance_score=85,
        predictive_policing_discrimination_score=82,
        biometric_data_exploitation_rights_score=83,
        algorithmic_accountability_gap_score=80,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-004",
        entity_name="USA/PredPol",
        description="Logiciels Prédictifs 150 Villes, Disparités Raciales Prouvées ACLU, Chicago List Score Libertés",
        mass_facial_recognition_surveillance_score=82,
        predictive_policing_discrimination_score=84,
        biometric_data_exploitation_rights_score=80,
        algorithmic_accountability_gap_score=83,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-005",
        entity_name="Éthiopie/Palantir",
        description="Contrats Défense Régimes Autoritaires, Ciblage Opposants, Absence Supervision",
        mass_facial_recognition_surveillance_score=55,
        predictive_policing_discrimination_score=52,
        biometric_data_exploitation_rights_score=53,
        algorithmic_accountability_gap_score=51,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-006",
        entity_name="Bangladesh/Surveillance",
        description="Système DSA Arrêter Critiques, Surveillance Journalistes Mobiles, Pegasus Confirmé",
        mass_facial_recognition_surveillance_score=51,
        predictive_policing_discrimination_score=48,
        biometric_data_exploitation_rights_score=49,
        algorithmic_accountability_gap_score=47,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-007",
        entity_name="UE/AI Act",
        description="Interdictions Partielles RF Masse 2024, Exemptions Sécurité Nationale, Application 2025-2026",
        mass_facial_recognition_surveillance_score=28,
        predictive_policing_discrimination_score=26,
        biometric_data_exploitation_rights_score=24,
        algorithmic_accountability_gap_score=27,
    ),
    AISurveillanceBiometricRightsCase(
        case_id="ASBR-008",
        entity_name="Allemagne/RGPD",
        description="Strict Biométrie RGPD Art.9, Amendes CNIL Équivalent, Recours Effectifs Citoyens",
        mass_facial_recognition_surveillance_score=5,
        predictive_policing_discrimination_score=4,
        biometric_data_exploitation_rights_score=5,
        algorithmic_accountability_gap_score=3,
    ),
]


def run_engine():
    print("=" * 65)
    print("AI SURVEILLANCE & BIOMETRIC RIGHTS ENGINE — Wave 125")
    print("=" * 65)

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    total_composite = 0.0

    for case in CASES:
        composite = case.composite_score
        level = case.severity_level
        index = case.estimated_ai_surveillance_biometric_rights_index
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
