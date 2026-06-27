"""
Social content planner for CaelumSwarm™ — plans, schedules and optimizes
social media content for CSDDD thought leadership.

Caelum Partners — CaelumSwarm™ Intelligence Layer
Agent: Social Content Planner
Version: 1.0.0
Audience: B2B — Directeurs RSE, Compliance Officers, Investisseurs ESG
Focus: CSDDD / CSRD / Droits humains dans les chaînes d'approvisionnement
"""

import math
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

SOCIAL_PLATFORMS = {
    "LINKEDIN": {
        "label": "LinkedIn",
        "audience_size_est": 12_500,
        "best_content_types": ["WAVE_INSIGHT", "REGULATORY_UPDATE", "CASE_STUDY", "EXPERT_OPINION", "DATA_VISUALIZATION"],
        "optimal_post_times": ["08:00", "12:00", "17:30"],
        "char_limit": 3000,
        "caelum_priority": "PRIMAIRE",
        "engagement_rate_avg": 0.042,
    },
    "TWITTER_X": {
        "label": "X (Twitter)",
        "audience_size_est": 6_800,
        "best_content_types": ["INDUSTRY_NEWS", "REGULATORY_UPDATE", "EXPERT_OPINION"],
        "optimal_post_times": ["07:30", "12:30", "18:00", "21:00"],
        "char_limit": 280,
        "caelum_priority": "SECONDAIRE",
        "engagement_rate_avg": 0.018,
    },
    "INSTAGRAM": {
        "label": "Instagram",
        "audience_size_est": 4_200,
        "best_content_types": ["DATA_VISUALIZATION", "HOW_TO_GUIDE", "BEHIND_SCENES"],
        "optimal_post_times": ["10:00", "13:00", "19:00"],
        "char_limit": 2200,
        "caelum_priority": "TERTIAIRE",
        "engagement_rate_avg": 0.031,
    },
    "YOUTUBE": {
        "label": "YouTube",
        "audience_size_est": 2_100,
        "best_content_types": ["HOW_TO_GUIDE", "CASE_STUDY", "EXPERT_OPINION", "BEHIND_SCENES"],
        "optimal_post_times": ["15:00", "18:00"],
        "duration_limit": 1800,  # seconds (30 min)
        "caelum_priority": "SECONDAIRE",
        "engagement_rate_avg": 0.055,
    },
    "PODCAST": {
        "label": "Podcast CaelumCast",
        "audience_size_est": 1_400,
        "best_content_types": ["EXPERT_OPINION", "CASE_STUDY", "REGULATORY_UPDATE"],
        "optimal_post_times": ["06:00", "12:00"],
        "duration_limit": 3600,  # seconds (60 min)
        "caelum_priority": "SECONDAIRE",
        "engagement_rate_avg": 0.068,
    },
}

CONTENT_TYPES = {
    "WAVE_INSIGHT": {
        "label": "Wave Insight",
        "avg_engagement_multiplier": 1.8,
        "production_time_hours": 2.5,
        "repurpose_potential": "HIGH",
    },
    "REGULATORY_UPDATE": {
        "label": "Mise à jour réglementaire",
        "avg_engagement_multiplier": 1.6,
        "production_time_hours": 1.5,
        "repurpose_potential": "HIGH",
    },
    "CASE_STUDY": {
        "label": "Étude de cas",
        "avg_engagement_multiplier": 2.1,
        "production_time_hours": 5.0,
        "repurpose_potential": "HIGH",
    },
    "EXPERT_OPINION": {
        "label": "Opinion d'expert",
        "avg_engagement_multiplier": 1.7,
        "production_time_hours": 1.0,
        "repurpose_potential": "MEDIUM",
    },
    "DATA_VISUALIZATION": {
        "label": "Visualisation de données",
        "avg_engagement_multiplier": 2.4,
        "production_time_hours": 3.0,
        "repurpose_potential": "HIGH",
    },
    "HOW_TO_GUIDE": {
        "label": "Guide pratique",
        "avg_engagement_multiplier": 1.9,
        "production_time_hours": 4.0,
        "repurpose_potential": "HIGH",
    },
    "INDUSTRY_NEWS": {
        "label": "Actualité sectorielle",
        "avg_engagement_multiplier": 1.3,
        "production_time_hours": 0.5,
        "repurpose_potential": "LOW",
    },
    "BEHIND_SCENES": {
        "label": "Coulisses",
        "avg_engagement_multiplier": 1.4,
        "production_time_hours": 1.0,
        "repurpose_potential": "MEDIUM",
    },
}

