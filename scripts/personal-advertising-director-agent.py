#!/usr/bin/env python3
"""
Personal Advertising Director Agent — Caelum Partners CaelumSwarm™
Directeur publicité IA tout-en-1 : stratégie, création, ciblage, budget,
A/B testing, reporting — pour CaelumSwarm™ et clients CSDDD.
"""

import sys
from datetime import datetime, timezone

AD_CHANNELS = {
    "LINKEDIN": {
        "label": "LinkedIn Ads",
        "audience": "Décideurs RSE, DG, Directeurs conformité, Investisseurs ESG",
        "cpm_eur": 18.50,
        "avg_ctr": 0.045,
        "best_format": ["Sponsored Content", "Message Ads", "Lead Gen Forms"],
        "caelum_relevance": "PRIMAIRE",
        "budget_pct": 40,
    },
    "GOOGLE_SEARCH": {
        "label": "Google Search Ads",
        "audience": "Recherches actives : CSDDD conformité, due diligence DH, ESG reporting",
        "cpc_eur": 4.20,
        "avg_ctr": 0.085,
        "best_format": ["Responsive Search Ads", "Performance Max"],
        "caelum_relevance": "PRIMAIRE",
        "budget_pct": 25,
    },
    "PROGRAMMATIC": {
        "label": "Programmatic Display (DV360)",
        "audience": "Retargeting visiteurs, lookalike audiences ESG",
        "cpm_eur": 3.50,
        "avg_ctr": 0.008,
        "best_format": ["HTML5 Banner", "Native Display", "Video"],
        "caelum_relevance": "SECONDAIRE",
        "budget_pct": 15,
    },
    "META_B2B": {
        "label": "Meta (Facebook/Instagram) B2B",
        "audience": "Consultants RSE, avocats droit des affaires, formateurs compliance",
        "cpm_eur": 9.00,
        "avg_ctr": 0.025,
        "best_format": ["Lead Ads", "Carousel", "Video"],
        "caelum_relevance": "TERTIAIRE",
        "budget_pct": 10,
    },
    "PODCAST_SPONSORSHIP": {
        "label": "Sponsoring Podcasts ESG/DH",
        "audience": "Professionnels RSE, juristes, investisseurs impact",
        "cpm_eur": 35.00,
        "avg_ctr": 0.120,
        "best_format": ["Mid-roll 30s", "Host-read 60s"],
        "caelum_relevance": "SECONDAIRE",
        "budget_pct": 10,
    },
}

AD_FORMATS_LIBRARY = {
    "LINKEDIN_SPONSORED": {
        "headline_max": 150,
        "body_max": 600,
        "cta_options": ["En savoir plus", "Télécharger", "Demander une démo", "Nous contacter"],
        "image_ratio": "1.91:1 (1200x627px)",
    },
    "GOOGLE_RSA": {
        "headlines": "3-15 titres (30 chars max each)",
        "descriptions": "2-4 descriptions (90 chars max each)",
        "display_url": "caelumpartners.com/conformite-csddd",
    },
    "VIDEO_30S": {
        "hook": "0-5s — accroche problème (violation DH coûte jusqu'à 5% CA)",
        "problem": "5-15s — exposition du risque CSDDD",
        "solution": "15-25s — CaelumSwarm™ comme solution",
        "cta": "25-30s — Call-to-action + URL",
    },
}

