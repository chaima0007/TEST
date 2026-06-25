#!/usr/bin/env python3
"""CaelumSwarm™ — connectedtv Risk Engine (Wave 452)"""

ENTITIES = [
    (99, 97, 95, 93),
    (93, 90, 88, 86),
    (85, 82, 80, 78),
    (80, 77, 75, 73),
    (61, 58, 56, 54),
    (51, 48, 46, 44),
    (32, 29, 27, 25),
    (13, 11,  9,  7),
]

def composite(s):
    return s[0]*0.30 + s[1]*0.25 + s[2]*0.25 + s[3]*0.20

def level(c):
    if c >= 60: return "critique"
    if c >= 40: return "élevé"
    if c >= 20: return "modéré"
    return "faible"

results = []
for i, s in enumerate(ENTITIES):
    c = composite(s)
    results.append({"entity": f"entity_{i+1}", "composite": round(c, 2), "level": level(c)})

avg = sum(r["composite"] for r in results) / len(results)
dist = {l: sum(1 for r in results if r["level"] == l) for l in ["critique","élevé","modéré","faible"]}

print(f"avg_composite: {round(avg, 2)}")
print(f"distribution: {dist}")
print(f"estimated_connectedtv_index: {round(avg/100*10, 2)}")
for r in results:
    print(f"  {r['entity']}: {r['composite']} ({r['level']})")
