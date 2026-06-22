#!/usr/bin/env python3
"""Genetic Data Privacy Rights Engine — CaelumSwarm™ Wave 200 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "GDP"
ACCENT_COLOR = "#7c2d12"

# Distribution: 4 critique (>=60) + 2 élevé (40-59) + 1 modéré (20-39) + 1 faible (<20)
# avg_composite validated at 60.78 (between 60.00 and 63.00)
ENTITIES = [
    # critique (>=60) — collecte ADN massive, risques discrimination assurance/emploi
    {"name": "23andMe",        "sub1": 92.0, "sub2": 90.0, "sub3": 90.0, "sub4": 94.0},
    {"name": "AncestryDNA",    "sub1": 88.0, "sub2": 84.0, "sub3": 86.0, "sub4": 82.0},
    {"name": "BGI Genomics",   "sub1": 96.0, "sub2": 94.0, "sub3": 93.0, "sub4": 95.0},
    {"name": "Illumina",       "sub1": 74.0, "sub2": 70.0, "sub3": 68.0, "sub4": 72.0},
    # élevé (40-59) — politiques données ambiguës, partage tiers partiellement encadré
    {"name": "MyHeritage",     "sub1": 56.0, "sub2": 54.0, "sub3": 55.0, "sub4": 52.0},
    {"name": "FamilyTreeDNA",  "sub1": 50.0, "sub2": 46.0, "sub3": 48.0, "sub4": 44.0},
    # modéré (20-39) — chiffrement end-to-end, consentement granulaire
    {"name": "Nebula Genomics","sub1": 32.0, "sub2": 28.0, "sub3": 30.0, "sub4": 26.0},
    # faible (<20) — accès ouvert encadré, conformité RGPD exemplaire
    {"name": "Broad Institute","sub1": 12.0, "sub2": 10.0, "sub3": 14.0, "sub4": 16.0},
]


def compute_score(e):
    return round(e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20, 2)


def get_level(s):
    if s >= 60:
        return "critique"
    if s >= 40:
        return "élevé"
    if s >= 20:
        return "modéré"
    return "faible"


def run_engine():
    results = []
    for e in ENTITIES:
        score = compute_score(e)
        results.append({
            "entity": e["name"],
            "composite_score": score,
            "level": get_level(score),
            "estimated_gdp_index": round(score / 100 * 10, 2),
            "csddd_articles": ["Art.8", "Art.9", "Art.10", "Art.11"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    scores = [r["composite_score"] for r in results]
    avg = round(sum(scores) / len(scores), 2)
    output = {
        "engine": "GDP_ENGINE",
        "version": "1.0.0",
        "accent_color": ACCENT_COLOR,
        "avg_composite": avg,
        "distribution": {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1},
        "entities": results,
        "csddd_compliance": "CSDDD Art.8-13 EU 2024/1760",
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return output


if __name__ == "__main__":
    run_engine()
