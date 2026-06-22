#!/usr/bin/env python3
"""Sports Labor Mega Events Engine — CaelumSwarm™ Wave 201 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "SLM"
ACCENT_COLOR = "#1d4ed8"

ENTITIES = [
    {"name": "FIFA Qatar 2022",        "sub1": 94.0, "sub2": 92.0, "sub3": 90.0, "sub4": 88.0},
    {"name": "IOC Beijing 2022",       "sub1": 90.0, "sub2": 88.0, "sub3": 86.0, "sub4": 84.0},
    {"name": "Formula 1 Saudi Arabia", "sub1": 87.0, "sub2": 85.0, "sub3": 83.0, "sub4": 80.0},
    {"name": "ATP/WTA Saudi",          "sub1": 83.0, "sub2": 81.0, "sub3": 79.0, "sub4": 76.0},
    {"name": "UEFA Super League",      "sub1": 56.0, "sub2": 54.0, "sub3": 52.0, "sub4": 50.0},
    {"name": "NBA China",              "sub1": 50.0, "sub2": 48.0, "sub3": 46.0, "sub4": 44.0},
    {"name": "Premier League",         "sub1": 30.0, "sub2": 28.0, "sub3": 26.0, "sub4": 24.0},
    {"name": "FIFPro",                 "sub1": 12.0, "sub2": 10.0, "sub3":  8.0, "sub4": 14.0},
]


def compute_score(e):
    return round(e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20, 2)


def get_level(s):
    if s >= 60: return "critique"
    if s >= 40: return "élevé"
    if s >= 20: return "modéré"
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
            "timestamp": datetime.utcnow().isoformat() + "Z"
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
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return output


if __name__ == "__main__":
    run_engine()
