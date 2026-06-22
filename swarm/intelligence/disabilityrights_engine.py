#!/usr/bin/env python3
"""CaelumSwarm™ — Disability Rights Risk Engine (Wave 490 — CRPD ONU)"""
import json

ENTITIES = [
    {"name": "Workplace Accessibility Denial", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93, "level": "critique"},
    {"name": "Reasonable Accommodation Refusal", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86, "level": "critique"},
    {"name": "Employment Discrimination Disability", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78, "level": "critique"},
    {"name": "Social Protection Exclusion CRPD", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73, "level": "critique"},
    {"name": "Education Inclusion Barrier", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54, "level": "élevé"},
    {"name": "Healthcare Access Disability Gap", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44, "level": "élevé"},
    {"name": "Digital Accessibility Compliance", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25, "level": "modéré"},
    {"name": "Transport Mobility Adaptation", "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7, "level": "faible"},
]

def compute(e):
    return e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20

results = []
for e in ENTITIES:
    score = compute(e)
    results.append({**e, "composite_score": round(score, 2)})

avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
dist = {l: sum(1 for r in results if r["level"] == l) for l in ["critique", "élevé", "modéré", "faible"]}
idx = round(avg / 100 * 10, 2)

print(f"avg_composite: {avg}")
print(f"distribution: {dist}")
print(f"estimated_disabilityrights_index: {idx}")
print(json.dumps(results, indent=2, ensure_ascii=False))
