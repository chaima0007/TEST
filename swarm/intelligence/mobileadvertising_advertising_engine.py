#!/usr/bin/env python3
"""CaelumSwarm™ — Mobile Advertising Compliance Engine CSDDD 2024/1760"""

ENTITIES = [
    ("Google Mobile Ads", 99, 97, 95, 93),
    ("Apple Search Ads", 93, 90, 88, 86),
    ("Meta Audience Network", 85, 82, 80, 78),
    ("Unity Ads", 80, 77, 75, 73),
    ("IronSource / Unity LevelPlay", 61, 58, 56, 54),
    ("AppLovin MAX", 51, 48, 46, 44),
    ("InMobi Platform", 32, 29, 27, 25),
    ("Verizon Media DSP", 13, 11, 9, 7),
]

def compute(entity):
    name, s1, s2, s3, s4 = entity
    score = round(s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20, 2)
    if score >= 60: level = "critique"
    elif score >= 40: level = "élevé"
    elif score >= 20: level = "modéré"
    else: level = "faible"
    idx = round(score / 100 * 10, 2)
    return {
        "name": name,
        "composite_score": score,
        "risk_level": level,
        "estimated_mobileadvertising_index": idx,
    }

if __name__ == "__main__":
    results = [compute(e) for e in ENTITIES]
    dist = {}
    total = 0
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
        total += r["composite_score"]
        print(r)
    avg = round(total / len(results), 2)
    print(f"\navg_composite={avg}")
    print(f"distribution={dist}")
