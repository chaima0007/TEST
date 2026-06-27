#!/usr/bin/env python3
"""
Geopolitical Risk Agent — Caelum Partners CaelumSwarm™
Analyse des risques géopolitiques impactant les scores droits humains.
Corrèle instabilité politique, sanctions, conflits avec violations DH.
"""

import sys
from datetime import datetime, timezone

GEOPOLITICAL_INDICATORS = {
    "CONFLICT_INTENSITY": {"weight": 0.25, "label": "Intensité conflit armé"},
    "REGIME_STABILITY": {"weight": 0.20, "label": "Stabilité régime politique"},
    "RULE_OF_LAW": {"weight": 0.20, "label": "État de droit"},
    "SANCTIONS_EXPOSURE": {"weight": 0.15, "label": "Exposition sanctions int."},
    "PRESS_FREEDOM": {"weight": 0.10, "label": "Liberté de la presse"},
    "CORRUPTION_LEVEL": {"weight": 0.10, "label": "Niveau de corruption"},
}

SANCTIONS_REGIMES = {
    "UN_SECURITY_COUNCIL": {"authority": "ONU", "binding": True, "scope": "Universel"},
    "EU_RESTRICTIVE_MEASURES": {"authority": "UE", "binding": True, "scope": "États membres"},
    "US_OFAC": {"authority": "États-Unis", "binding": False, "scope": "Entités US-nexus"},
    "UK_SANCTIONS": {"authority": "Royaume-Uni", "binding": False, "scope": "Entités UK-nexus"},
    "FATF_GREY_LIST": {"authority": "GAFI", "binding": False, "scope": "Recommandations"},
}

COUNTRY_GEOPOLITICAL_PROFILES = {
    "Myanmar": {
        "conflict_intensity": 95,
        "regime_stability": 10,
        "rule_of_law": 5,
        "sanctions_exposure": 90,
        "press_freedom": 8,
        "corruption_level": 85,
        "active_sanctions": ["EU_RESTRICTIVE_MEASURES", "US_OFAC", "UK_SANCTIONS"],
        "conflict_type": "Guerre civile + génocide",
        "icc_proceedings": True,
    },
    "Qatar": {
        "conflict_intensity": 5,
        "regime_stability": 85,
        "rule_of_law": 40,
        "sanctions_exposure": 10,
        "press_freedom": 20,
        "corruption_level": 45,
        "active_sanctions": [],
        "conflict_type": "Aucun",
        "icc_proceedings": False,
    },
    "Cayman Islands": {
        "conflict_intensity": 0,
        "regime_stability": 95,
        "rule_of_law": 70,
        "sanctions_exposure": 30,
        "press_freedom": 75,
        "corruption_level": 35,
        "active_sanctions": ["FATF_GREY_LIST"],
        "conflict_type": "Aucun",
        "icc_proceedings": False,
    },
    "Russia": {
        "conflict_intensity": 88,
        "regime_stability": 60,
        "rule_of_law": 20,
        "sanctions_exposure": 95,
        "press_freedom": 10,
        "corruption_level": 75,
        "active_sanctions": ["EU_RESTRICTIVE_MEASURES", "US_OFAC", "UK_SANCTIONS"],
        "conflict_type": "Guerre Ukraine + répression interne",
        "icc_proceedings": True,
    },
}

SCENARIO_TYPES = {
    "ESCALATION": "Aggravation — conflit s'intensifie ou régime se durcit",
    "STABILIZATION": "Stabilisation — cessez-le-feu ou ouverture politique",
    "REGIME_CHANGE": "Changement de régime — impact imprévisible ±30 pts",
    "SANCTIONS_EXPANSION": "Expansion sanctions — impact supply chain +15 pts",
    "SANCTIONS_RELIEF": "Levée partielle sanctions — opportunité -10 pts",
    "INTERNATIONAL_INTERVENTION": "Intervention internationale — réduction conflit -20 pts",
}


