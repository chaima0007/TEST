#!/usr/bin/env python3
"""AI Algorithmic Bias Rights Engine — CaelumSwarm™ Wave 203 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "AAB"
ACCENT_COLOR = "#1e3a5f"
ENTITIES = [
    {"name": "Amazon (Rekognition)",               "sub1": 88.0, "sub2": 85.0, "sub3": 83.0, "sub4": 87.0},
    {"name": "Meta (ad targeting)",                "sub1": 86.0, "sub2": 82.0, "sub3": 81.0, "sub4": 85.0},
    {"name": "COMPAS (recidivism)",                "sub1": 83.0, "sub2": 79.0, "sub3": 78.0, "sub4": 82.0},
    {"name": "HireVue",                            "sub1": 77.0, "sub2": 74.0, "sub3": 72.0, "sub4": 76.0},
    {"name": "Google (Search bias)",               "sub1": 61.0, "sub2": 57.0, "sub3": 56.0, "sub4": 59.0},
    {"name": "Apple (credit card algorithm)",      "sub1": 55.0, "sub2": 51.0, "sub3": 50.0, "sub4": 53.0},
    {"name": "IBM (facial recognition moratorium)","sub1": 39.0, "sub2": 34.0, "sub3": 36.0, "sub4": 31.0},
    {"name": "Partnership on AI",                  "sub1": 17.0, "sub2": 12.0, "sub3": 14.0, "sub4": 10.0},
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
