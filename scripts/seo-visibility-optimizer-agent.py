"""
CaelumSwarm™ — SEO Visibility Optimizer Agent
==============================================
Optimise la visibilité organique des contenus CSDDD pour les décideurs B2B :
directeurs RSE, responsables conformité et investisseurs ESG.

Objectif : positionner Caelum Partners comme référence incontournable sur les
requêtes stratégiques liées à la directive européenne CSDDD (Corporate
Sustainability Due Diligence Directive), CSRD et devoir de vigilance, afin de
générer un flux qualifié de leads decision-makers en phase d'évaluation ou
d'achat d'une solution de conformité droits humains.

Architecture :
- Analyse d'opportunités mots-clés (volume × difficulté × pertinence CSDDD)
- Scoring santé SEO on-page + technique
- Génération de briefs contenu par pilier éditorial
- Roadmap SEO 6 mois avec projections trafic

Usage : python3 seo-visibility-optimizer-agent.py
"""

import sys
import math
from datetime import datetime, timedelta
from typing import Any

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

KEYWORD_UNIVERSE: dict[str, dict[str, Any]] = {
    "conformite_csddd_2027": {
        "keyword": "conformité CSDDD 2027",
        "monthly_volume": 2400,
        "difficulty": 38,
        "intent": "INFORMATIONAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 8,
        "target_rank": 3,
    },
    "due_diligence_droits_humains": {
        "keyword": "due diligence droits humains",
        "monthly_volume": 1800,
        "difficulty": 45,
        "intent": "INFORMATIONAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 12,
        "target_rank": 4,
    },
    "esg_reporting_automation": {
        "keyword": "ESG reporting automation",
        "monthly_volume": 3200,
        "difficulty": 62,
        "intent": "COMMERCIAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 15,
        "target_rank": 5,
    },
    "csrd_compliance_tool": {
        "keyword": "CSRD compliance tool",
        "monthly_volume": 2900,
        "difficulty": 57,
        "intent": "COMMERCIAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 11,
        "target_rank": 3,
    },
    "human_rights_due_diligence_software": {
        "keyword": "human rights due diligence software",
        "monthly_volume": 1400,
        "difficulty": 41,
        "intent": "TRANSACTIONAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 9,
        "target_rank": 2,
    },
    "devoir_vigilance_entreprise": {
        "keyword": "devoir vigilance entreprise",
        "monthly_volume": 3800,
        "difficulty": 33,
        "intent": "INFORMATIONAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 7,
        "target_rank": 2,
    },
    "scope3_emissions_tracking": {
        "keyword": "scope 3 emissions tracking",
        "monthly_volume": 4100,
        "difficulty": 69,
        "intent": "COMMERCIAL",
        "csddd_relevance": "MEDIUM",
        "competitor_rank": 18,
        "target_rank": 7,
    },
    "supply_chain_risk_monitoring": {
        "keyword": "supply chain risk monitoring",
        "monthly_volume": 5600,
        "difficulty": 71,
        "intent": "COMMERCIAL",
        "csddd_relevance": "MEDIUM",
        "competitor_rank": 20,
        "target_rank": 8,
    },
    "rapport_extra_financier_automatise": {
        "keyword": "rapport extra-financier automatisé",
        "monthly_volume": 960,
        "difficulty": 28,
        "intent": "COMMERCIAL",
        "csddd_relevance": "HIGH",
        "competitor_rank": 6,
        "target_rank": 1,
    },
    "logiciel_conformite_rse": {
        "keyword": "logiciel conformité RSE",
        "monthly_volume": 1600,
        "difficulty": 44,
        "intent": "TRANSACTIONAL",
        "csddd_relevance": "MEDIUM",
        "competitor_rank": 14,
        "target_rank": 4,
    },
}

ON_PAGE_FACTORS: dict[str, dict[str, Any]] = {
    "title_tag": {
        "label": "Balise Title optimisée",
        "weight": 0.20,
        "current_score": 72,
        "target_score": 95,
        "description": "Inclure mot-clé primaire dans les 60 premiers caractères",
    },
    "meta_description": {
        "label": "Meta Description persuasive",
        "weight": 0.10,
        "current_score": 58,
        "target_score": 90,
        "description": "CTA explicite + mot-clé dans les 155 caractères",
    },
    "h1_optimization": {
        "label": "H1 unique et optimisé",
        "weight": 0.15,
        "current_score": 80,
        "target_score": 95,
        "description": "Un seul H1 par page, aligné avec l'intent de recherche",
    },
    "content_depth": {
        "label": "Profondeur de contenu",
        "weight": 0.20,
        "current_score": 55,
        "target_score": 85,
        "description": "Couverture sémantique complète, > 1500 mots pour piliers",
    },
    "schema_markup": {
        "label": "Schema Markup structuré",
        "weight": 0.10,
        "current_score": 40,
        "target_score": 90,
        "description": "JSON-LD : Article, Organization, FAQPage",
    },
    "core_web_vitals": {
        "label": "Core Web Vitals (LCP/FID/CLS)",
        "weight": 0.10,
        "current_score": 68,
        "target_score": 88,
        "description": "LCP < 2.5s, FID < 100ms, CLS < 0.1",
    },
    "internal_linking": {
        "label": "Maillage interne stratégique",
        "weight": 0.08,
        "current_score": 45,
        "target_score": 80,
        "description": "3-5 liens contextuels vers pages piliers par article cluster",
    },
    "image_alt": {
        "label": "Attributs Alt images",
        "weight": 0.07,
        "current_score": 62,
        "target_score": 95,
        "description": "Alt descriptif + mot-clé naturel sur toutes les images",
    },
}

