#!/usr/bin/env python3
"""
Agent Fidélisation Clients — analyse la rétention, identifie les risques de churn,
conçoit des programmes de fidélisation et maximise la LTV des clients CaelumSwarm™.

CaelumSwarm™ Customer Loyalty & Retention Agent v1.0
Caelum Partners — Intelligence Stratégique des Droits Humains & CSDDD Compliance

Métriques cibles B2B SaaS :
  - NRR (Net Revenue Retention) > 110%
  - Churn annuel < 5%
  - LTV/CAC ratio > 3x
  - Payback period < 18 mois
"""

import json
import sys
from datetime import date, datetime, timezone


# ---------------------------------------------------------------------------
# 1. CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

CHURN_RISK_SIGNALS = {
    "LOW_ENGAGEMENT": {
        "label": "Faible engagement produit",
        "weight": 0.20,
        "detection_method": "Sessions < 2/semaine ou < 5 waves consultées/mois",
        "days_to_churn_avg": 120,
        "recovery_rate_pct": 68,
    },
    "SUPPORT_TICKET_SPIKE": {
        "label": "Pic de tickets support",
        "weight": 0.15,
        "detection_method": "> 3 tickets en 30 jours ou sentiment négatif détecté dans les échanges",
        "days_to_churn_avg": 90,
        "recovery_rate_pct": 72,
    },
    "REDUCED_WAVE_USAGE": {
        "label": "Réduction de l'usage des waves",
        "weight": 0.18,
        "detection_method": "Baisse > 30% du nombre de waves actives vs. trimestre précédent",
        "days_to_churn_avg": 100,
        "recovery_rate_pct": 65,
    },
    "PAYMENT_DELAY": {
        "label": "Retard de paiement",
        "weight": 0.14,
        "detection_method": "Facture impayée > 15 jours après échéance ou demande de délai",
        "days_to_churn_avg": 60,
        "recovery_rate_pct": 55,
    },
    "COMPETITOR_MENTION": {
        "label": "Mention d'un concurrent",
        "weight": 0.12,
        "detection_method": "Nom d'un concurrent évoqué dans un ticket, email ou appel CS enregistré",
        "days_to_churn_avg": 75,
        "recovery_rate_pct": 48,
    },
    "NO_EXPANSION": {
        "label": "Absence d'expansion",
        "weight": 0.10,
        "detection_method": "Aucune discussion upsell acceptée en 12 mois sur un compte éligible",
        "days_to_churn_avg": 180,
        "recovery_rate_pct": 60,
    },
    "CHAMPION_LEFT": {
        "label": "Départ du champion interne",
        "weight": 0.06,
        "detection_method": "Contact principal identifié comme quittant l'entreprise (LinkedIn, signalement)",
        "days_to_churn_avg": 90,
        "recovery_rate_pct": 50,
    },
    "LOW_NPS": {
        "label": "NPS faible (score ≤ 6)",
        "weight": 0.05,
        "detection_method": "Réponse NPS ≤ 6 lors de la dernière enquête trimestrielle",
        "days_to_churn_avg": 150,
        "recovery_rate_pct": 62,
    },
}

LOYALTY_TIERS = {
    "BRONZE": {
        "label": "Bronze — Nouveaux clients",
        "tenure_months_range": (0, 6),
        "perks": [
            "Onboarding personnalisé (4 sessions)",
            "Accès à la base documentaire CaelumSwarm™",
            "Webinaires mensuels de formation",
            "Support standard (email, 48h SLA)",
            "Newsletter CSDDD exclusive bi-mensuelle",
        ],
        "dedicated_support": False,
        "custom_waves_per_year": 0,
        "price_lock_years": 1,
        "executive_access": False,
        "churn_rate_pct": 12.0,
    },
    "SILVER": {
        "label": "Silver — Clients établis",
        "tenure_months_range": (6, 18),
        "perks": [
            "Customer Success Manager dédié",
            "Business Review trimestrielle",
            "Accès anticipé aux nouvelles waves",
            "Support prioritaire (chat + email, 24h SLA)",
            "1 formation avancée CSDDD/an offerte",
            "Invitation aux événements Caelum Partners",
        ],
        "dedicated_support": True,
        "custom_waves_per_year": 1,
        "price_lock_years": 2,
        "executive_access": False,
        "churn_rate_pct": 6.5,
    },
    "GOLD": {
        "label": "Gold — Clients stratégiques",
        "tenure_months_range": (18, 36),
        "perks": [
            "Customer Success Manager senior dédié",
            "Business Review mensuelle + QBR exécutive",
            "Co-développement de 2 waves personnalisées/an",
            "Support 24/7 avec escalade directe (4h SLA critique)",
            "Accès bêta aux fonctionnalités en développement",
            "Certification CaelumSwarm™ pour l'équipe client (5 sièges)",
            "Mention partenaire sur site Caelum + co-communication",
            "Participation au Customer Advisory Board",
        ],
        "dedicated_support": True,
        "custom_waves_per_year": 2,
        "price_lock_years": 3,
        "executive_access": False,
        "churn_rate_pct": 3.5,
    },
    "PLATINUM": {
        "label": "Platinum — Partenaires long terme",
        "tenure_months_range": (36, 999),
        "perks": [
            "Équipe dédiée Caelum Partners (CSM + Solution Architect)",
            "Roadmap co-construite avec l'équipe produit",
            "Waves personnalisées illimitées",
            "SLA 99.99% garanti contractuellement",
            "Support 24/7 hotline directe (1h SLA critique)",
            "Certification CaelumSwarm™ illimitée pour l'organisation",
            "Accès aux données brutes et API avancée",
            "Siège observateur au Comité Stratégique Caelum",
            "Rapport annuel d'impact ESG co-signé",
            "Early access exclusif aux nouveaux marchés géographiques",
        ],
        "dedicated_support": True,
        "custom_waves_per_year": 999,
        "price_lock_years": 5,
        "executive_access": True,
        "churn_rate_pct": 1.5,
    },
}

