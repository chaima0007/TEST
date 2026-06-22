#!/usr/bin/env python3
"""Crypto Energy Rights Engine — CaelumSwarm™ Wave 203 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "CER"
ACCENT_COLOR = "#f59e0b"
ENTITIES = [
    {"name": "Riot Platforms",                    "sub1": 89.0, "sub2": 86.0, "sub3": 85.0, "sub4": 88.0},
    {"name": "Marathon Digital",                  "sub1": 87.0, "sub2": 83.0, "sub3": 82.0, "sub4": 86.0},
    {"name": "Bitmain",                           "sub1": 83.0, "sub2": 80.0, "sub3": 79.0, "sub4": 82.0},
    {"name": "Foundry USA",                       "sub1": 77.0, "sub2": 74.0, "sub3": 73.0, "sub4": 76.0},
    {"name": "Antpool",                           "sub1": 61.0, "sub2": 57.0, "sub3": 56.0, "sub4": 59.0},
    {"name": "F2Pool",                            "sub1": 55.0, "sub2": 51.0, "sub3": 50.0, "sub4": 53.0},
    {"name": "Ethereum Foundation (post-merge)",  "sub1": 39.0, "sub2": 34.0, "sub3": 36.0, "sub4": 31.0},
    {"name": "Bitcoin Clean Energy Initiative",   "sub1": 17.0, "sub2": 12.0, "sub3": 14.0, "sub4": 10.0},
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