CONTENT_PILLARS: dict[str, dict[str, Any]] = {
    "CSDDD_COMPLIANCE": {
        "label": "Conformité CSDDD & CSRD",
        "cluster_keywords": [
            "conformité CSDDD 2027",
            "CSRD compliance tool",
            "rapport extra-financier automatisé",
            "directive devoir de vigilance UE",
            "CSDDD implementation timeline",
        ],
        "content_formats": [
            "Guide pratique (5000 mots)",
            "Checklist téléchargeable",
            "Webinar mensuel",
            "FAQ interactive",
            "Template de rapport",
        ],
        "publishing_frequency": "2 articles / semaine",
        "priority": "CRITIQUE",
    },
    "ESG_DATA_ANALYTICS": {
        "label": "Analytics & Données ESG",
        "cluster_keywords": [
            "ESG reporting automation",
            "scope 3 emissions tracking",
            "ESG data management platform",
            "indicateurs ESG mesure",
            "automatisation reporting non-financier",
        ],
        "content_formats": [
            "Étude de cas client",
            "Benchmark sectoriel",
            "Démo interactive",
            "Infographie données",
            "Podcast expert",
        ],
        "publishing_frequency": "1 article + 1 étude de cas / semaine",
        "priority": "ÉLEVÉ",
    },
    "HUMAN_RIGHTS_METHODOLOGY": {
        "label": "Méthodologie Droits Humains",
        "cluster_keywords": [
            "due diligence droits humains",
            "human rights due diligence software",
            "devoir vigilance entreprise",
            "cartographie risques droits humains",
            "UNGPs business human rights",
        ],
        "content_formats": [
            "Livre blanc (10 000 mots)",
            "Matrice d'évaluation risques",
            "Interview expert ONG",
            "Glossaire juridique",
            "Étude comparative législations",
        ],
        "publishing_frequency": "1 contenu premium / semaine",
        "priority": "CRITIQUE",
    },
    "REGULATORY_INTELLIGENCE": {
        "label": "Veille Réglementaire UE",
        "cluster_keywords": [
            "veille réglementaire CSDDD",
            "mise à jour directive droits humains UE",
            "calendar conformité RSE 2025-2027",
            "transposition loi vigilance France",
            "amendements CSRD dernière heure",
        ],
        "content_formats": [
            "Newsletter hebdomadaire",
            "Alerte réglementaire flash",
            "Analyse juridique approfondie",
            "Timeline interactive",
            "Comparatif pays UE",
        ],
        "publishing_frequency": "3 newsletters + 1 analyse / semaine",
        "priority": "ÉLEVÉ",
    },
    "CASE_STUDIES": {
        "label": "Cas Clients & ROI",
        "cluster_keywords": [
            "supply chain risk monitoring",
            "logiciel conformité RSE",
            "ROI solution conformité ESG",
            "retour expérience due diligence",
            "benchmark temps conformité CSDDD",
        ],
        "content_formats": [
            "Étude de cas vidéo",
            "Témoignage client (PDF)",
            "Calculateur ROI interactif",
            "Before/After infographie",
            "Success story LinkedIn",
        ],
        "publishing_frequency": "2 case studies / mois",
        "priority": "MODÉRÉ",
    },
}

TECHNICAL_SEO_CHECKLIST: dict[str, dict[str, Any]] = {
    "mobile_friendly": {
        "label": "Responsive mobile",
        "status": "PASS",
        "priority": "HIGH",
        "impact": "Critère de classement Google depuis 2021",
    },
    "page_speed_score": {
        "label": "Score vitesse page (PageSpeed Insights)",
        "status": "WARNING",
        "priority": "HIGH",
        "impact": "Score actuel 71/100 — cible > 85/100",
    },
    "https_secure": {
        "label": "HTTPS & certificat SSL",
        "status": "PASS",
        "priority": "HIGH",
        "impact": "Signal de confiance et de sécurité Google",
    },
    "xml_sitemap": {
        "label": "Sitemap XML soumis & valide",
        "status": "PASS",
        "priority": "MEDIUM",
        "impact": "Facilite l'indexation de toutes les URLs",
    },
    "robots_txt": {
        "label": "robots.txt configuré",
        "status": "PASS",
        "priority": "MEDIUM",
        "impact": "Contrôle du crawl budget Googlebot",
    },
    "structured_data": {
        "label": "Données structurées JSON-LD",
        "status": "FAIL",
        "priority": "HIGH",
        "impact": "Rich snippets : FAQ, Article, Organization — +CTR estimé 30%",
    },
    "crawlability": {
        "label": "Crawlabilité & liens brisés",
        "status": "WARNING",
        "priority": "MEDIUM",
        "impact": "14 liens 404 détectés — perte de PageRank",
    },
    "canonical_tags": {
        "label": "Balises canonical",
        "status": "WARNING",
        "priority": "MEDIUM",
        "impact": "Risque de contenu dupliqué sur 8 pages pagination",
    },
}

# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

CSDDD_RELEVANCE_FACTOR: dict[str, float] = {
    "HIGH": 1.5,
    "MEDIUM": 1.0,
}

INTENT_WORD_COUNT: dict[str, int] = {
    "INFORMATIONAL": 2200,
    "COMMERCIAL": 1600,
    "TRANSACTIONAL": 1000,
}

TECHNICAL_STATUS_SCORE: dict[str, float] = {
    "PASS": 100.0,
    "WARNING": 60.0,
    "FAIL": 0.0,
}


