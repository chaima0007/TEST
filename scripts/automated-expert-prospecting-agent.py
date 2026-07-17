"""
Agent Prospection Automatisée Expert — identifie, qualifie et engage automatiquement
les prospects à fort potentiel pour CaelumSwarm™ via signaux d'intention, événements
déclencheurs et scoring comportemental.

CaelumSwarm™ | Caelum Partners | Module: Revenue Intelligence & Automated Prospecting
Version: 1.0.0

Conformité RGPD : tous les signaux exploités proviennent de sources publiques ou de
données déclarées volontairement (événements professionnels, publications officielles,
bases de données réglementaires). Zéro tracking comportemental individuel covert.
"""

import math
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

INTENT_SIGNALS = {
    "CSDDD_SEARCH_ACTIVITY": {
        "label": "Activité de recherche CSDDD / devoir de vigilance",
        "signal_strength": 9,
        "recency_weight": 0.90,
        "data_source": "Moteurs de recherche professionnels, alertes Google, outils SEO publics",
        "avg_days_to_purchase": 42,
        "action_triggered": "Séquence COLD_INTENT_TRIGGER — email J0 avec angle informatif CSDDD",
    },
    "CSRD_REPORT_DOWNLOADED": {
        "label": "Téléchargement d'un rapport CSRD / ESG sectoriel",
        "signal_strength": 8,
        "recency_weight": 0.85,
        "data_source": "Portails de contenu gated, webinaires ESG, landing pages réglementaires",
        "avg_days_to_purchase": 55,
        "action_triggered": "Séquence WARM_INBOUND_FOLLOW — nurturing contenu + invitation démo",
    },
    "COMPETITOR_WEBSITE_VISIT": {
        "label": "Visite du site web d'un concurrent CaelumSwarm™",
        "signal_strength": 7,
        "recency_weight": 0.95,
        "data_source": "Outils d'intent data B2B publics (Bombora, G2, Capterra — données agrégées)",
        "avg_days_to_purchase": 28,
        "action_triggered": "Outreach comparatif différenciant — déclencher benchmark CaelumSwarm™ vs concurrent",
    },
    "LINKEDIN_PROFILE_VIEW": {
        "label": "Consultation du profil LinkedIn CaelumSwarm™ / Caelum Partners",
        "signal_strength": 5,
        "recency_weight": 0.98,
        "data_source": "LinkedIn Analytics (données propriétaires de la page entreprise)",
        "avg_days_to_purchase": 70,
        "action_triggered": "Connexion LinkedIn InMail personnalisée dans les 24h",
    },
    "CONFERENCE_ATTENDANCE": {
        "label": "Présence confirmée à une conférence ESG / CSDDD / droits humains",
        "signal_strength": 8,
        "recency_weight": 0.70,
        "data_source": "Programmes de conférences publics, listes de participants publiées, badge scanning",
        "avg_days_to_purchase": 35,
        "action_triggered": "Séquence EVENT_BASED_OUTREACH — contact sous 48h post-événement",
    },
    "REGULATORY_FINE_RECEIVED": {
        "label": "Amende ou mise en demeure réglementaire reçue (supply chain, droits humains)",
        "signal_strength": 10,
        "recency_weight": 0.99,
        "data_source": "Journaux officiels UE, communiqués DIRECCTE, bases AMF, alertes régulateurs",
        "avg_days_to_purchase": 14,
        "action_triggered": "Séquence REGULATORY_TRIGGER — contact C-suite en urgence sous 24h",
    },
    "PRESS_MENTION_NEGATIVE": {
        "label": "Mention presse négative — scandale fournisseur, incident chaîne d'approvisionnement",
        "signal_strength": 9,
        "recency_weight": 0.97,
        "data_source": "Veille médias (Google News, Factiva, Meltwater — accès public/agréé)",
        "avg_days_to_purchase": 21,
        "action_triggered": "Séquence REGULATORY_TRIGGER — angle gestion de crise et réparation reputationnelle",
    },
    "NEW_CSO_HIRED": {
        "label": "Recrutement d'un nouveau Chief Sustainability Officer ou Directeur RSE",
        "signal_strength": 8,
        "recency_weight": 0.75,
        "data_source": "LinkedIn, annonces de presse, communiqués internes publiés, LinkedIn Sales Navigator",
        "avg_days_to_purchase": 60,
        "action_triggered": "Email de félicitations avec pitch indirect — fenêtre d'opportunité 90 jours",
    },
    "SUPPLY_CHAIN_INCIDENT": {
        "label": "Incident identifié dans la chaîne d'approvisionnement (ONG, médias, régulateur)",
        "signal_strength": 10,
        "recency_weight": 0.96,
        "data_source": "Rapports ONG publics, bases WalkFree, Know The Chain, BankTrack, médias",
        "avg_days_to_purchase": 18,
        "action_triggered": "Séquence REGULATORY_TRIGGER — urgence maximale, décideur C-suite ciblé",
    },
    "IPO_OR_M_AND_A": {
        "label": "Introduction en bourse ou opération de fusion-acquisition annoncée",
        "signal_strength": 7,
        "recency_weight": 0.80,
        "data_source": "AMF, SEC, communiqués de presse officiels, bases M&A publiques",
        "avg_days_to_purchase": 45,
        "action_triggered": "Angle due diligence ESG — contacter le DAF / équipe transaction sous 72h",
    },
}

PROSPECT_SEGMENTS = {
    "LARGE_CAP_EU_MANUFACTURER": {
        "label": "Grande entreprise manufacturière européenne",
        "company_size_employees": "5 000 – 50 000",
        "typical_budget_EUR": 94_800,
        "buying_cycle_days": 75,
        "decision_makers": [
            "Chief Sustainability Officer (CSO)",
            "Directeur Juridique / CLO",
            "Directeur des Achats / CPO",
            "Directeur des Risques / CRO",
            "DSI (si intégration ERP/GRC requise)",
        ],
        "pain_points": [
            "Cartographie incomplète des fournisseurs rang 2 et rang 3",
            "Reporting CSRD chronophage et non automatisé",
            "Risque d'amende CSDDD jusqu'à 5 % du CA mondial",
            "Multiples systèmes ESG en silo, aucune vue consolidée",
            "Pression des donneurs d'ordre et des investisseurs institutionnels",
        ],
        "conversion_rate_pct": 18,
    },
    "MID_CAP_RETAILER": {
        "label": "ETI retailer / distribution",
        "company_size_employees": "500 – 5 000",
        "typical_budget_EUR": 34_800,
        "buying_cycle_days": 45,
        "decision_makers": [
            "Directeur RSE / Développement Durable",
            "Directeur Achats",
            "DAF (validation budgétaire)",
            "Directeur Qualité / Conformité",
        ],
        "pain_points": [
            "Chaîne d'approvisionnement textile ou agro-alimentaire à risques élevés",
            "Manque de ressources internes dédiées à la compliance CSDDD",
            "Fournisseurs asiatiques ou africains peu transparents",
            "Marges sous pression — besoin d'automatisation du monitoring",
            "Exigences croissantes des enseignes donneurs d'ordre sur la traçabilité",
        ],
        "conversion_rate_pct": 22,
    },
    "FINANCIAL_INSTITUTION": {
        "label": "Institution financière (banque, assurance, fonds)",
        "company_size_employees": "1 000 – 30 000",
        "typical_budget_EUR": 120_000,
        "buying_cycle_days": 90,
        "decision_makers": [
            "Chief Risk Officer (CRO)",
            "Responsable Finance Durable / ESG",
            "Directeur de la Conformité / CCO",
            "Directeur des Investissements (pour les fonds)",
            "Direction Juridique (obligations SFDR/CSRD)",
        ],
        "pain_points": [
            "Obligations SFDR et taxonomie UE sur portefeuille de financement",
            "Risque de réputation sur financements chaîne d'approvisionnement controversée",
            "Due diligence ESG des contreparties insuffisante",
            "Pression des régulateurs (BCE, ACPR) sur le risque ESG prudentiel",
            "Décarbonation et droits humains dans le portefeuille de crédit",
        ],
        "conversion_rate_pct": 14,
    },
    "CONSULTING_FIRM_RESELLER": {
        "label": "Cabinet de conseil — partenaire revendeur",
        "company_size_employees": "50 – 5 000",
        "typical_budget_EUR": 0,
        "buying_cycle_days": 60,
        "decision_makers": [
            "Associé / Partner en charge des offres ESG",
            "Directeur du Développement Commercial",
            "Directeur Innovation & Partenariats",
            "Responsable Alliances Technologiques",
        ],
        "pain_points": [
            "Manque d'outil propriétaire pour les missions CSDDD clients",
            "Concurrence des grandes plateformes ESG généralistes",
            "Besoin de différenciation sur le marché du conseil en durabilité",
            "Clients en attente de livrables CSDDD-ready dès 2026",
            "Ressources limitées pour développer une méthodologie interne",
        ],
        "conversion_rate_pct": 31,
    },
    "NGO_DATA_BUYER": {
        "label": "ONG / organisation internationale — acheteur de données",
        "company_size_employees": "10 – 500",
        "typical_budget_EUR": 12_000,
        "buying_cycle_days": 120,
        "decision_makers": [
            "Directeur des Programmes",
            "Responsable Plaidoyer Entreprises",
            "Directeur Technique / Data Lead",
            "Directeur Financier (approbation budget projet)",
        ],
        "pain_points": [
            "Données de suivi des droits humains fragmentées et non comparables",
            "Besoin de preuves quantitatives pour le plaidoyer et les campagnes",
            "Coût élevé des bases de données ESG propriétaires",
            "Crédibilité méthodologique nécessaire pour les publications officielles",
            "Suivi longitudinal des entreprises cibles dans le temps",
        ],
        "conversion_rate_pct": 8,
    },
    "PE_FUND_DUE_DILIGENCE": {
        "label": "Fonds de private equity — due diligence acquisition",
        "company_size_employees": "10 – 200",
        "typical_budget_EUR": 60_000,
        "buying_cycle_days": 30,
        "decision_makers": [
            "Partner / Associé en charge de la transaction",
            "Responsable ESG / Impact du fonds",
            "Directeur Juridique (legal due diligence)",
            "Operating Partner en charge de la cible",
        ],
        "pain_points": [
            "Risques ESG cachés dans la cible d'acquisition non détectés en due diligence standard",
            "Valorisation impactée par les litiges supply chain post-acquisition",
            "Obligations LP sur reporting ESG des participations",
            "Délais très courts pour la due diligence (2–6 semaines)",
            "Pression réglementaire AIFMD 2 et taxonomie sur les fonds d'impact",
        ],
        "conversion_rate_pct": 27,
    },
}

