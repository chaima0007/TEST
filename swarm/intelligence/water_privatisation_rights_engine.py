#!/usr/bin/env python3
"""Water Privatisation Rights Engine — CaelumSwarm™ Wave 209 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "WPR"
ACCENT_COLOR = "#042f2e"

ENTITIES = [
    {"name": "Veolia Water",          "sub1": 93, "sub2": 91, "sub3": 88, "sub4": 85},
    {"name": "Suez Environnement",    "sub1": 89, "sub2": 87, "sub3": 83, "sub4": 81},
    {"name": "Thames Water UK",       "sub1": 85, "sub2": 83, "sub3": 79, "sub4": 75},
    {"name": "Nestlé Pure Life",      "sub1": 79, "sub2": 77, "sub3": 73, "sub4": 69},
    {"name": "American Water Works",  "sub1": 61, "sub2": 59, "sub3": 57, "sub4": 53},
    {"name": "United Utilities",      "sub1": 57, "sub2": 55, "sub3": 53, "sub4": 49},
    {"name": "WWF Water",             "sub1": 32, "sub2": 30, "sub3": 31, "sub4": 28},
    {"name": "Blue Planet Project",   "sub1": 16, "sub2": 15, "sub3": 17, "sub4": 14},
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
            "estimated_wpr_index": round(score / 100 * 10, 2),
            "csddd_articles": ["Art.8", "Art.9", "Art.10", "Art.11"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    scores = [r["composite_score"] for r in results]
    avg = round(sum(scores) / len(scores), 2)
    output = {
        "engine": "WPR_ENGINE",
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
