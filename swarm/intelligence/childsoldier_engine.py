#!/usr/bin/env python3
"""CaelumSwarm™ — Child Soldier Rehabilitation Engine"""
import statistics

def analyze_childsoldier_rights(entities):
    results = []
    for entity in entities:
        sub1 = statistics.mean(entity["indicators"][:4])
        sub2 = statistics.mean(entity["indicators"][4:8])
        sub3 = statistics.mean(entity["indicators"][8:12])
        sub4 = statistics.mean(entity["indicators"][12:16])
        composite = sub1*0.30 + sub2*0.25 + sub3*0.25 + sub4*0.20
        if composite >= 60: level = "critique"
        elif composite >= 40: level = "élevé"
        elif composite >= 20: level = "modéré"
        else: level = "faible"
        results.append({"entity": entity["name"], "composite": round(composite, 2), "level": level})
    return results

ENTITIES = [
    {"name": "DRC Armed Groups", "indicators": [99,97,95,93, 98,96,94,92, 97,95,93,91, 96,94,92,90]},
    {"name": "South Sudan Factions", "indicators": [93,90,88,86, 92,89,87,85, 91,88,86,84, 90,87,85,83]},
    {"name": "Myanmar Rebel Forces", "indicators": [85,82,80,78, 84,81,79,77, 83,80,78,76, 82,79,77,75]},
    {"name": "Somalia Al-Shabaab", "indicators": [80,77,75,73, 79,76,74,72, 78,75,73,71, 77,74,72,70]},
    {"name": "Colombia FARC Remnants", "indicators": [61,58,56,54, 60,57,55,53, 59,56,54,52, 58,55,53,51]},
    {"name": "CAR Militias", "indicators": [51,48,46,44, 50,47,45,43, 49,46,44,42, 48,45,43,41]},
    {"name": "Rehabilitation Centers", "indicators": [32,29,27,25, 31,28,26,24, 30,27,25,23, 29,26,24,22]},
    {"name": "Reintegration Programs", "indicators": [13,11,9,7, 12,10,8,6, 11,9,7,5, 10,8,6,4]},
]

if __name__ == "__main__":
    results = analyze_childsoldier_rights(ENTITIES)
    composites = [r["composite"] for r in results]
    avg = round(sum(composites)/len(composites), 2)
    levels = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        levels[r["level"]] += 1
    print("=== Child Soldier Rehabilitation Engine ===")
    for r in results:
        print(f"  {r['entity']}: {r['composite']} ({r['level']})")
    print(f"\navg_composite = {avg}")
    print(f"Distribution: {levels['critique']} critique / {levels['élevé']} élevé / {levels['modéré']} modéré / {levels['faible']} faible")
    print(f"estimated_childsoldier_index = {round(avg/100*10, 2)}")
