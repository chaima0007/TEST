import json
from datetime import datetime


def run():
    entities = [
        {
            "id": "FMH-001",
            "name": "Pakistan/Khyber-Pakhtunkhwa — environ 1 000 crimes d'honneur signalés/an, impunité quasi-totale",
            "sub1": 90.0, "sub2": 88.0, "sub3": 85.0, "sub4": 82.0,
        },
        {
            "id": "FMH-002",
            "name": "Bangladesh — mariage d'enfants parmi les plus répandus au monde, 59 % des filles mariées avant 18 ans",
            "sub1": 86.0, "sub2": 82.0, "sub3": 80.0, "sub4": 78.0,
        },
        {
            "id": "FMH-003",
            "name": "Yémen — conflit armé aggrave les mariages précoces, 32 % des filles mariées avant 15 ans",
            "sub1": 85.0, "sub2": 80.0, "sub3": 83.0, "sub4": 76.0,
        },
        {
            "id": "FMH-004",
            "name": "Irak/Kurdistan — pratique des crimes d'honneur codifiée, loi pénale déficiente",
            "sub1": 80.0, "sub2": 78.0, "sub3": 79.0, "sub4": 72.0,
        },
        {
            "id": "FMH-005",
            "name": "Jordanie — article 98 du code pénal atténue peines pour crimes d'honneur, réforme partielle",
            "sub1": 58.0, "sub2": 55.0, "sub3": 60.0, "sub4": 50.0,
        },
        {
            "id": "FMH-006",
            "name": "Maroc — mariages forcés ruraux persistants malgré réforme Moudawwana 2004",
            "sub1": 52.0, "sub2": 48.0, "sub3": 55.0, "sub4": 44.0,
        },
        {
            "id": "FMH-007",
            "name": "Turquie — féminicides en hausse, retraits de la Convention d'Istanbul en 2021",
            "sub1": 32.0, "sub2": 28.0, "sub3": 35.0, "sub4": 25.0,
        },
        {
            "id": "FMH-008",
            "name": "Islande — cadre légal exemplaire, tolérance zéro, mariages forcés quasi-inexistants",
            "sub1": 8.0, "sub2": 5.0, "sub3": 6.0, "sub4": 7.0,
        },
    ]

    results = []
    for e in entities:
        composite_score = e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20
        estimated_forced_marriage_honor_violence_index = round(composite_score / 100 * 10, 2)

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
            "estimated_forced_marriage_honor_violence_index": estimated_forced_marriage_honor_violence_index,
        })

    # Distribution OBLIGATOIRE: 4 critique, 2 élevé, 1 modéré, 1 faible
    risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        risk_distribution[r["risk_level"]] += 1

    assert risk_distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Wrong distribution: {risk_distribution}"

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    return {
        "domain": "forced-marriage-honor-violence-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": risk_distribution,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
