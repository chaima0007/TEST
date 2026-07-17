"""
Arms Embargo Violations & Rights Engine — Wave 125
Domain: Violations embargo armes, complicité États
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
Weights: sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20
"""

from dataclasses import dataclass


@dataclass
class ArmsEmbargoViolationsRightsCase:
    case_id: str
    entity_name: str
    description: str
    embargo_violation_state_complicity_score: float        # ×0.30
    civilian_harm_arms_transfer_score: float               # ×0.25
    accountability_prosecution_gap_score: float            # ×0.25
    arms_broker_regulation_failure_score: float            # ×0.20

    @property
    def composite_score(self) -> float:
        return (
            self.embargo_violation_state_complicity_score * 0.30
            + self.civilian_harm_arms_transfer_score * 0.25
            + self.accountability_prosecution_gap_score * 0.25
            + self.arms_broker_regulation_failure_score * 0.20
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
    def estimated_arms_embargo_violations_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)


CASES = [
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-001",
        entity_name="Yémen/Coalition Saoudienne",
        description="Ventes USA/UK/FR à Riyad Malgré Embargo ONU Partiel, 25K Raids Frappes Civils, ACLED 150K Morts",
        embargo_violation_state_complicity_score=96,
        civilian_harm_arms_transfer_score=94,
        accountability_prosecution_gap_score=93,
        arms_broker_regulation_failure_score=91,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-002",
        entity_name="Libye/Résolution 1970",
        description="Embargo ONU 2011 Violé 40+ États, Turquie/UAE/Russie Armes Directes, Panel ONU Rapports 2020-2023",
        embargo_violation_state_complicity_score=90,
        civilian_harm_arms_transfer_score=87,
        accountability_prosecution_gap_score=88,
        arms_broker_regulation_failure_score=86,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-003",
        entity_name="Soudan/Darfour",
        description="Embargo 2004 Résolution 1556, Armes Chinoises/Russes Janjawid, Génocide ICC Al-Bashir, Impunité",
        embargo_violation_state_complicity_score=87,
        civilian_harm_arms_transfer_score=84,
        accountability_prosecution_gap_score=85,
        arms_broker_regulation_failure_score=83,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-004",
        entity_name="Myanmar/Coup 2021",
        description="Embargo UE/USA Partiel, Russie/Chine Fournisseurs Jets & Armes Tatmadaw, 2M Déplacés Rohingyas",
        embargo_violation_state_complicity_score=84,
        civilian_harm_arms_transfer_score=81,
        accountability_prosecution_gap_score=82,
        arms_broker_regulation_failure_score=80,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-005",
        entity_name="Éthiopie/Tigré",
        description="Drones Turcs Bayraktar Achetés Pendant Conflit, Embargo Informel USA Contourné, 500K Victimes",
        embargo_violation_state_complicity_score=57,
        civilian_harm_arms_transfer_score=54,
        accountability_prosecution_gap_score=55,
        arms_broker_regulation_failure_score=52,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-006",
        entity_name="Iran/JCPOA Embargo",
        description="Embargo ONU Armes 2020 Expiré, Ventes Russes S-400, Drones Shahid Ukraine, Sanctions Contournées",
        embargo_violation_state_complicity_score=53,
        civilian_harm_arms_transfer_score=50,
        accountability_prosecution_gap_score=51,
        arms_broker_regulation_failure_score=48,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-007",
        entity_name="TCA/Traité Commerce Armes",
        description="113 États Ratifié, Contrôles Transferts Art.7 Partiellement Appliqués, Rapports Annuels Lacunaires",
        embargo_violation_state_complicity_score=28,
        civilian_harm_arms_transfer_score=25,
        accountability_prosecution_gap_score=24,
        arms_broker_regulation_failure_score=26,
    ),
    ArmsEmbargoViolationsRightsCase(
        case_id="AEVR-008",
        entity_name="Norvège/Contrôles Stricts",
        description="Loi Exportations Armes 1992 Révisée 2013, Parlement Vote Chaque Licence, Refus Yemen 2019 Exemplaire",
        embargo_violation_state_complicity_score=5,
        civilian_harm_arms_transfer_score=4,
        accountability_prosecution_gap_score=4,
        arms_broker_regulation_failure_score=3,
    ),
]


def run_engine():
    print("=" * 65)
    print("ARMS EMBARGO VIOLATIONS & RIGHTS ENGINE — Wave 125")
    print("=" * 65)

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    total_composite = 0.0

    for case in CASES:
        composite = case.composite_score
        level = case.severity_level
        index = case.estimated_arms_embargo_violations_rights_index
        distribution[level] += 1
        total_composite += composite

        print(
            f"[{case.case_id}] {case.entity_name:<35} "
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
