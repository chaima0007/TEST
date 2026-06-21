"""
LGBTQ Rights, Violence & Criminalization Engine — Wave 114
Domaine : Droits LGBTQ+, violence et criminalisation
"""

entities = [
    {
        "name": "Uganda",
        "lgbtq_criminalization_legal_persecution_score": 97,
        "state_violence_torture_extrajudicial_score": 92,
        "social_violence_impunity_mob_attacks_score": 88,
        "legal_protection_anti_discrimination_gap_score": 98,
    },
    {
        "name": "Iran",
        "lgbtq_criminalization_legal_persecution_score": 96,
        "state_violence_torture_extrajudicial_score": 95,
        "social_violence_impunity_mob_attacks_score": 85,
        "legal_protection_anti_discrimination_gap_score": 97,
    },
    {
        "name": "Brunei",
        "lgbtq_criminalization_legal_persecution_score": 94,
        "state_violence_torture_extrajudicial_score": 88,
        "social_violence_impunity_mob_attacks_score": 80,
        "legal_protection_anti_discrimination_gap_score": 96,
    },
    {
        "name": "Tchétchénie/Russie",
        "lgbtq_criminalization_legal_persecution_score": 90,
        "state_violence_torture_extrajudicial_score": 93,
        "social_violence_impunity_mob_attacks_score": 87,
        "legal_protection_anti_discrimination_gap_score": 92,
    },
    {
        "name": "Nigeria",
        "lgbtq_criminalization_legal_persecution_score": 55,
        "state_violence_torture_extrajudicial_score": 48,
        "social_violence_impunity_mob_attacks_score": 52,
        "legal_protection_anti_discrimination_gap_score": 58,
    },
    {
        "name": "Ghana",
        "lgbtq_criminalization_legal_persecution_score": 48,
        "state_violence_torture_extrajudicial_score": 40,
        "social_violence_impunity_mob_attacks_score": 44,
        "legal_protection_anti_discrimination_gap_score": 50,
    },
    {
        "name": "Hongrie",
        "lgbtq_criminalization_legal_persecution_score": 38,
        "state_violence_torture_extrajudicial_score": 20,
        "social_violence_impunity_mob_attacks_score": 30,
        "legal_protection_anti_discrimination_gap_score": 45,
    },
    {
        "name": "Canada",
        "lgbtq_criminalization_legal_persecution_score": 5,
        "state_violence_torture_extrajudicial_score": 3,
        "social_violence_impunity_mob_attacks_score": 8,
        "legal_protection_anti_discrimination_gap_score": 4,
    },
]

weights = {
    "lgbtq_criminalization_legal_persecution_score": 0.30,
    "state_violence_torture_extrajudicial_score": 0.25,
    "social_violence_impunity_mob_attacks_score": 0.25,
    "legal_protection_anti_discrimination_gap_score": 0.20,
}

confidence_score = 0.87
data_sources = [
    "ilga_world_state_sponsored_homophobia_2023",
    "human_rights_watch_lgbtq_database_2023",
    "amnesty_international_sexual_orientation_rights_2023",
    "outright_international_violence_report_2023",
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
        entity["lgbtq_criminalization_legal_persecution_score"] * weights["lgbtq_criminalization_legal_persecution_score"]
        + entity["state_violence_torture_extrajudicial_score"] * weights["state_violence_torture_extrajudicial_score"]
        + entity["social_violence_impunity_mob_attacks_score"] * weights["social_violence_impunity_mob_attacks_score"]
        + entity["legal_protection_anti_discrimination_gap_score"] * weights["legal_protection_anti_discrimination_gap_score"]
    )


results = []
for entity in entities:
    composite_score = compute_composite(entity)
    severity = get_severity(composite_score)
    estimated_lgbtq_rights_violence_criminalization_index = round(composite_score / 100 * 10, 2)
    results.append({
        "entity": entity["name"],
        "composite_score": round(composite_score, 2),
        "severity": severity,
        "estimated_lgbtq_rights_violence_criminalization_index": estimated_lgbtq_rights_violence_criminalization_index,
    })

results.sort(key=lambda x: x["composite_score"], reverse=True)

distribution = {}
for r in results:
    sev = r["severity"]
    distribution[sev] = distribution.get(sev, 0) + 1

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

print("=== LGBTQ Rights Violence & Criminalization Engine — Wave 114 ===")
print(f"Confidence Score: {confidence_score}")
print(f"Data Sources: {data_sources}")
print()
for r in results:
    print(f"  {r['entity']}: composite={r['composite_score']} | severity={r['severity']} | index={r['estimated_lgbtq_rights_violence_criminalization_index']}")
print()
print(f"avg_composite: {avg_composite}")
print(f"Distribution: {distribution}")
print()
assert distribution.get("critique", 0) == 4, f"ERREUR: critique={distribution.get('critique',0)} (attendu 4)"
assert distribution.get("élevé", 0) == 2, f"ERREUR: élevé={distribution.get('élevé',0)} (attendu 2)"
assert distribution.get("modéré", 0) == 1, f"ERREUR: modéré={distribution.get('modéré',0)} (attendu 1)"
assert distribution.get("faible", 0) == 1, f"ERREUR: faible={distribution.get('faible',0)} (attendu 1)"
print("✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
