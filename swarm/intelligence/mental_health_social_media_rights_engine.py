#!/usr/bin/env python3
"""Mental Health Social Media Rights Engine — CaelumSwarm™ Wave 208 | CSDDD Art.8-13"""
import json
from datetime import datetime

DOMAIN_CODE = "MHS"
ACCENT_COLOR = "#2d1b69"
ENTITIES = [
    {"name": "Instagram (body image)", "sub1": 94.0, "sub2": 92.0, "sub3": 90.0, "sub4": 93.0},
    {"name": "TikTok (addiction algorithm)", "sub1": 96.0, "sub2": 94.0, "sub3": 92.0, "sub4": 95.0},
    {"name": "Snapchat (streaks)", "sub1": 82.0, "sub2": 78.0, "sub3": 76.0, "sub4": 80.0},
    {"name": "YouTube (autoplay)", "sub1": 78.0, "sub2": 74.0, "sub3": 72.0, "sub4": 76.0},
    {"name": "Facebook (teens)", "sub1": 59.0, "sub2": 56.0, "sub3": 58.0, "sub4": 54.0},
    {"name": "Twitter/X (toxic discourse)", "sub1": 56.0, "sub2": 53.0, "sub3": 54.0, "sub4": 52.0},
    {"name": "Pinterest", "sub1": 32.0, "sub2": 28.0, "sub3": 30.0, "sub4": 26.0},
    {"name": "Center for Humane Technology", "sub1": 12.0, "sub2": 8.0, "sub3": 10.0, "sub4": 6.0},
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
