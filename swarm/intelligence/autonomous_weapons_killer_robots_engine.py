import json
from datetime import datetime


def run():
    entities = [
        {
            "id": "AWR-001",
            "name": "Russie/Kalashnikov — drone KUB-BLA, arme autonome létale déployée en Ukraine sans supervision humaine",
            "sub1": 92.0, "sub2": 90.0, "sub3": 85.0, "sub4": 88.0,
        },
        {
            "id": "AWR-002",
            "name": "Chine/STR — Programme LAWS 'Sharp Sword', intégration IA militaire massive, refus régulation internationale",
            "sub1": 88.0, "sub2": 86.0, "sub3": 82.0, "sub4": 84.0,
        },
        {
            "id": "AWR-003",
            "name": "Turquie/Kargu-2 — drone autonome à reconnaissance faciale, premier usage contre humain sans opérateur (Libye, 2020)",
            "sub1": 85.0, "sub2": 80.0, "sub3": 78.0, "sub4": 82.0,
        },
        {
            "id": "AWR-004",
            "name": "Israël/Harop — drone-kamikaze autonome vendu à 45+ pays, zone grise légale internationale",
            "sub1": 82.0, "sub2": 78.0, "sub3": 80.0, "sub4": 75.0,
        },
        {
            "id": "AWR-005",
            "name": "USA/LAWS — Programme Replicator DoD, déploiement d'essaims autonomes, absence traité international contraignant",
            "sub1": 55.0, "sub2": 60.0, "sub3": 58.0, "sub4": 52.0,
        },
        {
            "id": "AWR-006",
            "name": "Corée du Sud/Meta Border — tourelles SGR-A1 semi-autonomes à la frontière DMZ, supervision humaine partielle",
            "sub1": 50.0, "sub2": 48.0, "sub3": 55.0, "sub4": 44.0,
        },
        {
            "id": "AWR-007",
            "name": "UE/Campagne interdiction LAWS — pression normative forte, aucun État membre n'a signé traité contraignant",
            "sub1": 28.0, "sub2": 32.0, "sub3": 25.0, "sub4": 30.0,
        },
        {
            "id": "AWR-008",
            "name": "ONU/GGE CCW — négociations sur LAWS au point mort depuis 2014, États bloquants: USA, Russie, Chine",
            "sub1": 12.0, "sub2": 10.0, "sub3": 15.0, "sub4": 8.0,
        },
    ]

    results = []
    for e in entities:
        composite_score = e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20
        estimated_autonomous_weapons_risk_index = round(composite_score / 100 * 10, 2)

        if composite_score >= 60:
            risk_level = "critique"
        elif composite_score >= 40:
            risk_level = "élevé"
        elif composite_score >= 20:
            risk_level = "modéré"
        else:
            risk_level = "faible"

        results.append({
            "id": e["id"],
            "name": e["name"],
            "composite_score": round(composite_score, 2),
            "risk_level": risk_level,
            "estimated_autonomous_weapons_risk_index": estimated_autonomous_weapons_risk_index,
        })

    # Distribution OBLIGATOIRE: 4 critique, 2 élevé, 1 modéré, 1 faible
    risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        risk_distribution[r["risk_level"]] += 1

    assert risk_distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Wrong distribution: {risk_distribution}"

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    return {
        "domain": "autonomous-weapons-killer-robots-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": risk_distribution,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
