#!/usr/bin/env python3
"""
Conflict Mineral Supply Chain Rights Engine — CaelumSwarm™ Wave 194
Domain: conflict_mineral_supply_chain | Prefix: CMS | Accent: #dc2626
"""
import json
from datetime import datetime, timezone

DOMAIN = "conflict_mineral_supply_chain"
ACCENT = "#dc2626"
WAVE = 194

ENTITIES = [
    {
        "id": "CMS-001",
        "name": "DRC — Cobalt & Coltan Est-Congo, Financement Groupes Armés",
        "conflict_zone_sourcing_score": 97,
        "armed_group_financing_score": 95,
        "due_diligence_compliance_score": 91,
        "artisanal_miner_protection_score": 88,
    },
    {
        "id": "CMS-002",
        "name": "Myanmar — Jade & Rubis Kachin, Financement Armée & Milices",
        "conflict_zone_sourcing_score": 92,
        "armed_group_financing_score": 90,
        "due_diligence_compliance_score": 87,
        "artisanal_miner_protection_score": 86,
    },
    {
        "id": "CMS-003",
        "name": "Sudan/South Sudan — Or Darfour, Financement Milices Janjawid",
        "conflict_zone_sourcing_score": 90,
        "armed_group_financing_score": 88,
        "due_diligence_compliance_score": 83,
        "artisanal_miner_protection_score": 80,
    },
    {
        "id": "CMS-004",
        "name": "Zimbabwe — Chrome & Diamants Marange, Exploitation Militaire",
        "conflict_zone_sourcing_score": 85,
        "armed_group_financing_score": 83,
        "due_diligence_compliance_score": 81,
        "artisanal_miner_protection_score": 78,
    },
    {
        "id": "CMS-005",
        "name": "Colombie — Or Illégal Zones FARC, Blanchiment",
        "conflict_zone_sourcing_score": 62,
        "armed_group_financing_score": 58,
        "due_diligence_compliance_score": 54,
        "artisanal_miner_protection_score": 51,
    },
    {
        "id": "CMS-006",
        "name": "Pérou — Or Madre de Dios, Orpaillage Illégal & Mercure",
        "conflict_zone_sourcing_score": 57,
        "armed_group_financing_score": 53,
        "due_diligence_compliance_score": 50,
        "artisanal_miner_protection_score": 47,
    },
    {
        "id": "CMS-007",
        "name": "Bolivie — Étain Coopératives, Formalisation Partielle",
        "conflict_zone_sourcing_score": 32,
        "armed_group_financing_score": 29,
        "due_diligence_compliance_score": 26,
        "artisanal_miner_protection_score": 24,
    },
    {
        "id": "CMS-008",
        "name": "Canada — Normes RSDC, Traçabilité Blockchain Minière",
        "conflict_zone_sourcing_score": 9,
        "armed_group_financing_score": 8,
        "due_diligence_compliance_score": 7,
        "artisanal_miner_protection_score": 8,
    },
]


def compute_composite(e):
    return round(
        e["conflict_zone_sourcing_score"] * 0.30
        + e["armed_group_financing_score"] * 0.25
        + e["due_diligence_compliance_score"] * 0.25
        + e["artisanal_miner_protection_score"] * 0.20,
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
            "conflict_zone_sourcing_score": e["conflict_zone_sourcing_score"],
            "armed_group_financing_score": e["armed_group_financing_score"],
            "due_diligence_compliance_score": e["due_diligence_compliance_score"],
            "artisanal_miner_protection_score": e["artisanal_miner_protection_score"],
            "estimated_conflict_mineral_supply_chain_index": round(composite / 100 * 10, 2),
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
