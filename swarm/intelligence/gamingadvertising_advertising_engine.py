import json

ENTITIES = [
    ("Unity Ads Platform", 99, 97, 95, 93),
    ("IronSource Gaming Ads", 93, 90, 88, 86),
    ("AppLovin Gaming", 85, 82, 80, 78),
    ("Verizon Gaming Ads", 80, 77, 75, 73),
    ("Activision Blizzard Ads", 61, 58, 56, 54),
    ("Electronic Arts Advertising", 51, 48, 46, 44),
    ("Roblox Advertising", 32, 29, 27, 25),
    ("Miniclip Ads Network", 13, 11, 9, 7),
]

def compute(entity):
    name, s1, s2, s3, s4 = entity
    score = round(s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20, 2)
    if score >= 60: level = "critique"
    elif score >= 40: level = "élevé"
    elif score >= 20: level = "modéré"
    else: level = "faible"
    idx = round(score / 100 * 10, 2)
    return {"name": name, "composite_score": score, "risk_level": level, "estimated_gamingadvertising_index": idx}

def run():
    results = [compute(e) for e in ENTITIES]
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    payload = {"domain": "gamingadvertising-advertising", "entities": results, "avg_composite": avg, "distribution": dist}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload

if __name__ == "__main__":
    run()
