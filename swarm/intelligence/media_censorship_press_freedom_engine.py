#!/usr/bin/env python3
"""
Media Censorship Press Freedom Engine — CaelumSwarm™
CSDDD Art.8-13 | Censure médiatique et liberté de presse
"""
import json
from datetime import datetime

DOMAIN_CODE = "MCP"
ACCENT_COLOR = "#dc2626"

ENTITIES = [
    {"name": "North Korea", "sub1": 92.0, "sub2": 90.0, "sub3": 88.0, "sub4": 90.0},
    {"name": "Eritrea", "sub1": 88.0, "sub2": 86.0, "sub3": 85.0, "sub4": 84.0},
    {"name": "Turkmenistan", "sub1": 86.0, "sub2": 84.0, "sub3": 82.0, "sub4": 83.0},
    {"name": "China", "sub1": 80.0, "sub2": 78.0, "sub3": 76.0, "sub4": 78.0},
    {"name": "Russia", "sub1": 58.0, "sub2": 55.0, "sub3": 57.0, "sub4": 54.0},
    {"name": "Belarus", "sub1": 55.0, "sub2": 53.0, "sub3": 56.0, "sub4": 52.0},
    {"name": "Egypt", "sub1": 35.0, "sub2": 32.0, "sub3": 34.0, "sub4": 30.0},
    {"name": "CPJ (Committee to Protect Journalists)", "sub1": 8.0, "sub2": 6.0, "sub3": 5.0, "sub4": 10.0},
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
