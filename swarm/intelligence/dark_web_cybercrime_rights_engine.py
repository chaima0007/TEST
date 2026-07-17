"""dark_web_cybercrime_rights_engine.py — Wave 192"""

ENTITIES = [
    {
        "id": "DWC-001",
        "name": "Russie — Infrastructure Cybercrime État-Parrain, Impunité Totale",
        "country": "Russie",
        "cybercrime_infrastructure_state_nexus_score": 96,
        "victim_rights_redress_deficit_score": 92,
        "law_enforcement_overreach_rights_score": 88,
        "digital_privacy_erosion_score": 90,
        "primary_pattern": "APT29/Sandworm opèrent avec protection FSB, ransomware REvil toléré, victimes sans recours",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-002",
        "name": "Corée du Nord — Lazarus Group, Cybercrime Financement Régime",
        "country": "Corée du Nord",
        "cybercrime_infrastructure_state_nexus_score": 97,
        "victim_rights_redress_deficit_score": 95,
        "law_enforcement_overreach_rights_score": 85,
        "digital_privacy_erosion_score": 93,
        "primary_pattern": "Lazarus Group vole 3B$/an, financement missiles nucléaires, citoyens DPRK zéro droits numériques",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-003",
        "name": "Chine — Grand Firewall, APT41, Surveillance Numérique Totale",
        "country": "Chine",
        "cybercrime_infrastructure_state_nexus_score": 93,
        "victim_rights_redress_deficit_score": 88,
        "law_enforcement_overreach_rights_score": 94,
        "digital_privacy_erosion_score": 96,
        "primary_pattern": "APT41 hybride espionnage/cybercrime, PIPL détournée surveillance, dissidents ciblés dark web",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-004",
        "name": "Iran — MOIS Cyberops, Journalistes & Opposants Traqués",
        "country": "Iran",
        "cybercrime_infrastructure_state_nexus_score": 88,
        "victim_rights_redress_deficit_score": 90,
        "law_enforcement_overreach_rights_score": 91,
        "digital_privacy_erosion_score": 87,
        "primary_pattern": "Phosphorus/Charming Kitten cible diaspora iranienne, VPN criminalisé, journalistes surveillés Tor",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-005",
        "name": "Nigéria — Fraude BEC, Victimes Sans Protection Légale",
        "country": "Nigéria",
        "cybercrime_infrastructure_state_nexus_score": 52,
        "victim_rights_redress_deficit_score": 58,
        "law_enforcement_overreach_rights_score": 48,
        "digital_privacy_erosion_score": 50,
        "primary_pattern": "Business Email Compromise 1.5B$/an, EFCC sous-financée, victimes internationales sans recours",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-006",
        "name": "Brésil — Darkweb Favelas, Trafic Données Personnelles",
        "country": "Brésil",
        "cybercrime_infrastructure_state_nexus_score": 48,
        "victim_rights_redress_deficit_score": 55,
        "law_enforcement_overreach_rights_score": 52,
        "digital_privacy_erosion_score": 53,
        "primary_pattern": "220M données personnelles vendues dark web 2021, forums cybercrime Lusophone, LGPD ineffective",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-007",
        "name": "Inde — Dark Web Trafic Données Biométriques Aadhaar",
        "country": "Inde",
        "cybercrime_infrastructure_state_nexus_score": 28,
        "victim_rights_redress_deficit_score": 32,
        "law_enforcement_overreach_rights_score": 26,
        "digital_privacy_erosion_score": 30,
        "primary_pattern": "Données Aadhaar 1.1B citoyens vendues dark web, IT Act utilisé contre journalistes, protection faible",
        "last_updated": "2026-06-21",
    },
    {
        "id": "DWC-008",
        "name": "Pays-Bas — Europol Leader Anti-Cybercrime, Droits Numériques Protégés",
        "country": "Pays-Bas",
        "cybercrime_infrastructure_state_nexus_score": 6,
        "victim_rights_redress_deficit_score": 5,
        "law_enforcement_overreach_rights_score": 8,
        "digital_privacy_erosion_score": 7,
        "primary_pattern": "Siège Europol, démantèlement Hive ransomware, RGPD strict, droits numériques constitutionnels",
        "last_updated": "2026-06-21",
    },
]


def compute(e):
    keys = sorted([k for k in e if k.endswith("_score")])
    s = (
        e[keys[0]] * 0.30
        + e[keys[1]] * 0.25
        + e[keys[2]] * 0.25
        + e[keys[3]] * 0.20
    )
    lv = (
        "critique" if s >= 60
        else "élevé" if s >= 40
        else "modéré" if s >= 20
        else "faible"
    )
    return {
        **e,
        "composite_score": round(s, 2),
        "risk_level": lv,
        "estimated_dark_web_cybercrime_rights_index": round(s / 100 * 10, 2),
    }


results = [compute(e) for e in ENTITIES]
dist = {
    l: sum(1 for r in results if r["risk_level"] == l)
    for l in ["critique", "élevé", "modéré", "faible"]
}
avg = sum(r["composite_score"] for r in results) / len(results)

print(f"avg_composite: {avg:.2f}")
print(f"distribution: {dist}")
for r in results:
    print(f"  {r['id']} | {r['composite_score']:.2f} | {r['risk_level']} | {r['estimated_dark_web_cybercrime_rights_index']}")

assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
print("✓ Distribution validée")
print(f"✓ avg_composite = {avg:.2f}")
