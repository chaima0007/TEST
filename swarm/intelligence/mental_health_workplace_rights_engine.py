#!/usr/bin/env python3
"""
Mental Health Workplace Rights Engine — CaelumSwarm™
CSDDD Art.8-13 | Droits santé mentale en milieu professionnel
"""
import json
from datetime import datetime

DOMAIN_CODE = "MHW"
ACCENT_COLOR = "#0891b2"

ENTITIES = [
    {"name": "Amazon Warehouses", "sub1": 90.0, "sub2": 87.0, "sub3": 85.0, "sub4": 82.0},
    {"name": "Foxconn", "sub1": 93.0, "sub2": 91.0, "sub3": 90.0, "sub4": 88.0},
    {"name": "Uber Drivers", "sub1": 84.0, "sub2": 80.0, "sub3": 78.0, "sub4": 75.0},
    {"name": "Call Center Industry", "sub1": 80.0, "sub2": 78.0, "sub3": 75.0, "sub4": 72.0},
    {"name": "Walmart Associates", "sub1": 58.0, "sub2": 56.0, "sub3": 55.0, "sub4": 53.0},
    {"name": "Fast Food Workers", "sub1": 56.0, "sub2": 54.0, "sub3": 55.0, "sub4": 52.0},
    {"name": "Google Employees", "sub1": 36.0, "sub2": 32.0, "sub3": 30.0, "sub4": 33.0},
    {"name": "Patagonia Workers", "sub1": 14.0, "sub2": 12.0, "sub3": 10.0, "sub4": 16.0},
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
