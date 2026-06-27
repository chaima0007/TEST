"""
Agent connecteur de partenaires — identifie, évalue et connecte des partenaires stratégiques
pour CaelumSwarm™ (cabinets conseil, plateformes ESG, ONG, institutions académiques, régulateurs)

CaelumSwarm™ Partner Connector Agent v1.0
Caelum Partners — Intelligence Stratégique des Droits Humains & CSDDD Compliance
"""

import json
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# 1. CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

PARTNER_CATEGORIES = {
    "CONSULTING_FIRMS": {
        "label": "Cabinets de conseil",
        "strategic_value": 9,
        "partnership_type": "Revendeur / Co-implémentation",
        "typical_deal_value_EUR": 150_000,
        "integration_complexity": "MEDIUM",
        "time_to_activate_months": 3,
    },
    "ESG_PLATFORMS": {
        "label": "Plateformes ESG & Reporting",
        "strategic_value": 8,
        "partnership_type": "Intégration technique / API",
        "typical_deal_value_EUR": 80_000,
        "integration_complexity": "HIGH",
        "time_to_activate_months": 5,
    },
    "LEGAL_FIRMS": {
        "label": "Cabinets juridiques",
        "strategic_value": 7,
        "partnership_type": "Advisory / Co-marketing",
        "typical_deal_value_EUR": 60_000,
        "integration_complexity": "LOW",
        "time_to_activate_months": 2,
    },
    "NGO_NETWORKS": {
        "label": "Réseaux ONG & société civile",
        "strategic_value": 6,
        "partnership_type": "Advisory / Légitimité terrain",
        "typical_deal_value_EUR": 20_000,
        "integration_complexity": "LOW",
        "time_to_activate_months": 4,
    },
    "ACADEMIC_INSTITUTIONS": {
        "label": "Institutions académiques",
        "strategic_value": 5,
        "partnership_type": "Recherche / Validation méthodologique",
        "typical_deal_value_EUR": 30_000,
        "integration_complexity": "LOW",
        "time_to_activate_months": 6,
    },
    "REGULATORY_BODIES": {
        "label": "Organismes réglementaires & normalisateurs",
        "strategic_value": 10,
        "partnership_type": "Conformité / Reconnaissance officielle",
        "typical_deal_value_EUR": 0,
        "integration_complexity": "HIGH",
        "time_to_activate_months": 12,
    },
}

PARTNERSHIP_MODELS = {
    "RESELLER": {
        "label": "Revendeur agréé",
        "revenue_share_pct": 20,
        "exclusivity": False,
        "requirements": [
            "Équipe commerciale dédiée (≥2 ETP)",
            "Formation certifiante CaelumSwarm™ complétée",
            "Engagement minimum 3 clients/an",
            "Accord de confidentialité NDA signé",
        ],
        "expected_leads_per_year": 8,
    },
    "INTEGRATION": {
        "label": "Partenaire d'intégration technique",
        "revenue_share_pct": 15,
        "exclusivity": False,
        "requirements": [
            "Équipe technique API certifiée",
            "Environnement sandbox validé",
            "Documentation d'intégration approuvée",
            "SLA de support niveau 2 garanti",
        ],
        "expected_leads_per_year": 5,
    },
    "CO_MARKETING": {
        "label": "Partenaire co-marketing",
        "revenue_share_pct": 10,
        "exclusivity": False,
        "requirements": [
            "Base clients min. 500 entreprises",
            "Accord de co-branding signé",
            "Budget marketing partagé (≥20k€/an)",
            "Participation à 2 événements communs/an",
        ],
        "expected_leads_per_year": 12,
    },
    "ADVISORY": {
        "label": "Partenaire conseil & advisory",
        "revenue_share_pct": 8,
        "exclusivity": False,
        "requirements": [
            "Expertise CSDDD / droits humains reconnue",
            "Présence dans comité consultatif Caelum",
            "Publication de 1 rapport co-signé/an",
            "Référencement dans base partenaires publique",
        ],
        "expected_leads_per_year": 4,
    },
}

PARTNER_SCORING_CRITERIA = {
    "market_reach": {
        "weight": 0.25,
        "description": "Taille et qualité du réseau clients potentiels (entreprises cibles CSDDD)",
    },
    "brand_alignment": {
        "weight": 0.20,
        "description": "Alignement des valeurs — droits humains, durabilité, transparence des chaînes",
    },
    "technical_compatibility": {
        "weight": 0.18,
        "description": "Compatibilité technique avec l'écosystème CaelumSwarm™ (API, formats, stack)",
    },
    "client_overlap": {
        "weight": 0.17,
        "description": "Chevauchement positif du portefeuille clients — eviter la cannibalisation",
    },
    "compliance_expertise": {
        "weight": 0.12,
        "description": "Expertise en conformité CSDDD, CSRD, droits humains en entreprise",
    },
    "geographic_coverage": {
        "weight": 0.08,
        "description": "Couverture géographique complémentaire (UE, DACH, Nordics, Benelux, …)",
    },
}