RETENTION_PLAYBOOKS = {
    "ONBOARDING_SUCCESS": {
        "trigger": "Nouveau client signé — J0 à J90",
        "timeline_days": 90,
        "touchpoints": [
            {
                "day": 1,
                "action": "Kick-off call de bienvenue",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Bienvenue chez CaelumSwarm™ ! Ce call de 60 min vous permet de "
                    "rencontrer votre CSM, valider vos objectifs CSDDD prioritaires "
                    "et configurer vos 5 premières waves avec votre équipe."
                ),
            },
            {
                "day": 7,
                "action": "Session de configuration waves & premiers résultats",
                "owner_role": "Solution Engineer",
                "message_template": (
                    "Session pratique de 90 min : activation de vos waves sectorielles, "
                    "paramétrage des seuils d'alerte et génération de votre premier "
                    "rapport de due diligence. Objectif : 3 waves opérationnelles."
                ),
            },
            {
                "day": 30,
                "action": "Bilan J+30 & ajustements",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Point de 30 minutes pour valider l'adoption (cible : 80% des "
                    "waves configurées actives), recueillir vos premiers retours "
                    "et identifier les besoins de formation complémentaire."
                ),
            },
            {
                "day": 60,
                "action": "First Value Review — présentation des premiers insights CSDDD",
                "owner_role": "Customer Success Manager + Account Executive",
                "message_template": (
                    "Présentation de vos premiers résultats CaelumSwarm™ : panorama "
                    "des risques identifiés dans votre chaîne de valeur, conformité "
                    "CSDDD Art.8 et recommandations prioritaires. Base du renouvellement."
                ),
            },
            {
                "day": 90,
                "action": "Revue onboarding & plan d'expansion",
                "owner_role": "Customer Success Manager + Sales",
                "message_template": (
                    "Bilan complet des 90 premiers jours, NPS onboarding, "
                    "et présentation du plan de valeur an 2 avec opportunités "
                    "d'expansion identifiées (waves additionnelles, entités multi-sites)."
                ),
            },
        ],
        "success_metric": "Adoption > 80% des waves | NPS > 40 | 0 ticket critique non résolu",
        "escalation_threshold": "Adoption < 50% à J+60 → escalade CSM senior + Head of CS",
    },
    "HEALTH_CHECK_60D": {
        "trigger": "Revue de santé compte — tous les 60 jours (clients Silver+)",
        "timeline_days": 60,
        "touchpoints": [
            {
                "day": 0,
                "action": "Analyse automatique des signaux d'usage (tableau de bord interne)",
                "owner_role": "Customer Success Operations",
                "message_template": (
                    "Vérification automatique : fréquence de connexion, waves actives, "
                    "tickets ouverts, NPS dernière enquête. Score de santé calculé "
                    "et rapport envoyé au CSM sous 24h."
                ),
            },
            {
                "day": 5,
                "action": "Appel proactif si score de santé < 70",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Bonjour [Prénom], je vous contacte pour notre point bimestriel "
                    "sur votre utilisation de CaelumSwarm™. Avez-vous des questions "
                    "sur les nouvelles waves CSDDD disponibles ce trimestre ?"
                ),
            },
            {
                "day": 30,
                "action": "Partage d'un insight CSDDD personnalisé au secteur du client",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Nous avons identifié 3 nouvelles tendances de risque dans votre "
                    "secteur ce mois-ci — voici un brief exclusif avec les waves "
                    "les plus pertinentes pour votre contexte CSDDD."
                ),
            },
            {
                "day": 60,
                "action": "Rapport de valeur bimestriel + proposition d'expansion si éligible",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Bilan de vos 60 derniers jours sur CaelumSwarm™ : [N] risques "
                    "identifiés, [N] alertes traitées, conformité CSDDD Art.8 à "
                    "[X]%. Prochaine étape recommandée : [action prioritaire]."
                ),
            },
        ],
        "success_metric": "Score de santé > 70 | Engagement actif maintenu | NPS stable ou en hausse",
        "escalation_threshold": "Score de santé < 50 à J+30 → activation playbook CHURN_RISK_DETECTED",
    },
    "RENEWAL_90D_OUT": {
        "trigger": "Renouvellement à 90 jours — tous les comptes",
        "timeline_days": 90,
        "touchpoints": [
            {
                "day": 0,
                "action": "Audit interne ROI client & préparation dossier de renouvellement",
                "owner_role": "Customer Success Manager + Revenue Operations",
                "message_template": (
                    "Analyse interne : calcul du ROI client (risques détectés, "
                    "économies conformité estimées, NPS historique), préparation "
                    "de l'offre de renouvellement et identification des opportunités d'upsell."
                ),
            },
            {
                "day": 10,
                "action": "Réunion ROI Review — présentation de la valeur année écoulée",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Bilan annuel CaelumSwarm™ : [N] risques CSDDD identifiés et "
                    "traités, [N] waves actives, estimation de l'impact financier "
                    "évité grâce à la conformité proactive. Votre investissement CaelumSwarm™ "
                    "a généré un ROI estimé de [X]x."
                ),
            },
            {
                "day": 30,
                "action": "Envoi de la proposition de renouvellement + offre fidélité",
                "owner_role": "Account Executive + Customer Success Manager",
                "message_template": (
                    "Votre proposition de renouvellement personnalisée : tarif fidélité "
                    "maintenu, nouvelles fonctionnalités incluses, et option d'extension "
                    "vers le tier supérieur avec une période d'essai de 30 jours offerte."
                ),
            },
            {
                "day": 60,
                "action": "Relance et traitement des objections",
                "owner_role": "Account Executive",
                "message_template": (
                    "Nous souhaitons nous assurer que votre proposition de renouvellement "
                    "répond à vos attentes. Y a-t-il des points à ajuster — périmètre, "
                    "modalités de paiement, fonctionnalités prioritaires — pour finaliser "
                    "votre engagement CaelumSwarm™ pour l'année à venir ?"
                ),
            },
            {
                "day": 80,
                "action": "Signature ou escalade executives si non signé",
                "owner_role": "Head of Customer Success + VP Sales",
                "message_template": (
                    "Nous vous proposons un échange de 20 minutes avec notre direction "
                    "pour lever tout point bloquant avant la fin de votre contrat actuel. "
                    "Votre succès avec CaelumSwarm™ est notre priorité absolue."
                ),
            },
        ],
        "success_metric": "Renouvellement signé à J-10 minimum | NRR > 110% | Durée contrat ≥ 2 ans",
        "escalation_threshold": "Non signé à J+60 → escalade VP Sales + Head of CS + offre exceptionnelle",
    },
    "CHURN_RISK_DETECTED": {
        "trigger": "Score de risque churn >= 50 (HIGH ou CRITICAL)",
        "timeline_days": 30,
        "touchpoints": [
            {
                "day": 0,
                "action": "Alerte interne & mobilisation équipe de rétention",
                "owner_role": "Customer Success Operations",
                "message_template": (
                    "ALERTE CHURN — Compte [Client] : score de risque [X]/100. "
                    "Signaux détectés : [liste_signaux]. "
                    "CSM + Head of CS à briefer sous 24h. "
                    "Plan de rétention à activer immédiatement."
                ),
            },
            {
                "day": 2,
                "action": "Appel empathique de découverte des insatisfactions",
                "owner_role": "Customer Success Manager Senior",
                "message_template": (
                    "Bonjour [Prénom], je vous contacte personnellement pour m'assurer "
                    "que CaelumSwarm™ répond pleinement à vos attentes. Nous avons "
                    "remarqué une évolution dans vos usages et je souhaite comprendre "
                    "comment mieux vous accompagner dans vos enjeux CSDDD actuels."
                ),
            },
            {
                "day": 7,
                "action": "Présentation d'un plan de remédiation personnalisé",
                "owner_role": "Customer Success Manager + Solution Architect",
                "message_template": (
                    "Suite à notre échange, voici un plan d'action en 3 étapes "
                    "pour maximiser votre valeur CaelumSwarm™ : [action 1], [action 2], "
                    "[action 3]. Nous nous engageons à [engagement concret] d'ici [date]."
                ),
            },
            {
                "day": 14,
                "action": "Réunion executive — intervention du Head of Customer Success",
                "owner_role": "Head of Customer Success",
                "message_template": (
                    "Je souhaite vous rencontrer personnellement pour réaffirmer "
                    "l'engagement de Caelum Partners à votre réussite. Nous avons "
                    "préparé [proposition spécifique] pour vous démontrer concrètement "
                    "notre valeur dans votre contexte CSDDD."
                ),
            },
            {
                "day": 30,
                "action": "Point de clôture — décision maintien ou sortie accompagnée",
                "owner_role": "Head of Customer Success + Account Executive",
                "message_template": (
                    "Bilan de notre plan de rétention : [résultats obtenus]. "
                    "Si vous choisissez de renouveler, voici les conditions "
                    "exceptionnelles que nous vous proposons. Si vous décidez "
                    "de ne pas continuer, nous organisons une transition propre "
                    "et restons disponibles pour vous accueillir à nouveau."
                ),
            },
        ],
        "success_metric": "Score de risque < 30 à J+30 | Compte actif et engagé | Renouvellement confirmé",
        "escalation_threshold": "Score de risque > 75 à J+14 → intervention CEO + offre de retention exceptionnelle",
    },
    "POST_CHURN_WIN_BACK": {
        "trigger": "Client churné depuis 30 à 180 jours",
        "timeline_days": 120,
        "touchpoints": [
            {
                "day": 30,
                "action": "Enquête post-churn de compréhension (anonymisée)",
                "owner_role": "Customer Success Operations",
                "message_template": (
                    "Nous respectons votre décision et souhaitons apprendre de votre "
                    "expérience. Pourriez-vous consacrer 5 minutes à nous indiquer "
                    "les raisons principales de votre départ ? Vos retours sont "
                    "précieux pour améliorer CaelumSwarm™ — et resteront confidentiels."
                ),
            },
            {
                "day": 60,
                "action": "Partage d'une nouveauté produit majeure liée aux motifs de départ",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Depuis votre départ, nous avons lancé [fonctionnalité clé] "
                    "qui répond directement à [motif de départ mentionné]. "
                    "Je souhaitais vous en informer en avant-première — cette "
                    "évolution change significativement l'expérience que vous avez connue."
                ),
            },
            {
                "day": 90,
                "action": "Offre de win-back personnalisée",
                "owner_role": "Account Executive + Head of Customer Success",
                "message_template": (
                    "CaelumSwarm™ vous propose de revenir avec une offre de "
                    "réintégration sur mesure : [N] mois offerts, onboarding "
                    "Premium dédié, et accès immédiat aux waves CSDDD 2026 "
                    "qui couvrent précisément votre secteur. Aucun engagement "
                    "de durée pour les 90 premiers jours."
                ),
            },
            {
                "day": 120,
                "action": "Dernier contact — invitation à un événement exclusif",
                "owner_role": "Customer Success Manager",
                "message_template": (
                    "Nous vous invitons à notre prochain événement exclusif "
                    "CaelumSwarm™ — [Nom événement] — réservé aux anciens et actuels "
                    "clients. C'est l'occasion de découvrir notre roadmap 2027 "
                    "et de reconnecter avec notre équipe, sans aucune obligation."
                ),
            },
        ],
        "success_metric": "Taux de win-back > 15% | MRR récupéré en valeur > MRR initial",
        "escalation_threshold": "Aucune réponse à J+90 → archivage compte avec contact annuel maintenu",
    },
}

