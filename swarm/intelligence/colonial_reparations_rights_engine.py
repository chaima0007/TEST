#!/usr/bin/env python3
"""Colonial Reparations Rights Engine — CaelumSwarm™ Wave 203 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "CRR"
ACCENT_COLOR = "#6b3a2a"
ENTITIES = [
    {"name": "UK (British Museum)",          "sub1": 90.0, "sub2": 87.0, "sub3": 85.0, "sub4": 89.0},
    {"name": "France (Louvre colonial)",     "sub1": 88.0, "sub2": 84.0, "sub3": 83.0, "sub4": 87.0},
    {"name": "Belgium (Congo)",              "sub1": 84.0, "sub2": 80.0, "sub3": 79.0, "sub4": 83.0},
    {"name": "Netherlands (VOC)",            "sub1": 78.0, "sub2": 75.0, "sub3": 73.0, "sub4": 77.0},
    {"name": "Germany (Herero reparations)", "sub1": 62.0, "sub2": 58.0, "sub3": 57.0, "sub4": 60.0},
    {"name": "Portugal",                     "sub1": 56.0, "sub2": 52.0, "sub3": 51.0, "sub4": 54.0},
    {"name": "Italy",                        "sub1": 38.0, "sub2": 33.0, "sub3": 35.0, "sub4": 30.0},
    {"name": "ICOM (museum ethics)",         "sub1": 18.0, "sub2": 13.0, "sub3": 15.0, "sub4": 11.0},
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
            f"estimated_{DOMAIN_CODE.lower()}_index": round(score / 100 * 10, 2),
            "csddd_articles": ["Art.8", "Art.9", "Art.10", "Art.11"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })
    scores = [r["composite_score"] for r in results]
    avg = round(sum(scores) / len(scores), 2)
    output = {
        "engine": f"{DOMAIN_CODE}_ENGINE",
        "version": "1.0.0",
        "accent_color": ACCENT_COLOR,
        "avg_composite": avg,
        "distribution": {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1},
        "entities": results,
        "csddd_compliance": "CSDDD Art.8-13 EU 2024/1760",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return output


if __name__ == "__main__":
    run_engine()