POTENTIAL_PARTNERS_DB = [
    {
        "name": "BCG Compliance Advisory",
        "category": "CONSULTING_FIRMS",
        "country": "France",
        "revenue_MEUR": 4_200,
        "client_base_size": 2_500,
        "csddd_focus": True,
        "scores": {
            "market_reach": 95,
            "brand_alignment": 82,
            "technical_compatibility": 60,
            "client_overlap": 75,
            "compliance_expertise": 90,
            "geographic_coverage": 92,
        },
        "contact_role": "Directeur Associé — Sustainability & Risk",
    },
    {
        "name": "EcoVadis",
        "category": "ESG_PLATFORMS",
        "country": "France",
        "revenue_MEUR": 200,
        "client_base_size": 100_000,
        "csddd_focus": True,
        "scores": {
            "market_reach": 98,
            "brand_alignment": 90,
            "technical_compatibility": 85,
            "client_overlap": 70,
            "compliance_expertise": 88,
            "geographic_coverage": 95,
        },
        "contact_role": "VP Partnerships & Alliances",
    },
    {
        "name": "Linklaters ESG Practice",
        "category": "LEGAL_FIRMS",
        "country": "Belgique",
        "revenue_MEUR": 1_800,
        "client_base_size": 800,
        "csddd_focus": True,
        "scores": {
            "market_reach": 72,
            "brand_alignment": 85,
            "technical_compatibility": 40,
            "client_overlap": 80,
            "compliance_expertise": 95,
            "geographic_coverage": 78,
        },
        "contact_role": "Associé — Corporate Sustainability Law",
    },
    {
        "name": "Business & Human Rights Resource Centre",
        "category": "NGO_NETWORKS",
        "country": "Royaume-Uni",
        "revenue_MEUR": 8,
        "client_base_size": 9_000,
        "csddd_focus": True,
        "scores": {
            "market_reach": 65,
            "brand_alignment": 98,
            "technical_compatibility": 30,
            "client_overlap": 45,
            "compliance_expertise": 97,
            "geographic_coverage": 85,
        },
        "contact_role": "Directeur des Partenariats Institutionnels",
    },
    {
        "name": "PwC Sustainability Hub",
        "category": "CONSULTING_FIRMS",
        "country": "Luxembourg",
        "revenue_MEUR": 5_800,
        "client_base_size": 3_200,
        "csddd_focus": True,
        "scores": {
            "market_reach": 92,
            "brand_alignment": 76,
            "technical_compatibility": 68,
            "client_overlap": 72,
            "compliance_expertise": 85,
            "geographic_coverage": 89,
        },
        "contact_role": "Partner — ESG & Regulatory Compliance",
    },
    {
        "name": "Workiva",
        "category": "ESG_PLATFORMS",
        "country": "États-Unis",
        "revenue_MEUR": 620,
        "client_base_size": 6_000,
        "csddd_focus": False,
        "scores": {
            "market_reach": 80,
            "brand_alignment": 68,
            "technical_compatibility": 90,
            "client_overlap": 55,
            "compliance_expertise": 62,
            "geographic_coverage": 70,
        },
        "contact_role": "Director of Technology Partnerships",
    },
    {
        "name": "HEC Paris — Centre Droit & Commerce",
        "category": "ACADEMIC_INSTITUTIONS",
        "country": "France",
        "revenue_MEUR": 380,
        "client_base_size": 1_200,
        "csddd_focus": True,
        "scores": {
            "market_reach": 50,
            "brand_alignment": 88,
            "technical_compatibility": 35,
            "client_overlap": 40,
            "compliance_expertise": 80,
            "geographic_coverage": 55,
        },
        "contact_role": "Professeur — Chaire Entreprise & Droits Humains",
    },
    {
        "name": "EFRAG — European Financial Reporting Advisory Group",
        "category": "REGULATORY_BODIES",
        "country": "Belgique",
        "revenue_MEUR": 0,
        "client_base_size": 0,
        "csddd_focus": True,
        "scores": {
            "market_reach": 60,
            "brand_alignment": 92,
            "technical_compatibility": 45,
            "client_overlap": 30,
            "compliance_expertise": 98,
            "geographic_coverage": 88,
        },
        "contact_role": "Secrétaire Général — Sustainability Reporting",
    },
    {
        "name": "Deloitte Risk Advisory — Supply Chain",
        "category": "CONSULTING_FIRMS",
        "country": "Allemagne",
        "revenue_MEUR": 6_400,
        "client_base_size": 4_000,
        "csddd_focus": True,
        "scores": {
            "market_reach": 93,
            "brand_alignment": 78,
            "technical_compatibility": 72,
            "client_overlap": 68,
            "compliance_expertise": 87,
            "geographic_coverage": 94,
        },
        "contact_role": "Director — ESG Risk & Supply Chain Due Diligence",
    },
    {
        "name": "Amnesty International Business & Human Rights",
        "category": "NGO_NETWORKS",
        "country": "Pays-Bas",
        "revenue_MEUR": 350,
        "client_base_size": 12_000,
        "csddd_focus": True,
        "scores": {
            "market_reach": 70,
            "brand_alignment": 97,
            "technical_compatibility": 25,
            "client_overlap": 38,
            "compliance_expertise": 95,
            "geographic_coverage": 90,
        },
        "contact_role": "Responsable Partenariats Entreprises",
    },
]


