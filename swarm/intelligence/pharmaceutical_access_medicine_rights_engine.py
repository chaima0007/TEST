import json
from datetime import datetime


def run():
    entities = [
        {
            "id": "PAM-001",
            "name": "Afrique Sub-Saharienne/ARV — 20 M personnes sans antirétroviraux, prix de brevet 40× supérieur aux génériques",
            "sub1": 90.0, "sub2": 88.0, "sub3": 85.0, "sub4": 82.0,
        },
        {
            "id": "PAM-002",
            "name": "USA/Insuline — prix moyen 300$/flacon vs 6$ fabrication, 1 américain/4 rationne ses doses",
            "sub1": 86.0, "sub2": 84.0, "sub3": 80.0, "sub4": 78.0,
        },
        {
            "id": "PAM-003",
            "name": "Yémen/MSF — ruptures totales d'approvisionnement en médicaments essentiels, effondrement système santé",
            "sub1": 88.0, "sub2": 80.0, "sub3": 82.0, "sub4": 75.0,
        },
        {
            "id": "PAM-004",
            "name": "Venezuela — pénurie 80 % médicaments essentiels, fuite des compétences médicales, accès pharmaceutique en crise",
            "sub1": 82.0, "sub2": 78.0, "sub3": 80.0, "sub4": 70.0,
        },
        {
            "id": "PAM-005",
            "name": "Inde/HIV génériques — producteur mondial de génériques ARV mais sous pression TRIPS/accords bilatéraux USA",
            "sub1": 52.0, "sub2": 56.0, "sub3": 48.0, "sub4": 50.0,
        },
        {
            "id": "PAM-006",
            "name": "Brésil/Licences obligatoires — pionnier des licences TRIPS pour ARV, modèle contesté par l'industrie pharmaceutique",
            "sub1": 46.0, "sub2": 50.0, "sub3": 44.0, "sub4": 48.0,
        },
        {
            "id": "PAM-007",
            "name": "OMS/Flexibilités TRIPS — cadre Doha 2001 peu appliqué, 80 % des pays n'ont pas activé de licence obligatoire",
            "sub1": 30.0, "sub2": 28.0, "sub3": 32.0, "sub4": 25.0,
        },
        {
            "id": "PAM-008",
            "name": "Bangladesh/Modèle génériques — exemption LDC TRIPS jusqu'en 2033, industrie pharmaceutique nationale florissante",
            "sub1": 10.0, "sub2": 8.0, "sub3": 12.0, "sub4": 9.0,
        },
    ]

    results = []
    for e in entities:
        composite_score = e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20
        estimated_medicine_access_rights_index = round(composite_score / 100 * 10, 2)

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
            "estimated_medicine_access_rights_index": estimated_medicine_access_rights_index,
        })

    # Distribution OBLIGATOIRE: 4 critique, 2 élevé, 1 modéré, 1 faible
    risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        risk_distribution[r["risk_level"]] += 1

    assert risk_distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Wrong distribution: {risk_distribution}"

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    return {
        "domain": "pharmaceutical-access-medicine-rights-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": risk_distribution,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