CONTENT_CALENDAR_THEMES = {
    1:  {
        "month": "Janvier",
        "theme": "Bilan RSE annuel",
        "description": "Revue des performances ESG de l'année écoulée, objectifs CSDDD pour l'année",
        "key_dates": ["Publication rapports RSE", "Réunions CA sur gouvernance ESG"],
        "csddd_angle": "Cartographie initiale des risques droits humains en chaîne d'approvisionnement",
    },
    2:  {
        "month": "Février",
        "theme": "Diligence raisonnable : les fondamentaux",
        "description": "Pédagogie sur la due diligence, comparaison LDD France vs CSDDD UE",
        "key_dates": ["Forum ESG Paris", "Rapport OCDE diligence raisonnable"],
        "csddd_angle": "Obligations de diligence raisonnable — qui est concerné et quand",
    },
    3:  {
        "month": "Mars",
        "theme": "Droits humains & genre",
        "description": "Journée internationale des droits des femmes — focus travailleuses dans les chaînes",
        "key_dates": ["8 mars — Journée internationale des droits des femmes", "Rapport OIT travail décent"],
        "csddd_angle": "Indicateurs de genre dans les audits fournisseurs CSDDD",
    },
    4:  {
        "month": "Avril",
        "theme": "CSRD rapport & CSDDD articulation",
        "description": "Saison des rapports CSRD : liens avec CSDDD, double matérialité",
        "key_dates": ["Deadline rapports CSRD vague 1", "Publication normes EFRAG"],
        "csddd_angle": "Comment les données CSRD alimentent le plan d'action CSDDD",
    },
    5:  {
        "month": "Mai",
        "theme": "Minéraux de conflit & ressources naturelles",
        "description": "Focus sur les chaînes d'approvisionnement minières et extraction responsable",
        "key_dates": ["Forum minier international", "Rapport Responsible Minerals Initiative"],
        "csddd_angle": "Traçabilité des minéraux critiques sous CSDDD",
    },
    6:  {
        "month": "Juin",
        "theme": "Climat & transition juste",
        "description": "Intersections CSDDD et réglementation climatique, TCFD, Net Zero",
        "key_dates": ["Semaine du Développement Durable", "Publication CDP scores"],
        "csddd_angle": "Plans de transition climatique comme obligation CSDDD article 22",
    },
    7:  {
        "month": "Juillet",
        "theme": "CSDDD deadline awareness",
        "description": "Compte à rebours vers les premières échéances CSDDD — état de préparation",
        "key_dates": ["Transposition CSDDD dans les États membres", "Audit mi-année fournisseurs"],
        "csddd_angle": "Roadmap de mise en conformité — qui doit faire quoi et pour quand",
    },
    8:  {
        "month": "Août",
        "theme": "Travail forcé & migrations",
        "description": "Focus travailleurs migrants, travail forcé, Règlement UE travail forcé",
        "key_dates": ["Rapport ITUC Global Rights Index", "Conférence OIT"],
        "csddd_angle": "Détection du travail forcé dans les chaînes d'approvisionnement complexes",
    },
    9:  {
        "month": "Septembre",
        "theme": "Tech & conformité intelligente",
        "description": "IA et outils digitaux pour accélérer la due diligence",
        "key_dates": ["Forum IA responsable", "Lancement outils RegTech ESG"],
        "csddd_angle": "CaelumSwarm™ : l'IA au service de la cartographie des risques CSDDD",
    },
    10: {
        "month": "Octobre",
        "theme": "Chaînes d'approvisionnement & résilience",
        "description": "Résilience et diversification des fournisseurs, gestion des risques systémiques",
        "key_dates": ["Forum Supply Chain Responsable", "Publication Indice Fraser Institute"],
        "csddd_angle": "Segmentation fournisseurs par niveau de risque CSDDD",
    },
    11: {
        "month": "Novembre",
        "theme": "Investisseurs & due diligence ESG",
        "description": "Perspective investisseurs : notation ESG, engagement actionnarial et CSDDD",
        "key_dates": ["COP Finance", "Publication ratings ESG majeurs"],
        "csddd_angle": "Impact CSDDD sur les décisions d'investissement et le coût du capital",
    },
    12: {
        "month": "Décembre",
        "theme": "Bilan & prospective 2027",
        "description": "Récapitulatif de l'année réglementaire, projection vers les échéances 2027",
        "key_dates": ["Bilan Conseil Européen", "Conférence annuelle RSE"],
        "csddd_angle": "Préparer 2027 : les grandes entreprises sous CSDDD — check-list finale",
    },
}