CAMPAIGN_TEMPLATES = {
    "AWARENESS_CSDDD": {
        "objective": "Notoriété — CSDDD entre en vigueur 2027",
        "message": "Votre entreprise est-elle prête pour la CSDDD 2027 ?",
        "hook": "1 amende CSDDD = jusqu'à 5% de votre CA mondial",
        "tone": "Urgence réglementaire + autorité",
        "kpis": {"impressions": 500_000, "ctr": 0.04, "leads": 200},
        "budget_eur": 15_000,
    },
    "LEAD_GEN_DEMO": {
        "objective": "Génération leads — Démo CaelumSwarm™",
        "message": "Détectez vos violations droits humains avant les régulateurs",
        "hook": "CaelumSwarm™ analyse 190+ pays en temps réel",
        "tone": "Data-driven + exclusivité",
        "kpis": {"impressions": 100_000, "ctr": 0.06, "leads": 80},
        "budget_eur": 8_000,
    },
    "RETARGETING_NURTURE": {
        "objective": "Nurturing — Visiteurs du site non convertis",
        "message": "Vous avez visité CaelumSwarm™. Votre concurrent l'a adopté.",
        "hook": "FOMO + social proof ESG",
        "tone": "Urgence douce + preuve sociale",
        "kpis": {"impressions": 50_000, "ctr": 0.035, "leads": 30},
        "budget_eur": 3_000,
    },
    "THOUGHT_LEADERSHIP": {
        "objective": "Autorité — Positionnement expert droits humains",
        "message": "Caelum Partners : le standard de référence en compliance droits humains",
        "hook": "Wave 194 : 3 nouvelles menaces droits humains analysées",
        "tone": "Expertise + data",
        "kpis": {"impressions": 200_000, "ctr": 0.025, "downloads": 500},
        "budget_eur": 5_000,
    },
}

AB_TEST_VARIANTS = {
    "A": {"headline": "CSDDD 2027 : Êtes-vous en conformité ?", "cta": "Tester ma conformité"},
    "B": {"headline": "5% CA : le coût d'une violation CSDDD", "cta": "Calculer mon risque"},
    "C": {"headline": "CaelumSwarm™ détecte les violations avant les régulateurs", "cta": "Voir une démo"},
}

TARGET_PERSONAS = {
    "RSE_DIRECTOR": {
        "label": "Directeur RSE / Chief Sustainability Officer",
        "pain_points": ["Cartographier la chaîne valeur", "Rapport CSRD", "Budget conformité"],
        "linkedin_titles": ["RSE Director", "Chief Sustainability Officer", "Responsable Développement Durable"],
        "message_angle": "Gain de temps + conformité automatisée",
    },
    "LEGAL_COUNSEL": {
        "label": "Directeur Juridique / Compliance Officer",
        "pain_points": ["Risques sanctions", "Documentation audit", "Surveillance fournisseurs"],
        "linkedin_titles": ["General Counsel", "Chief Compliance Officer", "Head of Legal"],
        "message_angle": "Réduction risque légal + preuves documentées",
    },
    "ESG_INVESTOR": {
        "label": "Gestionnaire portefeuille ESG / Analyste Impact",
        "pain_points": ["Due diligence entreprises portefeuille", "SFDR reporting", "Risques réputation"],
        "linkedin_titles": ["ESG Analyst", "Impact Investor", "Portfolio Manager ESG"],
        "message_angle": "Data fiable + scoring standardisé",
    },
    "CEO_SME": {
        "label": "PDG PME >250 salariés",
        "pain_points": ["Coût conformité", "Simplification", "Compétitivité"],
        "linkedin_titles": ["CEO", "Managing Director", "PDG"],
        "message_angle": "ROI conformité + avantage concurrentiel",
    },
}