def analyze_keyword_opportunity(keywords: dict) -> dict:
    """
    Calcule un score d'opportunité SEO pour chaque mot-clé.

    Formule : (monthly_volume / 1000) × (1 - difficulty/100) × relevance_factor

    Retourne les opportunités triées par score décroissant avec gap analysis
    (écart entre position concurrente et position cible).
    """
    opportunities = []

    for key, kw in keywords.items():
        relevance_factor = CSDDD_RELEVANCE_FACTOR.get(kw["csddd_relevance"], 1.0)
        difficulty_ratio = 1 - (kw["difficulty"] / 100)
        volume_unit = kw["monthly_volume"] / 1000

        opportunity_score = round(volume_unit * difficulty_ratio * relevance_factor, 3)

        rank_gap = kw["competitor_rank"] - kw["target_rank"]

        # Estimation trafic potentiel mensuel en position cible
        # CTR moyen par position (données industry B2B SaaS)
        ctr_by_rank = {
            1: 0.28, 2: 0.18, 3: 0.12, 4: 0.08, 5: 0.06,
            6: 0.04, 7: 0.03, 8: 0.025, 9: 0.02, 10: 0.015,
        }
        target_ctr = ctr_by_rank.get(kw["target_rank"], 0.01)
        current_ctr = ctr_by_rank.get(kw["competitor_rank"], 0.005)
        traffic_potential = round(kw["monthly_volume"] * target_ctr)
        traffic_current_estimate = round(kw["monthly_volume"] * current_ctr)
        traffic_uplift = traffic_potential - traffic_current_estimate

        opportunities.append({
            "key": key,
            "keyword": kw["keyword"],
            "monthly_volume": kw["monthly_volume"],
            "difficulty": kw["difficulty"],
            "intent": kw["intent"],
            "csddd_relevance": kw["csddd_relevance"],
            "competitor_rank": kw["competitor_rank"],
            "target_rank": kw["target_rank"],
            "opportunity_score": opportunity_score,
            "rank_gap": rank_gap,
            "traffic_potential_monthly": traffic_potential,
            "traffic_uplift_monthly": traffic_uplift,
            "quick_win": rank_gap >= 5 and kw["difficulty"] < 50,
        })

    # Tri par score d'opportunité décroissant
    opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)

    # Segment quick wins (gains rapides < 3 mois)
    quick_wins = [o for o in opportunities if o["quick_win"]]
    strategic_bets = [o for o in opportunities if not o["quick_win"]]

    total_traffic_potential = sum(o["traffic_potential_monthly"] for o in opportunities)
    total_traffic_uplift = sum(o["traffic_uplift_monthly"] for o in opportunities)

    return {
        "opportunities": opportunities,
        "quick_wins": quick_wins,
        "strategic_bets": strategic_bets,
        "summary": {
            "total_keywords_analyzed": len(opportunities),
            "quick_wins_count": len(quick_wins),
            "total_traffic_potential_monthly": total_traffic_potential,
            "total_traffic_uplift_monthly": total_traffic_uplift,
            "avg_opportunity_score": round(
                sum(o["opportunity_score"] for o in opportunities) / len(opportunities), 3
            ),
            "top_keyword": opportunities[0]["keyword"] if opportunities else None,
        },
    }