HASHTAG_CLUSTERS = {
    "CSDDD_CORE": {
        "hashtags": [
            "#CSDDD",
            "#ChaineApprovisionnement",
            "#DiligenceRaisonnable",
            "#DroitsHumains",
            "#ConformiteESG",
            "#CSRD",
        ],
        "avg_reach_multiplier": 2.3,
    },
    "ESG_FINANCE": {
        "hashtags": [
            "#ESG",
            "#FinanceDurable",
            "#InvestissementResponsable",
            "#NotationESG",
            "#DoubleMatérialité",
            "#SFDR",
            "#TaxonomieVerte",
        ],
        "avg_reach_multiplier": 2.8,
    },
    "HUMAN_RIGHTS": {
        "hashtags": [
            "#DroitsHumains",
            "#BusinessAndHumanRights",
            "#TravailDecent",
            "#PrincipesDirecteursONU",
            "#ResponsabilitéEntreprises",
        ],
        "avg_reach_multiplier": 1.9,
    },
    "TECH_COMPLIANCE": {
        "hashtags": [
            "#RegTech",
            "#ComplianceIA",
            "#DigitalESG",
            "#CaelumSwarm",
            "#AutomationRSE",
            "#LegalTech",
        ],
        "avg_reach_multiplier": 2.1,
    },
    "SUSTAINABILITY": {
        "hashtags": [
            "#Durabilité",
            "#Sustainability",
            "#NetZero",
            "#TransitionJuste",
            "#RSE",
            "#ImpactPositif",
            "#GreenBusiness",
        ],
        "avg_reach_multiplier": 2.5,
    },
}

# ---------------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------------

_WEEKLY_PLAN = [
    # (platform, content_type, topic_template, hashtag_cluster, visual_suggestion)
    (
        "LINKEDIN",
        "WAVE_INSIGHT",
        "Analyse CaelumSwarm™ Wave {wave} : focus {domain1}",
        "CSDDD_CORE",
        "Infographie dark-mode — score composite + distribution 4/2/1/1 sur fond bleu nuit Caelum",
    ),
    (
        "TWITTER_X",
        "REGULATORY_UPDATE",
        "Veille réglementaire CSDDD — implications {domain2} pour vos fournisseurs",
        "CSDDD_CORE",
        "Visuel carré 1080×1080 — alerte réglementaire, icône balance de justice",
    ),
    (
        "LINKEDIN",
        "DATA_VISUALIZATION",
        "Cartographie des risques {domain1} & {domain2} : que dit notre indice ?",
        "ESG_FINANCE",
        "Carte mondiale choroplèthe — gradient rouge/orange/vert selon score risque pays",
    ),
    (
        "INSTAGRAM",
        "HOW_TO_GUIDE",
        "5 étapes pour auditer vos fournisseurs sur {domain3}",
        "SUSTAINABILITY",
        "Carrousel 5 slides — design minimaliste, icônes linéaires blanc sur fond Caelum",
    ),
    (
        "LINKEDIN",
        "EXPERT_OPINION",
        "Opinion : {domain1} comme nouveau critère de sélection fournisseurs post-CSDDD",
        "HUMAN_RIGHTS",
        "Portrait photo équipe + citation pull-quote en overlay typographique",
    ),
]

_DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

