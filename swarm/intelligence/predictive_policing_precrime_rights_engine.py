#!/usr/bin/env python3
"""CaelumSwarm™ — Predictive Policing & Pre-Crime Rights Engine"""
import random, json
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).parent.parent

ENTITIES = [
    {"name": "Algorithmic Racial Profiling", "level": "CRITIQUE", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Gang Database Wrongful Inclusion", "level": "CRITIQUE", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "PredPol Bias Against Black Communities", "level": "CRITIQUE", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "ShotSpotter False Positive Harm", "level": "CRITIQUE", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "Palantir Data Fusion Overreach", "level": "ELEVE", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Social Media Monitoring Chilling Effect", "level": "ELEVE", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "Risk Score Sentencing Bias", "level": "MODERE", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Predictive Bail Denial", "level": "FAIBLE", "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7},
]

def monte_carlo(e, n=50_000):
    base = e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20
    s = sum(1 for _ in range(n) if base * random.gauss(1, .15) * random.uniform(.8, 1.2) > 50)
    return {"success_rate": round(s / n * 100, 1), "approved": s / n >= .6}

def run():
    composites = []
    for e in ENTITIES:
        c = e["sub1"]*0.30 + e["sub2"]*0.25 + e["sub3"]*0.25 + e["sub4"]*0.20
        composites.append(c)
        mc = monte_carlo(e)
        print(f"  {'✓' if mc['approved'] else '·'} [{e['level']:8s}] {e['name'][:40]:40s} | {c:.2f} | {mc['success_rate']}%")
    avg = round(sum(composites) / 8, 2)
    print(f"\navg_composite = {avg}")
    print(f"estimated_predictive_policing_precrime_rights_index = {round(avg / 100 * 10, 2)}")

if __name__ == "__main__":
    run()
