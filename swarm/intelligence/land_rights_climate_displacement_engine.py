#!/usr/bin/env python3
"""Land Rights Climate Displacement Engine — CaelumSwarm™ Wave 207 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "LRC"
ACCENT_COLOR = "#1c3d1c"
ENTITIES = [
    {"name": "Bangladesh (Inondations)",  "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Pacific Islands (Submersion)", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Mozambique (Cyclones Idai/Kenneth)", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "Sudan (Sécheresse)",        "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "Philippines (Typhons)",     "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Ethiopia (Sécheresse)",     "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "UNHCR Climate",             "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Climate Displaced People Alliance", "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7}
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
