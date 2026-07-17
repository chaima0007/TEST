"""CaelumSwarm™ — Flash Sale Advertising Child Labor Rights Engine
© 2024-2026 Caelum Partners SPRL"""

ENTITIES = [
    ("Flash Sale Platform Corp", 99, 97, 95, 93),
    ("Overstock Liquidator Co", 93, 90, 88, 86),
    ("Deal Aggregator Systems", 85, 82, 80, 78),
    ("Express Logistics MFG", 80, 77, 75, 73),
    ("Discount Warehouse Ops", 61, 58, 56, 54),
    ("Bulk Import Supplier", 51, 48, 46, 44),
    ("Return Processing Co", 32, 29, 27, 25),
    ("Warehouse Labor Supply", 13, 11, 9, 7),
]

def compute(entity):
    name, s1, s2, s3, s4 = entity
    score = round(s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20, 2)
    if score >= 60: level = "critique"
    elif score >= 40: level = "élevé"
    elif score >= 20: level = "modéré"
    else: level = "faible"
    idx = round(score / 100 * 10, 2)
    return {"name": name, "composite_score": score, "risk_level": level, "estimated_flashsale_index": idx}

if __name__ == "__main__":
    results = [compute(e) for e in ENTITIES]
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {l: sum(1 for r in results if r["risk_level"] == l) for l in ["critique","élevé","modéré","faible"]}
    for r in results:
        print(f"{r['name']}: {r['composite_score']} ({r['risk_level']})")
    print(f"avg={avg}, dist={dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Bad dist: {dist}"
    print("✓ Engine flashsale valide")
