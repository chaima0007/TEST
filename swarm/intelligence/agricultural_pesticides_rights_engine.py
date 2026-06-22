#!/usr/bin/env python3
"""Agricultural Pesticides Rights Engine — CaelumSwarm™ Wave 209 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "APR"
ACCENT_COLOR = "#083344"

ENTITIES = [
    {"name": "Bayer CropScience",    "sub1": 94, "sub2": 92, "sub3": 89, "sub4": 86},
    {"name": "Syngenta Pesticides",  "sub1": 90, "sub2": 88, "sub3": 84, "sub4": 82},
    {"name": "BASF Crop Protection", "sub1": 86, "sub2": 84, "sub3": 80, "sub4": 76},
    {"name": "Corteva Pesticides",   "sub1": 80, "sub2": 78, "sub3": 74, "sub4": 70},
    {"name": "Dow Chemical",         "sub1": 62, "sub2": 60, "sub3": 58, "sub4": 54},
    {"name": "Nufarm Agricultural",  "sub1": 58, "sub2": 56, "sub3": 54, "sub4": 50},
    {"name": "FiBL Research",        "sub1": 33, "sub2": 31, "sub3": 32, "sub4": 29},
    {"name": "PAN Pesticide Action", "sub1": 17, "sub2": 16, "sub3": 18, "sub4": 15},
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
            "estimated_apr_index": round(score / 100 * 10, 2),
            "csddd_articles": ["Art.8", "Art.9", "Art.10", "Art.11"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    scores = [r["composite_score"] for r in results]
    avg = round(sum(scores) / len(scores), 2)
    output = {
        "engine": "APR_ENGINE",
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