def generate_content_brief(keyword: str, pillar: str, wave_number: int) -> dict:
    """
    Génère un brief contenu complet pour une équipe éditoriale.

    Adapte le format, le nombre de mots et la structure H2/H3 en fonction
    de l'intent de recherche détecté et du pilier éditorial cible.
    """
    # Détection intent à partir du mot-clé
    kw_data = next(
        (v for v in KEYWORD_UNIVERSE.values() if v["keyword"] == keyword),
        None,
    )

    intent = kw_data["intent"] if kw_data else "INFORMATIONAL"
    monthly_volume = kw_data["monthly_volume"] if kw_data else 1000
    difficulty = kw_data["difficulty"] if kw_data else 50
    target_word_count = INTENT_WORD_COUNT.get(intent, 1800)

    # Pilier editorial
    pillar_data = CONTENT_PILLARS.get(pillar, {})
    pillar_label = pillar_data.get("label", pillar)

    # Options de titres selon intent
    title_templates = {
        "INFORMATIONAL": [
            f"Tout comprendre sur : {keyword} — Guide complet {datetime.now().year}",
            f"{keyword.capitalize()} : définition, enjeux et obligations pour les entreprises UE",
            f"Guide expert {keyword} : ce que chaque directeur RSE doit savoir",
        ],
        "COMMERCIAL": [
            f"Comparer les solutions {keyword} — Benchmark {datetime.now().year}",
            f"{keyword.capitalize()} : comment choisir la bonne plateforme pour votre entreprise ?",
            f"Top 5 outils {keyword} — évaluation indépendante Caelum Partners",
        ],
        "TRANSACTIONAL": [
            f"Demander une démo {keyword} — Caelum Partners",
            f"{keyword.capitalize()} : essai gratuit 14 jours — sans engagement",
            f"Tarifs et fonctionnalités {keyword} — Demandez votre offre personnalisée",
        ],
    }

    title_options = title_templates.get(intent, title_templates["INFORMATIONAL"])

    # Meta description
    meta_templates = {
        "INFORMATIONAL": (
            f"Découvrez tout ce qu'il faut savoir sur {keyword} : cadre réglementaire, "
            f"obligations 2027 et outils pour se conformer. Guide expert Caelum Partners. ▶ Lire maintenant"
        ),
        "COMMERCIAL": (
            f"Comparez les meilleures solutions {keyword} du marché. "
            f"Benchmark objectif, critères d'évaluation et recommandations expertes. ▶ Télécharger le benchmark"
        ),
        "TRANSACTIONAL": (
            f"Découvrez comment Caelum Partners automatise votre {keyword}. "
            f"Essai gratuit 14 jours, onboarding en 48h. ▶ Démarrer maintenant"
        ),
    }
    meta_description = meta_templates.get(intent, meta_templates["INFORMATIONAL"])

    # Structure H2/H3 selon intent
    h_structures = {
        "INFORMATIONAL": [
            {"level": "H2", "text": f"Qu'est-ce que {keyword} ? Définition et contexte réglementaire"},
            {"level": "H3", "text": "Cadre juridique européen : CSDDD, CSRD et loi de vigilance française"},
            {"level": "H3", "text": "Qui est concerné ? Seuils et calendriers d'application"},
            {"level": "H2", "text": f"Pourquoi {keyword} est devenu une priorité stratégique en {datetime.now().year}"},
            {"level": "H3", "text": "Risques financiers et réputationnels en cas de non-conformité"},
            {"level": "H3", "text": "Pression des investisseurs ESG et des marchés financiers"},
            {"level": "H2", "text": "Comment mettre en œuvre une démarche conforme : étapes clés"},
            {"level": "H3", "text": "Étape 1 — Cartographie des risques dans la chaîne de valeur"},
            {"level": "H3", "text": "Étape 2 — Collecte et vérification des données fournisseurs"},
            {"level": "H3", "text": "Étape 3 — Rapport de diligence raisonnable et publication"},
            {"level": "H2", "text": "Outils et plateformes pour automatiser votre conformité"},
            {"level": "H2", "text": "FAQ — Questions fréquentes sur " + keyword},
        ],
        "COMMERCIAL": [
            {"level": "H2", "text": f"Pourquoi votre entreprise a besoin d'une solution {keyword}"},
            {"level": "H3", "text": "Limites des approches manuelles et tableurs Excel"},
            {"level": "H3", "text": "ROI d'une plateforme dédiée : calcul et benchmark sectoriel"},
            {"level": "H2", "text": "Critères d'évaluation d'une solution " + keyword},
            {"level": "H3", "text": "Intégrations ERP et connecteurs data (SAP, Workday, Oracle)"},
            {"level": "H3", "text": "Sécurité, RGPD et hébergement des données sensibles"},
            {"level": "H3", "text": "Support, SLA et accompagnement au changement"},
            {"level": "H2", "text": "Benchmark des 5 principales solutions du marché"},
            {"level": "H3", "text": "Tableau comparatif fonctionnalités × prix × support"},
            {"level": "H2", "text": "Caelum Partners — Pourquoi nous choisissent les leaders CAC 40"},
            {"level": "H2", "text": "Étapes suivantes : demander une démo personnalisée"},
        ],
        "TRANSACTIONAL": [
            {"level": "H2", "text": f"Caelum Partners — La solution de référence pour {keyword}"},
            {"level": "H3", "text": "Fonctionnalités clés incluses dès l'essai gratuit"},
            {"level": "H3", "text": "Onboarding en 48h avec votre Customer Success Manager dédié"},
            {"level": "H2", "text": "Résultats clients après 90 jours d'utilisation"},
            {"level": "H3", "text": "Témoignages : directeurs RSE CAC 40 et ETI européennes"},
            {"level": "H2", "text": "Tarifs et plans — Transparent, sans surprise"},
            {"level": "H2", "text": "Démarrer votre essai gratuit — Processus en 3 étapes"},
        ],
    }
    suggested_headers = h_structures.get(intent, h_structures["INFORMATIONAL"])

    # Liens internes suggérés (basés sur cluster du pilier)
    cluster_kws = pillar_data.get("cluster_keywords", [])[:4]
    internal_links = [
        {
            "anchor": kw,
            "url": f"/blog/{kw.lower().replace(' ', '-').replace('/', '-')}",
            "context": "Lier dans la section pertinente thématiquement",
        }
        for kw in cluster_kws
        if kw != keyword
    ]
    # Ajouter lien vers page produit
    internal_links.append({
        "anchor": "plateforme de conformité Caelum Partners",
        "url": "/plateforme",
        "context": "CTA interne en fin d'article ou dans la section outils",
    })

    # CTA primaire selon intent
    cta_map = {
        "INFORMATIONAL": {
            "text": "Télécharger le guide complet PDF gratuit",
            "url": "/ressources/guide-csddd-2027",
            "type": "LEAD_MAGNET",
        },
        "COMMERCIAL": {
            "text": "Demander le benchmark complet (version longue)",
            "url": "/benchmark-solutions-conformite",
            "type": "GATED_CONTENT",
        },
        "TRANSACTIONAL": {
            "text": "Démarrer mon essai gratuit 14 jours",
            "url": "/essai-gratuit",
            "type": "FREE_TRIAL",
        },
    }
    cta_primary = cta_map.get(intent, cta_map["INFORMATIONAL"])

    return {
        "brief_metadata": {
            "keyword_primary": keyword,
            "pillar": pillar,
            "pillar_label": pillar_label,
            "wave_number": wave_number,
            "intent": intent,
            "generated_at": datetime.now().isoformat(),
            "monthly_volume": monthly_volume,
            "keyword_difficulty": difficulty,
        },
        "content_specs": {
            "target_word_count": target_word_count,
            "content_format": pillar_data.get("content_formats", ["Article de blog"])[0],
            "reading_time_minutes": math.ceil(target_word_count / 200),
            "expertise_level": "Expert B2B — ton professionnel, données chiffrées obligatoires",
            "tone": "Autoritaire mais accessible, sans jargon inutile",
            "language_primary": "Français",
            "language_secondary": "Termes techniques en anglais acceptés (CSDDD, ESG, KPI)",
        },
        "title_options": title_options,
        "meta_description": meta_description,
        "suggested_headers": suggested_headers,
        "internal_links_suggested": internal_links,
        "cta_primary": cta_primary,
        "seo_requirements": {
            "keyword_density_primary": "0.8% - 1.2% (naturel, pas de sur-optimisation)",
            "keyword_in_first_100_words": True,
            "keyword_in_at_least_one_h2": True,
            "min_external_sources": 3,
            "required_schema": "Article + FAQPage (si FAQ présente)",
            "image_count_recommended": "3-5 images avec alt optimisé",
            "structured_data": "JSON-LD Article avec author Caelum Partners",
        },
        "audience": {
            "primary_persona": "Directeur(rice) RSE — ETI/Grande entreprise UE",
            "secondary_persona": "Responsable conformité / Juriste d'entreprise",
            "pain_points": [
                "Complexité des exigences réglementaires CSDDD/CSRD",
                "Manque de ressources internes pour la collecte de données",
                "Pression du board et des investisseurs sur le calendrier de conformité",
                "Risque de sanctions financières en cas de non-conformité 2027",
            ],
        },
    }


