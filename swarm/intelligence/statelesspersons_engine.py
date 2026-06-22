#!/usr/bin/env python3
"""CaelumSwarm™ — Stateless Persons Rights Engine"""

def analyze_statelesspersons_rights(entities):
    results = []
    for entity in entities:
        s1, s2, s3, s4 = entity["sub1"], entity["sub2"], entity["sub3"], entity["sub4"]
        composite = s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20
        if composite >= 60: level = "critique"
        elif composite >= 40: level = "élevé"
        elif composite >= 20: level = "modéré"
        else: level = "faible"
        results.append({"entity": entity["name"], "composite": round(composite, 2), "level": level})
    return results

ENTITIES = [
    {"name": "Gulf Bidoon Communities",     "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Rohingya Stateless",          "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Caribbean Dominicanness",     "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "Soviet Successor States",     "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "European Roma Stateless",     "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Nubian Kenyans",              "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "Hill Tribes Thailand",        "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Registered Non-Citizens",     "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7},
]

if __name__ == "__main__":
    results = analyze_statelesspersons_rights(ENTITIES)
    composites = [r["composite"] for r in results]
    avg = round(sum(composites)/len(composites), 2)
    levels = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        levels[r["level"]] += 1
    print("=== Stateless Persons Rights Engine ===")
    for r in results:
        print(f"  {r['entity']}: {r['composite']} ({r['level']})")
    print(f"\navg_composite = {avg}")
    print(f"Distribution: {levels['critique']} critique / {levels['élevé']} élevé / {levels['modéré']} modéré / {levels['faible']} faible")
    print(f"estimated_statelesspersons_index = {round(avg/100*10, 2)}")