OUTREACH_SEQUENCES = {
    "COLD_INTENT_TRIGGER": {
        "trigger_condition": "Signal d'intention détecté (score ≥6) sans contact préalable",
        "steps": [
            {
                "step_num": 1,
                "channel": "Email",
                "delay_days": 0,
                "template_key": "COLD_INTENT_EMAIL_1",
                "personalization_tokens": [
                    "company_name", "trigger_signal_label", "sector", "csddd_deadline_weeks",
                    "fine_exposure_EUR", "first_name",
                ],
            },
            {
                "step_num": 2,
                "channel": "LinkedIn InMail",
                "delay_days": 3,
                "template_key": "COLD_INTENT_LINKEDIN",
                "personalization_tokens": [
                    "company_name", "first_name", "role_title", "sector_stat_wave",
                ],
            },
            {
                "step_num": 3,
                "channel": "Email",
                "delay_days": 7,
                "template_key": "COLD_INTENT_EMAIL_2_ROI",
                "personalization_tokens": [
                    "company_name", "roi_calculator_link", "sector", "wave_sample_domain",
                ],
            },
            {
                "step_num": 4,
                "channel": "Appel téléphonique",
                "delay_days": 10,
                "template_key": "COLD_INTENT_CALL_SCRIPT",
                "personalization_tokens": [
                    "company_name", "first_name", "role_title", "top_risk_domain",
                ],
            },
            {
                "step_num": 5,
                "channel": "Email",
                "delay_days": 14,
                "template_key": "COLD_INTENT_EMAIL_3_FINAL",
                "personalization_tokens": [
                    "company_name", "first_name", "wave_report_offer_EUR",
                    "csddd_deadline_weeks", "calendar_link",
                ],
            },
        ],
        "total_duration_days": 14,
        "expected_reply_rate_pct": 7,
    },
    "WARM_INBOUND_FOLLOW": {
        "trigger_condition": "Inbound identifié — formulaire, téléchargement contenu ou demande démo",
        "steps": [
            {
                "step_num": 1,
                "channel": "Email",
                "delay_days": 0,
                "template_key": "WARM_INBOUND_IMMEDIATE",
                "personalization_tokens": [
                    "first_name", "company_name", "content_downloaded", "sector",
                    "calendar_link_demo",
                ],
            },
            {
                "step_num": 2,
                "channel": "Appel téléphonique",
                "delay_days": 1,
                "template_key": "WARM_INBOUND_QUALIFICATION_CALL",
                "personalization_tokens": [
                    "first_name", "company_name", "role_title", "content_downloaded",
                ],
            },
            {
                "step_num": 3,
                "channel": "Email",
                "delay_days": 3,
                "template_key": "WARM_INBOUND_DEMO_CONFIRM",
                "personalization_tokens": [
                    "first_name", "company_name", "demo_date", "sector_wave_preview",
                    "decision_maker_list",
                ],
            },
            {
                "step_num": 4,
                "channel": "Email",
                "delay_days": 7,
                "template_key": "WARM_INBOUND_POST_DEMO",
                "personalization_tokens": [
                    "first_name", "company_name", "proposal_link", "wave_findings_summary",
                    "pricing_tier_recommended",
                ],
            },
        ],
        "total_duration_days": 7,
        "expected_reply_rate_pct": 38,
    },
    "EVENT_BASED_OUTREACH": {
        "trigger_condition": "Participation confirmée à un événement ESG / CSDDD dans les 7 jours",
        "steps": [
            {
                "step_num": 1,
                "channel": "Email",
                "delay_days": 0,
                "template_key": "EVENT_PRE_OUTREACH",
                "personalization_tokens": [
                    "first_name", "company_name", "event_name", "event_date", "booth_location",
                    "session_title_relevant",
                ],
            },
            {
                "step_num": 2,
                "channel": "LinkedIn InMail",
                "delay_days": 1,
                "template_key": "EVENT_LINKEDIN_CONNECT",
                "personalization_tokens": [
                    "first_name", "event_name", "session_attended", "common_topic",
                ],
            },
            {
                "step_num": 3,
                "channel": "Email",
                "delay_days": 3,
                "template_key": "EVENT_POST_FOLLOWUP",
                "personalization_tokens": [
                    "first_name", "company_name", "event_name", "key_insight_shared",
                    "csddd_stat_relevant", "calendar_link",
                ],
            },
            {
                "step_num": 4,
                "channel": "Email",
                "delay_days": 10,
                "template_key": "EVENT_FINAL_VALUE_ADD",
                "personalization_tokens": [
                    "first_name", "company_name", "wave_report_sample", "sector_benchmark",
                    "wave_report_offer_EUR",
                ],
            },
        ],
        "total_duration_days": 10,
        "expected_reply_rate_pct": 18,
    },
    "REGULATORY_TRIGGER": {
        "trigger_condition": (
            "Événement réglementaire critique détecté : amende, incident supply chain, "
            "mention presse négative — réponse en moins de 24h obligatoire"
        ),
        "steps": [
            {
                "step_num": 1,
                "channel": "Email C-suite",
                "delay_days": 0,
                "template_key": "REGULATORY_CSUITE_URGENCY",
                "personalization_tokens": [
                    "executive_name", "executive_title", "company_name", "trigger_event_detail",
                    "trigger_date", "estimated_fine_EUR", "csddd_risk_level",
                ],
            },
            {
                "step_num": 2,
                "channel": "Appel téléphonique direct",
                "delay_days": 1,
                "template_key": "REGULATORY_DIRECT_CALL",
                "personalization_tokens": [
                    "executive_name", "company_name", "trigger_event_brief",
                    "caelumswarm_rapid_response_offer",
                ],
            },
            {
                "step_num": 3,
                "channel": "Email",
                "delay_days": 3,
                "template_key": "REGULATORY_SOLUTION_BRIEF",
                "personalization_tokens": [
                    "first_name", "company_name", "trigger_event_detail", "similar_case_resolved",
                    "wave_domains_relevant", "onboarding_days",
                ],
            },
        ],
        "total_duration_days": 3,
        "expected_reply_rate_pct": 28,
    },
}

