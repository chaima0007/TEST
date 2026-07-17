import json

ENTITIES = [
    ("Brave Ads BAT", 99, 97, 95, 93),
    ("Coinzilla Crypto Ads", 93, 90, 88, 86),
    ("Adshares Web3", 85, 82, 80, 78),
    ("Token Ads Platform", 80, 77, 75, 73),
    ("DappRadar Ads", 61, 58, 56, 54),
    ("CoinTraffic Network", 51, 48, 46, 44),
    ("A-ADS Crypto", 32, 29, 27, 25),
    ("Bitmedia Network", 13, 11,  9,  7),
]

def compute(entity):
    name, s1, s2, s3, s4 = entity
    score = round(s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20, 2)
    if score >= 60: level = "critique"
    elif score >= 40: level = "élevé"
    elif score >= 20: level = "modéré"
    else: level = "faible"
    idx = round(score / 100 * 10, 2)
    return {"name": name, "composite_score": score, "risk_level": level, "estimated_web3advertising_index": idx}

def run():
    results = [compute(e) for e in ENTITIES]
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    payload = {"domain": "web3advertising-advertising", "entities": results, "avg_composite": avg, "distribution": dist}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload

if __name__ == "__main__":
    run()
