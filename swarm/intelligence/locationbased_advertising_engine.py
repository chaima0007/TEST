import json

ENTITIES = [
    {"name": "Meta Platforms", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Alphabet (Google)", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Amazon Advertising", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "Microsoft Advertising", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "The Trade Desk", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Criteo", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "DoubleVerify", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Integral Ad Science", "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7},
]

domain = "locationbased"

results = []
for e in ENTITIES:
    score = round(e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20, 2)
    if score >= 60: risk = "critique"
    elif score >= 40: risk = "élevé"
    elif score >= 20: risk = "modéré"
    else: risk = "faible"
    results.append({**e, "composite_score": score, "risk_level": risk,
                    f"estimated_{domain}_index": round(score/100 * 10, 2)})

avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
dist = {}
for r in results:
    dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

output = {"domain": domain, "entities": results, "avg_composite": avg, "distribution": dist}
print(json.dumps(output, ensure_ascii=False, indent=2))