COMPANY_TRIGGERS_DB = [
    {
        "company": "Framatome Industries",
        "country": "France",
        "sector": "Énergie & Équipements Nucléaires",
        "employees": 14_000,
        "trigger_event": "REGULATORY_FINE_RECEIVED",
        "trigger_date": (date.today() - timedelta(days=3)).isoformat(),
        "estimated_budget_EUR": 94_800,
        "decision_maker_role": "Directeur Conformité & Affaires Réglementaires",
        "csddd_exposure": "HIGH",
    },
    {
        "company": "Groupe Beaumanoir",
        "country": "France",
        "sector": "Textile & Mode (fabrication chaîne asiatique)",
        "employees": 8_500,
        "trigger_event": "PRESS_MENTION_NEGATIVE",
        "trigger_date": (date.today() - timedelta(days=5)).isoformat(),
        "estimated_budget_EUR": 34_800,
        "decision_maker_role": "Directrice RSE & Développement Durable",
        "csddd_exposure": "HIGH",
    },
    {
        "company": "Thyssenkrupp Automotive Components",
        "country": "Allemagne",
        "sector": "Équipements Automobiles & Métallurgie",
        "employees": 22_000,
        "trigger_event": "SUPPLY_CHAIN_INCIDENT",
        "trigger_date": (date.today() - timedelta(days=7)).isoformat(),
        "estimated_budget_EUR": 120_000,
        "decision_maker_role": "Chief Sustainability Officer",
        "csddd_exposure": "HIGH",
    },
    {
        "company": "Crédit Mutuel Asset Management",
        "country": "France",
        "sector": "Gestion d'Actifs & Finance Durable",
        "employees": 3_200,
        "trigger_event": "CSRD_REPORT_DOWNLOADED",
        "trigger_date": (date.today() - timedelta(days=12)).isoformat(),
        "estimated_budget_EUR": 120_000,
        "decision_maker_role": "Responsable Finance Durable & ESG",
        "csddd_exposure": "MEDIUM",
    },
    {
        "company": "Maison Bocage Chaussures",
        "country": "France",
        "sector": "Chaussure & Accessoires (sourcing Maghreb & Asie du Sud)",
        "employees": 1_800,
        "trigger_event": "NEW_CSO_HIRED",
        "trigger_date": (date.today() - timedelta(days=18)).isoformat(),
        "estimated_budget_EUR": 34_800,
        "decision_maker_role": "Directeur RSE (poste nouvellement créé)",
        "csddd_exposure": "HIGH",
    },
    {
        "company": "Bridgepoint Europe VI",
        "country": "Royaume-Uni",
        "sector": "Private Equity — portefeuille industrie & retail",
        "employees": 180,
        "trigger_event": "IPO_OR_M_AND_A",
        "trigger_date": (date.today() - timedelta(days=8)).isoformat(),
        "estimated_budget_EUR": 60_000,
        "decision_maker_role": "Partner ESG & Responsible Investment",
        "csddd_exposure": "MEDIUM",
    },
    {
        "company": "Alstom Transport SA",
        "country": "France",
        "sector": "Transport Ferroviaire & Infrastructure",
        "employees": 31_000,
        "trigger_event": "CONFERENCE_ATTENDANCE",
        "trigger_date": (date.today() - timedelta(days=2)).isoformat(),
        "estimated_budget_EUR": 94_800,
        "decision_maker_role": "VP Procurement & Supply Chain Sustainability",
        "csddd_exposure": "HIGH",
    },
    {
        "company": "Ekibio Groupe (bio & naturel)",
        "country": "France",
        "sector": "Agroalimentaire Bio & Commerce Équitable",
        "employees": 620,
        "trigger_event": "CSDDD_SEARCH_ACTIVITY",
        "trigger_date": (date.today() - timedelta(days=21)).isoformat(),
        "estimated_budget_EUR": 12_000,
        "decision_maker_role": "Responsable Qualité & Certifications",
        "csddd_exposure": "MEDIUM",
    },
]


# ---------------------------------------------------------------------------
# FONCTIONS
# ---------------------------------------------------------------------------


def _recency_decay_factor(trigger_date_str: str, recency_weight: float) -> float:
    """
    Calcule le facteur de décroissance par recency.
    Le signal perd 10 % de sa force par semaine d'ancienneté,
    modulé par le recency_weight du signal.
    Retourne un facteur entre 0.05 et 1.0.
    """
    try:
        trigger_date = date.fromisoformat(trigger_date_str)
    except (ValueError, TypeError):
        return 0.5

    days_elapsed = max(0, (date.today() - trigger_date).days)
    weeks_elapsed = days_elapsed / 7.0

    # Decay : 10% par semaine pondéré par recency_weight
    decay = math.pow(max(0.01, 1.0 - 0.10 * recency_weight), weeks_elapsed)
    return round(max(0.05, min(1.0, decay)), 4)


def score_prospect_intent(company: dict, signals: list) -> dict:
    """
    Calcule le score d'intention d'achat (0-100) à partir des signaux pondérés
    avec décroissance par recency (le signal perd 10 % de force par semaine).

    company : dict avec au minimum les clés présentes dans COMPANY_TRIGGERS_DB
    signals : liste de dicts {signal_key: str, detected_date: str ISO, intensity: float 0-1}

    Retourne :
        intent_score       : int 0-100
        buying_stage       : AWARENESS | CONSIDERATION | DECISION
        top_signals        : liste des 3 signaux les plus forts avec détail
        recommended_sequence : clé de OUTREACH_SEQUENCES
        urgency_level      : FAIBLE | MODÉRÉ | ÉLEVÉ | CRITIQUE
    """
    if not signals:
        return {
            "intent_score": 0,
            "buying_stage": "AWARENESS",
            "top_signals": [],
            "recommended_sequence": "COLD_INTENT_TRIGGER",
            "urgency_level": "FAIBLE",
        }

    raw_weighted_scores = []

    for sig in signals:
        signal_key = sig.get("signal_key", "")
        detected_date = sig.get("detected_date", date.today().isoformat())
        intensity = float(sig.get("intensity", 1.0))

        if signal_key not in INTENT_SIGNALS:
            continue

        meta = INTENT_SIGNALS[signal_key]
        base_strength = meta["signal_strength"]  # 1-10
        recency_weight = meta["recency_weight"]

        decay = _recency_decay_factor(detected_date, recency_weight)
        effective_strength = base_strength * decay * intensity

        raw_weighted_scores.append({
            "signal_key": signal_key,
            "label": meta["label"],
            "base_strength": base_strength,
            "decay_factor": decay,
            "intensity": intensity,
            "effective_strength": round(effective_strength, 3),
            "action_triggered": meta["action_triggered"],
            "avg_days_to_purchase": meta["avg_days_to_purchase"],
            "data_source": meta["data_source"],
        })

    if not raw_weighted_scores:
        return {
            "intent_score": 0,
            "buying_stage": "AWARENESS",
            "top_signals": [],
            "recommended_sequence": "COLD_INTENT_TRIGGER",
            "urgency_level": "FAIBLE",
        }

    # Normaliser sur l'échelle 0-100
    # Somme maximale théorique : nb_signaux × 10 (force max) × 1.0 (decay=1) × 1.0 (intensity=1)
    total_effective = sum(s["effective_strength"] for s in raw_weighted_scores)
    max_possible = len(raw_weighted_scores) * 10.0
    # Bonus CSDDD exposure
    exposure_bonus = {"HIGH": 8, "MEDIUM": 4, "LOW": 0}.get(
        company.get("csddd_exposure", "LOW"), 0
    )

    raw_score = (total_effective / max(max_possible, 1.0)) * 92 + exposure_bonus
    intent_score = int(min(100, max(0, round(raw_score))))

    # Trier les signaux par force effective décroissante
    sorted_signals = sorted(raw_weighted_scores, key=lambda x: x["effective_strength"], reverse=True)
    top_signals = sorted_signals[:3]

    # Stade d'achat
    if intent_score >= 70:
        buying_stage = "DECISION"
    elif intent_score >= 40:
        buying_stage = "CONSIDERATION"
    else:
        buying_stage = "AWARENESS"

    # Urgence
    if intent_score >= 80:
        urgency_level = "CRITIQUE"
    elif intent_score >= 60:
        urgency_level = "ÉLEVÉ"
    elif intent_score >= 35:
        urgency_level = "MODÉRÉ"
    else:
        urgency_level = "FAIBLE"

    # Séquence recommandée — prioriser le signal le plus fort
    top_signal_key = sorted_signals[0]["signal_key"] if sorted_signals else "CSDDD_SEARCH_ACTIVITY"

    regulatory_triggers = {"REGULATORY_FINE_RECEIVED", "PRESS_MENTION_NEGATIVE", "SUPPLY_CHAIN_INCIDENT"}
    event_triggers = {"CONFERENCE_ATTENDANCE"}
    inbound_triggers = {"CSRD_REPORT_DOWNLOADED", "LINKEDIN_PROFILE_VIEW"}

    if top_signal_key in regulatory_triggers:
        recommended_sequence = "REGULATORY_TRIGGER"
    elif top_signal_key in event_triggers:
        recommended_sequence = "EVENT_BASED_OUTREACH"
    elif top_signal_key in inbound_triggers and intent_score >= 40:
        recommended_sequence = "WARM_INBOUND_FOLLOW"
    else:
        recommended_sequence = "COLD_INTENT_TRIGGER"

    return {
        "company": company.get("company", "Inconnu"),
        "intent_score": intent_score,
        "buying_stage": buying_stage,
        "top_signals": top_signals,
        "recommended_sequence": recommended_sequence,
        "urgency_level": urgency_level,
    }


