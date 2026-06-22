#!/usr/bin/env python3
"""Seed Patents Food Sovereignty Engine — CaelumSwarm™ Wave 206 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "SPF"
ACCENT_COLOR = "#3d1a00"
ENTITIES = [
    {"name": "Bayer/Monsanto",       "sub1": 92.0, "sub2": 88.0, "sub3": 84.0, "sub4": 80.0},
    {"name": "Corteva (DowDuPont)", "sub1": 88.0, "sub2": 84.0, "sub3": 80.0, "sub4": 76.0},
    {"name": "Syngenta/ChemChina",  "sub1": 86.0, "sub2": 80.0, "sub3": 78.0, "sub4": 76.0},
    {"name": "BASF Seeds",          "sub1": 82.0, "sub2": 77.0, "sub3": 75.0, "sub4": 74.0},
    {"name": "Limagrain",           "sub1": 64.0, "sub2": 60.0, "sub3": 58.0, "sub4": 56.0},
    {"name": "KWS Seeds",           "sub1": 58.0, "sub2": 54.0, "sub3": 52.0, "sub4": 50.0},
    {"name": "Rijk Zwaan",          "sub1": 40.0, "sub2": 36.0, "sub3": 34.0, "sub4": 32.0},
    {"name": "La Via Campesina",    "sub1": 18.0, "sub2": 17.0, "sub3": 16.0, "sub4": 14.0},
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