def calculate_seo_health_score(on_page: dict, technical: dict) -> dict:
    """
    Calcule un score global de santé SEO pondéré.

    Score on-page : moyenne pondérée des facteurs on-page (current_score × weight).
    Score technique : moyenne des scores PASS=100 / WARNING=60 / FAIL=0.
    Score global : 70% on-page + 30% technique.

    Retourne le score, les sous-scores et une liste de correctifs prioritaires.
    """
    # Score on-page pondéré
    on_page_score = 0.0
    for factor_key, factor in on_page.items():
        on_page_score += factor["current_score"] * factor["weight"]
    on_page_score = round(on_page_score, 1)

    # Score technique (moyenne simple des statuts)
    tech_scores = []
    for item_key, item in technical.items():
        status = item.get("status", "FAIL")
        tech_scores.append(TECHNICAL_STATUS_SCORE.get(status, 0.0))
    technical_score = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 0.0

    # Score global (pondération : on-page 70%, technique 30%)
    overall_score = round(on_page_score * 0.70 + technical_score * 0.30, 1)

    # Niveau de maturité SEO
    if overall_score >= 85:
        maturity_level = "EXCELLENT"
        maturity_label = "Site SEO mature — phase d'optimisation fine"
    elif overall_score >= 70:
        maturity_level = "BON"
        maturity_label = "Fondations solides — gains rapides identifiés"
    elif overall_score >= 55:
        maturity_level = "MOYEN"
        maturity_label = "Travaux fondamentaux requis avant de scaler"
    else:
        maturity_level = "FAIBLE"
        maturity_label = "Audit complet nécessaire en urgence"

    # Correctifs prioritaires
    priority_fixes = []

    # Facteurs on-page avec le plus grand écart
    on_page_gaps = []
    for factor_key, factor in on_page.items():
        gap = factor["target_score"] - factor["current_score"]
        if gap > 10:
            on_page_gaps.append({
                "type": "ON_PAGE",
                "factor": factor_key,
                "label": factor.get("label", factor_key),
                "current": factor["current_score"],
                "target": factor["target_score"],
                "gap": gap,
                "priority": "HIGH" if gap > 30 else "MEDIUM",
                "action": factor.get("description", "Optimiser ce facteur"),
            })
    on_page_gaps.sort(key=lambda x: x["gap"], reverse=True)
    priority_fixes.extend(on_page_gaps[:4])

    # Éléments techniques FAIL ou WARNING
    for item_key, item in technical.items():
        if item["status"] in ("FAIL", "WARNING"):
            priority_fixes.append({
                "type": "TECHNICAL",
                "factor": item_key,
                "label": item.get("label", item_key),
                "status": item["status"],
                "priority": item["priority"],
                "action": item.get("impact", "Corriger cet élément technique"),
            })

    # Trier par priorité (HIGH > MEDIUM > LOW)
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    priority_fixes.sort(key=lambda x: priority_order.get(x["priority"], 3))

    return {
        "overall_score": overall_score,
        "on_page_score": on_page_score,
        "technical_score": technical_score,
        "maturity_level": maturity_level,
        "maturity_label": maturity_label,
        "score_breakdown": {
            "on_page_weight": "70%",
            "technical_weight": "30%",
            "factors_analyzed": len(on_page) + len(technical),
        },
        "priority_fixes": priority_fixes,
        "quick_score_lifts": [
            fix for fix in priority_fixes
            if fix.get("priority") == "HIGH" and fix.get("gap", 0) > 20
        ],
    }