_SERIES_STRUCTURES = {
    4: [
        ("Épisode 1 — Les fondamentaux", "Comprendre les enjeux de base"),
        ("Épisode 2 — Les acteurs clés",  "Qui fait quoi dans l'écosystème"),
        ("Épisode 3 — Les outils",        "Méthodes et frameworks pratiques"),
        ("Épisode 4 — Passage à l'action","Roadmap concrète pour votre organisation"),
    ],
    5: [
        ("Épisode 1 — Panorama",          "Vue d'ensemble et enjeux stratégiques"),
        ("Épisode 2 — Réglementation",    "Ce que la loi impose réellement"),
        ("Épisode 3 — Bonnes pratiques",  "Ce que font les leaders du secteur"),
        ("Épisode 4 — Erreurs à éviter",  "Les pièges courants et comment les contourner"),
        ("Épisode 5 — Feuille de route",  "Plan d'action 90 jours"),
    ],
    6: [
        ("Épisode 1 — Contexte",          "Pourquoi ce sujet est devenu incontournable"),
        ("Épisode 2 — Cadre légal",       "CSDDD, CSRD et directives associées"),
        ("Épisode 3 — Risques",           "Identifier et hiérarchiser les risques"),
        ("Épisode 4 — Solutions",         "Technologies et méthodologies disponibles"),
        ("Épisode 5 — Cas concrets",      "Retours d'expérience terrain"),
        ("Épisode 6 — Perspectives",      "Ce qui nous attend en 2027 et au-delà"),
    ],
}


