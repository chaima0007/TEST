#!/usr/bin/env python3
"""
Corporate Impunity Legal Gap Engine — CaelumSwarm™ Wave 194
Domain: corporate_impunity_legal_gap | Prefix: CIL | Accent: #7c3aed
"""
import json
from datetime import datetime, timezone

DOMAIN = "corporate_impunity_legal_gap"
ACCENT = "#7c3aed"
WAVE = 194

ENTITIES = [
    # CIL-001: Shell Nigeria — target composite ~93 (critique)
    # 95*0.30 + 94*0.25 + 91*0.25 + 92*0.20 = 28.5 + 23.5 + 22.75 + 18.4 = 93.15
    {
        "id": "CIL-001",
        "name": "Shell Nigeria — 50 Ans Impunité Pétrole Delta Niger, 0 Condamné",
        "corporate_liability_evasion_score": 95.0,
        "victim_access_justice_barrier_score": 94.0,
        "extraterritorial_jurisdiction_gap_score": 91.0,
        "enforcement_capacity_deficit_score": 92.0,
    },
    # CIL-002: Chevron Ecuador — target composite ~88 (critique)
    # 90*0.30 + 88*0.25 + 87*0.25 + 87*0.20 = 27.0 + 22.0 + 21.75 + 17.4 = 88.15
    {
        "id": "CIL-002",
        "name": "Chevron Ecuador — Procès 20 Ans, Jugement 9.5Mds$ Non Exécuté",
        "corporate_liability_evasion_score": 90.0,
        "victim_access_justice_barrier_score": 88.0,
        "extraterritorial_jurisdiction_gap_score": 87.0,
        "enforcement_capacity_deficit_score": 87.0,
    },
    # CIL-003: Glencore DRC — target composite ~85 (critique)
    # 87*0.30 + 85*0.25 + 84*0.25 + 83*0.20 = 26.1 + 21.25 + 21.0 + 16.6 = 84.95
    {
        "id": "CIL-003",
        "name": "Glencore DRC — Cobalt Enfants, Procédures Belgique Bloquées",
        "corporate_liability_evasion_score": 87.0,
        "victim_access_justice_barrier_score": 85.0,
        "extraterritorial_jurisdiction_gap_score": 84.0,
        "enforcement_capacity_deficit_score": 83.0,
    },
    # CIL-004: Facebook Myanmar — target composite ~81 (critique)
    # 78*0.30 + 80*0.25 + 85*0.25 + 82*0.20 = 23.4 + 20.0 + 21.25 + 16.4 = 81.05
    {
        "id": "CIL-004",
        "name": "Facebook Myanmar — Génocide Amplifié, Immunité Section 230 USA",
        "corporate_liability_evasion_score": 78.0,
        "victim_access_justice_barrier_score": 80.0,
        "extraterritorial_jurisdiction_gap_score": 85.0,
        "enforcement_capacity_deficit_score": 82.0,
    },
    # CIL-005: Nestlé Côte d'Ivoire — target composite ~57 (élevé)
    # 58*0.30 + 56*0.25 + 58*0.25 + 56*0.20 = 17.4 + 14.0 + 14.5 + 11.2 = 57.1
    {
        "id": "CIL-005",
        "name": "Nestlé Côte d'Ivoire — Travail Enfants Cacao, Procès SCOTUS Rejeté",
        "corporate_liability_evasion_score": 58.0,
        "victim_access_justice_barrier_score": 56.0,
        "extraterritorial_jurisdiction_gap_score": 58.0,
        "enforcement_capacity_deficit_score": 56.0,
    },
    # CIL-006: H&M Bangladesh — target composite ~52 (élevé)
    # 54*0.30 + 52*0.25 + 50*0.25 + 52*0.20 = 16.2 + 13.0 + 12.5 + 10.4 = 52.1
    {
        "id": "CIL-006",
        "name": "H&M Bangladesh — Effondrement Rana Plaza, Compensations Partielles",
        "corporate_liability_evasion_score": 54.0,
        "victim_access_justice_barrier_score": 52.0,
        "extraterritorial_jurisdiction_gap_score": 50.0,
        "enforcement_capacity_deficit_score": 52.0,
    },
    # CIL-007: Apple-Foxconn — target composite ~27 (modéré)
    # 28*0.30 + 27*0.25 + 26*0.25 + 27*0.20 = 8.4 + 6.75 + 6.5 + 5.4 = 27.05
    {
        "id": "CIL-007",
        "name": "Apple-Foxconn — Accord Moniteur Indépendant, Améliorations Partielles",
        "corporate_liability_evasion_score": 28.0,
        "victim_access_justice_barrier_score": 27.0,
        "extraterritorial_jurisdiction_gap_score": 26.0,
        "enforcement_capacity_deficit_score": 27.0,
    },
    # CIL-008: Patagonia — target composite ~9 (faible)
    # 8*0.30 + 9*0.25 + 10*0.25 + 9*0.20 = 2.4 + 2.25 + 2.5 + 1.8 = 8.95
    {
        "id": "CIL-008",
        "name": "Patagonia — Traçabilité Totale, B-Corp, Engagements Légaux Volontaires",
        "corporate_liability_evasion_score": 8.0,
        "victim_access_justice_barrier_score": 9.0,
        "extraterritorial_jurisdiction_gap_score": 10.0,
        "enforcement_capacity_deficit_score": 9.0,
    },
]


def compute_composite(e):
    return round(
        e["corporate_liability_evasion_score"] * 0.30
        + e["victim_access_justice_barrier_score"] * 0.25
        + e["extraterritorial_jurisdiction_gap_score"] * 0.25
        + e["enforcement_capacity_deficit_score"] * 0.20,
        2
    )


def risk_level(score):
    if score >= 60:
        return "critique"
    if score >= 40:
        return "élevé"
    if score >= 20:
        return "modéré"
    return "faible"


def run():
    entities = []
    for e in ENTITIES:
        composite = compute_composite(e)
        entities.append({
            "id": e["id"],
            "name": e["name"],
            "composite_score": composite,
            "risk_level": risk_level(composite),
            "corporate_liability_evasion_score": e["corporate_liability_evasion_score"],
            "victim_access_justice_barrier_score": e["victim_access_justice_barrier_score"],
            "extraterritorial_jurisdiction_gap_score": e["extraterritorial_jurisdiction_gap_score"],
            "enforcement_capacity_deficit_score": e["enforcement_capacity_deficit_score"],
            "estimated_corporate_impunity_legal_gap_index": round(composite / 100 * 10, 2),
        })

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        dist[e["risk_level"]] += 1

    avg = round(sum(e["composite_score"] for e in entities) / len(entities), 2)

    payload = {
        "domain": DOMAIN,
        "wave": WAVE,
        "accent": ACCENT,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "avg_composite": avg,
        "risk_distribution": dist,
        "entities": entities,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\n✅ avg={avg} | dist={dist}", flush=True)
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution invalide: {dist}"
    return payload


if __name__ == "__main__":
    run()