# ---------------------------------------------------------------------------
# 2. FONCTIONS PRINCIPALES
# ---------------------------------------------------------------------------


def score_partner(partner: dict) -> dict:
    """
    Calcule le score pondéré de partenariat selon les critères PARTNER_SCORING_CRITERIA.
    Retourne : total_score (0-100), tier, recommended_model, priority_ranking.
    """
    raw_score = 0.0
    breakdown = {}

    for criterion, meta in PARTNER_SCORING_CRITERIA.items():
        raw_value = partner["scores"].get(criterion, 0)
        weighted = raw_value * meta["weight"]
        raw_score += weighted
        breakdown[criterion] = {
            "raw": raw_value,
            "weight": meta["weight"],
            "weighted_contribution": round(weighted, 2),
        }

    # Bonus CSDDD si le partenaire est déjà focalisé sur le sujet
    csddd_bonus = 3.0 if partner.get("csddd_focus") else 0.0
    total_score = min(100, round(raw_score + csddd_bonus, 2))

    # Détermination du tier
    if total_score >= 80:
        tier = "PLATINUM"
    elif total_score >= 60:
        tier = "GOLD"
    elif total_score >= 40:
        tier = "SILVER"
    else:
        tier = "BRONZE"

    # Recommandation du modèle de partenariat selon la catégorie
    category = partner.get("category", "")
    category_to_model = {
        "CONSULTING_FIRMS": "RESELLER",
        "ESG_PLATFORMS": "INTEGRATION",
        "LEGAL_FIRMS": "CO_MARKETING",
        "NGO_NETWORKS": "ADVISORY",
        "ACADEMIC_INSTITUTIONS": "ADVISORY",
        "REGULATORY_BODIES": "ADVISORY",
    }
    recommended_model = category_to_model.get(category, "CO_MARKETING")

    # Priority ranking : score normalisé à 4 niveaux
    if total_score >= 85:
        priority_ranking = 1
    elif total_score >= 70:
        priority_ranking = 2
    elif total_score >= 55:
        priority_ranking = 3
    else:
        priority_ranking = 4

    return {
        "partner_name": partner["name"],
        "total_score": total_score,
        "tier": tier,
        "recommended_model": recommended_model,
        "priority_ranking": priority_ranking,
        "breakdown": breakdown,
        "csddd_bonus_applied": csddd_bonus,
    }