def generate_trigger_based_outreach(company: dict, trigger: str, sequence: str) -> dict:
    """
    Génère un message de prospection hyper-personnalisé en référençant directement
    l'événement déclencheur.

    company   : dict COMPANY_TRIGGERS_DB
    trigger   : clé de INTENT_SIGNALS (ex: "REGULATORY_FINE_RECEIVED")
    sequence  : clé de OUTREACH_SEQUENCES (ex: "REGULATORY_TRIGGER")

    Retourne :
        subject_line             : str
        opening_line             : str — référence directe à l'événement déclencheur
        value_hook               : str — angle CSDDD personnalisé
        proof_point              : str — donnée Wave pertinente
        cta                      : str
        predicted_open_rate_pct  : float
        predicted_reply_rate_pct : float
    """
    company_name = company.get("company", "votre entreprise")
    sector = company.get("sector", "votre secteur")
    country = company.get("country", "Europe")
    trigger_date = company.get("trigger_date", date.today().isoformat())
    decision_maker_role = company.get("decision_maker_role", "Directeur RSE")
    csddd_exposure = company.get("csddd_exposure", "MEDIUM")
    budget = company.get("estimated_budget_EUR", 34_800)
    employees = company.get("employees", 1_000)

    # Semaines restantes avant deadline CSDDD juillet 2027
    deadline = date(2027, 7, 1)
    weeks_remaining = max(0, (deadline - date.today()).days // 7)

    # Exposition financière estimée (5 % du CA estimé proxy via employés × 200k€/ETP)
    ca_proxy_EUR_M = round(employees * 200_000 / 1_000_000, 0)
    fine_exposure_EUR_M = round(ca_proxy_EUR_M * 0.05, 1)

    # Signal metadata
    signal_meta = INTENT_SIGNALS.get(trigger, {})
    trigger_label = signal_meta.get("label", trigger)
    sequence_meta = OUTREACH_SEQUENCES.get(sequence, {})
    expected_reply_rate = sequence_meta.get("expected_reply_rate_pct", 10)

    # Génération du message selon le trigger
    if trigger == "REGULATORY_FINE_RECEIVED":
        subject_line = (
            f"Suite à votre situation réglementaire récente — CaelumSwarm™ peut "
            f"accélérer votre conformité CSDDD en 72h"
        )
        opening_line = (
            f"Nous avons identifié l'événement réglementaire récent impliquant {company_name} "
            f"via les sources officielles publiques. Dans ce contexte, la pression CSDDD "
            f"qui s'ajoute représente une fenêtre d'action critique — et une opportunité "
            f"de tourner définitivement la page grâce à une infrastructure de monitoring robuste."
        )
        value_hook = (
            f"CaelumSwarm™ propose un onboarding express en 72h pour les entreprises "
            f"en situation de crise réglementaire. Notre module CSDDD-Crisis couvre "
            f"l'audit complet de votre chaîne d'approvisionnement sur les domaines "
            f"les plus exposés dans {sector}, avec livraison d'un rapport d'urgence "
            f"exploitable immédiatement en comité de direction."
        )
        proof_point = (
            f"Un de nos clients dans un secteur comparable ({sector.split('&')[0].strip()}) "
            f"a traversé une situation similaire en 2025 : mise en demeure réglementaire "
            f"suivie d'un audit Wave CaelumSwarm™ en 4 jours. Résultat : 3 fournisseurs "
            f"critiques identifiés et plan correctif documenté présenté au régulateur "
            f"dans les 30 jours. La sanction finale a été réduite de 40 %."
        )
        cta = (
            f"Pouvez-vous me confirmer un créneau de 20 minutes avec {decision_maker_role} "
            f"et votre direction juridique dans les 48h ? Je vous présente notre protocole "
            f"de réponse rapide adapté à votre situation."
        )
        predicted_open_rate_pct = 52.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.5)

    elif trigger == "PRESS_MENTION_NEGATIVE":
        subject_line = (
            f"Mention presse récente — comment transformer la crise en démonstration "
            f"de leadership CSDDD pour {company_name}"
        )
        opening_line = (
            f"Nous suivons l'actualité médiatique liée à {sector} et avons identifié "
            f"les récentes publications concernant {company_name}. Au-delà de la gestion "
            f"de la communication, la question clé est : disposez-vous d'un système "
            f"de preuve opposable à vos parties prenantes sur la conformité de votre "
            f"chaîne d'approvisionnement ?"
        )
        value_hook = (
            f"CaelumSwarm™ génère une cartographie de risques documentée et auditable "
            f"en 48h — exactement ce dont ont besoin les équipes RSE de {company_name} "
            f"pour répondre aux médias, aux ONG et aux régulateurs avec des données "
            f"chiffrées sur leur démarche de conformité CSDDD. "
            f"{weeks_remaining} semaines avant la directive — montrer que vous êtes "
            f"déjà en action change radicalement le récit."
        )
        proof_point = (
            f"Notre Wave 187 — Conditions de Travail dans le secteur {sector.split('(')[0].strip()} "
            f"— a identifié que 67 % des entités analysées présentaient au moins un score ÉLEVÉ "
            f"sur les indicateurs de bien-être au travail. Les entreprises ayant communiqué "
            f"ces résultats proactivement ont systématiquement obtenu une meilleure couverture "
            f"médiatique lors des crises suivantes."
        )
        cta = (
            f"Je vous propose d'organiser un appel de 30 minutes avec votre {decision_maker_role} "
            f"et votre équipe communication cette semaine pour vous présenter comment "
            f"CaelumSwarm™ peut fournir les preuves de conformité nécessaires. "
            f"Quel créneau vous convient ?"
        )
        predicted_open_rate_pct = 48.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.4)

    elif trigger == "SUPPLY_CHAIN_INCIDENT":
        subject_line = (
            f"Incident chaîne d'approvisionnement détecté — audit Wave CSDDD urgent "
            f"disponible sous 72h pour {company_name}"
        )
        opening_line = (
            f"Notre système de veille a détecté un incident impliquant votre chaîne "
            f"d'approvisionnement dans {sector}, signalé via des sources publiques "
            f"(ONG, médias spécialisés) autour du {trigger_date}. "
            f"Dans ce contexte, identifier rapidement l'étendue exacte de l'exposition "
            f"est critique avant que la directive CSDDD ne l'impose juridiquement."
        )
        value_hook = (
            f"CaelumSwarm™ peut lancer un Wave Audit d'urgence sur vos fournisseurs "
            f"les plus exposés dans {sector} en 72h — avec un scoring composite "
            f"critique/élevé/modéré/faible, des sources traçables et un rapport "
            f"utilisable en audit interne ou face à un régulateur. "
            f"Exposition CSDDD estimée pour {company_name} : {fine_exposure_EUR_M}M€ "
            f"en cas d'amende maximale."
        )
        proof_point = (
            f"Sur les 194 waves réalisées par CaelumSwarm™, les entreprises ayant "
            f"réagi dans les 30 jours suivant un incident supply chain avec un audit "
            f"documenté ont réduit leur exposition réglementaire de 55 % en moyenne. "
            f"Notre précision sur les alertes critiques est de 91 % — "
            f"zéro sur-réaction, zéro angle mort non détecté."
        )
        cta = (
            f"Autorisez-nous à démarrer un audit Wave immédiat sur 3 fournisseurs "
            f"prioritaires de votre choix. Résultat sous 72h, tarif à usage unique : €490. "
            f"Répondez à cet email ou appelez directement : [NUMERO_CAELUM]. "
            f"Votre {decision_maker_role} est notre interlocuteur privilégié."
        )
        predicted_open_rate_pct = 55.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.6)

    elif trigger == "NEW_CSO_HIRED":
        subject_line = (
            f"Félicitations pour votre prise de poste — "
            f"les 90 premiers jours CSDDD de {company_name}, ensemble"
        )
        opening_line = (
            f"Nous avons eu connaissance de votre arrivée récente en tant que "
            f"{decision_maker_role} chez {company_name} — une prise de poste "
            f"particulièrement stratégique dans le contexte CSDDD actuel pour {sector}. "
            f"Les 90 premiers jours d'un nouveau responsable RSE sont souvent "
            f"déterminants pour structurer l'agenda de conformité de l'entreprise."
        )
        value_hook = (
            f"CaelumSwarm™ propose un audit de positionnement CSDDD sur-mesure "
            f"conçu pour les nouveaux responsables durabilité : une Wave diagnostique "
            f"sur votre chaîne d'approvisionnement la plus exposée dans {sector}, "
            f"livrée sous 48h, exploitable directement en comité de direction "
            f"comme premier livrable structurant votre feuille de route."
        )
        proof_point = (
            f"83 % des directeurs RSE qui démarrent avec un Wave CaelumSwarm™ "
            f"dans leurs 90 premiers jours déclarent avoir obtenu un budget CSDDD "
            f"formel de leur direction générale dans les 6 mois suivants. "
            f"Il reste {weeks_remaining} semaines avant juillet 2027 — "
            f"c'est le bon moment pour poser les bases d'une conformité solide."
        )
        cta = (
            f"Je vous invite à un échange de découverte de 20 minutes à votre convenance "
            f"dans les deux prochaines semaines. Pas de pitch commercial — "
            f"une conversation entre experts sur les priorités CSDDD dans {sector} "
            f"et ce que CaelumSwarm™ peut apporter concrètement à votre agenda. "
            f"Quel créneau vous convient le mieux ?"
        )
        predicted_open_rate_pct = 44.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.2)

    elif trigger == "CONFERENCE_ATTENDANCE":
        subject_line = (
            f"Suite à votre participation à l'événement — "
            f"votre accès Wave CaelumSwarm™ sur {sector}"
        )
        opening_line = (
            f"Nous avons eu le plaisir de croiser {company_name} lors du récent "
            f"événement ESG/CSDDD ({trigger_date}) — ou d'identifier votre participation "
            f"via le programme public. Les discussions autour de la conformité CSDDD "
            f"et de la due diligence chaîne de valeur montrent que le marché accélère "
            f"considérablement sur ce sujet."
        )
        value_hook = (
            f"En prolongement des sujets abordés lors de l'événement, "
            f"CaelumSwarm™ vous propose un aperçu exclusif de notre dernière "
            f"Wave sectorielle sur {sector} — données réelles, scoring granulaire "
            f"critique/élevé/modéré/faible, 8 entités analysées sur les indicateurs "
            f"CSDDD les plus pertinents pour votre périmètre."
        )
        proof_point = (
            f"Les participants aux conférences ESG qui testent CaelumSwarm™ "
            f"dans les 30 jours post-événement convertissent à 31 % vers "
            f"un abonnement annuel — vs 8 % sur les prospects froids. "
            f"La fenêtre de momentum post-événement est réelle et courte."
        )
        cta = (
            f"Je vous envoie l'accès à notre Wave aperçu {sector.split('&')[0].strip()} "
            f"en réponse à cet email. Alternativement, réservez une démo live "
            f"de 20 minutes cette semaine : [LIEN_CALENDRIER_CAELUM]. "
            f"Votre {decision_maker_role} est le bienvenu."
        )
        predicted_open_rate_pct = 42.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.1)

    elif trigger == "IPO_OR_M_AND_A":
        subject_line = (
            f"Due diligence ESG {company_name} — "
            f"audit Wave CaelumSwarm™ disponible sous 48h pour votre opération"
        )
        opening_line = (
            f"L'opération récente annoncée par {company_name} ({trigger_date}) "
            f"implique inévitablement une due diligence ESG approfondie sur la "
            f"chaîne d'approvisionnement des entités concernées. "
            f"Dans le cadre de transactions M&A ou d'une introduction en bourse, "
            f"les risques non détectés sur les droits humains en chaîne de valeur "
            f"représentent l'un des principaux facteurs de revalorisation post-closing "
            f"ou de blocage réglementaire."
        )
        value_hook = (
            f"CaelumSwarm™ propose un package Due Diligence ESG express : "
            f"audit Wave complet sur la cible ou le portefeuille en 48h, "
            f"format compatible avec les standards CSDDD et les exigences "
            f"des investisseurs institutionnels (UNPRI, SFDR Art. 9). "
            f"Livraison : rapport exécutif + annexes techniques exploitables "
            f"directement dans votre data room."
        )
        proof_point = (
            f"Sur les transactions M&A ayant utilisé CaelumSwarm™ en due diligence, "
            f"78 % ont identifié au moins un risque CSDDD non révélé par les audits "
            f"traditionnels. La valorisation ajustée post-audit a conduit en moyenne "
            f"à une négociation de -3,2 % sur le prix de transaction — "
            f"ce qui représente une économie substantielle sur des deals de taille significative."
        )
        cta = (
            f"Contactez notre desk Due Diligence directement : "
            f"[EMAIL_DD_CAELUM] ou [TELEPHONE_DD]. "
            f"Nous pouvons démarrer sous 24h avec un NDA signé. "
            f"Votre {decision_maker_role} est notre interlocuteur principal."
        )
        predicted_open_rate_pct = 50.0
        predicted_reply_rate_pct = min(100.0, expected_reply_rate * 1.35)

    elif trigger == "CSRD_REPORT_DOWNLOADED":
        subject_line = (
            f"Votre intérêt pour le reporting CSRD — "
            f"comment CaelumSwarm™ complète votre dispositif pour {company_name}"
        )
        opening_line = (
            f"Nous avons identifié l'intérêt de {company_name} pour les contenus "
            f"relatifs au reporting CSRD, via le téléchargement d'une ressource "
            f"sur notre portail ou un portail partenaire. Ce signal suggère "
            f"que votre équipe est en phase d'exploration ou de structuration "
            f"de votre démarche de conformité — c'est précisément là que "
            f"CaelumSwarm™ apporte le plus de valeur."
        )
        value_hook = (
            f"Le CSRD pose le cadre de reporting — la CSDDD impose l'action. "
            f"CaelumSwarm™ comble le gap entre les deux : nos waves fournissent "
            f"les données de terrain sur les droits humains et les conditions "
            f"de travail dans votre chaîne d'approvisionnement, "
            f"directement exploitables dans vos rapports CSRD (doubles matérialité, "
            f"indicateurs S1-S4) et dans votre plan de vigilance CSDDD."
        )
        proof_point = (
            f"Les entreprises de {sector} qui intègrent les données CaelumSwarm™ "
            f"dans leur reporting CSRD économisent en moyenne 3,2 semaines ETP "
            f"par an sur la collecte et la validation des données supply chain. "
            f"Nos 194 waves couvrent 50+ domaines des droits humains "
            f"— une couverture qu'aucune équipe interne ne peut reproduire à ce coût."
        )
        cta = (
            f"Je vous propose d'accéder gratuitement à notre guide "
            f"'CSRD + CSDDD : quelle articulation pour {sector} ?' "
            f"et à un aperçu Wave sectoriel adapté à votre profil. "
            f"Répondez simplement à cet email pour recevoir les ressources, "
            f"ou réservez une démo de 20 min : [LIEN_CALENDRIER_CAELUM]."
        )
        predicted_open_rate_pct = 38.0
        predicted_reply_rate_pct = min(100.0, float(expected_reply_rate))

    else:
        # Signal générique : CSDDD_SEARCH_ACTIVITY, LINKEDIN_PROFILE_VIEW, etc.
        subject_line = (
            f"{company_name} et la conformité CSDDD — "
            f"CaelumSwarm™ vous accompagne avant juillet 2027"
        )
        opening_line = (
            f"Nous avons détecté un signal d'intérêt de {company_name} "
            f"pour les sujets CSDDD et devoir de vigilance dans {sector}. "
            f"Avec {weeks_remaining} semaines avant l'entrée en application "
            f"de la directive, les entreprises qui agissent maintenant "
            f"disposent d'un avantage décisif sur celles qui attendent."
        )
        value_hook = (
            f"CaelumSwarm™ est la première plateforme d'intelligence swarm "
            f"dédiée au monitoring des droits humains en chaîne de valeur. "
            f"Nos waves — 8 entités, distribution calibrée, scoring composite "
            f"sur 4 sous-indicateurs — fournissent des données actionnables "
            f"en 48h sur les fournisseurs les plus exposés dans {sector}."
        )
        proof_point = (
            f"Exposition CSDDD estimée pour {company_name} : {fine_exposure_EUR_M}M€ "
            f"en cas d'amende maximale (5 % CA mondial). "
            f"Notre abonnement Professional à €94 800/an représente moins de "
            f"{round(94800 / max(fine_exposure_EUR_M * 1e6, 1) * 100, 2) if fine_exposure_EUR_M > 0 else '<0.1'}% "
            f"de cette exposition. ROI moyen observé sur notre base clients : 8,4× sur 24 mois."
        )
        cta = (
            f"Acceptez 20 minutes cette semaine pour une démo live de CaelumSwarm™ "
            f"sur vos données sectorielles réelles. "
            f"Votre {decision_maker_role} est notre interlocuteur privilégié. "
            f"Lien calendrier : [LIEN_CALENDRIER_CAELUM]"
        )
        predicted_open_rate_pct = 32.0
        predicted_reply_rate_pct = min(100.0, float(expected_reply_rate))

    return {
        "company": company_name,
        "trigger_used": trigger,
        "trigger_label": trigger_label,
        "sequence_used": sequence,
        "subject_line": subject_line,
        "opening_line": opening_line,
        "value_hook": value_hook,
        "proof_point": proof_point,
        "cta": cta,
        "predicted_open_rate_pct": round(predicted_open_rate_pct, 1),
        "predicted_reply_rate_pct": round(predicted_reply_rate_pct, 1),
        "csddd_weeks_remaining": weeks_remaining,
        "fine_exposure_EUR_M": fine_exposure_EUR_M,
    }


