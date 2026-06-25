#!/usr/bin/env python3
"""
Wave 144 — Afrodescendant Reparations Rights Engine
Scores 8 country contexts on structural racism against Afrodescendants,
reparations demands, acknowledgment of historical injustices, and implementation
of compensatory policies.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""
from dataclasses import dataclass, field
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # structural_racism_severity (0-10)
    sub2: float  # reparations_demand_denial (0-10, higher = more denial)
    sub3: float  # historical_acknowledgment_failure (0-10)
    sub4: float  # compensatory_policy_implementation_gap (0-10)
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


def main():
    entities = [
        # 4 critique
        EntityScore(
            entity_id="USA_afrodescendants",
            name="États-Unis — Afrodescendants (réparations & racisme structurel)",
            sub1=8.5,   # police killings, mass incarceration, wealth gap, redlining legacy
            sub2=9.0,   # federal reparations bill HR 40 blocked for 30+ years
            sub3=8.3,   # partial acknowledgment; no formal apology for slavery at federal level
            sub4=8.7,   # affirmative action rollback (SFFA 2023); HBCUs underfunded
        ),
        EntityScore(
            entity_id="BRA_quilombolas",
            name="Brésil — Quilombolas & Afrodescendants",
            sub1=8.7,   # Afrodescendants 75% of homicide victims; land theft ongoing
            sub2=8.2,   # quilombola land titling frozen under consecutive administrations
            sub3=7.8,   # Palmares Foundation defunded; cultural erasure policies
            sub4=8.5,   # racial quotas challenged; quilombola demarcation halted
        ),
        EntityScore(
            entity_id="COL_afrocolombianos",
            name="Colombie — Afrocolombianos (Ley 70 & réparations)",
            sub1=8.3,   # highest poverty rates; Pacific communities targeted by armed groups
            sub2=8.0,   # Ley 70 territorial rights systematically violated by mining/agro
            sub3=7.9,   # Truth Commission recognized Afro-Colombian suffering; state response weak
            sub4=8.1,   # reparations framework for conflict victims applied unequally
        ),
        EntityScore(
            entity_id="JAM_caricom",
            name="Jamaïque & CARICOM — Réparations esclavage britannique",
            sub1=7.8,   # legacy of plantation economy; persistent poverty; colonial debt burden
            sub2=8.8,   # UK government refuses CARICOM reparations negotiations
            sub3=8.5,   # UK acknowledges history rhetorically; zero material commitment
            sub4=8.0,   # no reparations fund established; CARICOM commission unfunded
        ),
        # 2 élevé
        EntityScore(
            entity_id="GBR_afrodescendants",
            name="Royaume-Uni — Afrodescendants (Windrush & réparations)",
            sub1=5.0,   # racial wealth gap; Windrush deportations; stop-and-search disparity
            sub2=5.5,   # Windrush compensation scheme inadequate; slavery reparations refused
            sub3=4.8,   # some acknowledgment post-BLM; Sewell Report disputed
            sub4=5.2,   # EHRC resources cut; Race Disparity Unit limited scope
        ),
        EntityScore(
            entity_id="FRA_antillais",
            name="France — Antillais & Afrodescendants (réparations & Taubira law)",
            sub1=4.8,   # employment discrimination; Martinique/Guadeloupe chlordecone scandal
            sub2=5.2,   # Loi Taubira (2001) recognizes slavery as crime against humanity; no reparations
            sub3=4.9,   # chlordecone poisoning uncompensated; colonial archive access restricted
            sub4=5.0,   # overseas territories infrastructure gap; reparations blocked by universalism
        ),
        # 1 modéré
        EntityScore(
            entity_id="CAN_afrodescendants",
            name="Canada — Afrodescendants (programme réparations & racisme anti-Noirs)",
            sub1=4.2,   # anti-Black racism recognized; Black Canadians overrepresented in incarceration
            sub2=3.8,   # UN WGEPAD recommendations partially acknowledged
            sub3=4.0,   # National Day for Truth and Reconciliation excludes Black history
            sub4=3.5,   # Federal anti-racism strategy; Black-specific funding programs emerging
        ),
        # 1 faible
        EntityScore(
            entity_id="URY_afrodescendants",
            name="Uruguay — Afrodescendants (Ley 19.122)",
            sub1=2.0,   # structural disparities remain but declining
            sub2=1.8,   # Ley 19.122 quotas for Afrodescendants in public sector implemented
            sub3=2.2,   # government acknowledgment of Afrodescendant history improving
            sub4=1.9,   # national reparations mechanism partially functional; civil society active
        ),
    ]

    results = []
    total_composite = 0.0
    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

    for e in entities:
        total_composite += e.composite_score
        distribution[e.risk_level] += 1
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub_scores": {
                "structural_racism_severity": e.sub1,
                "reparations_demand_denial": e.sub2,
                "historical_acknowledgment_failure": e.sub3,
                "compensatory_policy_implementation_gap": e.sub4,
            },
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_afrodescendant_reparations_index": e.estimated_index,
        })

    avg_composite = round(total_composite / len(entities), 2)

    output = {
        "engine": "afrodescendant_reparations_rights_engine",
        "wave": 144,
        "domain": "Afrodescendant Reparations Rights",
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
