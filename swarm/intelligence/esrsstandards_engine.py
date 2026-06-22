#!/usr/bin/env python3
"""CaelumSwarm™ — ESRS Standards Risk Engine"""

ENTITIES = [
    {"name": "ESRS E1 Climate Change Non-Compliance",  "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "ESRS S1 Own Workforce Disclosure Gap",   "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "ESRS G1 Governance Transparency Risk",   "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "ESRS E3 Water Resources Compliance",     "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "ESRS S2 Value Chain Workers Gap",        "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "ESRS E4 Biodiversity Non-Reporting",     "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "ESRS S4 Consumer Rights Disclosure",     "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "ESRS E5 Circular Economy Reporting Gap", "sub1": 13, "sub2": 11, "sub3": 9,  "sub4": 7},
]

def compute(e):
    return e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20

SEUILS = {"critique": 60, "élevé": 40, "modéré": 20}

def classify(score):
    if score >= SEUILS["critique"]: return "critique"
    if score >= SEUILS["élevé"]: return "élevé"
    if score >= SEUILS["modéré"]: return "modéré"
    return "faible"

results = []
for e in ENTITIES:
    score = compute(e)
    results.append({**e, "composite_score": round(score, 2), "risk_level": classify(score)})

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
estimated_esrsstandards_index = round(avg_composite / 100 * 10, 2)

if __name__ == "__main__":
    for r in results:
        print(f"{r['risk_level']:10} | {r['composite_score']:5.2f} | {r['name']}")
    print(f"\navg_composite = {avg_composite}")
    print(f"estimated_esrsstandards_index = {estimated_esrsstandards_index}")
