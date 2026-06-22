#!/usr/bin/env python3
"""CaelumSwarm™ — Worker Safety Risk Engine"""

ENTITIES = [
    {"name": "Fatal Workplace Accident Risk",          "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Chemical Exposure Corporate Liability",  "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Psychosocial Risk at Work",              "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "PPE Non-Compliance Supply Chain",        "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "Ergonomic Hazard Management Gaps",       "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Heat Stress Outdoor Worker Risk",        "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "Noise Induced Occupational Disease",     "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Remote Worker Safety Protocol Gap",      "sub1": 13, "sub2": 11, "sub3": 9,  "sub4": 7},
]

def compute(e):
    return e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20

def classify(score):
    if score >= 60: return "critique"
    if score >= 40: return "élevé"
    if score >= 20: return "modéré"
    return "faible"

results = []
for e in ENTITIES:
    score = compute(e)
    results.append({**e, "composite_score": round(score, 2), "risk_level": classify(score)})

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
dist = {l: sum(1 for r in results if r["risk_level"] == l) for l in ["critique", "élevé", "modéré", "faible"]}
estimated_workersafety_index = round(avg_composite / 100 * 10, 2)

if __name__ == "__main__":
    print(f"avg_composite: {avg_composite}")
    print(f"distribution: {dist}")
    print(f"estimated_workersafety_index: {estimated_workersafety_index}")
    for r in results:
        print(f"  {r['name']}: {r['composite_score']} ({r['risk_level']})")
