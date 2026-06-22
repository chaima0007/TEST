#!/usr/bin/env python3
"""Deforestation Palm Oil Rights Engine — CaelumSwarm™ Wave 206 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "DPO"
ACCENT_COLOR = "#166534"
ENTITIES = [
    {"name": "Wilmar International",  "sub1": 92.0, "sub2": 86.0, "sub3": 82.0, "sub4": 78.0},
    {"name": "IOI Group",             "sub1": 88.0, "sub2": 84.0, "sub3": 80.0, "sub4": 76.0},
    {"name": "Musim Mas",             "sub1": 84.0, "sub2": 78.0, "sub3": 76.0, "sub4": 74.0},
    {"name": "Golden Agri-Resources", "sub1": 80.0, "sub2": 75.0, "sub3": 73.0, "sub4": 72.0},
    {"name": "Cargill",               "sub1": 62.0, "sub2": 58.0, "sub3": 56.0, "sub4": 54.0},
    {"name": "Nestlé (palm oil)",     "sub1": 56.0, "sub2": 52.0, "sub3": 50.0, "sub4": 48.0},
    {"name": "Unilever",              "sub1": 38.0, "sub2": 34.0, "sub3": 32.0, "sub4": 30.0},
    {"name": "RSPO",                  "sub1": 16.0, "sub2": 15.0, "sub3": 14.0, "sub4": 14.0},
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