EXPANSION_OPPORTUNITIES = {
    "ADDITIONAL_WAVES": {
        "label": "Waves supplémentaires — couverture sectorielle étendue",
        "target_tier": "BRONZE",
        "avg_expansion_EUR": 8_000,
        "conversion_rate_pct": 45,
        "best_timing": "J+60 post-onboarding ou lors du renouvellement annuel",
        "pitch_angle": (
            "Votre usage actuel couvre [N] secteurs — l'ajout de [secteur cible] "
            "vous permettrait de compléter votre due diligence CSDDD Art.8 sur "
            "100% de votre chaîne de valeur. ROI estimé : [X]x en 6 mois."
        ),
    },
    "PREMIUM_TIER_UPGRADE": {
        "label": "Upgrade vers tier supérieur",
        "target_tier": "SILVER",
        "avg_expansion_EUR": 18_000,
        "conversion_rate_pct": 32,
        "best_timing": "Lors de la Business Review Q3 ou à 90 jours du renouvellement",
        "pitch_angle": (
            "En passant au tier Gold, vous bénéficiez d'un CSM Senior dédié, "
            "de 2 waves personnalisées/an et d'un accès au Customer Advisory Board. "
            "Pour [client] dont l'équipe CSDDD grandit, c'est l'investissement "
            "structurant pour aborder 2027 avec sérénité."
        ),
    },
    "MULTI_ENTITY_LICENSE": {
        "label": "Licence multi-entités — déploiement groupe",
        "target_tier": "GOLD",
        "avg_expansion_EUR": 45_000,
        "conversion_rate_pct": 28,
        "best_timing": "Après 12 mois d'usage validé sur une entité pilote",
        "pitch_angle": (
            "Vous avez démontré la valeur de CaelumSwarm™ sur [entité pilote]. "
            "Un déploiement groupe sur [N] filiales vous permet de centraliser "
            "le reporting CSDDD au niveau consolidé — exigence clé de la directive "
            "pour les groupes > 1000 salariés. Remise groupe : -20%."
        ),
    },
    "BOARD_REPORTING_ADD_ON": {
        "label": "Module Board Reporting — tableaux de bord executives",
        "target_tier": "SILVER",
        "avg_expansion_EUR": 12_000,
        "conversion_rate_pct": 38,
        "best_timing": "Lors d'un changement de DG ou RSE, ou avant une AG",
        "pitch_angle": (
            "Le module Board Reporting génère automatiquement des synthèses "
            "exécutives mensuelles en format CA — indicateurs CSDDD, alertes "
            "prioritaires et progrès vs. plan d'action. Idéal pour votre "
            "prochain rapport CSRD et la communication avec vos parties prenantes."
        ),
    },
    "CUSTOM_SECTOR_ENGINE": {
        "label": "Engine sectoriel personnalisé — développement sur mesure",
        "target_tier": "PLATINUM",
        "avg_expansion_EUR": 75_000,
        "conversion_rate_pct": 18,
        "best_timing": "Lors de la revue roadmap annuelle ou suite à un événement sectoriel majeur",
        "pitch_angle": (
            "Votre secteur [X] présente des spécificités de risques droits humains "
            "non couverts par les engines standards. Caelum Partners peut développer "
            "un engine sur mesure calibré sur vos chaînes de valeur spécifiques, "
            "vos fournisseurs clés et vos obligations réglementaires sectorielles."
        ),
    },
}


# ---------------------------------------------------------------------------
# 2. FONCTIONS PRINCIPALES
# ---------------------------------------------------------------------------


