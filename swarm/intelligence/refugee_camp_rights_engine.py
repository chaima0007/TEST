#!/usr/bin/env python3
"""
Refugee Camp Rights Engine — CaelumSwarm™ Wave 194
Domain: refugee_camp_rights | Prefix: RCR | Accent: #0891b2
"""
import json
from datetime import datetime, timezone

DOMAIN = "refugee_camp_rights"
ACCENT = "#0891b2"
WAVE = 194

ENTITIES = [
    {
        "id": "RCR-001",
        "name": "Cox's Bazar Bangladesh — 900K Rohingyas, Surpopulation Catastrophique",
        # composite target ~94 → critique
        "camp_living_conditions_score": 98,
        "protection_from_violence_score": 92,
        "freedom_of_movement_score": 95,
        "legal_status_access_score": 88,
    },
    {
        "id": "RCR-002",
        "name": "Dadaab Kenya — 220K Réfugiés 30 Ans, Conditions Dégradées",
        # composite target ~88 → critique
        "camp_living_conditions_score": 90,
        "protection_from_violence_score": 88,
        "freedom_of_movement_score": 86,
        "legal_status_access_score": 84,
    },
    {
        "id": "RCR-003",
        "name": "Zaatari Jordanie — 80K Syriens, Accès Eau Limité & Violences",
        # composite target ~85 → critique
        "camp_living_conditions_score": 87,
        "protection_from_violence_score": 85,
        "freedom_of_movement_score": 84,
        "legal_status_access_score": 80,
    },
    {
        "id": "RCR-004",
        "name": "Moria Lesbos Grèce — Surpopulation Extrême, Incendie 2020",
        # composite target ~82 → critique
        "camp_living_conditions_score": 85,
        "protection_from_violence_score": 82,
        "freedom_of_movement_score": 80,
        "legal_status_access_score": 76,
    },
    {
        "id": "RCR-005",
        "name": "Kakuma Kenya — 190K Réfugiés, Services Insuffisants",
        # composite target ~56 → élevé
        "camp_living_conditions_score": 58,
        "protection_from_violence_score": 55,
        "freedom_of_movement_score": 57,
        "legal_status_access_score": 50,
    },
    {
        "id": "RCR-006",
        "name": "Nyarugusu Tanzanie — 150K Congolais, Rations Réduites",
        # composite target ~51 → élevé
        "camp_living_conditions_score": 53,
        "protection_from_violence_score": 50,
        "freedom_of_movement_score": 52,
        "legal_status_access_score": 46,
    },
    {
        "id": "RCR-007",
        "name": "Azraq Jordanie — Meilleure Gestion, Énergie Solaire",
        # composite target ~27 → modéré
        "camp_living_conditions_score": 28,
        "protection_from_violence_score": 26,
        "freedom_of_movement_score": 27,
        "legal_status_access_score": 25,
    },
    {
        "id": "RCR-008",
        "name": "Za'atari Amélioration — Nouvelles Infrastructures UNHCR",
        # composite target ~9 → faible
        "camp_living_conditions_score": 10,
        "protection_from_violence_score": 9,
        "freedom_of_movement_score": 8,
        "legal_status_access_score": 7,
    },
]


def compute_composite(e):
    return round(
        e["camp_living_conditions_score"] * 0.30
        + e["protection_from_violence_score"] * 0.25
        + e["freedom_of_movement_score"] * 0.25
        + e["legal_status_access_score"] * 0.20,
        2,
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
        entities.append(
            {
                "id": e["id"],
                "name": e["name"],
                "composite_score": composite,
                "risk_level": risk_level(composite),
                "camp_living_conditions_score": e["camp_living_conditions_score"],
                "protection_from_violence_score": e["protection_from_violence_score"],
                "freedom_of_movement_score": e["freedom_of_movement_score"],
                "legal_status_access_score": e["legal_status_access_score"],
                "estimated_refugee_camp_rights_index": round(composite / 100 * 10, 2),
            }
        )

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
    assert dist == {
        "critique": 4,
        "élevé": 2,
        "modéré": 1,
        "faible": 1,
    }, f"Distribution invalide: {dist}"
    return payload


if __name__ == "__main__":
    run()
