#!/usr/bin/env python3
"""
Scope 3 Emissions Tracking Agent — Caelum Partners CaelumSwarm™
Suivi des émissions Scope 3 selon GHG Protocol et CSRD ESRS E1.
Corrèle empreinte carbone Scope 3 avec violations droits humains chaîne valeur.
"""

import sys
from datetime import datetime, timezone

GHG_PROTOCOL_SCOPE3_CATEGORIES = {
    "C1_PURCHASED_GOODS": {
        "label": "Cat.1 — Biens et services achetés",
        "upstream": True,
        "typical_pct": 40,
        "human_rights_link": "Fournisseurs T1-T3 — droits travailleurs",
    },
    "C2_CAPITAL_GOODS": {
        "label": "Cat.2 — Biens d'équipement",
        "upstream": True,
        "typical_pct": 10,
        "human_rights_link": "Mines minerais critiques",
    },
    "C3_FUEL_ENERGY": {
        "label": "Cat.3 — Énergie non incluse Scope 1/2",
        "upstream": True,
        "typical_pct": 5,
        "human_rights_link": "Communautés extractives énergie",
    },
    "C4_TRANSPORT_UPSTREAM": {
        "label": "Cat.4 — Transport amont",
        "upstream": True,
        "typical_pct": 5,
        "human_rights_link": "Travailleurs transport maritime",
    },
    "C5_WASTE": {
        "label": "Cat.5 — Déchets générés",
        "upstream": True,
        "typical_pct": 2,
        "human_rights_link": "Travailleurs déchets informels",
    },
    "C6_BUSINESS_TRAVEL": {
        "label": "Cat.6 — Déplacements professionnels",
        "upstream": False,
        "typical_pct": 3,
        "human_rights_link": "Impact minimal direct",
    },
    "C7_COMMUTING": {
        "label": "Cat.7 — Trajets domicile-travail",
        "upstream": False,
        "typical_pct": 4,
        "human_rights_link": "Accès mobilité travailleurs",
    },
    "C11_USE_OF_PRODUCTS": {
        "label": "Cat.11 — Utilisation des produits vendus",
        "upstream": False,
        "typical_pct": 20,
        "human_rights_link": "Consommateurs finaux",
    },
    "C12_END_OF_LIFE": {
        "label": "Cat.12 — Traitement fin de vie produits",
        "upstream": False,
        "typical_pct": 6,
        "human_rights_link": "Décharges pays en développement",
    },
    "C15_INVESTMENTS": {
        "label": "Cat.15 — Investissements (finance uniquement)",
        "upstream": False,
        "typical_pct": 5,
        "human_rights_link": "Portefeuille entreprises → impacts DH",
    },
}

EMISSION_FACTORS = {
    "electricity_EU_grid_kgCO2_kWh": 0.233,
    "freight_road_kgCO2_tkm": 0.096,
    "freight_sea_kgCO2_tkm": 0.010,
    "freight_air_kgCO2_tkm": 0.602,
    "business_travel_flight_kgCO2_km": 0.133,
    "data_center_kgCO2_kWh": 0.180,
    "crypto_mining_kgCO2_USD": 0.042,
}

CSRD_DISCLOSURE_REQUIREMENTS = {
    "ESRS_E1_1": "Politiques réduction émissions",
    "ESRS_E1_2": "Plans transition décarbonation",
    "ESRS_E1_3": "Cibles réduction Scope 1/2/3",
    "ESRS_E1_4": "Énergie renouvelable",
    "ESRS_E1_5": "Émissions GES Scope 1/2",
    "ESRS_E1_6": "Émissions GES Scope 3",
    "ESRS_E1_7": "Intensité carbone",
}

SBTI_TARGETS = {
    "1.5C_PATHWAY": {"reduction_by_2030": 50, "reduction_by_2050": 100},
    "WELL_BELOW_2C": {"reduction_by_2030": 35, "reduction_by_2050": 100},
    "SECTOR_SPECIFIC": {"reduction_by_2030": 46, "reduction_by_2050": 100},
}