def calculate_churn_risk(client: dict, usage_data: dict) -> dict:
    """
    Calcule le score de risque churn d'un client (0-100) à partir
    des signaux pondérés détectés dans son usage et son historique.

    Args:
        client: dict avec id, name, tier, mrr_EUR, tenure_months, nps_score
        usage_data: dict avec les signaux booléens ou intensités (0-1) par signal

    Returns:
        dict avec risk_score, risk_level, top_risk_factors,
              recommended_intervention, days_to_act
    """
    risk_score = 0.0
    active_signals = []

    for signal_key, signal_meta in CHURN_RISK_SIGNALS.items():
        signal_value = usage_data.get(signal_key, 0)
        if isinstance(signal_value, bool):
            intensity = 1.0 if signal_value else 0.0
        else:
            intensity = float(max(0, min(1, signal_value)))

        if intensity > 0:
            contribution = signal_meta["weight"] * intensity * 100
            risk_score += contribution
            active_signals.append({
                "signal": signal_key,
                "label": signal_meta["label"],
                "intensity": round(intensity, 2),
                "contribution": round(contribution, 2),
                "days_to_churn_avg": signal_meta["days_to_churn_avg"],
                "recovery_rate_pct": signal_meta["recovery_rate_pct"],
            })

    risk_score = round(min(100, risk_score), 1)

    # Ajustement selon le tenure — les clients récents sont plus vulnérables
    tenure_months = client.get("tenure_months", 12)
    if tenure_months < 3:
        risk_score = min(100, risk_score * 1.20)
    elif tenure_months > 36:
        risk_score = risk_score * 0.85

    risk_score = round(risk_score, 1)

    # Détermination du niveau de risque
    if risk_score >= 75:
        risk_level = "CRITICAL"
        recommended_intervention = "CHURN_RISK_DETECTED"
        days_to_act = 2
    elif risk_score >= 50:
        risk_level = "HIGH"
        recommended_intervention = "CHURN_RISK_DETECTED"
        days_to_act = 7
    elif risk_score >= 25:
        risk_level = "MEDIUM"
        recommended_intervention = "HEALTH_CHECK_60D"
        days_to_act = 14
    else:
        risk_level = "LOW"
        recommended_intervention = "HEALTH_CHECK_60D"
        days_to_act = 60

    # Top risques triés par contribution décroissante
    top_risk_factors = sorted(active_signals, key=lambda x: x["contribution"], reverse=True)[:3]

    # Estimation du MRR à risque
    mrr_at_risk = client.get("mrr_EUR", 0) if risk_level in ("HIGH", "CRITICAL") else 0

    return {
        "client_id": client.get("id"),
        "client_name": client.get("name"),
        "tier": client.get("tier"),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "signals_detected": len(active_signals),
        "top_risk_factors": top_risk_factors,
        "recommended_intervention": recommended_intervention,
        "days_to_act": days_to_act,
        "mrr_at_risk_EUR": mrr_at_risk,
        "playbook": RETENTION_PLAYBOOKS.get(recommended_intervention, {}).get("trigger", ""),
        "assessed_at": datetime.now(timezone.utc).isoformat(),
    }


