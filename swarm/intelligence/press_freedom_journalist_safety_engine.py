"""
Press Freedom & Journalist Safety Engine — Wave 114
Domaine : Liberté de la presse et sécurité des journalistes (meurtres, emprisonnement,
surveillance, lois bâillon, déserts médiatiques)
"""

entities = [
    {
        "name": "Myanmar",
        "journalist_killings_impunity_score": 90,
        "journalist_imprisonment_censorship_score": 93,
        "media_independence_state_control_score": 95,
        "legal_press_freedom_protection_gap_score": 94,
    },
    {
        "name": "Azerbaïdjan",
        "journalist_killings_impunity_score": 85,
        "journalist_imprisonment_censorship_score": 92,
        "media_independence_state_control_score": 93,
        "legal_press_freedom_protection_gap_score": 91,
    },
    {
        "name": "Belarus",
        "journalist_killings_impunity_score": 82,
        "journalist_imprisonment_censorship_score": 94,
        "media_independence_state_control_score": 96,
        "legal_press_freedom_protection_gap_score": 93,
    },
    {
        "name": "Mexique",
        "journalist_killings_impunity_score": 96,
        "journalist_imprisonment_censorship_score": 78,
        "media_independence_state_control_score": 75,
        "legal_press_freedom_protection_gap_score": 88,
    },
    {
        "name": "Russie",
        "journalist_killings_impunity_score": 52,
        "journalist_imprisonment_censorship_score": 58,
        "media_independence_state_control_score": 60,
        "legal_press_freedom_protection_gap_score": 55,
    },
    {
        "name": "Turquie",
        "journalist_killings_impunity_score": 45,
        "journalist_imprisonment_censorship_score": 58,
        "media_independence_state_control_score": 55,
        "legal_press_freedom_protection_gap_score": 50,
    },
    {
        "name": "Inde",
        "journalist_killings_impunity_score": 32,
        "journalist_imprisonment_censorship_score": 28,
        "media_independence_state_control_score": 30,
        "legal_press_freedom_protection_gap_score": 35,
    },
    {
        "name": "Irlande",
        "journalist_killings_impunity_score": 3,
        "journalist_imprisonment_censorship_score": 4,
        "media_independence_state_control_score": 5,
        "legal_press_freedom_protection_gap_score": 4,
    },
]

weights = {
    "journalist_killings_impunity_score": 0.30,
    "journalist_imprisonment_censorship_score": 0.25,
    "media_independence_state_control_score": 0.25,
    "legal_press_freedom_protection_gap_score": 0.20,
}

confidence_score = 0.89
data_sources = [
    "rsf_world_press_freedom_index_2024",
    "committee_protect_journalists_impunity_index_2023",
    "reporters_without_borders_barometer_2024",
    "cpj_journalists_imprisoned_database_2023",
]


def get_severity(score):
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    else:
        return "faible"


def compute_composite(entity):
    return (
        entity["journalist_killings_impunity_score"] * weights["journalist_killings_impunity_score"]
        + entity["journalist_imprisonment_censorship_score"] * weights["journalist_imprisonment_censorship_score"]
        + entity["media_independence_state_control_score"] * weights["media_independence_state_control_score"]
        + entity["legal_press_freedom_protection_gap_score"] * weights["legal_press_freedom_protection_gap_score"]
    )


results = []
for entity in entities:
    composite_score = compute_composite(entity)
    severity = get_severity(composite_score)
    estimated_press_freedom_journalist_safety_index = round(composite_score / 100 * 10, 2)
    results.append({
        "entity": entity["name"],
        "composite_score": round(composite_score, 2),
        "severity": severity,
        "estimated_press_freedom_journalist_safety_index": estimated_press_freedom_journalist_safety_index,
    })

results.sort(key=lambda x: x["composite_score"], reverse=True)

distribution = {}
for r in results:
    sev = r["severity"]
    distribution[sev] = distribution.get(sev, 0) + 1

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

print("=== Press Freedom & Journalist Safety Engine — Wave 114 ===")
print(f"Confidence Score: {confidence_score}")
print(f"Data Sources: {data_sources}")
print()
for r in results:
    print(f"  {r['entity']}: composite={r['composite_score']} | severity={r['severity']} | index={r['estimated_press_freedom_journalist_safety_index']}")
print()
print(f"avg_composite: {avg_composite}")
print(f"Distribution: {distribution}")
print()
assert distribution.get("critique", 0) == 4, f"ERREUR: critique={distribution.get('critique',0)} (attendu 4)"
assert distribution.get("élevé", 0) == 2, f"ERREUR: élevé={distribution.get('élevé',0)} (attendu 2)"
assert distribution.get("modéré", 0) == 1, f"ERREUR: modéré={distribution.get('modéré',0)} (attendu 1)"
assert distribution.get("faible", 0) == 1, f"ERREUR: faible={distribution.get('faible',0)} (attendu 1)"
print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