def estimate_scope3_by_category(company_revenue_MEUR: float, sector: str) -> dict:
    """Estime les émissions Scope 3 par catégorie."""
    intensity_kgCO2_EUR_revenue = {
        "tech": 0.08,
        "finance": 0.05,
        "manufacturing": 0.45,
        "retail": 0.25,
        "food_agriculture": 0.60,
        "default": 0.15,
    }.get(sector, 0.15)

    total_scope3_tCO2 = company_revenue_MEUR * 1_000_000 * intensity_kgCO2_EUR_revenue / 1000

    categories_breakdown = {}
    for cat_key, cat_config in GHG_PROTOCOL_SCOPE3_CATEGORIES.items():
        pct = cat_config["typical_pct"] / 100
        cat_tCO2 = total_scope3_tCO2 * pct
        categories_breakdown[cat_key] = {
            "label": cat_config["label"],
            "upstream": cat_config["upstream"],
            "estimated_tCO2": round(cat_tCO2, 0),
            "pct_of_total": cat_config["typical_pct"],
            "human_rights_link": cat_config["human_rights_link"],
        }

    return {
        "total_scope3_tCO2": round(total_scope3_tCO2, 0),
        "upstream_tCO2": round(sum(
            v["estimated_tCO2"] for v in categories_breakdown.values() if v["upstream"]
        ), 0),
        "downstream_tCO2": round(sum(
            v["estimated_tCO2"] for v in categories_breakdown.values() if not v["upstream"]
        ), 0),
        "categories": categories_breakdown,
        "carbon_price_EUR_ton": 65,
        "financial_liability_EUR": round(total_scope3_tCO2 * 65, -3),
    }


def track_progress(baseline_tCO2: float, current_tCO2: float, target_year: int = 2030) -> dict:
    """Suit la progression vers les objectifs de réduction."""
    reduction_pct = (baseline_tCO2 - current_tCO2) / baseline_tCO2 * 100 if baseline_tCO2 > 0 else 0

    current_year = datetime.now().year
    years_to_target = target_year - current_year
    sbti_target_2030 = SBTI_TARGETS["1.5C_PATHWAY"]["reduction_by_2030"]

    required_annual_reduction = sbti_target_2030 / max(target_year - 2020, 1)
    achieved_annual = reduction_pct / max(current_year - 2020, 1) if current_year > 2020 else 0

    on_track = achieved_annual >= required_annual_reduction

    return {
        "baseline_tCO2": baseline_tCO2,
        "current_tCO2": current_tCO2,
        "reduction_achieved_pct": round(reduction_pct, 1),
        "sbti_target_2030_pct": sbti_target_2030,
        "on_track_sbti": on_track,
        "required_annual_reduction_pct": round(required_annual_reduction, 1),
        "achieved_annual_pct": round(achieved_annual, 1),
        "gap_to_close": max(0, sbti_target_2030 - reduction_pct),
        "status": "ON TRACK ✅" if on_track else "OFF TRACK ❌",
    }