def design_loyalty_program(tier: str, client_segment: str) -> dict:
    """
    Conçoit un programme de fidélisation personnalisé pour un client
    selon son tier et son segment métier.

    Args:
        tier: BRONZE / SILVER / GOLD / PLATINUM
        client_segment: ex. "supply_chain", "finance", "tech_industrial"

    Returns:
        dict avec perks_activated, quarterly_touchpoints, success_milestones,
              renewal_offer, estimated_ltv_impact_EUR
    """
    if tier not in LOYALTY_TIERS:
        raise ValueError(f"Tier inconnu : {tier}. Valeurs valides : {list(LOYALTY_TIERS.keys())}")

    tier_meta = LOYALTY_TIERS[tier]

    # Avantages activés selon le tier
    perks_activated = tier_meta["perks"]

    # Génération d'un plan de touchpoints trimestriels
    quarterly_touchpoints = {
        "Q1": [
            {
                "mois": 1,
                "action": "Business Review trimestrielle",
                "objectif": "Aligner les priorités CSDDD du client avec la roadmap produit",
                "owner": "Customer Success Manager",
                "format": "Visioconférence 60 min + compte-rendu partagé",
            },
            {
                "mois": 2,
                "action": f"Partage d'insights sectoriels — {client_segment}",
                "objectif": "Démontrer la valeur continue et identifier de nouvelles waves pertinentes",
                "owner": "Customer Success Manager",
                "format": "Email + brief sectoriel exclusif (2 pages)",
            },
            {
                "mois": 3,
                "action": "Enquête NPS + plan de valeur trimestre suivant",
                "objectif": "Mesurer la satisfaction et anticiper les besoins d'expansion",
                "owner": "Customer Success Operations",
                "format": "Enquête en ligne + appel de suivi si NPS < 7",
            },
        ],
        "Q2": [
            {
                "mois": 4,
                "action": "Business Review Q2 + bilan semestre",
                "objectif": "Présenter les KPIs de conformité CSDDD sur le premier semestre",
                "owner": "Customer Success Manager + Account Executive",
                "format": "Réunion en présentiel si compte Gold/Platinum",
            },
            {
                "mois": 5,
                "action": "Formation avancée sur nouvelles fonctionnalités",
                "objectif": "Maximiser l'adoption des fonctionnalités sous-utilisées",
                "owner": "Solution Engineer",
                "format": "Workshop en ligne 90 min (enregistré et partagé)",
            },
            {
                "mois": 6,
                "action": "Point de mi-année — anticipation renouvellement",
                "objectif": "Sécuriser l'intention de renouvellement et identifier l'upsell",
                "owner": "Customer Success Manager",
                "format": "Appel 45 min + envoi dossier ROI semi-annuel",
            },
        ],
        "Q3": [
            {
                "mois": 7,
                "action": "Business Review Q3 + preview roadmap H2",
                "objectif": "Impliquer le client dans l'évolution produit et renforcer le partenariat",
                "owner": "Customer Success Manager + Product Manager",
                "format": "Visioconférence 75 min avec démo fonctionnalités bêta",
            },
            {
                "mois": 8,
                "action": "Analyse concurrentielle — positionnement CaelumSwarm™",
                "objectif": "Renforcer la perception de valeur face aux alternatives du marché",
                "owner": "Customer Success Manager",
                "format": "Rapport comparatif personnalisé (4 pages)",
            },
            {
                "mois": 9,
                "action": "Activation du playbook de renouvellement (si contrat < 90 jours)",
                "objectif": "Initier formellement le processus de renouvellement",
                "owner": "Account Executive",
                "format": "Réunion ROI Review + envoi proposition commerciale",
            },
        ],
        "Q4": [
            {
                "mois": 10,
                "action": "Revue annuelle de conformité CSDDD — rapport d'impact",
                "objectif": "Documenter la valeur créée sur l'année et préparer le rapport CSRD",
                "owner": "Customer Success Manager + Compliance Expert",
                "format": "Rapport annuel personnalisé + présentation au COMEX si Platinum",
            },
            {
                "mois": 11,
                "action": "Négociation et signature du renouvellement",
                "objectif": "Renouvellement signé avec expansion MRR (NRR > 110%)",
                "owner": "Account Executive + Head of CS",
                "format": "Réunion de signature + célébration partenariat",
            },
            {
                "mois": 12,
                "action": "Bilan annuel & plan de fidélisation année N+1",
                "objectif": "Fixer les objectifs de l'année suivante et renforcer la relation",
                "owner": "Customer Success Manager",
                "format": "Réunion annuelle + envoi kit fidélité du tier supérieur si éligible",
            },
        ],
    }

    # Jalons de succès personnalisés
    success_milestones = [
        {
            "mois": 3,
            "milestone": "Premier rapport CSDDD Art.8 validé par l'équipe compliance du client",
            "kpi": "Score de santé compte > 75 | NPS ≥ 7",
        },
        {
            "mois": 6,
            "milestone": "100% des waves prioritaires actives et intégrées au processus interne",
            "kpi": "Taux d'adoption > 85% | 0 ticket bloquant",
        },
        {
            "mois": 12,
            "milestone": "Renouvellement signé avec expansion ≥ 10% MRR",
            "kpi": "NRR ≥ 110% | NPS ≥ 40 | Durée contrat ≥ 2 ans",
        },
        {
            "mois": 24,
            "milestone": "Upgrade vers tier supérieur ou déploiement multi-entités",
            "kpi": "LTV multipliée × 1.5 vs. contrat initial | Référence client acceptée",
        },
    ]

    # Offre de renouvellement adaptée au tier
    tier_discounts = {"BRONZE": 0, "SILVER": 5, "GOLD": 10, "PLATINUM": 15}
    tier_bonus_months = {"BRONZE": 0, "SILVER": 1, "GOLD": 2, "PLATINUM": 3}

    renewal_offer = {
        "price_lock_years": tier_meta["price_lock_years"],
        "loyalty_discount_pct": tier_discounts.get(tier, 0),
        "bonus_months_offered": tier_bonus_months.get(tier, 0),
        "included_perks_upgrade": (
            f"Accès 30 jours au tier {list(LOYALTY_TIERS.keys())[min(list(LOYALTY_TIERS.keys()).index(tier) + 1, len(LOYALTY_TIERS) - 1)]} "
            f"inclus dans l'offre de renouvellement"
            if tier != "PLATINUM"
            else "Conditions Platinum renouvelées avec audit stratégique offert"
        ),
        "multi_year_incentive": (
            "Engagement 2 ans : -8% supplémentaire | "
            "Engagement 3 ans : -15% supplémentaire + onboarding team illimité"
        ),
    }

    # Impact estimé sur la LTV
    churn_rate_current = tier_meta["churn_rate_pct"] / 100
    churn_rate_with_program = churn_rate_current * 0.65  # Réduction de 35% via programme fidélité
    ltv_multiplier = (1 / churn_rate_with_program) / (1 / churn_rate_current)
    estimated_ltv_impact_EUR = round(ltv_multiplier * 15_000, -2)  # Arrondi à 100€

    return {
        "tier": tier,
        "tier_label": tier_meta["label"],
        "client_segment": client_segment,
        "dedicated_support": tier_meta["dedicated_support"],
        "executive_access": tier_meta["executive_access"],
        "custom_waves_per_year": tier_meta["custom_waves_per_year"],
        "perks_activated": perks_activated,
        "quarterly_touchpoints": quarterly_touchpoints,
        "success_milestones": success_milestones,
        "renewal_offer": renewal_offer,
        "estimated_ltv_impact_EUR": estimated_ltv_impact_EUR,
        "churn_rate_baseline_pct": tier_meta["churn_rate_pct"],
        "churn_rate_with_program_pct": round(churn_rate_with_program * 100, 2),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def calculate_ltv(client: dict, churn_probability: float) -> dict:
    """
    Calcule la Customer Lifetime Value (LTV) d'un client B2B SaaS.

    Args:
        client: dict avec id, name, tier, mrr_EUR, cac_EUR, tenure_months
        churn_probability: probabilité de churn annuelle (0.0-1.0)

    Returns:
        dict avec monthly_revenue, gross_margin_pct, ltv_EUR, ltv_to_cac_ratio,
              payback_period_months, expansion_potential_EUR
    """
    mrr = client.get("mrr_EUR", 0)
    arr = mrr * 12
    cac = client.get("cac_EUR", 15_000)
    tier = client.get("tier", "SILVER")
    tenure_months = client.get("tenure_months", 12)

    # Marge brute SaaS standard : 80%
    gross_margin_pct = 80.0
    gross_margin_rate = gross_margin_pct / 100

    # LTV = (MRR × Marge brute) / Taux de churn mensuel
    # Taux de churn mensuel = 1 - (1 - churn_annuel)^(1/12)
    monthly_churn_rate = 1 - (1 - max(churn_probability, 0.001)) ** (1 / 12)
    ltv_eur = round((mrr * gross_margin_rate) / monthly_churn_rate, 2)

    # Ratio LTV/CAC (objectif SaaS : > 3x, idéal > 5x)
    ltv_to_cac_ratio = round(ltv_eur / cac, 2) if cac > 0 else 0

    # Payback period = CAC / (MRR × marge brute) en mois
    monthly_gross_profit = mrr * gross_margin_rate
    payback_period_months = round(cac / monthly_gross_profit, 1) if monthly_gross_profit > 0 else 999

    # Potentiel d'expansion selon le tier et le MRR actuel
    expansion_rates = {"BRONZE": 0.25, "SILVER": 0.40, "GOLD": 0.55, "PLATINUM": 0.70}
    expansion_rate = expansion_rates.get(tier, 0.30)
    expansion_potential_eur = round(arr * expansion_rate, 2)

    # Score de santé LTV
    if ltv_to_cac_ratio >= 5:
        ltv_health = "EXCELLENT — LTV/CAC > 5x, expansion priorisée"
    elif ltv_to_cac_ratio >= 3:
        ltv_health = "SAIN — LTV/CAC > 3x, seuil B2B SaaS validé"
    elif ltv_to_cac_ratio >= 1:
        ltv_health = "ATTENTION — LTV/CAC < 3x, réduire CAC ou augmenter MRR"
    else:
        ltv_health = "CRITIQUE — LTV inférieure au CAC, compte non rentable"

    # NRR projeté basé sur expansion
    projected_nrr_pct = round((1 + expansion_rate - churn_probability) * 100, 1)

    return {
        "client_id": client.get("id"),
        "client_name": client.get("name"),
        "tier": tier,
        "tenure_months": tenure_months,
        "monthly_revenue_EUR": mrr,
        "arr_EUR": arr,
        "gross_margin_pct": gross_margin_pct,
        "churn_probability_annual": round(churn_probability, 4),
        "monthly_churn_rate": round(monthly_churn_rate, 4),
        "ltv_EUR": ltv_eur,
        "cac_EUR": cac,
        "ltv_to_cac_ratio": ltv_to_cac_ratio,
        "ltv_health": ltv_health,
        "payback_period_months": payback_period_months,
        "payback_benchmark": "< 18 mois (cible CaelumSwarm™)",
        "expansion_potential_EUR": expansion_potential_eur,
        "projected_nrr_pct": projected_nrr_pct,
        "nrr_target_pct": 110,
        "nrr_on_track": projected_nrr_pct >= 110,
        "calculated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_retention_report(client_portfolio: list) -> dict:
    """
    Génère un rapport de rétention au niveau du portefeuille clients.
    Analyse le risque agrégé, la santé MRR et les priorités d'action.

    Args:
        client_portfolio: liste de dicts avec id, name, tier, mrr_EUR,
                          cac_EUR, tenure_months, nps_score, usage_data

    Returns:
        dict avec avg_churn_risk, clients_at_risk_count, mrr_at_risk_EUR,
              top_churn_reasons, retention_rate_pct, net_revenue_retention_pct,
              recommended_priority_actions
    """
    if not client_portfolio:
        return {"error": "Portefeuille client vide", "clients_analyzed": 0}

    risk_assessments = []
    for client in client_portfolio:
        usage_data = client.get("usage_data", {})
        assessment = calculate_churn_risk(client, usage_data)
        risk_assessments.append(assessment)

    # Métriques agrégées
    total_clients = len(risk_assessments)
    avg_churn_risk = round(sum(a["risk_score"] for a in risk_assessments) / total_clients, 1)

    clients_at_risk = [a for a in risk_assessments if a["risk_level"] in ("HIGH", "CRITICAL")]
    clients_at_risk_count = len(clients_at_risk)
    mrr_at_risk_eur = sum(a["mrr_at_risk_EUR"] for a in risk_assessments)

    # Taux de rétention estimé
    critical_count = sum(1 for a in risk_assessments if a["risk_level"] == "CRITICAL")
    high_count = sum(1 for a in risk_assessments if a["risk_level"] == "HIGH")
    medium_count = sum(1 for a in risk_assessments if a["risk_level"] == "MEDIUM")

    # Probabilité de churn pondérée par niveau de risque
    estimated_churns = critical_count * 0.70 + high_count * 0.35 + medium_count * 0.10
    retention_rate_pct = round((1 - estimated_churns / total_clients) * 100, 1)

    # Top raisons de churn (signaux les plus fréquents dans les cas HIGH/CRITICAL)
    churn_reason_counts = {}
    for assessment in clients_at_risk:
        for factor in assessment.get("top_risk_factors", []):
            label = factor["label"]
            churn_reason_counts[label] = churn_reason_counts.get(label, 0) + 1

    top_churn_reasons = sorted(
        [{"reason": k, "count": v, "frequency_pct": round(v / max(clients_at_risk_count, 1) * 100, 0)}
         for k, v in churn_reason_counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:5]

    # Calcul NRR simplifié basé sur la distribution des tiers
    tier_nrr = {"BRONZE": 95, "SILVER": 105, "GOLD": 115, "PLATINUM": 125}
    total_mrr = sum(c.get("mrr_EUR", 0) for c in client_portfolio)

    weighted_nrr = 0.0
    for client in client_portfolio:
        tier = client.get("tier", "SILVER")
        weight = client.get("mrr_EUR", 0) / total_mrr if total_mrr > 0 else 1 / total_clients
        weighted_nrr += tier_nrr.get(tier, 105) * weight

    net_revenue_retention_pct = round(weighted_nrr, 1)

    # Répartition du portefeuille par niveau de risque
    risk_distribution = {
        "CRITICAL": critical_count,
        "HIGH": high_count,
        "MEDIUM": medium_count,
        "LOW": total_clients - critical_count - high_count - medium_count,
    }

    # Actions prioritaires recommandées
    recommended_priority_actions = []

    if critical_count > 0:
        recommended_priority_actions.append({
            "priorité": 1,
            "action": f"Activer le playbook CHURN_RISK_DETECTED pour {critical_count} compte(s) CRITICAL",
            "responsable": "Head of Customer Success",
            "délai": "Immédiat — 24h",
            "mrr_à_sauvegarder_EUR": sum(
                a["mrr_at_risk_EUR"] for a in risk_assessments if a["risk_level"] == "CRITICAL"
            ),
        })

    if high_count > 0:
        recommended_priority_actions.append({
            "priorité": 2,
            "action": f"Planifier des appels proactifs pour {high_count} compte(s) HIGH risk cette semaine",
            "responsable": "Customer Success Managers",
            "délai": "Cette semaine — J+7",
            "mrr_à_sauvegarder_EUR": sum(
                a["mrr_at_risk_EUR"] for a in risk_assessments if a["risk_level"] == "HIGH"
            ),
        })

    if net_revenue_retention_pct < 110:
        recommended_priority_actions.append({
            "priorité": 3,
            "action": f"NRR à {net_revenue_retention_pct}% — sous l'objectif 110%. Accélérer les opportunités d'expansion sur les comptes Gold et Platinum.",
            "responsable": "Account Executives + CSM",
            "délai": "Ce mois — J+30",
            "mrr_à_sauvegarder_EUR": 0,
        })

    if top_churn_reasons:
        top_reason = top_churn_reasons[0]["reason"]
        recommended_priority_actions.append({
            "priorité": 4,
            "action": (
                f"Principal signal de churn : '{top_reason}' ({top_churn_reasons[0]['count']} comptes). "
                f"Investiguer la cause racine et déployer un plan de remédiation systémique."
            ),
            "responsable": "Head of Product + Customer Success",
            "délai": "Ce trimestre — J+60",
            "mrr_à_sauvegarder_EUR": 0,
        })

    recommended_priority_actions.append({
        "priorité": 5,
        "action": "Lancer la campagne d'enquête NPS trimestrielle sur l'ensemble du portefeuille",
        "responsable": "Customer Success Operations",
        "délai": "Ce mois — J+14",
        "mrr_à_sauvegarder_EUR": 0,
    })

    return {
        "report_type": "PORTFOLIO_RETENTION_REPORT",
        "report_id": f"RET-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Customer Loyalty & Retention Agent v1.0",
        "clients_analyzed": total_clients,
        "portfolio_mrr_EUR": total_mrr,
        "portfolio_arr_EUR": total_mrr * 12,
        "avg_churn_risk": avg_churn_risk,
        "clients_at_risk_count": clients_at_risk_count,
        "clients_at_risk_pct": round(clients_at_risk_count / total_clients * 100, 1),
        "mrr_at_risk_EUR": mrr_at_risk_eur,
        "risk_distribution": risk_distribution,
        "retention_rate_pct": retention_rate_pct,
        "retention_target_pct": 95.0,
        "retention_on_track": retention_rate_pct >= 95.0,
        "net_revenue_retention_pct": net_revenue_retention_pct,
        "nrr_target_pct": 110.0,
        "nrr_on_track": net_revenue_retention_pct >= 110.0,
        "top_churn_reasons": top_churn_reasons,
        "recommended_priority_actions": recommended_priority_actions,
        "csddd_context": (
            "Conformité CSDDD 2027 : la fidélisation des clients est un levier "
            "stratégique — chaque client perdu représente une réduction de la "
            "couverture due diligence collective et un risque de non-conformité "
            "pour les entreprises concernées par la directive."
        ),
        "disclaimer": (
            "Ce rapport est généré automatiquement par CaelumSwarm™. "
            "Les estimations de risque churn sont basées sur les signaux "
            "comportementaux disponibles et ne constituent pas une prévision garantie."
        ),
    }


# ---------------------------------------------------------------------------
# 3. DÉMONSTRATION
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démontre les capacités du Customer Loyalty & Retention Agent :
    1. Analyse churn risk pour 3 clients (faible, moyen, critique)
    2. Programme de fidélisation pour un client GOLD
    3. Calcul LTV du meilleur client
    4. Rapport de rétention pour un portefeuille de 8 clients
    """
    separator = "=" * 72
    print(separator)
    print("  CaelumSwarm™ — AGENT FIDÉLISATION CLIENTS")
    print("  Customer Loyalty & Retention Agent v1.0")
    print(f"  Date : {date.today().isoformat()}")
    print(separator)

    # ------------------------------------------------------------------
    # SECTION 1 : Analyse de risque churn — 3 profils clients
    # ------------------------------------------------------------------
    print("\n[1/4] ANALYSE DU RISQUE CHURN — 3 PROFILS CLIENTS\n")

    mock_clients = [
        {
            "id": "CLI-001",
            "name": "Veolia Environnement — Conformité Chaîne de Valeur",
            "tier": "GOLD",
            "mrr_EUR": 4_500,
            "cac_EUR": 18_000,
            "tenure_months": 28,
            "nps_score": 8,
            "usage_data": {
                "LOW_ENGAGEMENT": 0.0,
                "SUPPORT_TICKET_SPIKE": 0.0,
                "REDUCED_WAVE_USAGE": 0.0,
                "PAYMENT_DELAY": 0.0,
                "COMPETITOR_MENTION": 0.0,
                "NO_EXPANSION": 0.1,
                "CHAMPION_LEFT": 0.0,
                "LOW_NPS": 0.0,
            },
        },
        {
            "id": "CLI-002",
            "name": "Schneider Electric — CSDDD Supply Chain",
            "tier": "SILVER",
            "mrr_EUR": 2_800,
            "cac_EUR": 12_000,
            "tenure_months": 10,
            "nps_score": 6,
            "usage_data": {
                "LOW_ENGAGEMENT": 0.6,
                "SUPPORT_TICKET_SPIKE": 0.4,
                "REDUCED_WAVE_USAGE": 0.5,
                "PAYMENT_DELAY": 0.0,
                "COMPETITOR_MENTION": 0.2,
                "NO_EXPANSION": 0.8,
                "CHAMPION_LEFT": 0.0,
                "LOW_NPS": 1.0,
            },
        },
        {
            "id": "CLI-003",
            "name": "Atos SE — Risk Intelligence Platform",
            "tier": "BRONZE",
            "mrr_EUR": 1_200,
            "cac_EUR": 8_000,
            "tenure_months": 4,
            "nps_score": 4,
            "usage_data": {
                "LOW_ENGAGEMENT": 1.0,
                "SUPPORT_TICKET_SPIKE": 1.0,
                "REDUCED_WAVE_USAGE": 0.9,
                "PAYMENT_DELAY": 1.0,
                "COMPETITOR_MENTION": 0.8,
                "NO_EXPANSION": 1.0,
                "CHAMPION_LEFT": 1.0,
                "LOW_NPS": 1.0,
            },
        },
    ]

    risk_labels = {"LOW": "FAIBLE", "MEDIUM": "MODÉRÉ", "HIGH": "ÉLEVÉ", "CRITICAL": "CRITIQUE"}
    risk_icons = {"LOW": "V", "MEDIUM": "~", "HIGH": "!", "CRITICAL": "X"}

    for client in mock_clients:
        result = calculate_churn_risk(client, client["usage_data"])
        icon = risk_icons.get(result["risk_level"], "?")
        label = risk_labels.get(result["risk_level"], result["risk_level"])
        print(f"  [{icon}] {result['client_name']}")
        print(f"      Tier               : {result['tier']}")
        print(f"      Score de risque    : {result['risk_score']}/100 — {label}")
        print(f"      Signaux détectés   : {result['signals_detected']}")
        print(f"      MRR à risque       : {result['mrr_at_risk_EUR']:,}€")
        print(f"      Action dans        : {result['days_to_act']} jour(s)")
        print(f"      Intervention reco. : {result['recommended_intervention']}")
        if result["top_risk_factors"]:
            print(f"      Top signaux :")
            for factor in result["top_risk_factors"]:
                bar = "#" * int(factor["intensity"] * 10)
                print(f"        - {factor['label']:<40} [{bar:<10}] contribution : {factor['contribution']:.1f}/100")
        print()

    # ------------------------------------------------------------------
    # SECTION 2 : Programme de fidélisation — client GOLD
    # ------------------------------------------------------------------
    print(separator)
    print("[2/4] PROGRAMME DE FIDÉLISATION — CLIENT GOLD (Secteur Finance)\n")

    loyalty = design_loyalty_program("GOLD", "finance_banking")

    print(f"  Tier                     : {loyalty['tier_label']}")
    print(f"  Support dédié            : {'Oui' if loyalty['dedicated_support'] else 'Non'}")
    print(f"  Accès executives         : {'Oui' if loyalty['executive_access'] else 'Non'}")
    print(f"  Waves personnalisées/an  : {loyalty['custom_waves_per_year']}")
    print(f"  Prix bloqué (années)     : {loyalty['renewal_offer']['price_lock_years']}")
    print(f"  Taux churn baseline      : {loyalty['churn_rate_baseline_pct']}%")
    print(f"  Taux churn avec programme: {loyalty['churn_rate_with_program_pct']}%")
    print(f"  Impact LTV estimé        : +{loyalty['estimated_ltv_impact_EUR']:,}€\n")

    print("  Avantages activés :")
    for perk in loyalty["perks_activated"]:
        print(f"    + {perk}")

    print("\n  Jalons de succès :")
    for ms in loyalty["success_milestones"]:
        print(f"    Mois {ms['mois']:>2} — {ms['milestone']}")
        print(f"           KPI : {ms['kpi']}")

    renewal = loyalty["renewal_offer"]
    print("\n  Offre de renouvellement :")
    print(f"    Remise fidélité     : {renewal['loyalty_discount_pct']}%")
    print(f"    Mois offerts        : {renewal['bonus_months_offered']}")
    print(f"    Incentive multi-ans : {renewal['multi_year_incentive']}")

    # ------------------------------------------------------------------
    # SECTION 3 : Calcul LTV — meilleur client (Veolia)
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[3/4] CALCUL LTV — MEILLEUR CLIENT PORTEFEUILLE\n")

    best_client = mock_clients[0]
    ltv_result = calculate_ltv(best_client, churn_probability=0.035)

    print(f"  Client               : {best_client['name']}")
    print(f"  Tier                 : {ltv_result['tier']}")
    print(f"  MRR                  : {ltv_result['monthly_revenue_EUR']:,}€")
    print(f"  ARR                  : {ltv_result['arr_EUR']:,}€")
    print(f"  Marge brute SaaS     : {ltv_result['gross_margin_pct']}%")
    print(f"  Probabilité churn/an : {ltv_result['churn_probability_annual'] * 100:.1f}%")
    print(f"  LTV calculée         : {ltv_result['ltv_EUR']:,.0f}€")
    print(f"  CAC                  : {ltv_result['cac_EUR']:,}€")
    print(f"  LTV/CAC ratio        : {ltv_result['ltv_to_cac_ratio']}x — {ltv_result['ltv_health']}")
    print(f"  Payback period       : {ltv_result['payback_period_months']} mois ({ltv_result['payback_benchmark']})")
    print(f"  Potentiel expansion  : {ltv_result['expansion_potential_EUR']:,}€/an")
    print(f"  NRR projeté          : {ltv_result['projected_nrr_pct']}% (cible : {ltv_result['nrr_target_pct']}%)")
    nrr_status = "ON TRACK" if ltv_result["nrr_on_track"] else "SOUS OBJECTIF"
    print(f"  NRR statut           : {nrr_status}")

    # ------------------------------------------------------------------
    # SECTION 4 : Rapport de rétention — portefeuille 8 clients
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[4/4] RAPPORT DE RÉTENTION — PORTEFEUILLE 8 CLIENTS\n")

    portfolio = [
        {
            "id": "CLI-001", "name": "Veolia Environnement", "tier": "GOLD",
            "mrr_EUR": 4_500, "cac_EUR": 18_000, "tenure_months": 28,
            "usage_data": {"LOW_ENGAGEMENT": 0.0, "REDUCED_WAVE_USAGE": 0.0, "NO_EXPANSION": 0.1,
                           "SUPPORT_TICKET_SPIKE": 0.0, "PAYMENT_DELAY": 0.0,
                           "COMPETITOR_MENTION": 0.0, "CHAMPION_LEFT": 0.0, "LOW_NPS": 0.0},
        },
        {
            "id": "CLI-002", "name": "Schneider Electric", "tier": "SILVER",
            "mrr_EUR": 2_800, "cac_EUR": 12_000, "tenure_months": 10,
            "usage_data": {"LOW_ENGAGEMENT": 0.6, "REDUCED_WAVE_USAGE": 0.5, "LOW_NPS": 1.0,
                           "SUPPORT_TICKET_SPIKE": 0.4, "PAYMENT_DELAY": 0.0,
                           "COMPETITOR_MENTION": 0.2, "CHAMPION_LEFT": 0.0, "NO_EXPANSION": 0.8},
        },
        {
            "id": "CLI-003", "name": "Atos SE", "tier": "BRONZE",
            "mrr_EUR": 1_200, "cac_EUR": 8_000, "tenure_months": 4,
            "usage_data": {"LOW_ENGAGEMENT": 1.0, "SUPPORT_TICKET_SPIKE": 1.0, "REDUCED_WAVE_USAGE": 0.9,
                           "PAYMENT_DELAY": 1.0, "COMPETITOR_MENTION": 0.8,
                           "NO_EXPANSION": 1.0, "CHAMPION_LEFT": 1.0, "LOW_NPS": 1.0},
        },
        {
            "id": "CLI-004", "name": "TotalEnergies — Due Diligence", "tier": "PLATINUM",
            "mrr_EUR": 9_500, "cac_EUR": 30_000, "tenure_months": 42,
            "usage_data": {"LOW_ENGAGEMENT": 0.0, "SUPPORT_TICKET_SPIKE": 0.0, "REDUCED_WAVE_USAGE": 0.0,
                           "PAYMENT_DELAY": 0.0, "COMPETITOR_MENTION": 0.0,
                           "NO_EXPANSION": 0.0, "CHAMPION_LEFT": 0.0, "LOW_NPS": 0.0},
        },
        {
            "id": "CLI-005", "name": "Engie CSDDD Compliance", "tier": "GOLD",
            "mrr_EUR": 3_800, "cac_EUR": 16_000, "tenure_months": 22,
            "usage_data": {"LOW_ENGAGEMENT": 0.2, "SUPPORT_TICKET_SPIKE": 0.0, "REDUCED_WAVE_USAGE": 0.1,
                           "PAYMENT_DELAY": 0.0, "COMPETITOR_MENTION": 0.0,
                           "NO_EXPANSION": 0.3, "CHAMPION_LEFT": 0.0, "LOW_NPS": 0.0},
        },
        {
            "id": "CLI-006", "name": "BNP Paribas — Supply Chain Risk", "tier": "SILVER",
            "mrr_EUR": 3_200, "cac_EUR": 14_000, "tenure_months": 14,
            "usage_data": {"LOW_ENGAGEMENT": 0.3, "SUPPORT_TICKET_SPIKE": 0.5, "REDUCED_WAVE_USAGE": 0.2,
                           "PAYMENT_DELAY": 0.3, "COMPETITOR_MENTION": 0.4,
                           "NO_EXPANSION": 0.5, "CHAMPION_LEFT": 0.5, "LOW_NPS": 0.0},
        },
        {
            "id": "CLI-007", "name": "Renault Group — Chaîne Fournisseurs", "tier": "GOLD",
            "mrr_EUR": 5_100, "cac_EUR": 20_000, "tenure_months": 30,
            "usage_data": {"LOW_ENGAGEMENT": 0.0, "SUPPORT_TICKET_SPIKE": 0.1, "REDUCED_WAVE_USAGE": 0.0,
                           "PAYMENT_DELAY": 0.0, "COMPETITOR_MENTION": 0.1,
                           "NO_EXPANSION": 0.2, "CHAMPION_LEFT": 0.0, "LOW_NPS": 0.0},
        },
        {
            "id": "CLI-008", "name": "Carrefour — Éthique Fournisseurs", "tier": "BRONZE",
            "mrr_EUR": 1_800, "cac_EUR": 9_000, "tenure_months": 5,
            "usage_data": {"LOW_ENGAGEMENT": 0.5, "SUPPORT_TICKET_SPIKE": 0.2, "REDUCED_WAVE_USAGE": 0.4,
                           "PAYMENT_DELAY": 0.0, "COMPETITOR_MENTION": 0.0,
                           "NO_EXPANSION": 0.6, "CHAMPION_LEFT": 0.0, "LOW_NPS": 0.3},
        },
    ]

    report = generate_retention_report(portfolio)

    print(f"  Rapport ID               : {report['report_id']}")
    print(f"  Clients analysés         : {report['clients_analyzed']}")
    print(f"  MRR portefeuille         : {report['portfolio_mrr_EUR']:,}€")
    print(f"  ARR portefeuille         : {report['portfolio_arr_EUR']:,}€\n")

    ret_status = "ON TRACK" if report["retention_on_track"] else "SOUS OBJECTIF"
    nrr_status = "ON TRACK" if report["nrr_on_track"] else "SOUS OBJECTIF"

    print(f"  Risque churn moyen       : {report['avg_churn_risk']}/100")
    print(f"  Clients à risque         : {report['clients_at_risk_count']} / {report['clients_analyzed']} ({report['clients_at_risk_pct']}%)")
    print(f"  MRR à risque             : {report['mrr_at_risk_EUR']:,}€")
    print(f"  Taux de rétention estimé : {report['retention_rate_pct']}% (cible ≥ 95%) — {ret_status}")
    print(f"  NRR portefeuille         : {report['net_revenue_retention_pct']}% (cible ≥ 110%) — {nrr_status}\n")

    print("  Distribution des risques :")
    for level, count in report["risk_distribution"].items():
        bar = "#" * count + "-" * (8 - count)
        label = risk_labels.get(level, level)
        print(f"    [{bar}] {label:<10} : {count} client(s)")

    if report["top_churn_reasons"]:
        print("\n  Top raisons de churn :")
        for reason in report["top_churn_reasons"]:
            print(f"    - {reason['reason']:<45} : {reason['count']} compte(s) ({int(reason['frequency_pct'])}%)")

    print("\n  Actions prioritaires recommandées :")
    for action in report["recommended_priority_actions"]:
        mrr_info = f" | MRR à sauvegarder : {action['mrr_à_sauvegarder_EUR']:,}€" if action["mrr_à_sauvegarder_EUR"] > 0 else ""
        print(f"    #{action['priorité']} [{action['délai']}] {action['action']}")
        print(f"       Responsable : {action['responsable']}{mrr_info}")

    print(f"\n{separator}")
    print("  CaelumSwarm™ Customer Loyalty & Retention Agent — Démonstration terminée")
    print(f"  {report['clients_analyzed']} clients analysés | MRR total : {report['portfolio_mrr_EUR']:,}€")
    print(f"  NRR portefeuille : {report['net_revenue_retention_pct']}% | Rétention estimée : {report['retention_rate_pct']}%")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# 4. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