def compute_geopolitical_score(country: str) -> dict:
    """Calcule le score géopolitique d'un pays."""
    profile = COUNTRY_GEOPOLITICAL_PROFILES.get(country, {})
    if not profile:
        return {"error": f"Pays {country} non profilé"}

    indicator_values = {
        "CONFLICT_INTENSITY": profile.get("conflict_intensity", 50),
        "REGIME_STABILITY": 100 - profile.get("regime_stability", 50),
        "RULE_OF_LAW": 100 - profile.get("rule_of_law", 50),
        "SANCTIONS_EXPOSURE": profile.get("sanctions_exposure", 0),
        "PRESS_FREEDOM": 100 - profile.get("press_freedom", 50),
        "CORRUPTION_LEVEL": profile.get("corruption_level", 30),
    }

    geo_score = sum(
        indicator_values[ind] * cfg["weight"]
        for ind, cfg in GEOPOLITICAL_INDICATORS.items()
        if ind in indicator_values
    )

    geo_risk = (
        "CRITIQUE" if geo_score >= 70
        else "ÉLEVÉ" if geo_score >= 50
        else "MODÉRÉ" if geo_score >= 30
        else "FAIBLE"
    )

    sanctions = profile.get("active_sanctions", [])
    supply_chain_risk = (
        "PROHIBITIF" if "UN_SECURITY_COUNCIL" in sanctions
        else "TRÈS ÉLEVÉ" if len(sanctions) >= 2
        else "ÉLEVÉ" if len(sanctions) >= 1
        else "MODÉRÉ" if geo_score >= 50
        else "STANDARD"
    )

    return {
        "country": country,
        "geo_score": round(geo_score, 1),
        "geo_risk_level": geo_risk,
        "indicator_scores": {
            ind: {"raw": indicator_values[ind], "label": cfg["label"]}
            for ind, cfg in GEOPOLITICAL_INDICATORS.items()
            if ind in indicator_values
        },
        "active_sanctions": sanctions,
        "active_sanctions_details": {
            s: SANCTIONS_REGIMES[s] for s in sanctions if s in SANCTIONS_REGIMES
        },
        "supply_chain_risk": supply_chain_risk,
        "icc_proceedings": profile.get("icc_proceedings", False),
        "conflict_type": profile.get("conflict_type", "N/A"),
        "scenarios": [
            {
                "type": sc,
                "description": desc,
                "score_impact": (
                    +15 if "ESCALATION" in sc else
                    -10 if "STABILIZATION" in sc else
                    +15 if "SANCTIONS_EXPANSION" in sc else
                    -10 if "SANCTIONS_RELIEF" in sc else
                    -20 if "INTERNATIONAL" in sc else 0
                ),
            }
            for sc, desc in list(SCENARIO_TYPES.items())[:3]
        ],
        "business_advisory": (
            "NE PAS OPÉRER — Risque géopolitique prohibitif" if supply_chain_risk == "PROHIBITIF"
            else "DILIGENCE RENFORCÉE OBLIGATOIRE — Risque très élevé" if supply_chain_risk == "TRÈS ÉLEVÉ"
            else "SURVEILLANCE CONTINUE — Plan de contingence requis" if supply_chain_risk == "ÉLEVÉ"
            else "OPÉRATIONS SURVEILLÉES — KPIs géopolitiques actifs"
        ),
    }


def generate_geopolitical_report(entities: list, domain: str) -> dict:
    """Génère le rapport géopolitique pour un domaine."""
    analyses = []
    for entity in entities:
        country = entity.get("name", "").split("—")[0].strip()
        analysis = compute_geopolitical_score(country)
        analysis["entity_id"] = entity.get("id")
        analysis["composite_score"] = entity.get("composite_score")
        analyses.append(analysis)

    valid = [a for a in analyses if "error" not in a]
    critical_geo = [a for a in valid if a.get("geo_risk_level") == "CRITIQUE"]
    sanctioned = [a for a in valid if a.get("active_sanctions")]

    return {
        "report_type": "GEOPOLITICAL_RISK",
        "report_id": f"GEO-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Geopolitical Risk Agent v1.0",
        "domain": domain,
        "summary": {
            "countries_analyzed": len(valid),
            "critical_geopolitical_risk": len(critical_geo),
            "under_international_sanctions": len(sanctioned),
            "icc_proceedings_active": sum(1 for a in valid if a.get("icc_proceedings")),
        },
        "critical_entities": critical_geo,
        "entity_analyses": valid,
        "strategic_advisory": (
            "EXPOSITION CRITIQUE — Revue portefeuille géopolitique urgente"
            if len(critical_geo) >= 3
            else "EXPOSITION SIGNIFICATIVE — Plan de contingence requis"
            if len(critical_geo) >= 1
            else "EXPOSITION MODÉRÉE — Surveillance standard"
        ),
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — GEOPOLITICAL RISK AGENT")
    print("  Analyse Risques Géopolitiques & Impact Droits Humains")
    print("=" * 70)

    entities = [
        {"id": "SDR-001", "name": "Myanmar — Rohingyas", "composite_score": 94.40},
        {"id": "DSM-001", "name": "Russia — Deepfakes Guerre", "composite_score": 93.45},
        {"id": "OTH-001", "name": "Cayman Islands — 0% Impôt", "composite_score": 91.60},
    ]

    report = generate_geopolitical_report(entities, "multi-domain")

    print(f"\n🌍 RAPPORT GÉOPOLITIQUE: {report['report_id']}")
    s = report["summary"]
    print(f"   Pays analysés: {s['countries_analyzed']}")
    print(f"   Risque géopolitique critique: {s['critical_geopolitical_risk']}")
    print(f"   Sous sanctions internationales: {s['under_international_sanctions']}")
    print(f"   Procédures CPI actives: {s['icc_proceedings_active']}")

    print(f"\n⚡ ANALYSE PAR PAYS:")
    for a in report["entity_analyses"]:
        if "error" in a:
            continue
        icon = "🔴" if a.get("geo_risk_level") == "CRITIQUE" else "🟠" if a.get("geo_risk_level") == "ÉLEVÉ" else "🟡"
        print(f"\n   {icon} {a['entity_id']} — {a['country']}")
        print(f"      Score géopolitique: {a['geo_score']} | Niveau: {a['geo_risk_level']}")
        print(f"      Type conflit: {a['conflict_type']}")
        if a.get("active_sanctions"):
            print(f"      Sanctions actives: {', '.join(a['active_sanctions'])}")
        print(f"      Chaîne valeur: {a['supply_chain_risk']}")
        print(f"      CPI: {'⚖️  Procédure active' if a.get('icc_proceedings') else '—'}")
        print(f"      Advisory: {a['business_advisory'][:65]}...")

    print(f"\n📋 CONSEIL STRATÉGIQUE: {report['strategic_advisory']}")
    print(f"\n✅ Geopolitical Risk Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
