#!/usr/bin/env python3
"""CaelumSwarm™ — Tobacco Nicotine Poisoning Rights Engine (Wave 299)

Domaine : "Green Tobacco Sickness" — absorption cutanée de nicotine par les
travailleurs du tabac sans équipements de protection individuelle (EPI)
(USA — Caroline du Nord, Brésil — Rio Grande do Sul/Bahia,
Zimbabwe, Bangladesh — sans protections, travail en conditions humides)
"""
import json, statistics

ENTITIES = [
    # (ID, sub1_nic_exposure_severity, sub2_epi_absence, sub3_health_access, sub4_wage_vulnerability)
    ("TNP-001", 99, 97, 95, 93),  # Bangladesh — Kushtia/Jhenaidah, GTS aigu sans aucun EPI, accès santé nul
    ("TNP-002", 93, 90, 88, 86),  # Zimbabwe — Mashonaland, travailleurs saisonniers migrants, zéro formation
    ("TNP-003", 85, 82, 80, 78),  # Brésil — Bahia, petits producteurs familiaux, exposition enfants incluse
    ("TNP-004", 80, 77, 75, 73),  # Brésil — Rio Grande do Sul, GTS documenté 40% travailleurs, HRW 2011
    ("TNP-005", 61, 58, 56, 54),  # Malawi — zone Lilongwe, contrats informels, absence contrôle sanitaire
    ("TNP-006", 51, 48, 46, 44),  # USA — Caroline du Nord, Latino migrants, gants distribués mais non portés
    ("TNP-007", 32, 29, 27, 25),  # Inde — Andhra Pradesh, tabac Burley, programmes prévention partiels APVS
    ("TNP-008", 13, 11, 9, 7),    # USA — Kentucky, exploitations certifiées, EPI obligatoires, cliniques mobiles
]

WEIGHTS = (0.30, 0.25, 0.25, 0.20)
THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}


def classify(score):
    if score >= THRESHOLDS["critique"]:
        return "critique"
    if score >= THRESHOLDS["élevé"]:
        return "élevé"
    if score >= THRESHOLDS["modéré"]:
        return "modéré"
    return "faible"


def compute():
    results = []
    for entity in ENTITIES:
        eid, *subs = entity
        composite = sum(s * w for s, w in zip(subs, WEIGHTS))
        results.append({
            "entity": eid,
            "composite_score": round(composite, 2),
            "risk_level": classify(composite),
            "estimated_tobacco_nicotine_poisoning_index": round(composite / 100 * 10, 2),
        })
    avg = statistics.mean(r["composite_score"] for r in results)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1
    return {
        "entities": results,
        "avg_composite": round(avg, 2),
        "distribution": distribution,
    }


if __name__ == "__main__":
    output = compute()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    avg = output["avg_composite"]
    dist = output["distribution"]
    assert avg >= 60, f"avg_composite trop bas: {avg}"
    assert dist.get("critique", 0) == 4
    assert dist.get("élevé", 0) == 2
    assert dist.get("modéré", 0) == 1
    assert dist.get("faible", 0) == 1
    print("✓ Assertions passées")
