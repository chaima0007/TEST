#!/usr/bin/env python3
"""Land Rights Climate Displacement Engine — CaelumSwarm™ Wave 207 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "LRC"
ACCENT_COLOR = "#1c3d1c"
ENTITIES = [
    {"name": "Bangladesh (Inondations)", "sub1": 95.0, "sub2": 91.0, "sub3": 88.0, "sub4": 85.0},
    {"name": "Pacific Islands (Submersion)", "sub1": 92.0, "sub2": 88.0, "sub3": 84.0, "sub4": 81.0},
    {"name": "Mozambique (Cyclones Idai/Kenneth)", "sub1": 88.0, "sub2": 84.0, "sub3": 80.0, "sub4": 77.0},
    {"name": "Sudan (Sécheresse)", "sub1": 84.0, "sub2": 79.0, "sub3": 76.0, "sub4": 73.0},
    {"name": "Philippines (Typhons)", "sub1": 58.0, "sub2": 52.0, "sub3": 50.0, "sub4": 47.0},
    {"name": "Ethiopia (Sécheresse)", "sub1": 55.0, "sub2": 49.0, "sub3": 47.0, "sub4": 44.0},
    {"name": "UNHCR Climate", "sub1": 37.0, "sub2": 32.0, "sub3": 29.0, "sub4": 26.0},
    {"name": "Climate Displaced People Alliance", "sub1": 16.0, "sub2": 13.0, "sub3": 11.0, "sub4": 9.0},
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