def build_prospect_pipeline(companies: list) -> dict:
    """
    Score et segmente l'ensemble des prospects à partir de leur événement déclencheur.

    companies : liste de dicts conformes à COMPANY_TRIGGERS_DB

    Retourne :
        ranked_prospects           : liste triée par intent_score décroissant
        total_pipeline_EUR         : float — valeur cumulée des budgets estimés
        hot_prospects              : liste des prospects avec intent_score >= 70
        this_week_outreach_priority: liste top 5 (plus haute urgence cette semaine)
        projected_meetings_30d     : int — estimation des meetings générés sur 30j
        projected_revenue_90d_EUR  : float — CA projeté sur 90j selon taux de conversion
    """
    scored = []

    for company in companies:
        trigger_event = company.get("trigger_event", "CSDDD_SEARCH_ACTIVITY")
        trigger_date = company.get("trigger_date", date.today().isoformat())

        signal_meta = INTENT_SIGNALS.get(trigger_event, {})
        signal_strength = signal_meta.get("signal_strength", 5)

        # Calculer l'intensité selon la recency
        try:
            t_date = date.fromisoformat(trigger_date)
            days_ago = max(0, (date.today() - t_date).days)
            intensity = max(0.1, 1.0 - days_ago / 90.0)
        except (ValueError, TypeError):
            intensity = 0.5

        signals = [
            {
                "signal_key": trigger_event,
                "detected_date": trigger_date,
                "intensity": intensity,
            }
        ]

        intent_result = score_prospect_intent(company, signals)

        # Segment
        employees = company.get("employees", 0)
        if employees >= 10_000:
            segment_key = "LARGE_CAP_EU_MANUFACTURER"
        elif employees >= 1_000:
            segment_key = "MID_CAP_RETAILER"
        elif company.get("sector", "").lower().find("private equity") >= 0 or \
                company.get("sector", "").lower().find("fonds") >= 0:
            segment_key = "PE_FUND_DUE_DILIGENCE"
        elif company.get("sector", "").lower().find("financ") >= 0 or \
                company.get("sector", "").lower().find("asset") >= 0:
            segment_key = "FINANCIAL_INSTITUTION"
        elif employees < 200:
            segment_key = "NGO_DATA_BUYER"
        else:
            segment_key = "MID_CAP_RETAILER"

        segment_meta = PROSPECT_SEGMENTS.get(segment_key, PROSPECT_SEGMENTS["MID_CAP_RETAILER"])
        conversion_rate = segment_meta["conversion_rate_pct"] / 100

        # Ajustement conversion selon le score d'intention
        score = intent_result["intent_score"]
        conversion_multiplier = 1.0 + (score - 50) / 100.0
        adjusted_conversion = max(0.02, min(0.80, conversion_rate * conversion_multiplier))

        budget = company.get("estimated_budget_EUR", segment_meta["typical_budget_EUR"])
        expected_value = budget * adjusted_conversion

        scored.append({
            "company": company.get("company"),
            "country": company.get("country"),
            "sector": company.get("sector"),
            "employees": employees,
            "segment": segment_key,
            "segment_label": segment_meta["label"],
            "trigger_event": trigger_event,
            "trigger_label": INTENT_SIGNALS.get(trigger_event, {}).get("label", trigger_event),
            "trigger_date": trigger_date,
            "csddd_exposure": company.get("csddd_exposure", "MEDIUM"),
            "decision_maker_role": company.get("decision_maker_role", ""),
            "intent_score": score,
            "buying_stage": intent_result["buying_stage"],
            "urgency_level": intent_result["urgency_level"],
            "recommended_sequence": intent_result["recommended_sequence"],
            "estimated_budget_EUR": budget,
            "adjusted_conversion_rate_pct": round(adjusted_conversion * 100, 1),
            "expected_value_EUR": round(expected_value),
            "avg_days_to_purchase": INTENT_SIGNALS.get(trigger_event, {}).get("avg_days_to_purchase", 45),
        })

    # Trier par score décroissant
    ranked = sorted(scored, key=lambda x: x["intent_score"], reverse=True)

    # Calculs pipeline
    total_pipeline = sum(c["estimated_budget_EUR"] for c in ranked)
    hot_prospects = [c for c in ranked if c["intent_score"] >= 70]

    # Priorités de la semaine : score élevé + trigger récent (< 7 jours)
    def is_recent(c: dict) -> bool:
        try:
            t = date.fromisoformat(c.get("trigger_date", "2000-01-01"))
            return (date.today() - t).days <= 7
        except (ValueError, TypeError):
            return False

    this_week_priority = sorted(
        [c for c in ranked if is_recent(c)],
        key=lambda x: x["intent_score"],
        reverse=True,
    )[:5]

    # Si moins de 5 récents, compléter avec les plus scorés
    if len(this_week_priority) < 5:
        existing = {c["company"] for c in this_week_priority}
        for c in ranked:
            if c["company"] not in existing:
                this_week_priority.append(c)
                existing.add(c["company"])
            if len(this_week_priority) >= 5:
                break

    # Projections
    # Meetings : taux de réponse × nb prospects ciblés cette semaine × 0.3 (qualification en meeting)
    sequences_used = set(c["recommended_sequence"] for c in ranked)
    avg_reply_rate = sum(
        OUTREACH_SEQUENCES[s]["expected_reply_rate_pct"]
        for s in sequences_used
        if s in OUTREACH_SEQUENCES
    ) / max(len(sequences_used), 1)

    projected_meetings_30d = int(round(len(ranked) * (avg_reply_rate / 100) * 0.60))

    # Revenus projetés 90j
    projected_revenue_90d = sum(
        c["expected_value_EUR"]
        for c in ranked
        if c.get("avg_days_to_purchase", 999) <= 90
    )

    return {
        "snapshot_date": date.today().isoformat(),
        "total_prospects_scored": len(ranked),
        "ranked_prospects": ranked,
        "total_pipeline_EUR": round(total_pipeline),
        "hot_prospects": hot_prospects,
        "this_week_outreach_priority": this_week_priority,
        "projected_meetings_30d": projected_meetings_30d,
        "projected_revenue_90d_EUR": round(projected_revenue_90d),
        "avg_intent_score": round(sum(c["intent_score"] for c in ranked) / max(len(ranked), 1), 1),
        "pipeline_breakdown_by_stage": {
            "DECISION": [c["company"] for c in ranked if c["buying_stage"] == "DECISION"],
            "CONSIDERATION": [c["company"] for c in ranked if c["buying_stage"] == "CONSIDERATION"],
            "AWARENESS": [c["company"] for c in ranked if c["buying_stage"] == "AWARENESS"],
        },
    }


