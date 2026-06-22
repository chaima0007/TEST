#!/usr/bin/env python3
"""Debt Bondage Migrant Workers Engine — CaelumSwarm™ Wave 205 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "DBM"
ACCENT_COLOR = "#4c0519"
ENTITIES = [
    # critique (≥60)
    {"name": "Qatar (kafala)", "sub1": 94.0, "sub2": 92.0, "sub3": 91.0, "sub4": 89.0},
    {"name": "UAE construction", "sub1": 91.0, "sub2": 88.0, "sub3": 87.0, "sub4": 85.0},
    {"name": "Saudi Arabia domestic", "sub1": 86.0, "sub2": 83.0, "sub3": 82.0, "sub4": 80.0},
    {"name": "Kuwait construction", "sub1": 80.0, "sub2": 77.0, "sub3": 76.0, "sub4": 74.0},
    # élevé (40-59)
    {"name": "Bahrain hospitality", "sub1": 56.0, "sub2": 53.0, "sub3": 52.0, "sub4": 50.0},
    {"name": "Oman agriculture", "sub1": 54.0, "sub2": 51.0, "sub3": 50.0, "sub4": 48.0},
    # modéré (20-39)
    {"name": "Jordan garment industry", "sub1": 30.0, "sub2": 27.0, "sub3": 26.0, "sub4": 24.0},
    # faible (<20)
    {"name": "ILO Fair Recruitment Initiative", "sub1": 13.0, "sub2": 11.0, "sub3": 10.0, "sub4": 9.0},
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
