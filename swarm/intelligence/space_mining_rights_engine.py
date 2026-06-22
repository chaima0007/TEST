#!/usr/bin/env python3
"""Space Mining Rights Engine — CaelumSwarm™ Wave 208 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "SMR"
ACCENT_COLOR = "#0c1445"
ENTITIES = [
    {"name": "SpaceX (Starship mining)", "sub1": 94.0, "sub2": 92.0, "sub3": 90.0, "sub4": 93.0},
    {"name": "Planetary Resources (asteroid)", "sub1": 88.0, "sub2": 85.0, "sub3": 83.0, "sub4": 86.0},
    {"name": "Deep Space Industries", "sub1": 84.0, "sub2": 80.0, "sub3": 78.0, "sub4": 82.0},
    {"name": "ispace", "sub1": 78.0, "sub2": 74.0, "sub3": 72.0, "sub4": 76.0},
    {"name": "NASA Artemis Program", "sub1": 58.0, "sub2": 55.0, "sub3": 57.0, "sub4": 53.0},
    {"name": "ESA Moon Village", "sub1": 56.0, "sub2": 53.0, "sub3": 54.0, "sub4": 52.0},
    {"name": "UN COPUOS", "sub1": 33.0, "sub2": 29.0, "sub3": 31.0, "sub4": 27.0},
    {"name": "Space Law Institute", "sub1": 16.0, "sub2": 12.0, "sub3": 14.0, "sub4": 10.0},
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