def create_campaign_plan(
    objective: str,
    budget_eur: float,
    target_personas: list,
    duration_weeks: int = 8,
) -> dict:
    """Génère un plan de campagne publicitaire complet."""
    template = CAMPAIGN_TEMPLATES.get(objective, CAMPAIGN_TEMPLATES["AWARENESS_CSDDD"])

    channel_allocation = {}
    for channel_key, channel in AD_CHANNELS.items():
        allocated = budget_eur * channel["budget_pct"] / 100
        if channel["caelum_relevance"] in ("PRIMAIRE", "SECONDAIRE"):
            if objective == "LEAD_GEN_DEMO" and channel_key == "LINKEDIN":
                allocated *= 1.2
            channel_allocation[channel_key] = {
                "label": channel["label"],
                "budget_eur": round(allocated, 0),
                "relevance": channel["caelum_relevance"],
                "best_format": channel["best_format"][0],
                "estimated_reach": int(allocated * 1000 / channel.get("cpm_eur", 10)),
                "estimated_clicks": int(allocated * 1000 / channel.get("cpm_eur", 10) * channel.get("avg_ctr", 0.03)),
            }

    total_estimated_reach = sum(v["estimated_reach"] for v in channel_allocation.values())
    total_estimated_clicks = sum(v["estimated_clicks"] for v in channel_allocation.values())
    estimated_leads = int(total_estimated_clicks * 0.08)

    personas_targeted = [TARGET_PERSONAS.get(p, {}) for p in target_personas if p in TARGET_PERSONAS]

    weekly_budget = budget_eur / duration_weeks

    return {
        "campaign_id": f"CAM-{datetime.now().strftime('%Y%m%d%H%M')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Personal Advertising Director Agent v1.0",
        "campaign_name": f"CaelumSwarm™ — {template['objective']}",
        "objective": objective,
        "creative_brief": {
            "main_message": template["message"],
            "hook": template["hook"],
            "tone": template["tone"],
            "ab_variants": AB_TEST_VARIANTS,
        },
        "target_personas": personas_targeted,
        "media_plan": {
            "total_budget_eur": budget_eur,
            "duration_weeks": duration_weeks,
            "weekly_budget_eur": round(weekly_budget, 0),
            "channel_allocation": channel_allocation,
        },
        "projected_kpis": {
            "total_reach": total_estimated_reach,
            "total_clicks": total_estimated_clicks,
            "estimated_leads": estimated_leads,
            "cost_per_lead_eur": round(budget_eur / max(estimated_leads, 1), 0),
            "target_kpis": template["kpis"],
        },
        "ab_testing_plan": {
            "variants": AB_TEST_VARIANTS,
            "test_duration_weeks": 2,
            "winner_selection": "CTR + Conversion rate after Week 2",
            "scaling_plan": "Scale winner with 80% budget, retire losers",
        },
        "reporting_cadence": {
            "weekly": "Rapport automatique : impressions, CTR, leads, CPC",
            "biweekly": "A/B test analysis + optimisation enchères",
            "monthly": "Rapport ROI complet + recommandations stratégiques",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — PERSONAL ADVERTISING DIRECTOR AGENT")
    print("  Directeur Pub IA Tout-en-1 : Stratégie → Création → Reporting")
    print("=" * 70)

    plan = create_campaign_plan(
        objective="LEAD_GEN_DEMO",
        budget_eur=25_000,
        target_personas=["RSE_DIRECTOR", "LEGAL_COUNSEL", "ESG_INVESTOR"],
        duration_weeks=8,
    )

    print(f"\n📢 CAMPAGNE: {plan['campaign_id']}")
    print(f"   Objectif: {plan['objective']}")
    print(f"   Message principal: {plan['creative_brief']['main_message']}")
    print(f"   Hook: {plan['creative_brief']['hook']}")
    print(f"   Ton: {plan['creative_brief']['tone']}")

    print(f"\n🎯 PERSONAS CIBLÉS:")
    for persona in plan["target_personas"][:2]:
        print(f"   • {persona.get('label', '')}")
        print(f"     Pain points: {', '.join(persona.get('pain_points', [])[:2])}")
        print(f"     Angle message: {persona.get('message_angle', '')}")

    print(f"\n💰 PLAN MÉDIAS ({plan['media_plan']['total_budget_eur']:,.0f}€ / {plan['media_plan']['duration_weeks']}sem):")
    for ch_key, ch in plan["media_plan"]["channel_allocation"].items():
        print(f"   {ch['label']:35} {ch['budget_eur']:6.0f}€ | Reach: {ch['estimated_reach']:,} | Format: {ch['best_format']}")

    kpis = plan["projected_kpis"]
    print(f"\n📊 KPIs PROJETÉS:")
    print(f"   Portée totale: {kpis['total_reach']:,}")
    print(f"   Clics: {kpis['total_clicks']:,}")
    print(f"   Leads estimés: {kpis['estimated_leads']}")
    print(f"   Coût par lead: {kpis['cost_per_lead_eur']:,.0f}€")

    print(f"\n🧪 PLAN A/B TESTING:")
    for variant, content in plan["ab_testing_plan"]["variants"].items():
        print(f"   Variant {variant}: '{content['headline']}' → CTA: '{content['cta']}'")
    print(f"   Sélection gagnant: {plan['ab_testing_plan']['winner_selection']}")

    print(f"\n📅 REPORTING:")
    for freq, desc in plan["reporting_cadence"].items():
        print(f"   {freq.title()}: {desc}")

    print(f"\n✅ Personal Advertising Director Agent — Plan campagne 25K€ généré")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