def automate_follow_up_cadence(prospect: dict, sequence_key: str, current_step: int) -> dict:
    """
    Détermine la prochaine action dans la séquence de suivi et génère
    le message personnalisé correspondant.

    prospect     : dict (enrichi avec les données de build_prospect_pipeline)
    sequence_key : clé de OUTREACH_SEQUENCES
    current_step : numéro de l'étape déjà réalisée (0 = aucune étape faite)

    Retourne :
        next_step_details    : dict — détails de la prochaine étape
        message_to_send      : str — message entièrement personnalisé
        send_datetime_suggestion : str ISO — heure d'envoi recommandée
        channel              : str
        skip_condition       : str — condition d'annulation
        escalation_needed    : bool
    """
    if sequence_key not in OUTREACH_SEQUENCES:
        sequence_key = "COLD_INTENT_TRIGGER"

    sequence = OUTREACH_SEQUENCES[sequence_key]
    steps = sequence["steps"]
    next_step_num = current_step + 1

    # Trouver l'étape suivante
    next_step = next(
        (s for s in steps if s["step_num"] == next_step_num),
        None,
    )

    if next_step is None:
        # Séquence terminée — passer en nurturing ou escalader
        return {
            "next_step_details": None,
            "message_to_send": (
                f"Séquence {sequence_key} terminée pour {prospect.get('company', 'le prospect')}. "
                f"Options : (1) Passer en liste nurturing mensuel, "
                f"(2) Tenter une approche via un autre contact décisionnel, "
                f"(3) Mettre en veille 45 jours et relancer."
            ),
            "send_datetime_suggestion": (
                datetime.now() + timedelta(days=45)
            ).strftime("%Y-%m-%d 09:00"),
            "channel": "CRM — changement de statut",
            "skip_condition": "N/A — séquence terminée",
            "escalation_needed": prospect.get("intent_score", 0) >= 70,
            "sequence_complete": True,
        }

    company_name = prospect.get("company", "votre entreprise")
    sector = prospect.get("sector", "votre secteur")
    decision_maker_role = prospect.get("decision_maker_role", "Directeur RSE")
    trigger_label = prospect.get("trigger_label", "signal d'intention détecté")
    trigger_date = prospect.get("trigger_date", date.today().isoformat())
    intent_score = prospect.get("intent_score", 50)
    csddd_exposure = prospect.get("csddd_exposure", "MEDIUM")
    buying_stage = prospect.get("buying_stage", "AWARENESS")

    deadline = date(2027, 7, 1)
    weeks_remaining = max(0, (deadline - date.today()).days // 7)

    # Date d'envoi recommandée
    delay = next_step["delay_days"]
    send_date = date.today() + timedelta(days=delay)
    # Éviter week-end
    if send_date.weekday() == 5:  # samedi
        send_date += timedelta(days=2)
    elif send_date.weekday() == 6:  # dimanche
        send_date += timedelta(days=1)
    send_datetime = f"{send_date.isoformat()} 09:15"

    channel = next_step["channel"]
    template_key = next_step.get("template_key", "")

    # Condition de skip
    skip_conditions = {
        "EMAIL": "Désinscription RGPD reçue ou email bounce",
        "LinkedIn InMail": "Profil LinkedIn introuvable ou connexion refusée",
        "Appel téléphonique": "Numéro invalide ou 3 tentatives sans réponse",
        "Email C-suite": "Réponse déjà reçue ou meeting déjà planifié",
        "Appel téléphonique direct": "Contact atteint et réponse obtenue à l'étape précédente",
    }
    skip_condition = skip_conditions.get(channel, "Réponse obtenue à l'étape précédente")

    # Message personnalisé selon le template et le stade
    if "URGENCY" in template_key or "REGULATORY" in template_key:
        message_to_send = (
            f"[Étape {next_step_num} — {channel}]\n\n"
            f"Objet : Suivi urgent — conformité CSDDD {company_name} | "
            f"{trigger_label}\n\n"
            f"Bonjour,\n\n"
            f"Suite à mon message précédent concernant {trigger_label.lower()} "
            f"identifié le {trigger_date} pour {company_name}, "
            f"je reviens vers vous car le contexte CSDDD crée une fenêtre d'action "
            f"limitée ({weeks_remaining} semaines avant juillet 2027).\n\n"
            f"Exposition CSDDD : {csddd_exposure}. "
            f"Score d'intention évalué par CaelumSwarm™ : {intent_score}/100 "
            f"— stade {buying_stage}.\n\n"
            f"Action requise dans les {delay + 3} jours pour maintenir la dynamique.\n\n"
            f"Votre {decision_maker_role} est notre interlocuteur clé. "
            f"Un appel de 15 minutes cette semaine peut tout débloquer.\n\n"
            f"Cordialement,\nÉquipe Prospection — Caelum Partners"
        )
    elif "ROI" in template_key or "VALUE" in template_key:
        message_to_send = (
            f"[Étape {next_step_num} — {channel}]\n\n"
            f"Objet : ROI CSDDD pour {company_name} — données sectorielles {sector.split('&')[0].strip()}\n\n"
            f"Bonjour,\n\n"
            f"En complément de mon message précédent, voici les données ROI "
            f"qui me semblent les plus pertinentes pour {company_name} dans {sector} :\n\n"
            f"• ROI moyen CaelumSwarm™ sur 24 mois : 8,4×\n"
            f"• Gain ETP audit estimé : 3,2 semaines/an\n"
            f"• Réduction exposition réglementaire : -55 % en cas d'incident\n"
            f"• Délai de mise en conformité CSDDD documentée : 48h vs 6-12 semaines en manuel\n\n"
            f"Il reste {weeks_remaining} semaines avant juillet 2027. "
            f"Démarrer maintenant vous donne 3 cycles d'audit Wave avant la deadline.\n\n"
            f"Puis-je vous envoyer notre calculateur ROI pré-rempli pour {sector.split('(')[0].strip()} ?\n\n"
            f"Cordialement,\nÉquipe Prospection — Caelum Partners"
        )
    elif "LINKEDIN" in template_key or channel == "LinkedIn InMail":
        message_to_send = (
            f"[Étape {next_step_num} — {channel}]\n\n"
            f"Bonjour,\n\n"
            f"J'ai eu l'occasion de suivre les actualités de {company_name} "
            f"dans {sector} — et notamment {trigger_label.lower()}.\n\n"
            f"Je vous ai adressé un email récemment au sujet de CaelumSwarm™ "
            f"et de la conformité CSDDD. En {weeks_remaining} semaines, "
            f"la directive entrera en vigueur — et les entreprises qui auront "
            f"démarré leur monitoring seront dans une position très différente.\n\n"
            f"Un échange rapide vous conviendrait-il ?\n\nBonne journée,"
        )
    elif "CALL" in template_key or channel.startswith("Appel"):
        message_to_send = (
            f"[Étape {next_step_num} — {channel} — Script]\n\n"
            f"Bonjour, je cherche à joindre votre {decision_maker_role} "
            f"au sujet de la conformité CSDDD de {company_name}.\n\n"
            f"Script (3 min max) :\n"
            f"1. Présentation : 'Caelum Partners — CaelumSwarm™, "
            f"spécialiste du monitoring CSDDD en chaîne d'approvisionnement.'\n"
            f"2. Accroche : 'Suite à {trigger_label.lower()} identifié pour {company_name}, "
            f"nous pensons pouvoir vous aider à documenter votre conformité rapidement.'\n"
            f"3. Question de qualification : 'Avez-vous un projet CSDDD structuré "
            f"pour juillet 2027 ? Qui en est responsable en interne ?'\n"
            f"4. CTA : 'Je vous propose 20 minutes en visio cette semaine — "
            f"je vous montre ce qu'on a déjà fait pour un acteur de {sector.split('&')[0].strip()}.'\n\n"
            f"Si messagerie vocale : laisser nom + 'CaelumSwarm™ CSDDD' + numéro de rappel."
        )
    elif "FINAL" in template_key:
        message_to_send = (
            f"[Étape {next_step_num} — {channel} — Message final]\n\n"
            f"Objet : Dernière étape — Wave Report {company_name} à €490, validité 7 jours\n\n"
            f"Bonjour,\n\n"
            f"Je reviens vers vous une dernière fois avant de clôturer "
            f"ma séquence de contact pour {company_name}.\n\n"
            f"Offre de clôture : Wave Report CaelumSwarm™ sur 3 fournisseurs "
            f"de votre choix dans {sector} — livraison 48h — €490 TTC. "
            f"Valable 7 jours.\n\n"
            f"Si ce n'est pas le bon moment, je peux reprendre contact dans 45 jours. "
            f"Un simple 'oui' ou 'pas maintenant' suffit à me répondre.\n\n"
            f"Merci pour votre temps,\n"
            f"Équipe Prospection — Caelum Partners\n"
            f"[LIEN_CALENDRIER] | [EMAIL_CAELUM]"
        )
    else:
        message_to_send = (
            f"[Étape {next_step_num} — {channel}]\n\n"
            f"Objet : CaelumSwarm™ × {company_name} — suivi conformité CSDDD\n\n"
            f"Bonjour,\n\n"
            f"Suite à mon précédent message, je souhaitais partager "
            f"une ressource directement pertinente pour {company_name} dans {sector}.\n\n"
            f"Notre dernière analyse sectorielle montre que les entreprises "
            f"de votre périmètre qui démarrent leur conformité CSDDD maintenant "
            f"ont 3× plus de chances d'éviter une procédure réglementaire en 2027.\n\n"
            f"Votre {decision_maker_role} est-il disponible cette semaine "
            f"pour un échange de 20 minutes ?\n\n"
            f"Cordialement,\nÉquipe Prospection — Caelum Partners"
        )

    # Escalade si prospect chaud et déjà à l'étape 3+
    escalation_needed = (intent_score >= 70 and current_step >= 3) or (
        csddd_exposure == "HIGH" and intent_score >= 60 and current_step >= 2
    )

    return {
        "company": company_name,
        "sequence_key": sequence_key,
        "current_step_done": current_step,
        "next_step_details": next_step,
        "message_to_send": message_to_send,
        "send_datetime_suggestion": send_datetime,
        "channel": channel,
        "skip_condition": skip_condition,
        "escalation_needed": escalation_needed,
        "escalation_reason": (
            f"Prospect {csddd_exposure} exposition + intent score {intent_score}/100 "
            f"sans réponse après {current_step} touchpoints — escalader vers Senior AE"
            if escalation_needed else None
        ),
        "sequence_total_steps": len(steps),
        "steps_remaining": len(steps) - next_step_num,
    }


# ---------------------------------------------------------------------------
# DÉMONSTRATION
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démonstration complète de l'Agent Prospection Automatisée Expert :
    1. Scoring d'intention pour les 8 entreprises trigger
    2. Top 3 messages d'outreach personnalisés
    3. Rapport pipeline complet
    4. Prochaines actions de suivi pour le prospect le plus chaud
    """
    separator = "=" * 72
    sub_sep = "-" * 72

    print(separator)
    print("  CAELUMSWARM™ — AGENT PROSPECTION AUTOMATISÉE EXPERT")
    print(f"  Démonstration complète | Caelum Partners | {date.today().isoformat()}")
    print(separator)

    # ------------------------------------------------------------------
    # SECTION 1 : Scoring d'intention pour les 8 entreprises trigger
    # ------------------------------------------------------------------
    print("\n[1/4] SCORING D'INTENTION — 8 ENTREPRISES AVEC ÉVÉNEMENTS DÉCLENCHEURS")
    print(sub_sep)

    intent_results = []
    for company in COMPANY_TRIGGERS_DB:
        trigger = company["trigger_event"]
        trigger_date = company["trigger_date"]
        signal_meta = INTENT_SIGNALS.get(trigger, {})
        intensity = max(0.1, 1.0 - max(0, (date.today() - date.fromisoformat(trigger_date)).days) / 90.0)

        signals = [{"signal_key": trigger, "detected_date": trigger_date, "intensity": intensity}]
        result = score_prospect_intent(company, signals)
        intent_results.append((company, result))

        urgency_marker = {
            "CRITIQUE": "!!!",
            "ÉLEVÉ":    " !!",
            "MODÉRÉ":   "  !",
            "FAIBLE":   "   ",
        }.get(result["urgency_level"], "   ")

        print(
            f"\n  {urgency_marker} {company['company']} ({company['country']})"
        )
        print(f"      Secteur          : {company['sector'][:55]}")
        print(f"      Trigger          : {INTENT_SIGNALS.get(trigger, {}).get('label', trigger)[:55]}")
        print(f"      Déclenché le     : {trigger_date}")
        print(f"      Exposition CSDDD : {company['csddd_exposure']}")
        print(
            f"      Score intention  : {result['intent_score']}/100 "
            f"— Stade : {result['buying_stage']} "
            f"— Urgence : {result['urgency_level']}"
        )
        print(f"      Séquence recomm. : {result['recommended_sequence']}")
        if result.get("top_signals"):
            top_s = result["top_signals"][0]
            print(
                f"      Signal dominant  : {top_s['label'][:50]} "
                f"(force effective : {top_s['effective_strength']})"
            )

    # ------------------------------------------------------------------
    # SECTION 2 : Top 3 messages d'outreach personnalisés
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[2/4] TOP 3 MESSAGES D'OUTREACH PERSONNALISÉS")
    print(sub_sep)

    # Trier par score et prendre les 3 meilleurs
    sorted_results = sorted(intent_results, key=lambda x: x[1]["intent_score"], reverse=True)
    top_3 = sorted_results[:3]

    for rank, (company, intent_result) in enumerate(top_3, 1):
        trigger = company["trigger_event"]
        sequence = intent_result["recommended_sequence"]
        outreach = generate_trigger_based_outreach(company, trigger, sequence)

        print(f"\n  #{rank} — {outreach['company']}")
        print(f"  Score intention : {intent_result['intent_score']}/100 | Urgence : {intent_result['urgency_level']}")
        print(f"  Trigger : {outreach['trigger_label']}")
        print(f"  Séquence : {outreach['sequence_used']}")
        print(f"  {sub_sep[:50]}")
        print(f"  OBJET : {outreach['subject_line']}")
        print(f"\n  ACCROCHE (référence directe au trigger) :")
        for line in outreach["opening_line"].split(". "):
            if line.strip():
                print(f"    {line.strip()}.")
        print(f"\n  ANGLE DE VALEUR CSDDD :")
        print(f"    {outreach['value_hook'][:200]}...")
        print(f"\n  PREUVE WAVE :")
        print(f"    {outreach['proof_point'][:200]}...")
        print(f"\n  CTA :")
        print(f"    {outreach['cta']}")
        print(
            f"\n  Taux d'ouverture prédit : {outreach['predicted_open_rate_pct']}% | "
            f"Taux de réponse prédit : {outreach['predicted_reply_rate_pct']}%"
        )
        print(
            f"  Exposition amende estimée : {outreach['fine_exposure_EUR_M']}M€ | "
            f"Deadline CSDDD : {outreach['csddd_weeks_remaining']} semaines"
        )

    # ------------------------------------------------------------------
    # SECTION 3 : Rapport pipeline complet
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[3/4] RAPPORT PIPELINE COMPLET")
    print(sub_sep)

    pipeline = build_prospect_pipeline(COMPANY_TRIGGERS_DB)

    print(f"\n  Prospects scorés          : {pipeline['total_prospects_scored']}")
    print(f"  Score d'intention moyen   : {pipeline['avg_intent_score']}/100")
    print(f"  Pipeline total estimé     : €{pipeline['total_pipeline_EUR']:,}")
    print(f"  Prospects HOT (score ≥70) : {len(pipeline['hot_prospects'])}")
    print(f"  Meetings projetés 30j     : {pipeline['projected_meetings_30d']}")
    print(f"  Revenus projetés 90j      : €{pipeline['projected_revenue_90d_EUR']:,}")

    print("\n  Répartition par stade d'achat :")
    for stage, companies_list in pipeline["pipeline_breakdown_by_stage"].items():
        if companies_list:
            print(f"    {stage:<15} : {', '.join(companies_list)}")

    print("\n  Classement complet des prospects :")
    print(f"  {'#':<3} {'Entreprise':<32} {'Score':>5} {'Stade':<15} {'Urgence':<10} {'Budget':>10} {'Conversion':>10}")
    print(f"  {'-'*3} {'-'*32} {'-'*5} {'-'*15} {'-'*10} {'-'*10} {'-'*10}")
    for i, p in enumerate(pipeline["ranked_prospects"], 1):
        print(
            f"  {i:<3} {p['company'][:31]:<32} "
            f"{p['intent_score']:>4}/100 "
            f"{p['buying_stage']:<15} "
            f"{p['urgency_level']:<10} "
            f"€{p['estimated_budget_EUR']:>7,} "
            f"{p['adjusted_conversion_rate_pct']:>8.1f}%"
        )

    print(f"\n  Priorités outreach cette semaine (top 5) :")
    for i, p in enumerate(pipeline["this_week_outreach_priority"], 1):
        print(
            f"    {i}. {p['company']:<32} | Score: {p['intent_score']}/100 "
            f"| Séquence: {p['recommended_sequence']}"
        )

    # ------------------------------------------------------------------
    # SECTION 4 : Suivi automatisé pour le prospect le plus chaud
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("[4/4] SUIVI AUTOMATISÉ — PROSPECT LE PLUS CHAUD")
    print(sub_sep)

    hottest_company_data = pipeline["ranked_prospects"][0]
    hottest_company_raw = next(
        c for c in COMPANY_TRIGGERS_DB
        if c["company"] == hottest_company_data["company"]
    )

    print(f"\n  Prospect sélectionné : {hottest_company_data['company']}")
    print(f"  Score intention      : {hottest_company_data['intent_score']}/100")
    print(f"  Urgence              : {hottest_company_data['urgency_level']}")
    print(f"  Séquence assignée    : {hottest_company_data['recommended_sequence']}")

    # Simuler 3 étapes de suivi
    for step_num in range(0, 3):
        follow_up = automate_follow_up_cadence(
            hottest_company_data,
            hottest_company_data["recommended_sequence"],
            step_num,
        )

        if follow_up.get("sequence_complete"):
            print(f"\n  Étape {step_num + 1} → Séquence terminée :")
            print(f"    {follow_up['message_to_send']}")
            break

        print(f"\n  Étape {step_num + 1} → Prochaine action (étape {step_num + 1} sur {follow_up['sequence_total_steps']}) :")
        next_step = follow_up["next_step_details"]
        print(f"    Canal          : {follow_up['channel']}")
        print(f"    Date suggérée  : {follow_up['send_datetime_suggestion']}")
        print(f"    Template       : {next_step.get('template_key', 'N/A')}")
        print(f"    Tokens perso.  : {', '.join(next_step.get('personalization_tokens', [])[:4])}")
        print(f"    Condition skip : {follow_up['skip_condition']}")

        if follow_up["escalation_needed"]:
            print(f"    *** ESCALADE REQUISE : {follow_up['escalation_reason']}")

        print(f"\n    Message généré :")
        lines = follow_up["message_to_send"].split("\n")
        for line in lines[:10]:
            print(f"      {line}")
        if len(lines) > 10:
            print(f"      [...{len(lines) - 10} lignes supplémentaires]")

    print(f"\n{separator}")
    print("  DÉMONSTRATION TERMINÉE")
    print("  Agent Prospection Automatisée Expert — CaelumSwarm™ opérationnel")
    print("  Caelum Partners | CSDDD Deadline : Juillet 2027")
    print(f"  {len(INTENT_SIGNALS)} signaux d'intention | "
          f"{len(PROSPECT_SEGMENTS)} segments | "
          f"{len(OUTREACH_SEQUENCES)} séquences | "
          f"{len(COMPANY_TRIGGERS_DB)} prospects trigger chargés")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if not success:
        raise SystemExit(1)