def _clamp_text(text: str, max_chars: int) -> str:
    """Truncate text to max_chars, appending ellipsis if needed."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


# ---------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------------------------

def generate_weekly_calendar(week_number: int, wave_number: int, wave_domains: list) -> dict:
    """
    Creates a 5-day content calendar (Mon–Fri) for a given wave.

    Parameters
    ----------
    week_number  : ISO week number (1–52)
    wave_number  : CaelumSwarm™ wave index
    wave_domains : list of domain labels covered by this wave (at least 3)

    Returns
    -------
    dict with keys: week_number, wave_number, wave_domains, days (list of 5 day dicts)
    """
    if len(wave_domains) < 3:
        wave_domains = (wave_domains + ["Domaine A", "Domaine B", "Domaine C"])[:3]

    domain1, domain2, domain3 = wave_domains[0], wave_domains[1], wave_domains[2]

    calendar_days = []
    for idx, day_name in enumerate(_DAYS):
        platform_key, content_type_key, topic_tpl, hashtag_cluster_key, visual = _WEEKLY_PLAN[idx]
        platform = SOCIAL_PLATFORMS[platform_key]
        content_type = CONTENT_TYPES[content_type_key]
        cluster = HASHTAG_CLUSTERS[hashtag_cluster_key]

        topic = topic_tpl.format(wave=wave_number, domain1=domain1, domain2=domain2, domain3=domain3)

        caption_template = (
            f"[HOOK] Saviez-vous que {domain1} figure parmi les domaines à risque critique "
            f"dans notre Wave {wave_number} ?\n\n"
            f"[BODY] Notre indice CaelumSwarm™ analyse {topic}.\n\n"
            f"[CTA] Téléchargez le rapport complet → lien en commentaire\n\n"
            + " ".join(cluster["hashtags"])
        )

        best_time = platform["optimal_post_times"][0]

        estimated_reach = int(
            platform["audience_size_est"]
            * platform["engagement_rate_avg"]
            * content_type["avg_engagement_multiplier"]
            * cluster["avg_reach_multiplier"]
        )

        calendar_days.append({
            "day": day_name,
            "platform": platform["label"],
            "content_type": content_type["label"],
            "topic": topic,
            "caption_template": caption_template,
            "hashtag_cluster": hashtag_cluster_key,
            "hashtags": cluster["hashtags"],
            "visual_suggestion": visual,
            "best_time_to_post": best_time,
            "estimated_reach": estimated_reach,
        })

    return {
        "week_number": week_number,
        "wave_number": wave_number,
        "wave_domains": wave_domains,
        "days": calendar_days,
    }


def create_content_series(theme: str, episodes: int = 4) -> dict:
    """
    Creates a multi-episode content series plan.

    Parameters
    ----------
    theme    : high-level topic (e.g. "CSDDD en 4 étapes")
    episodes : number of episodes (4, 5, or 6; defaults to 4)

    Returns
    -------
    dict with keys: theme, episodes, platform_recommendation, episode_plan
    """
    if episodes not in _SERIES_STRUCTURES:
        episodes = min(_SERIES_STRUCTURES.keys(), key=lambda k: abs(k - episodes))

    structure = _SERIES_STRUCTURES[episodes]

    episode_plan = []
    for i, (title_tpl, key_message) in enumerate(structure, start=1):
        hook_line = (
            f"🧵 [{i}/{episodes}] {theme} — "
            + [
                "Commençons par les bases : pourquoi ce sujet ne peut plus attendre.",
                "Maintenant que les bases sont posées, voyons qui sont les acteurs.",
                "Place aux outils concrets — voici ce qui fonctionne vraiment.",
                "Le moment d'agir : voici votre feuille de route.",
                "Bilan et perspectives — où en sommes-nous vraiment ?",
                "Passons à l'action ensemble — voici la suite.",
            ][min(i - 1, 5)]
        )

        cta = (
            "💬 Partagez votre expérience en commentaire"
            if i < episodes
            else "📥 Téléchargez la synthèse complète — lien en bio"
        )

        episode_plan.append({
            "episode_number": i,
            "title": title_tpl,
            "key_message": key_message,
            "hook_line": hook_line,
            "cta": cta,
            "recommended_format": "Carrousel LinkedIn" if i % 2 == 0 else "Post texte long LinkedIn",
            "hashtag_cluster": "CSDDD_CORE",
        })

    return {
        "theme": theme,
        "total_episodes": episodes,
        "platform_recommendation": "LinkedIn (publication tous les 3 jours)",
        "estimated_series_duration_days": episodes * 3,
        "episode_plan": episode_plan,
    }


def calculate_content_roi(posts_per_week: int, avg_engagement_rate: float, follower_count: int) -> dict:
    """
    Projects monthly content marketing ROI metrics.

    Parameters
    ----------
    posts_per_week     : number of posts published per week
    avg_engagement_rate: decimal (e.g. 0.042 for 4.2%)
    follower_count     : current total followers across primary platform

    Returns
    -------
    dict with monthly projections and brand_awareness_score
    """
    posts_per_month = posts_per_week * 4

    monthly_reach = int(follower_count * (1 + avg_engagement_rate * 10) * posts_per_month * 0.15)

    total_engagements = int(monthly_reach * avg_engagement_rate)

    leads_generated = int(total_engagements * 0.02)

    brand_awareness_score = round(
        min(100.0, (
            math.log1p(monthly_reach) * 2.5
            + avg_engagement_rate * 1000
            + posts_per_month * 1.5
        ) / 10),
        1,
    )

    cost_per_lead_equivalent = round(2500 / max(leads_generated, 1), 0)  # baseline agency cost

    return {
        "inputs": {
            "posts_per_week": posts_per_week,
            "avg_engagement_rate": f"{avg_engagement_rate * 100:.1f}%",
            "follower_count": follower_count,
        },
        "monthly_projections": {
            "posts_published": posts_per_month,
            "monthly_reach": monthly_reach,
            "total_engagements": total_engagements,
            "leads_generated": leads_generated,
            "brand_awareness_score": brand_awareness_score,
            "cost_per_lead_equivalent_eur": int(cost_per_lead_equivalent),
        },
        "interpretation": {
            "reach_tier": (
                "Excellente portée" if monthly_reach > 50_000
                else "Bonne portée" if monthly_reach > 20_000
                else "Portée en développement"
            ),
            "engagement_tier": (
                "Communauté très engagée" if avg_engagement_rate >= 0.05
                else "Engagement dans la norme B2B" if avg_engagement_rate >= 0.02
                else "Engagement à optimiser"
            ),
            "lead_quality": "Leads qualifiés CSDDD/ESG — forte intention d'achat estimée",
        },
    }


def generate_post_caption(content_type: str, wave: int, domain: str, key_stat: str) -> dict:
    """
    Generates a ready-to-publish LinkedIn caption.

    Parameters
    ----------
    content_type : key from CONTENT_TYPES
    wave         : wave number
    domain       : domain label (e.g. "minéraux de conflit")
    key_stat     : a striking statistic or data point

    Returns
    -------
    dict with hook, body, cta, hashtags, full_caption (≤1300 chars), char_count
    """
    ct_label = CONTENT_TYPES.get(content_type, {}).get("label", content_type)

    hooks = {
        "WAVE_INSIGHT": f"📊 Notre indice CaelumSwarm™ Wave {wave} révèle une réalité préoccupante sur {domain}.",
        "REGULATORY_UPDATE": f"⚖️ Alerte réglementaire : ce que la CSDDD implique concrètement pour {domain}.",
        "CASE_STUDY": f"🔍 Étude de cas : comment une ETI a transformé ses risques {domain} en avantage compétitif.",
        "EXPERT_OPINION": f"💡 Mon analyse : {domain} sera le terrain de jeu de la conformité CSDDD d'ici 2027.",
        "DATA_VISUALIZATION": f"📈 Les chiffres parlent d'eux-mêmes : {key_stat} — voici ce que ça signifie pour {domain}.",
        "HOW_TO_GUIDE": f"🗺️ Guide pratique : 5 étapes pour maîtriser vos risques {domain} avant l'échéance CSDDD.",
        "INDUSTRY_NEWS": f"🗞️ L'actualité {domain} que vous ne pouvez pas manquer cette semaine.",
        "BEHIND_SCENES": f"🎬 Dans les coulisses de CaelumSwarm™ : comment nous analysons {domain} à grande échelle.",
    }

    hook = hooks.get(content_type, f"📌 Focus Wave {wave} : {domain} sous l'angle CSDDD.")

    body = (
        f"Notre analyse Wave {wave} place {domain} parmi les domaines nécessitant une attention immédiate "
        f"dans vos chaînes d'approvisionnement.\n\n"
        f"🔑 Donnée clé : {key_stat}\n\n"
        f"Ce que cela signifie pour votre organisation :\n"
        f"→ Vos fournisseurs de rang 2 et 3 sont exposés\n"
        f"→ La due diligence documentée devient obligatoire sous CSDDD article 8\n"
        f"→ Les investisseurs ESG scrutent désormais ces indicateurs dans leurs grilles de notation\n\n"
        f"Chez Caelum Partners, nous avons développé une méthodologie en 4 niveaux de risque "
        f"(critique / élevé / modéré / faible) qui permet à vos équipes compliance de prioriser "
        f"leurs audits fournisseurs avec précision."
    )

    cta = (
        f"📥 Accédez au rapport complet Wave {wave} — lien en premier commentaire.\n"
        f"💬 Et vous, comment votre organisation aborde-t-elle {domain} dans sa cartographie CSDDD ?"
    )

    hashtags_list = (
        HASHTAG_CLUSTERS["CSDDD_CORE"]["hashtags"][:4]
        + HASHTAG_CLUSTERS["ESG_FINANCE"]["hashtags"][:2]
    )
    hashtags_str = " ".join(hashtags_list)

    full_caption = f"{hook}\n\n{body}\n\n{cta}\n\n{hashtags_str}"

    # Enforce 1300-char LinkedIn best-practice limit (not hard limit, but optimal)
    full_caption = _clamp_text(full_caption, 1300)

    return {
        "content_type": ct_label,
        "wave": wave,
        "domain": domain,
        "hook": hook,
        "body": body,
        "cta": cta,
        "hashtags": hashtags_list,
        "full_caption": full_caption,
        "char_count": len(full_caption),
        "platform": "LinkedIn",
        "ready_to_publish": len(full_caption) <= 3000,
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """Demonstrates the social content planner with Wave 194 — conflict minerals."""

    sep = "=" * 70

    print(f"\n{sep}")
    print("  🌐  CaelumSwarm™ — Social Content Planner Agent")
    print(f"  📅  Démo du {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(sep)

    # ------------------------------------------------------------------
    # 1. Weekly calendar
    # ------------------------------------------------------------------
    print("\n📆  CALENDRIER HEBDOMADAIRE — Wave 194 (semaine 25)\n")
    calendar = generate_weekly_calendar(
        week_number=25,
        wave_number=194,
        wave_domains=["minéraux de conflit", "exploitation minière artisanale", "traçabilité OCDE"],
    )

    for day in calendar["days"]:
        print(f"  📌 {day['day'].upper()} — {day['platform']} | {day['content_type']}")
        print(f"     🎯 Sujet   : {day['topic']}")
        print(f"     ⏰ Heure   : {day['best_time_to_post']}")
        print(f"     👁️  Reach   : ~{day['estimated_reach']:,} personnes")
        print(f"     🖼️  Visuel  : {day['visual_suggestion'][:80]}...")
        print()

    # ------------------------------------------------------------------
    # 2. Content series
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n📚  SÉRIE DE CONTENU — \"CSDDD & Minéraux de Conflit en 4 Épisodes\"\n")
    series = create_content_series(
        theme="CSDDD & Minéraux de Conflit",
        episodes=4,
    )

    print(f"  🎙️  Thème    : {series['theme']}")
    print(f"  📡  Plateforme : {series['platform_recommendation']}")
    print(f"  ⏳  Durée série : {series['estimated_series_duration_days']} jours\n")

    for ep in series["episode_plan"]:
        print(f"  ▶️  {ep['title']}")
        print(f"     💡 Message clé : {ep['key_message']}")
        print(f"     🪝 Hook        : {ep['hook_line']}")
        print(f"     📢 CTA         : {ep['cta']}")
        print(f"     🎨 Format      : {ep['recommended_format']}")
        print()

    # ------------------------------------------------------------------
    # 3. ROI calculation
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n💹  PROJECTION ROI MENSUEL\n")
    roi = calculate_content_roi(
        posts_per_week=5,
        avg_engagement_rate=0.042,
        follower_count=12_500,
    )

    inputs = roi["inputs"]
    proj = roi["monthly_projections"]
    interp = roi["interpretation"]

    print(f"  📥  Paramètres d'entrée")
    print(f"     Posts/semaine       : {inputs['posts_per_week']}")
    print(f"     Taux d'engagement   : {inputs['avg_engagement_rate']}")
    print(f"     Abonnés (LinkedIn)  : {inputs['follower_count']:,}\n")

    print(f"  📊  Projections mensuelles")
    print(f"     Posts publiés       : {proj['posts_published']}")
    print(f"     Portée mensuelle    : {proj['monthly_reach']:,} personnes")
    print(f"     Engagements totaux  : {proj['total_engagements']:,}")
    print(f"     Leads générés       : {proj['leads_generated']}")
    print(f"     Score notoriété     : {proj['brand_awareness_score']} / 100")
    print(f"     Coût/lead équiv.    : {proj['cost_per_lead_equivalent_eur']} €\n")

    print(f"  📌  Interprétation")
    print(f"     Portée     : {interp['reach_tier']}")
    print(f"     Engagement : {interp['engagement_tier']}")
    print(f"     Qualité    : {interp['lead_quality']}")

    # ------------------------------------------------------------------
    # 4. Sample LinkedIn post
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n✍️   POST LINKEDIN PRÊT À PUBLIER — Wave 194 : Minéraux de Conflit\n")
    post = generate_post_caption(
        content_type="WAVE_INSIGHT",
        wave=194,
        domain="minéraux de conflit",
        key_stat="73 % des entreprises européennes n'ont aucune visibilité au-delà du rang 1 fournisseur",
    )

    print(f"  📋  Type de contenu : {post['content_type']} | Plateforme : {post['platform']}")
    print(f"  📏  Caractères      : {post['char_count']} / 1300 (best practice)\n")
    print("  " + "-" * 60)
    print()
    for line in post["full_caption"].split("\n"):
        print(f"  {line}")
    print()
    print("  " + "-" * 60)
    print(f"\n  ✅  Prêt à publier : {'Oui' if post['ready_to_publish'] else 'Non — révision requise'}")
    print(f"  🏷️   Hashtags : {' '.join(post['hashtags'])}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n✅  Démo terminée — CaelumSwarm™ Social Content Planner Agent opérationnel.\n")
    print(f"  Plateformes couvertes  : {len(SOCIAL_PLATFORMS)}")
    print(f"  Types de contenu       : {len(CONTENT_TYPES)}")
    print(f"  Thèmes calendrier      : {len(CONTENT_CALENDAR_THEMES)} mois")
    print(f"  Clusters de hashtags   : {len(HASHTAG_CLUSTERS)}")
    print(f"\n{sep}\n")

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    exit(0 if success else 1)