def generate_partnership_proposal(partner: dict, model: str) -> dict:
    """
    Génère une proposition de partenariat personnalisée pour un partenaire donné
    selon le modèle PARTNERSHIP_MODELS sélectionné.
    """
    if model not in PARTNERSHIP_MODELS:
        raise ValueError(f"Modèle inconnu : {model}. Choisir parmi {list(PARTNERSHIP_MODELS.keys())}")

    model_meta = PARTNERSHIP_MODELS[model]
    category_meta = PARTNER_CATEGORIES.get(partner["category"], {})
    score_result = score_partner(partner)

    today = date.today()
    phase2_start = today + timedelta(days=90)
    phase3_start = today + timedelta(days=180)

    # Valeur commerciale estimée sur 3 ans
    base_deal = category_meta.get("typical_deal_value_EUR", 50_000)
    leads_per_year = model_meta["expected_leads_per_year"]
    estimated_3y_revenue = leads_per_year * base_deal * 3 * (model_meta["revenue_share_pct"] / 100)

    proposal = {
        "proposal_id": f"CP-{partner['name'][:4].upper()}-{today.strftime('%Y%m')}-{model[:3]}",
        "generated_date": today.isoformat(),
        "partner": partner["name"],
        "country": partner["country"],
        "partnership_model": model_meta["label"],
        "tier": score_result["tier"],

        "executive_summary": (
            f"CaelumSwarm™ invite {partner['name']} à rejoindre son programme partenaires "
            f"en qualité de {model_meta['label']}. Dans un contexte de montée en puissance "
            f"de la directive CSDDD (Corporate Sustainability Due Diligence Directive), "
            f"{partner['name']} bénéficiera d'un accès privilégié à la plateforme d'intelligence "
            f"swarm la plus avancée pour le suivi des droits humains en chaîne de valeur. "
            f"Ce partenariat de tier {score_result['tier']} projette une génération de "
            f"{leads_per_year} leads qualifiés par an, pour une valeur pipeline estimée "
            f"à {base_deal:,}€ par engagement client."
        ),

        "value_proposition_for_partner": {
            "headline": f"Différenciez votre offre CSDDD avec l'intelligence CaelumSwarm™",
            "points": [
                f"Accès à une technologie swarm exclusive d'analyse des droits humains "
                f"couvrant 190+ pays et 47 secteurs industriels",
                f"Revenue share de {model_meta['revenue_share_pct']}% sur chaque contrat "
                f"signé via votre réseau ({partner['client_base_size']:,} clients potentiels)",
                f"Formation et certification CaelumSwarm™ pour vos équipes — positionnement "
                f"d'expert reconnu sur le marché CSDDD",
                f"Co-branding sur les rapports de conformité générés pour vos clients communs",
                f"Accès prioritaire aux mises à jour réglementaires et aux nouvelles fonctionnalités",
            ],
        },

        "value_proposition_for_caelum": {
            "headline": f"Accélération de la pénétration marché via le réseau {partner['name']}",
            "points": [
                f"Accès au réseau de {partner['client_base_size']:,} organisations clientes "
                f"de {partner['name']} en {partner['country']} et au-delà",
                f"Légitimité renforcée par l'association avec un acteur reconnu "
                f"({partner['name']}, {partner['revenue_MEUR']:,}M€ de revenus)",
                f"Génération estimée de {leads_per_year} leads qualifiés/an pour CaelumSwarm™",
                f"Couverture géographique étendue — score géo : "
                f"{partner['scores']['geographic_coverage']}/100",
                f"Renforcement de l'expertise CSDDD via la combinaison des savoir-faire",
            ],
        },

        "commercial_terms": {
            "model": model_meta["label"],
            "revenue_share_pct": model_meta["revenue_share_pct"],
            "exclusivity": "Oui" if model_meta["exclusivity"] else "Non — partenariat ouvert",
            "contract_duration_years": 2,
            "renewal": "Tacite reconduction annuelle",
            "estimated_pipeline_3y_EUR": round(estimated_3y_revenue),
            "requirements": model_meta["requirements"],
            "onboarding_fee_EUR": 0,
            "minimum_commitment": f"{max(1, leads_per_year // 3)} contrats clients signés/an",
        },

        "integration_roadmap": [
            {
                "phase": 1,
                "label": "Onboarding & Certification",
                "timeline": f"{today.strftime('%B %Y')} → {phase2_start.strftime('%B %Y')}",
                "duration_weeks": 12,
                "milestones": [
                    "Signature NDA et accord de partenariat",
                    "Accès sandbox CaelumSwarm™ API",
                    "Formation équipe commerciale et technique (2 jours)",
                    "Certification officielle CaelumSwarm™ Partner obtenue",
                    "Kit de vente co-brandé livré",
                ],
            },
            {
                "phase": 2,
                "label": "Lancement commercial & premiers clients",
                "timeline": f"{phase2_start.strftime('%B %Y')} → {phase3_start.strftime('%B %Y')}",
                "duration_weeks": 12,
                "milestones": [
                    "Premier webinaire co-organisé auprès des clients de " + partner["name"],
                    "Présentation au pipeline commercial existant (top 20 prospects CSDDD)",
                    "Signature des 2 premiers contrats pilotes",
                    "Retour d'expérience et ajustement de l'argumentaire",
                    "Publication d'un cas client commun",
                ],
            },
            {
                "phase": 3,
                "label": "Déploiement à grande échelle & co-innovation",
                "timeline": f"{phase3_start.strftime('%B %Y')} → (continu)",
                "duration_weeks": None,
                "milestones": [
                    f"Intégration dans l'offre standard de {partner['name']}",
                    "Co-développement d'un module sectoriel spécifique",
                    "Participation conjointe à 2 conférences ESG majeures",
                    f"Objectif : {leads_per_year} nouveaux clients CaelumSwarm™/an",
                    "Revue annuelle de partenariat et renégociation si nécessaire",
                ],
            },
        ],

        "success_metrics": {
            "kpi_leads_qualifies_par_an": leads_per_year,
            "kpi_taux_conversion_cible_pct": 35,
            "kpi_satisfaction_partenaire_cible": "NPS ≥ 50",
            "kpi_contrats_signes_an1": max(1, leads_per_year // 4),
            "kpi_revenue_partage_an1_EUR": round(base_deal * (leads_per_year // 4) * model_meta["revenue_share_pct"] / 100),
            "kpi_pipeline_genere_an1_EUR": base_deal * (leads_per_year // 4),
            "revue_trimestrielle": True,
            "reporting_mensuel_pipeline": True,
        },
    }

    return proposal


def map_partner_ecosystem() -> dict:
    """
    Cartographie l'écosystème partenaires complet par catégorie.
    Identifie les gaps de couverture, priorités stratégiques,
    opportunités d'expansion géographique et pipeline estimé.
    """
    # Regrouper les partenaires par catégorie
    by_category = {cat: [] for cat in PARTNER_CATEGORIES}
    for partner in POTENTIAL_PARTNERS_DB:
        cat = partner.get("category")
        if cat in by_category:
            by_category[cat].append(partner)

    # Calculer les scores moyens par catégorie
    category_stats = {}
    total_pipeline = 0

    for cat, partners in by_category.items():
        if not partners:
            avg_score = 0
            csddd_count = 0
        else:
            scores = [score_partner(p)["total_score"] for p in partners]
            avg_score = round(sum(scores) / len(scores), 1)
            csddd_count = sum(1 for p in partners if p.get("csddd_focus"))

        meta = PARTNER_CATEGORIES[cat]
        pipeline = meta["typical_deal_value_EUR"] * max(1, len(partners)) * meta["strategic_value"] / 10
        total_pipeline += pipeline

        category_stats[cat] = {
            "label": meta["label"],
            "nb_partenaires_identifies": len(partners),
            "strategic_value": meta["strategic_value"],
            "avg_score": avg_score,
            "csddd_focused_count": csddd_count if partners else 0,
            "estimated_pipeline_EUR": round(pipeline),
            "time_to_activate_months": meta["time_to_activate_months"],
            "integration_complexity": meta["integration_complexity"],
            "partners": [p["name"] for p in partners],
        }

    # Identifier les gaps de couverture
    coverage_gaps = []
    for cat, stats in category_stats.items():
        if stats["nb_partenaires_identifies"] == 0:
            coverage_gaps.append({
                "category": cat,
                "label": PARTNER_CATEGORIES[cat]["label"],
                "urgency": "CRITIQUE" if PARTNER_CATEGORIES[cat]["strategic_value"] >= 8 else "MODÉRÉE",
                "action": f"Identifier et approcher 2-3 {PARTNER_CATEGORIES[cat]['label'].lower()} prioritaires",
            })
        elif stats["nb_partenaires_identifies"] < 2:
            coverage_gaps.append({
                "category": cat,
                "label": PARTNER_CATEGORIES[cat]["label"],
                "urgency": "MODÉRÉE",
                "action": f"Renforcer le pipeline — objectif : ≥3 partenaires {PARTNER_CATEGORIES[cat]['label'].lower()}",
            })

    # Priorités stratégiques (top 3 par valeur stratégique × score moyen)
    priority_scores = {
        cat: stats["strategic_value"] * (stats["avg_score"] / 100)
        for cat, stats in category_stats.items()
        if stats["nb_partenaires_identifies"] > 0
    }
    sorted_priorities = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
    strategic_priorities = [
        {
            "rank": i + 1,
            "category": cat,
            "label": PARTNER_CATEGORIES[cat]["label"],
            "composite_priority_score": round(score, 2),
            "rationale": (
                f"Valeur stratégique {PARTNER_CATEGORIES[cat]['strategic_value']}/10 × "
                f"score moyen {category_stats[cat]['avg_score']}/100"
            ),
        }
        for i, (cat, score) in enumerate(sorted_priorities[:3])
    ]

    # Opportunités d'expansion géographique
    countries_covered = set(p["country"] for p in POTENTIAL_PARTNERS_DB)
    target_markets_missing = [
        m for m in ["Allemagne", "Pays-Bas", "Suède", "Espagne", "Italie", "Suisse", "Autriche"]
        if m not in countries_covered
    ]
    geographic_expansion_opportunities = {
        "marchés_actuellement_couverts": sorted(countries_covered),
        "marchés_cibles_non_couverts": target_markets_missing,
        "priorité_dach": "Allemagne" in target_markets_missing,
        "priorité_nordics": "Suède" in target_markets_missing or "Danemark" in target_markets_missing,
        "recommandation": (
            "Cibler en priorité les marchés DACH (Allemagne, Autriche, Suisse) — "
            "fort cadre réglementaire LkSG et sensibilité CSDDD élevée"
        ),
    }

    return {
        "ecosystem_snapshot_date": date.today().isoformat(),
        "total_partners_identified": len(POTENTIAL_PARTNERS_DB),
        "total_estimated_pipeline_EUR": round(total_pipeline),
        "category_stats": category_stats,
        "coverage_gaps": coverage_gaps,
        "strategic_priorities": strategic_priorities,
        "geographic_expansion_opportunities": geographic_expansion_opportunities,
        "csddd_focused_partners_total": sum(1 for p in POTENTIAL_PARTNERS_DB if p.get("csddd_focus")),
    }


def create_outreach_sequence(partner: dict, contact_role: str) -> dict:
    """
    Génère une séquence de prospection en 4 étapes personnalisée
    pour le contact désigné chez un partenaire potentiel.
    Séquence : email à froid → LinkedIn → relance → demande de réunion.
    """
    score_result = score_partner(partner)
    category_meta = PARTNER_CATEGORIES.get(partner["category"], {})

    today = date.today()
    day_1 = today
    day_7 = today + timedelta(days=7)
    day_14 = today + timedelta(days=14)
    day_21 = today + timedelta(days=21)

    # Personnalisation selon le tier
    tier_intro = {
        "PLATINUM": "en tant que partenaire stratégique prioritaire",
        "GOLD": "comme partenaire clé de notre écosystème",
        "SILVER": "dans notre programme partenaires en développement",
        "BRONZE": "dans le cadre d'une exploration de synergies",
    }.get(score_result["tier"], "dans notre réseau partenaires")

    csddd_angle = (
        "Votre positionnement déjà établi sur la conformité CSDDD"
        if partner.get("csddd_focus")
        else "Les enjeux CSDDD qui impactent vos clients"
    )

    sequence = {
        "sequence_id": f"OUT-{partner['name'][:5].upper().replace(' ', '')}-{today.strftime('%Y%m%d')}",
        "partner": partner["name"],
        "contact_role": contact_role,
        "tier": score_result["tier"],
        "total_steps": 4,
        "estimated_duration_days": 21,
        "steps": [
            {
                "step": 1,
                "type": "EMAIL_FROID",
                "label": "Premier contact — email personnalisé",
                "send_date": day_1.isoformat(),
                "channel": "Email professionnel",
                "subject": (
                    f"[CaelumSwarm™] Partenariat CSDDD — {partner['name']} × Caelum Partners"
                ),
                "body": (
                    f"Bonjour,\n\n"
                    f"Je me permets de vous contacter en tant que {contact_role} "
                    f"chez {partner['name']}.\n\n"
                    f"{csddd_angle} représente une opportunité majeure de différenciation "
                    f"que CaelumSwarm™ peut amplifier directement au bénéfice de vos clients.\n\n"
                    f"CaelumSwarm™ est la première plateforme d'intelligence collective dédiée "
                    f"au suivi des droits humains en chaîne de valeur — conçue pour accompagner "
                    f"les entreprises dans leur conformité CSDDD avec des données temps réel "
                    f"sur 190 pays et 47 secteurs.\n\n"
                    f"Nous identifions {partner['name']} {tier_intro} dans notre écosystème, "
                    f"avec un fort alignement sur les critères : expertise conformité, "
                    f"portée marché et couverture géographique.\n\n"
                    f"Seriez-vous disponible pour un échange de 20 minutes la semaine prochaine "
                    f"afin d'explorer les synergies possibles ?\n\n"
                    f"Cordialement,\n"
                    f"Équipe Partenariats — Caelum Partners\n"
                    f"partnerships@caelum-partners.com"
                ),
                "call_to_action": "Répondre pour fixer un créneau de 20 min",
                "personalization_tokens": ["contact_role", "partner_name", "csddd_focus", "tier"],
            },
            {
                "step": 2,
                "type": "LINKEDIN",
                "label": "Message LinkedIn — approche réseau professionnel",
                "send_date": day_7.isoformat(),
                "channel": "LinkedIn InMail ou connexion directe",
                "subject": "N/A — message direct LinkedIn",
                "body": (
                    f"Bonjour,\n\n"
                    f"J'ai eu l'occasion de suivre les travaux de {partner['name']} "
                    f"sur les enjeux de durabilité et de conformité — un travail remarquable "
                    f"dans un contexte réglementaire qui évolue très vite.\n\n"
                    f"Je vous ai adressé un email il y a quelques jours au sujet d'une "
                    f"collaboration potentielle entre {partner['name']} et CaelumSwarm™ "
                    f"sur le segment CSDDD. Je souhaitais également vous contacter ici "
                    f"pour m'assurer que le message ne s'est pas perdu.\n\n"
                    f"En quelques mots : notre plateforme permet à des acteurs comme "
                    f"{partner['name']} de proposer à leurs clients une solution de "
                    f"conformité CSDDD clé-en-main, avec un modèle de revenue share attractif.\n\n"
                    f"Un échange rapide vous conviendrait-il ?\n\n"
                    f"Bonne journée,"
                ),
                "call_to_action": "Accepter la connexion et répondre au message",
                "personalization_tokens": ["partner_name", "previous_email_reference"],
            },
            {
                "step": 3,
                "type": "RELANCE_EMAIL",
                "label": "Relance email — partage de ressource à valeur ajoutée",
                "send_date": day_14.isoformat(),
                "channel": "Email professionnel",
                "subject": (
                    f"[Ressource CSDDD] Comment {partner['name']} peut valoriser "
                    f"la conformité chaîne de valeur — Caelum Partners"
                ),
                "body": (
                    f"Bonjour,\n\n"
                    f"Je reviens vers vous avec une ressource qui pourrait directement "
                    f"intéresser les équipes de {partner['name']}.\n\n"
                    f"Nous venons de publier notre baromètre CaelumSwarm™ Q2 2026 sur "
                    f"l'état de préparation CSDDD des entreprises européennes : seulement "
                    f"23% des entreprises soumises à la directive disposent d'un système "
                    f"de monitoring de leur chaîne de valeur conforme aux exigences 2027.\n\n"
                    f"Cette fenêtre d'opportunité est précisément là où le partenariat "
                    f"{partner['name']} × CaelumSwarm™ crée de la valeur immédiate "
                    f"pour vos clients — en {category_meta.get('time_to_activate_months', 3)} mois "
                    f"d'activation.\n\n"
                    f"Je reste à votre disposition pour un échange. Sinon, n'hésitez pas "
                    f"à me faire savoir si un autre interlocuteur chez {partner['name']} "
                    f"serait plus approprié.\n\n"
                    f"Cordialement,\n"
                    f"Équipe Partenariats — Caelum Partners"
                ),
                "call_to_action": "Télécharger le baromètre et fixer un RDV",
                "personalization_tokens": ["partner_name", "category_time_to_activate", "sector_stat"],
            },
            {
                "step": 4,
                "type": "DEMANDE_REUNION",
                "label": "Invitation réunion formelle — dernière étape séquence",
                "send_date": day_21.isoformat(),
                "channel": "Email + invitation calendrier",
                "subject": (
                    f"Invitation : Exploration partenariat CaelumSwarm™ × {partner['name']} "
                    f"— 30 min — [DATE À COMPLÉTER]"
                ),
                "body": (
                    f"Bonjour,\n\n"
                    f"Je vous contacte une dernière fois pour cette séquence, "
                    f"en espérant que le timing sera cette fois plus favorable.\n\n"
                    f"Je me permets de vous proposer directement quelques créneaux "
                    f"pour un appel de découverte de 30 minutes :\n\n"
                    f"  • Mardi {(day_21 + timedelta(days=2)).strftime('%d/%m')} — 10h00 ou 14h30\n"
                    f"  • Jeudi {(day_21 + timedelta(days=4)).strftime('%d/%m')} — 11h00 ou 16h00\n"
                    f"  • Ou tout autre créneau selon vos disponibilités\n\n"
                    f"Objectif de l'appel : vous présenter en 20 minutes le modèle de "
                    f"partenariat CaelumSwarm™ adapté à {partner['name']}, les modalités "
                    f"commerciales et un cas client similaire dans votre secteur.\n\n"
                    f"Si ce sujet ne vous concerne pas directement, pourriez-vous me "
                    f"rediriger vers la personne en charge des partenariats stratégiques "
                    f"chez {partner['name']} ?\n\n"
                    f"Merci et bonne journée,\n"
                    f"Équipe Partenariats — Caelum Partners\n"
                    f"partnerships@caelum-partners.com | caelum-partners.com"
                ),
                "call_to_action": "Sélectionner un créneau ou rediriger vers la bonne personne",
                "personalization_tokens": ["partner_name", "proposed_slots", "redirect_option"],
                "attachment_suggested": "One-pager CaelumSwarm™ Partner Program (PDF)",
            },
        ],
        "sequence_tips": {
            "optimal_send_time": "Mardi-jeudi, 8h30-9h30 ou 17h00-18h00",
            "expected_response_rate_pct": 18 if score_result["tier"] in ("PLATINUM", "GOLD") else 12,
            "abort_if_unsubscribe": True,
            "crm_tracking_required": True,
            "follow_up_after_meeting": "Envoyer proposition formelle sous 48h post-réunion",
        },
    }

    return sequence


# ---------------------------------------------------------------------------
# 3. DÉMONSTRATION
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démontre les capacités du Partner Connector Agent :
    - Cartographie de l'écosystème
    - Top 3 des partenaires scorés
    - Proposition complète pour le meilleur partenaire
    - Séquence de prospection personnalisée
    """
    separator = "=" * 70

    print(separator)
    print("  CaelumSwarm™ PARTNER CONNECTOR AGENT — Démonstration")
    print(f"  Date : {date.today().isoformat()}")
    print(separator)

    # ------------------------------------------------------------------
    # SECTION 1 : Cartographie de l'écosystème
    # ------------------------------------------------------------------
    print("\n[1/4] CARTOGRAPHIE DE L'ÉCOSYSTÈME PARTENAIRES\n")
    ecosystem = map_partner_ecosystem()

    print(f"  Partenaires identifiés  : {ecosystem['total_partners_identified']}")
    print(f"  Focus CSDDD confirmé   : {ecosystem['csddd_focused_partners_total']}")
    print(f"  Pipeline total estimé  : {ecosystem['total_estimated_pipeline_EUR']:,}€\n")

    print("  Couverture par catégorie :")
    for cat, stats in ecosystem["category_stats"].items():
        bar = "#" * stats["nb_partenaires_identifies"] + "-" * max(0, 3 - stats["nb_partenaires_identifies"])
        print(
            f"    [{bar}] {stats['label']:<40} "
            f"{stats['nb_partenaires_identifies']} partenaires | "
            f"score moy. {stats['avg_score']}/100 | "
            f"pipeline {stats['estimated_pipeline_EUR']:,}€"
        )

    if ecosystem["coverage_gaps"]:
        print("\n  Gaps de couverture identifiés :")
        for gap in ecosystem["coverage_gaps"]:
            print(f"    ! [{gap['urgency']}] {gap['label']} — {gap['action']}")

    print("\n  Priorités stratégiques (top 3) :")
    for p in ecosystem["strategic_priorities"]:
        print(f"    #{p['rank']} {p['label']} (score priorité : {p['composite_priority_score']})")

    geo = ecosystem["geographic_expansion_opportunities"]
    print(f"\n  Marchés couverts      : {', '.join(geo['marchés_actuellement_couverts'])}")
    if geo["marchés_cibles_non_couverts"]:
        print(f"  Marchés à cibler      : {', '.join(geo['marchés_cibles_non_couverts'])}")
    print(f"  Recommandation géo    : {geo['recommandation']}")

    # ------------------------------------------------------------------
    # SECTION 2 : Top 3 partenaires scorés
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[2/4] TOP 3 PARTENAIRES — SCORING PONDÉRÉ\n")

    scored = sorted(
        [score_partner(p) for p in POTENTIAL_PARTNERS_DB],
        key=lambda x: x["total_score"],
        reverse=True,
    )

    for rank, result in enumerate(scored[:3], 1):
        print(f"  #{rank} {result['partner_name']}")
        print(f"      Score total   : {result['total_score']}/100")
        print(f"      Tier          : {result['tier']}")
        print(f"      Modèle recomm.: {PARTNERSHIP_MODELS[result['recommended_model']]['label']}")
        print(f"      Priorité      : Niveau {result['priority_ranking']}")
        print(f"      Détail scores :")
        for crit, vals in result["breakdown"].items():
            bar = "█" * int(vals["raw"] / 10)
            print(f"        {crit:<28} {bar:<10} {vals['raw']}/100 × {vals['weight']} = {vals['weighted_contribution']}")
        if result["csddd_bonus_applied"]:
            print(f"      Bonus CSDDD   : +{result['csddd_bonus_applied']}")
        print()

    # ------------------------------------------------------------------
    # SECTION 3 : Proposition de partenariat complète pour le #1
    # ------------------------------------------------------------------
    print(f"{separator}")
    print("[3/4] PROPOSITION DE PARTENARIAT — MEILLEUR PARTENAIRE\n")

    top_partner_name = scored[0]["partner_name"]
    top_partner = next(p for p in POTENTIAL_PARTNERS_DB if p["name"] == top_partner_name)
    recommended_model = scored[0]["recommended_model"]

    proposal = generate_partnership_proposal(top_partner, recommended_model)

    print(f"  Référence proposition : {proposal['proposal_id']}")
    print(f"  Partenaire            : {proposal['partner']} ({proposal['country']})")
    print(f"  Modèle                : {proposal['partnership_model']}")
    print(f"  Tier                  : {proposal['tier']}\n")

    print("  RÉSUMÉ EXÉCUTIF :")
    for line in proposal["executive_summary"].split(". "):
        if line.strip():
            print(f"    {line.strip()}.")

    print("\n  VALEUR POUR LE PARTENAIRE :")
    print(f"    {proposal['value_proposition_for_partner']['headline']}")
    for pt in proposal["value_proposition_for_partner"]["points"]:
        print(f"    • {pt}")

    print("\n  VALEUR POUR CAELUM :")
    print(f"    {proposal['value_proposition_for_caelum']['headline']}")
    for pt in proposal["value_proposition_for_caelum"]["points"]:
        print(f"    • {pt}")

    terms = proposal["commercial_terms"]
    print("\n  CONDITIONS COMMERCIALES :")
    print(f"    Revenue share    : {terms['revenue_share_pct']}%")
    print(f"    Exclusivité      : {terms['exclusivity']}")
    print(f"    Durée contrat    : {terms['contract_duration_years']} ans")
    print(f"    Pipeline estimé  : {terms['estimated_pipeline_3y_EUR']:,}€ sur 3 ans")
    print(f"    Engagement min.  : {terms['minimum_commitment']}")
    print("    Prérequis        :")
    for req in terms["requirements"]:
        print(f"      ✓ {req}")

    print("\n  ROADMAP D'INTÉGRATION :")
    for phase in proposal["integration_roadmap"]:
        print(f"    Phase {phase['phase']} — {phase['label']} ({phase['timeline']})")
        for ms in phase["milestones"]:
            print(f"      → {ms}")

    metrics = proposal["success_metrics"]
    print("\n  MÉTRIQUES DE SUCCÈS :")
    print(f"    Leads/an            : {metrics['kpi_leads_qualifies_par_an']}")
    print(f"    Taux conversion     : {metrics['kpi_taux_conversion_cible_pct']}%")
    print(f"    Satisfaction cible  : {metrics['kpi_satisfaction_partenaire_cible']}")
    print(f"    Contrats signés an1 : {metrics['kpi_contrats_signes_an1']}")
    print(f"    Revenue partagé an1 : {metrics['kpi_revenue_partage_an1_EUR']:,}€")

    # ------------------------------------------------------------------
    # SECTION 4 : Séquence de prospection
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[4/4] SÉQUENCE DE PROSPECTION — 4 ÉTAPES\n")

    outreach = create_outreach_sequence(top_partner, top_partner["contact_role"])

    print(f"  ID séquence    : {outreach['sequence_id']}")
    print(f"  Partenaire     : {outreach['partner']}")
    print(f"  Contact cible  : {outreach['contact_role']}")
    print(f"  Tier           : {outreach['tier']}")
    print(f"  Durée totale   : {outreach['estimated_duration_days']} jours\n")

    for step in outreach["steps"]:
        print(f"  ÉTAPE {step['step']} — {step['label']}")
        print(f"    Date      : {step['send_date']}")
        print(f"    Canal     : {step['channel']}")
        if step.get("subject") and step["subject"] != "N/A — message direct LinkedIn":
            print(f"    Objet     : {step['subject']}")
        print(f"    CTA       : {step['call_to_action']}")
        preview = step["body"].replace("\n", " ")[:120]
        print(f"    Aperçu    : {preview}…")
        print()

    tips = outreach["sequence_tips"]
    print(f"  Heure optimale d'envoi  : {tips['optimal_send_time']}")
    print(f"  Taux réponse estimé     : {tips['expected_response_rate_pct']}%")
    print(f"  Suivi post-réunion      : {tips['follow_up_after_meeting']}")

    print(f"\n{separator}")
    print("  Démonstration terminée — CaelumSwarm™ Partner Connector Agent v1.0")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# 4. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if not success:
        raise SystemExit(1)
