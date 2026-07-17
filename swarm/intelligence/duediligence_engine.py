#!/usr/bin/env python3
"""CaelumSwarm™ — Due Diligence Risk Engine"""

DOMAIN = "duediligence"
ENTITIES = [
    {"name": "Foxconn (Electronics Supply Chain)", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},  # critique
    {"name": "Li & Fung (Garment Sourcing)", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},  # critique
    {"name": "Tyson Foods (Meatpacking Audit)", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},  # critique
    {"name": "Primark (Fast Fashion Tier-3)", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},  # critique
    {"name": "Tesco (Agricultural Sourcing)", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},  # élevé
    {"name": "Adidas (Sportswear Tier-2)", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},  # élevé
    {"name": "IKEA (Forest Procurement)", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},  # modéré
    {"name": "Fairtrade International (Benchmark)", "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7},  # faible
]

def compute(e):
    score = e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20
    risk = "critique" if score >= 60 else "élevé" if score >= 40 else "modéré" if score >= 20 else "faible"
    return {**e, "composite_score": round(score, 2), "risk_level": risk,
            f"estimated_{DOMAIN}_index": round(score / 100 * 10, 2)}

def main():
    results = [compute(e) for e in ENTITIES]
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Domain: {DOMAIN}")
    print(f"avg_composite: {avg}")
    print(f"distribution: {dist}")
    for r in results:
        print(f"  {r['name']}: {r['composite_score']} ({r['risk_level']})")

if __name__ == "__main__":
    main()
