#!/usr/bin/env python3
from dataclasses import dataclass, field
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Désinformation d'État & manipulation de masse
    sub2: float  # Impact sur droits civils & espace civique
    sub3: float  # Impunité des opérateurs & absence de régulation
    sub4: float  # Résilience sociétale & contre-mesures
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


def run_information_warfare_civilian_rights_analysis():
    entities = [
        EntityScore(
            entity_id="iwcr_001",
            name="Russie — Guerre informationnelle (Ukraine & Occident)",
            sub1=9.7, sub2=9.5, sub3=9.8, sub4=9.2
        ),
        EntityScore(
            entity_id="iwcr_002",
            name="Chine — Opérations d'influence & censure transnationale",
            sub1=9.5, sub2=9.3, sub3=9.6, sub4=9.0
        ),
        EntityScore(
            entity_id="iwcr_003",
            name="Myanmar — Génocide Rohingya via Facebook/TATMADAW",
            sub1=9.2, sub2=9.6, sub3=9.4, sub4=9.5
        ),
        EntityScore(
            entity_id="iwcr_004",
            name="Iran — Désinformation interne & répression numérique",
            sub1=8.8, sub2=8.6, sub3=8.9, sub4=8.3
        ),
        EntityScore(
            entity_id="iwcr_005",
            name="Éthiopie — Propagande de guerre & discours de haine Tigré",
            sub1=5.8, sub2=6.2, sub3=5.5, sub4=5.8
        ),
        EntityScore(
            entity_id="iwcr_006",
            name="Brésil — Campagnes de désinformation électorale",
            sub1=5.2, sub2=5.0, sub3=5.5, sub4=4.8
        ),
        EntityScore(
            entity_id="iwcr_007",
            name="Inde — Lynchages mobiles & désinformation communautaire",
            sub1=3.5, sub2=4.0, sub3=3.2, sub4=3.8
        ),
        EntityScore(
            entity_id="iwcr_008",
            name="Union Européenne — DSA & cadre résilience démocratique",
            sub1=1.5, sub2=1.2, sub3=1.8, sub4=1.0
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_state_disinfo": e.sub1,
            "sub2_civil_rights_impact": e.sub2,
            "sub3_impunity_no_regulation": e.sub3,
            "sub4_societal_resilience": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_info_warfare_index": e.estimated_index,
        })

    results.sort(key=lambda x: x["composite_score"], reverse=True)

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "information_warfare_civilian_rights_engine",
        "wave": 146,
        "domain": "Guerre de l'information & droits civils des populations civiles",
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    print(f"\n--- VALIDATION ---")
    print(f"avg_composite : {avg_composite}")
    print(f"Distribution  : {distribution}")
    for r in results:
        print(f"  [{r['risk_level']:8s}] {r['composite_score']:5.2f}  {r['name']}")

    assert distribution.get("critique", 0) == 4, f"Attendu 4 critique, obtenu {distribution.get('critique', 0)}"
    assert distribution.get("élevé", 0) == 2, f"Attendu 2 élevé, obtenu {distribution.get('élevé', 0)}"
    assert distribution.get("modéré", 0) == 1, f"Attendu 1 modéré, obtenu {distribution.get('modéré', 0)}"
    assert distribution.get("faible", 0) == 1, f"Attendu 1 faible, obtenu {distribution.get('faible', 0)}"
    assert 58 <= avg_composite <= 68, f"avg_composite hors plage [58-68]: {avg_composite}"
    print("✓ Toutes les assertions passent.")


if __name__ == "__main__":
    run_information_warfare_civilian_rights_analysis()