def generate_seo_roadmap(months: int = 6) -> dict:
    """
    Génère une roadmap SEO mensuelle sur N mois.

    Chaque mois : focus stratégique, mots-clés cibles, contenus à créer,
    actions techniques prioritaires et projection de lift de trafic cumulatif.
    """
    base_date = datetime.now()

    roadmap_template = [
        {
            "month_offset": 1,
            "focus_area": "Fondations techniques & audit",
            "strategic_theme": "Corriger les bloquants techniques + publier contenu pilier #1",
            "target_keywords": [
                "devoir vigilance entreprise",
                "conformité CSDDD 2027",
                "rapport extra-financier automatisé",
            ],
            "content_pieces": [
                {"type": "Guide pilier", "title": "Guide complet devoir de vigilance 2027", "word_count": 5000, "pillar": "CSDDD_COMPLIANCE"},
                {"type": "Landing page", "title": "Conformité CSDDD — Plateforme Caelum", "word_count": 1200, "pillar": "CSDDD_COMPLIANCE"},
                {"type": "Article cluster", "title": "Rapport extra-financier : automatiser en 5 étapes", "word_count": 2200, "pillar": "ESG_DATA_ANALYTICS"},
            ],
            "technical_actions": [
                "Implémenter JSON-LD sur toutes les pages (structured_data FAIL → PASS)",
                "Corriger les 14 liens 404 identifiés (crawlability WARNING)",
                "Ajouter canonical tags sur pages de pagination (canonical_tags WARNING)",
            ],
            "expected_traffic_lift_pct": 8,
            "kpi_targets": {
                "organic_sessions": "+8%",
                "keywords_top_10": "+3 nouveaux mots-clés",
                "technical_score": "75 → 88",
            },
        },
        {
            "month_offset": 2,
            "focus_area": "Content velocity — Droits Humains & CSRD",
            "strategic_theme": "Accélérer la publication sur piliers Droits Humains et Conformité CSRD",
            "target_keywords": [
                "due diligence droits humains",
                "CSRD compliance tool",
                "human rights due diligence software",
            ],
            "content_pieces": [
                {"type": "Livre blanc", "title": "Due diligence droits humains : méthodologie UNGPs", "word_count": 8000, "pillar": "HUMAN_RIGHTS_METHODOLOGY"},
                {"type": "Article comparatif", "title": "CSRD vs CSDDD : différences, calendrier et impacts entreprise", "word_count": 3000, "pillar": "CSDDD_COMPLIANCE"},
                {"type": "Étude de cas", "title": "Comment [Client CAC40] a réduit son risque fournisseur de 40%", "word_count": 1800, "pillar": "CASE_STUDIES"},
                {"type": "FAQ page", "title": "FAQ — Human Rights Due Diligence Software : toutes vos questions", "word_count": 2500, "pillar": "HUMAN_RIGHTS_METHODOLOGY"},
            ],
            "technical_actions": [
                "Optimiser Core Web Vitals — compression images & lazy loading",
                "Mettre en place le maillage interne stratégique (pilier → clusters)",
                "A/B test title tags sur top 5 pages trafic",
            ],
            "expected_traffic_lift_pct": 18,
            "kpi_targets": {
                "organic_sessions": "+18% vs M0",
                "keywords_top_10": "+8 nouveaux mots-clés",
                "backlinks_earned": "+12 domaines référents (PR livre blanc)",
            },
        },
        {
            "month_offset": 3,
            "focus_area": "Autorité thématique & link earning",
            "strategic_theme": "Construire l'autorité de domaine via PR digitale et contenus linkbait",
            "target_keywords": [
                "ESG reporting automation",
                "logiciel conformité RSE",
                "veille réglementaire CSDDD",
            ],
            "content_pieces": [
                {"type": "Rapport de recherche", "title": "Baromètre conformité CSDDD 2025 — 200 entreprises françaises", "word_count": 6000, "pillar": "REGULATORY_INTELLIGENCE"},
                {"type": "Outil interactif", "title": "Calculateur — Mon entreprise est-elle prête pour la CSDDD ?", "word_count": 800, "pillar": "CSDDD_COMPLIANCE"},
                {"type": "Article SEO", "title": "Top 7 logiciels conformité RSE comparés en 2025", "word_count": 3500, "pillar": "CASE_STUDIES"},
                {"type": "Newsletter SEO", "title": "Série mensuelle : Veille réglementaire ESG (archive Google-indexable)", "word_count": 1500, "pillar": "REGULATORY_INTELLIGENCE"},
            ],
            "technical_actions": [
                "Campagne outreach presse spécialisée (Les Échos Executives, Novethic, ESG News)",
                "Optimisation vitesse page — cible PageSpeed > 85",
                "Mise en place du tracking heatmaps pour données UX",
            ],
            "expected_traffic_lift_pct": 32,
            "kpi_targets": {
                "organic_sessions": "+32% vs M0",
                "keywords_top_5": "+5 mots-clés en top 5",
                "domain_authority": "DA 38 → 45",
            },
        },
        {
            "month_offset": 4,
            "focus_area": "Conversion & intent transactionnel",
            "strategic_theme": "Capturer l'intent commercial/transactionnel — pipeline MQL",
            "target_keywords": [
                "human rights due diligence software",
                "scope 3 emissions tracking",
                "supply chain risk monitoring",
            ],
            "content_pieces": [
                {"type": "Page produit SEO", "title": "Human Rights Due Diligence Software — Caelum Partners", "word_count": 1800, "pillar": "HUMAN_RIGHTS_METHODOLOGY"},
                {"type": "Benchmark", "title": "Scope 3 tracking : comparatif 8 plateformes 2025", "word_count": 4000, "pillar": "ESG_DATA_ANALYTICS"},
                {"type": "Étude de cas vidéo", "title": "Supply chain risk : comment Caelum détecte les incidents en temps réel", "word_count": 1200, "pillar": "CASE_STUDIES"},
                {"type": "Landing page ABM", "title": "CSDDD Compliance — Solutions pour ETI > 500M€", "word_count": 1000, "pillar": "CSDDD_COMPLIANCE"},
            ],
            "technical_actions": [
                "Déploiement schema Product sur pages solutions",
                "Optimisation CTA above-the-fold (test A/B sur taux de conversion)",
                "Mise en place remarketing SEO → SEA pour les visiteurs top pages",
            ],
            "expected_traffic_lift_pct": 47,
            "kpi_targets": {
                "organic_sessions": "+47% vs M0",
                "organic_leads_mql": "+25 MQL/mois organiques",
                "keywords_commercial": "+6 mots-clés COMMERCIAL en top 5",
            },
        },
        {
            "month_offset": 5,
            "focus_area": "Internationalisation & reach UE",
            "strategic_theme": "Étendre la visibilité aux marchés UE : Belgique, Allemagne, Pays-Bas",
            "target_keywords": [
                "CSDDD compliance 2027",
                "Lieferkettensorgfaltspflichtengesetz software",
                "corporate due diligence directive EU",
            ],
            "content_pieces": [
                {"type": "Guide EN", "title": "CSDDD Compliance Guide 2027 — Complete Implementation Roadmap", "word_count": 4500, "pillar": "CSDDD_COMPLIANCE"},
                {"type": "Article DE", "title": "LkSG und CSDDD : Vergleich und Anforderungen für Unternehmen", "word_count": 3000, "pillar": "REGULATORY_INTELLIGENCE"},
                {"type": "Article NL", "title": "CSDDD implementatie — gids voor Nederlandse bedrijven", "word_count": 2500, "pillar": "REGULATORY_INTELLIGENCE"},
                {"type": "Webinar replay", "title": "EU CSDDD Compliance — Cross-Border Panel (EN/FR/DE)", "word_count": 1000, "pillar": "HUMAN_RIGHTS_METHODOLOGY"},
            ],
            "technical_actions": [
                "Implémentation hreflang FR/EN/DE/NL",
                "Configuration sous-répertoires /en/ /de/ /nl/",
                "Soumission sitemaps localisés Google Search Console",
            ],
            "expected_traffic_lift_pct": 68,
            "kpi_targets": {
                "organic_sessions": "+68% vs M0 (dont +30% hors France)",
                "international_keywords": "+15 mots-clés EN/DE/NL en top 10",
                "international_leads": "+18 MQL internationaux/mois",
            },
        },
        {
            "month_offset": 6,
            "focus_area": "Consolidation & scale — leadership thématique",
            "strategic_theme": "Verrouiller les positions top 3 et maximiser le trafic organique qualifié",
            "target_keywords": [
                "conformité CSDDD 2027",
                "due diligence droits humains",
                "ESG reporting automation",
            ],
            "content_pieces": [
                {"type": "Rapport annuel", "title": "État de la conformité CSDDD en Europe — Rapport Caelum 2025", "word_count": 12000, "pillar": "REGULATORY_INTELLIGENCE"},
                {"type": "Série pilier étendu", "title": "10 articles cluster Droits Humains (mise à jour + extension)", "word_count": 25000, "pillar": "HUMAN_RIGHTS_METHODOLOGY"},
                {"type": "Case studies pack", "title": "6 études de cas clients — formats PDF + web + vidéo", "word_count": 9000, "pillar": "CASE_STUDIES"},
            ],
            "technical_actions": [
                "Audit SEO complet post-6-mois — identifier nouveaux gaps",
                "Refresh contenu pages M1-M2 (mise à jour données 2025)",
                "Configuration Content Decay alerts (Google Search Console)",
                "Review et renforcement maillage interne global",
            ],
            "expected_traffic_lift_pct": 95,
            "kpi_targets": {
                "organic_sessions": "+95% vs M0 (quasi-doublement trafic organique)",
                "keywords_top_3": "+12 mots-clés stratégiques en top 3",
                "organic_mrr_attributed": "Trafic organique = 35% du pipeline MQL total",
            },
        },
    ]

    # Enrichir avec dates réelles
    roadmap_months = []
    for template in roadmap_template[:months]:
        month_date = base_date + timedelta(days=30 * template["month_offset"])
        entry = dict(template)
        entry["month_label"] = month_date.strftime("%B %Y")
        entry["start_date"] = (base_date + timedelta(days=30 * (template["month_offset"] - 1))).strftime("%Y-%m-%d")
        entry["end_date"] = month_date.strftime("%Y-%m-%d")
        roadmap_months.append(entry)

    total_content_pieces = sum(len(m["content_pieces"]) for m in roadmap_months)
    final_traffic_lift = roadmap_months[-1]["expected_traffic_lift_pct"] if roadmap_months else 0

    return {
        "roadmap": roadmap_months,
        "summary": {
            "duration_months": months,
            "total_content_pieces": total_content_pieces,
            "final_traffic_lift_pct": final_traffic_lift,
            "strategy": "Content-led SEO avec autorité thématique CSDDD/ESG",
            "primary_objective": "Devenir la référence SEO n°1 sur la conformité CSDDD en France d'ici M6",
        },
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète de l'agent SEO Visibility Optimizer.

    Affiche les opportunités mots-clés, le score de santé SEO,
    un brief contenu exemple et la roadmap 6 mois.
    """
    print()
    print("=" * 70)
    print("🔍  CaelumSwarm™ — SEO Visibility Optimizer Agent")
    print("     Conformité CSDDD · ESG · Droits Humains B2B")
    print("=" * 70)
    print(f"     Analyse générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print()

    # ------------------------------------------------------------------
    # 1. ANALYSE D'OPPORTUNITÉS MOTS-CLÉS
    # ------------------------------------------------------------------
    print("━" * 70)
    print("📊  MODULE 1 — Analyse d'opportunités mots-clés")
    print("━" * 70)

    kw_analysis = analyze_keyword_opportunity(KEYWORD_UNIVERSE)
    summary = kw_analysis["summary"]

    print(f"\n  📌 {summary['total_keywords_analyzed']} mots-clés analysés")
    print(f"  ⚡ {summary['quick_wins_count']} quick wins identifiés (gains < 3 mois)")
    print(f"  🚀 Trafic potentiel mensuel cumulé : +{summary['total_traffic_potential_monthly']:,} visites/mois")
    print(f"  📈 Uplift estimé vs positions actuelles : +{summary['total_traffic_uplift_monthly']:,} visites/mois")
    print(f"  🏆 Mot-clé #1 opportunité : « {summary['top_keyword']} »")
    print()

    print("  TOP 5 OPPORTUNITÉS (score = volume × facilité × pertinence CSDDD)")
    print("  " + "-" * 66)
    header = f"  {'Mot-clé':<38} {'Score':>6}  {'Vol/m':>6}  {'Diff':>4}  {'Gap':>5}  {'QW':>3}"
    print(header)
    print("  " + "-" * 66)
    for opp in kw_analysis["opportunities"][:5]:
        qw_marker = "✅" if opp["quick_win"] else "  "
        gap_str = f"+{opp['rank_gap']}" if opp["rank_gap"] > 0 else str(opp["rank_gap"])
        print(
            f"  {opp['keyword']:<38} {opp['opportunity_score']:>6.3f}  "
            f"{opp['monthly_volume']:>6,}  {opp['difficulty']:>4}  "
            f"{gap_str:>5}  {qw_marker}"
        )
    print("  " + "-" * 66)
    print("  Gap = écart de rang (concurrent → cible) | QW = Quick Win")

    print("\n  ⚡ QUICK WINS PRIORITAIRES")
    for qw in kw_analysis["quick_wins"]:
        print(f"     → « {qw['keyword']} » : pos.{qw['competitor_rank']} → pos.{qw['target_rank']} "
              f"| +{qw['traffic_uplift_monthly']} visites/mois")

    # ------------------------------------------------------------------
    # 2. SCORE DE SANTÉ SEO
    # ------------------------------------------------------------------
    print()
    print("━" * 70)
    print("🏥  MODULE 2 — Score de santé SEO")
    print("━" * 70)

    health = calculate_seo_health_score(ON_PAGE_FACTORS, TECHNICAL_SEO_CHECKLIST)

    print(f"\n  🎯 SCORE GLOBAL    : {health['overall_score']:>5.1f} / 100  [{health['maturity_level']}]")
    print(f"     {health['maturity_label']}")
    print(f"\n  📄 Score On-Page   : {health['on_page_score']:>5.1f} / 100  (pondération 70%)")
    print(f"  🔧 Score Technique : {health['technical_score']:>5.1f} / 100  (pondération 30%)")
    print(f"  🔍 Facteurs SEO analysés : {health['score_breakdown']['factors_analyzed']}")

    print("\n  🚨 CORRECTIFS PRIORITAIRES (HIGH)")
    high_fixes = [f for f in health["priority_fixes"] if f["priority"] == "HIGH"]
    for fix in high_fixes[:5]:
        prefix = "❌" if fix.get("status") == "FAIL" else "⚠️ "
        label = fix["label"]
        action = fix.get("action", "")
        print(f"     {prefix} [{fix['type']}] {label}")
        if action:
            print(f"        → {action[:65]}")

    print("\n  📋 FACTEURS ON-PAGE (score actuel vs cible)")
    for key, factor in ON_PAGE_FACTORS.items():
        gap = factor["target_score"] - factor["current_score"]
        bar_filled = int(factor["current_score"] / 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        status_icon = "✅" if gap <= 10 else ("⚠️ " if gap <= 30 else "🔴")
        print(f"     {status_icon} {factor['label']:<40} [{bar}] {factor['current_score']:>3}/100 → {factor['target_score']}")

    # ------------------------------------------------------------------
    # 3. BRIEF CONTENU EXEMPLE
    # ------------------------------------------------------------------
    print()
    print("━" * 70)
    print("✍️   MODULE 3 — Génération de brief contenu")
    print("━" * 70)

    brief = generate_content_brief(
        keyword="due diligence droits humains",
        pillar="HUMAN_RIGHTS_METHODOLOGY",
        wave_number=62,
    )

    meta = brief["brief_metadata"]
    specs = brief["content_specs"]

    print(f"\n  🎯 Mot-clé cible  : « {meta['keyword_primary']} »")
    print(f"  📂 Pilier éditorial : {meta['pillar_label']}")
    print(f"  🎭 Intent          : {meta['intent']}")
    print(f"  📊 Volume mensuel  : {meta['monthly_volume']:,} recherches/mois")
    print(f"  💪 Difficulté KW   : {meta['keyword_difficulty']}/100")
    print()
    print(f"  📏 Nombre de mots cible : {specs['target_word_count']:,} mots")
    print(f"  ⏱️  Temps de lecture     : ~{specs['reading_time_minutes']} min")
    print(f"  🎨 Format              : {specs['content_format']}")
    print(f"  🗣️  Ton                 : {specs['tone']}")

    print("\n  💡 OPTIONS DE TITRES")
    for i, title in enumerate(brief["title_options"], 1):
        print(f"     {i}. {title}")

    print(f"\n  📝 META DESCRIPTION")
    md = brief["meta_description"]
    # Wrap meta description à 68 caractères
    words = md.split()
    lines = []
    current_line = "     "
    for word in words:
        if len(current_line) + len(word) + 1 > 72:
            lines.append(current_line)
            current_line = "     " + word
        else:
            current_line += (" " if current_line.strip() else "") + word
    if current_line.strip():
        lines.append(current_line)
    print("\n".join(lines))

    print("\n  🏗️  STRUCTURE H2/H3 SUGGÉRÉE")
    for header in brief["suggested_headers"][:6]:
        indent = "        " if header["level"] == "H3" else "     "
        marker = "▸" if header["level"] == "H3" else "▶"
        print(f"{indent}{marker} [{header['level']}] {header['text']}")
    if len(brief["suggested_headers"]) > 6:
        print(f"     ... + {len(brief['suggested_headers']) - 6} autres sections")

    print(f"\n  🔗 LIENS INTERNES SUGGÉRÉS ({len(brief['internal_links_suggested'])} liens)")
    for link in brief["internal_links_suggested"][:4]:
        print(f"     → Ancre : « {link['anchor']} »")
        print(f"       URL   : {link['url']}")

    cta = brief["cta_primary"]
    print(f"\n  🎯 CTA PRIMAIRE [{cta['type']}]")
    print(f"     Texte : « {cta['text']} »")
    print(f"     URL   : {cta['url']}")

    print("\n  👥 AUDIENCE CIBLE")
    audience = brief["audience"]
    print(f"     Persona 1° : {audience['primary_persona']}")
    print(f"     Persona 2° : {audience['secondary_persona']}")
    print("     Pain points clés :")
    for pain in audience["pain_points"][:2]:
        print(f"       • {pain}")

    # ------------------------------------------------------------------
    # 4. ROADMAP SEO 6 MOIS
    # ------------------------------------------------------------------
    print()
    print("━" * 70)
    print("🗓️   MODULE 4 — Roadmap SEO 6 mois")
    print("━" * 70)

    roadmap = generate_seo_roadmap(months=6)
    rsummary = roadmap["summary"]

    print(f"\n  🎯 Objectif : {rsummary['primary_objective']}")
    print(f"  📦 Contenus à produire : {rsummary['total_content_pieces']} pièces sur 6 mois")
    print(f"  🚀 Croissance trafic attendue : +{rsummary['final_traffic_lift_pct']}% vs aujourd'hui")
    print()

    for month in roadmap["roadmap"]:
        lift = month["expected_traffic_lift_pct"]
        bar_filled = int(lift / 10)
        bar_filled = min(bar_filled, 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)

        print(f"  📅 MOIS {month['month_offset']} — {month['month_label'].upper()}")
        print(f"     Focus : {month['focus_area']}")
        print(f"     Trafic lift cumulatif : +{lift}%  [{bar}]")
        print(f"     Mots-clés cibles :")
        for kw in month["target_keywords"]:
            print(f"       • {kw}")
        print(f"     Contenus à créer ({len(month['content_pieces'])} pièces) :")
        for piece in month["content_pieces"][:2]:
            print(f"       📄 [{piece['type']}] {piece['title'][:55]}")
        if len(month["content_pieces"]) > 2:
            print(f"       ... + {len(month['content_pieces']) - 2} autre(s)")
        kpis = month["kpi_targets"]
        print(f"     KPIs M{month['month_offset']} :")
        for kpi_key, kpi_val in list(kpis.items())[:2]:
            print(f"       ✓ {kpi_key.replace('_', ' ').title()} : {kpi_val}")
        print()

    # ------------------------------------------------------------------
    # SYNTHÈSE FINALE
    # ------------------------------------------------------------------
    print("━" * 70)
    print("✅  SYNTHÈSE EXÉCUTIVE — CaelumSwarm™ SEO Intelligence")
    print("━" * 70)
    print()
    print("  ÉTAT ACTUEL")
    print(f"    Score SEO global          : {health['overall_score']}/100 ({health['maturity_level']})")
    print(f"    Mots-clés analysés        : {summary['total_keywords_analyzed']}")
    print(f"    Quick wins disponibles    : {summary['quick_wins_count']}")
    print()
    print("  POTENTIEL 6 MOIS")
    print(f"    Croissance trafic organique : +{rsummary['final_traffic_lift_pct']}%")
    print(f"    Contenus à produire         : {rsummary['total_content_pieces']} pièces")
    print(f"    Trafic additionnel/mois     : +{summary['total_traffic_uplift_monthly']:,} visites")
    print()
    print("  ACTIONS IMMÉDIATES (< 30 jours)")
    for fix in health["quick_score_lifts"][:3]:
        print(f"    🔴 {fix['label']}")
    print()
    print("  MOTS-CLÉS QUICK WIN (< 3 mois)")
    for qw in kw_analysis["quick_wins"][:3]:
        print(f"    ⚡ « {qw['keyword']} » → pos.{qw['competitor_rank']} → pos.{qw['target_rank']} "
              f"| +{qw['traffic_uplift_monthly']} visites/mois")
    print()
    print("=" * 70)
    print("  CaelumSwarm™ SEO Optimizer — Rapport généré avec succès ✅")
    print("=" * 70)
    print()

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