def generate_scope3_report(company: str, revenue_MEUR: float, sector: str, hr_score: float) -> dict:
    """Génère le rapport de suivi Scope 3 complet."""
    scope3 = estimate_scope3_by_category(revenue_MEUR, sector)

    baseline = scope3["total_scope3_tCO2"] * 1.2
    progress = track_progress(baseline, scope3["total_scope3_tCO2"])

    hr_high_risk_categories = [
        cat_key for cat_key, cat in scope3["categories"].items()
        if cat["upstream"] and hr_score >= 50
    ]

    return {
        "report_type": "SCOPE3_EMISSIONS_TRACKING",
        "report_id": f"SC3-{company[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Scope 3 Emissions Tracking Agent v1.0",
        "company": company,
        "sector": sector,
        "revenue_MEUR": revenue_MEUR,
        "human_rights_score": hr_score,
        "scope3_inventory": scope3,
        "progress_tracking": progress,
        "hr_scope3_intersection": {
            "high_risk_upstream_categories": hr_high_risk_categories,
            "key_insight": (
                f"Score DH {hr_score:.0f}/100 — {len(hr_high_risk_categories)} catégories Scope 3 "
                f"amont à haut risque droits humains ({scope3['upstream_tCO2']:,.0f} tCO2 concernées)"
            ),
            "double_materiality_triggered": hr_score >= 30 and scope3["total_scope3_tCO2"] > 10_000,
        },
        "csrd_esrs_e1_disclosure": {
            disclosure: "REQUIS" for disclosure in CSRD_DISCLOSURE_REQUIREMENTS
        },
        "sbti_targets": SBTI_TARGETS,
        "recommended_actions": [
            {
                "action": "Audit émissions fournisseurs T1 — collecte données primaires",
                "category": "C1_PURCHASED_GOODS",
                "potential_reduction_tCO2": round(scope3["categories"]["C1_PURCHASED_GOODS"]["estimated_tCO2"] * 0.30, 0),
                "co_benefit_hr": "Amélioration conditions travail fournisseurs simultanée",
            },
            {
                "action": "Transition énergies renouvelables fournisseurs stratégiques",
                "category": "C1_PURCHASED_GOODS",
                "potential_reduction_tCO2": round(scope3["total_scope3_tCO2"] * 0.15, 0),
                "co_benefit_hr": "Réduction dépendance combustibles fossiles dans communautés fragiles",
            },
            {
                "action": "Compensation carbone communautés affectées (Gold Standard Social)",
                "category": "C12_END_OF_LIFE",
                "potential_reduction_tCO2": round(scope3["total_scope3_tCO2"] * 0.10, 0),
                "co_benefit_hr": "Bénéfice direct communautés vulnérables ciblées CaelumSwarm™",
            },
        ],
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — SCOPE 3 EMISSIONS TRACKING AGENT")
    print("  Suivi Émissions GES Scope 3 — GHG Protocol + CSRD ESRS E1")
    print("=" * 70)

    report = generate_scope3_report(
        company="Caelum Partners SPRL",
        revenue_MEUR=600,
        sector="tech",
        hr_score=62.0,
    )

    s3 = report["scope3_inventory"]
    prog = report["progress_tracking"]
    hr_int = report["hr_scope3_intersection"]

    print(f"\n🌍 RAPPORT SCOPE 3: {report['report_id']}")
    print(f"   Entreprise: {report['company']} | Secteur: {report['sector']}")
    print(f"   Score DH CaelumSwarm™: {report['human_rights_score']}/100")

    print(f"\n📊 INVENTAIRE SCOPE 3:")
    print(f"   Total Scope 3: {s3['total_scope3_tCO2']:,.0f} tCO2e/an")
    print(f"   Amont: {s3['upstream_tCO2']:,.0f} tCO2e ({s3['upstream_tCO2']/s3['total_scope3_tCO2']*100:.0f}%)")
    print(f"   Aval: {s3['downstream_tCO2']:,.0f} tCO2e ({s3['downstream_tCO2']/s3['total_scope3_tCO2']*100:.0f}%)")
    print(f"   Passif carbone: {s3['financial_liability_EUR']:,.0f}€ à 65€/tonne")

    print(f"\n📋 TOP CATÉGORIES:")
    top_cats = sorted(s3["categories"].items(), key=lambda x: x[1]["estimated_tCO2"], reverse=True)[:4]
    for cat_key, cat in top_cats:
        print(f"   {cat['pct_of_total']:3d}% — {cat['label'][:45]}")
        print(f"         {cat['estimated_tCO2']:,.0f} tCO2e | DH: {cat['human_rights_link'][:40]}")

    print(f"\n🎯 PROGRESSION SBTI 1.5°C:")
    print(f"   Baseline → Actuel: {prog['baseline_tCO2']:,.0f} → {prog['current_tCO2']:,.0f} tCO2e")
    print(f"   Réduction atteinte: {prog['reduction_achieved_pct']}%")
    print(f"   Objectif 2030: {prog['sbti_target_2030_pct']}%")
    print(f"   Statut: {prog['status']}")
    if prog["gap_to_close"] > 0:
        print(f"   Gap à combler: {prog['gap_to_close']:.1f}%")

    print(f"\n🔗 INTERSECTION SCOPE 3 × DROITS HUMAINS:")
    print(f"   {hr_int['key_insight']}")
    print(f"   Double matérialité CSRD: {'✅ DÉCLENCHÉE' if hr_int['double_materiality_triggered'] else '❌ NON DÉCLENCHÉE'}")

    print(f"\n⚡ ACTIONS RECOMMANDÉES:")
    for action in report["recommended_actions"]:
        print(f"\n   • {action['action']}")
        print(f"     Catégorie: {action['category']}")
        print(f"     Réduction potentielle: {action['potential_reduction_tCO2']:,.0f} tCO2e")
        print(f"     Co-bénéfice DH: {action['co_benefit_hr'][:65]}...")

    print(f"\n✅ Scope 3 Emissions Tracking Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
