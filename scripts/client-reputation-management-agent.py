"""
Agent Gestion & Réputation Clients — surveille, protège et améliore la réputation
des clients CaelumSwarm™ en matière de droits humains et d'ESG. Alerte en cas de
crise, gère le narratif et renforce la réputation positive.
"""

import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

REPUTATION_DIMENSIONS = {
    "ESG_RATING_SCORE": {
        "label": "Score de notation ESG",
        "weight": 0.22,
        "measurement_frequency": "Trimestrielle",
        "data_sources": [
            "MSCI ESG Ratings",
            "Sustainalytics",
            "ISS ESG",
            "Refinitiv ESG Scores",
        ],
        "benchmark_leader_score": 88,
        "impact_on_csddd_compliance": "Critique — indicateur central pour la CSDD et la SFDR",
    },
    "MEDIA_SENTIMENT": {
        "label": "Sentiment médiatique",
        "weight": 0.18,
        "measurement_frequency": "Quotidienne",
        "data_sources": [
            "Meltwater",
            "Mention",
            "Google News API",
            "LexisNexis",
            "Factiva",
        ],
        "benchmark_leader_score": 82,
        "impact_on_csddd_compliance": "Élevé — crises médiatiques peuvent déclencher audits réglementaires",
    },
    "NGO_PERCEPTION": {
        "label": "Perception des ONG",
        "weight": 0.16,
        "measurement_frequency": "Mensuelle",
        "data_sources": [
            "Rapports Amnesty International",
            "Human Rights Watch",
            "Sherpa",
            "Business & Human Rights Resource Centre",
        ],
        "benchmark_leader_score": 79,
        "impact_on_csddd_compliance": "Critique — les ONG sont des parties prenantes clés des procédures CSDD",
    },
    "REGULATORY_STANDING": {
        "label": "Position réglementaire",
        "weight": 0.16,
        "measurement_frequency": "Mensuelle",
        "data_sources": [
            "Registres AMF",
            "Sanctions BCE",
            "Bases de données OFAC",
            "Registre des condamnations DIRECCTE",
        ],
        "benchmark_leader_score": 95,
        "impact_on_csddd_compliance": "Critique — non-conformité réglementaire = risque CSDD direct",
    },
    "INVESTOR_CONFIDENCE": {
        "label": "Confiance des investisseurs",
        "weight": 0.14,
        "measurement_frequency": "Trimestrielle",
        "data_sources": [
            "Enquêtes actionnaires",
            "Flux ESG Bloomberg",
            "Données PRI",
            "Rapports proxy advisors",
        ],
        "benchmark_leader_score": 85,
        "impact_on_csddd_compliance": "Modéré — les investisseurs institutionnels intègrent la conformité CSDD",
    },
    "EMPLOYEE_PERCEPTION": {
        "label": "Perception des employés",
        "weight": 0.08,
        "measurement_frequency": "Semestrielle",
        "data_sources": [
            "Glassdoor",
            "Indeed",
            "Enquêtes internes eNPS",
            "LinkedIn Talent Insights",
        ],
        "benchmark_leader_score": 78,
        "impact_on_csddd_compliance": "Modéré — indicateur de gouvernance sociale interne",
    },
    "SUPPLY_CHAIN_TRANSPARENCY": {
        "label": "Transparence chaîne d'approvisionnement",
        "weight": 0.06,
        "measurement_frequency": "Semestrielle",
        "data_sources": [
            "EcoVadis",
            "Sedex",
            "Open Supply Hub",
            "Rapports Wave CaelumSwarm™",
        ],
        "benchmark_leader_score": 74,
        "impact_on_csddd_compliance": "Critique — exigence de diligence raisonnable chaîne d'approvisionnement CSDD",
    },
}

CRISIS_TYPES = {
    "SUPPLY_CHAIN_SCANDAL": {
        "label": "Scandale chaîne d'approvisionnement",
        "severity": "P1",
        "avg_duration_days": 45,
        "reputation_impact_score": -9,
        "recovery_time_months": 18,
        "first_24h_actions": [
            "Activation cellule de crise — convocation DG, DRH, DAF, DirCom",
            "Audit d'urgence des fournisseurs concernés (suspension préventive)",
            "Préparation déclaration initiale : reconnaissance, engagement, délai de transparence",
            "Notification proactive régulateurs (DIRECCTE, AMF si coté)",
            "Briefing investisseurs institutionnels clés (top 10 actionnaires)",
            "Contact préventif ONG partenaires avant qu'elles ne réagissent publiquement",
            "Gel des publications marketing — revue de tout contenu en attente",
        ],
    },
    "REGULATORY_FINE": {
        "label": "Amende réglementaire",
        "severity": "P2",
        "avg_duration_days": 30,
        "reputation_impact_score": -7,
        "recovery_time_months": 12,
        "first_24h_actions": [
            "Publication communiqué officiel en moins de 4h après notification",
            "Annonce plan de mise en conformité immédiate avec calendrier précis",
            "Réunion conseil d'administration extraordinaire",
            "Briefing analystes financiers et agences de notation ESG",
            "Désignation d'un responsable conformité CSDD dédié",
        ],
    },
    "NGO_CAMPAIGN": {
        "label": "Campagne ONG",
        "severity": "P2",
        "avg_duration_days": 60,
        "reputation_impact_score": -6,
        "recovery_time_months": 9,
        "first_24h_actions": [
            "Prise de contact directe avec l'ONG initiatrice (dialogue, pas confrontation)",
            "Demande d'accès aux preuves documentaires citées",
            "Vérification interne des allégations — audit flash 48h",
            "Préparation réponse factuelle et transparente",
            "Activation réseau d'ONG partenaires pour contre-narratif équilibré",
        ],
    },
    "MEDIA_INVESTIGATION": {
        "label": "Enquête journalistique",
        "severity": "P2",
        "avg_duration_days": 21,
        "reputation_impact_score": -8,
        "recovery_time_months": 10,
        "first_24h_actions": [
            "Réponse rapide et complète aux questions journalistiques (politique door-open)",
            "Désignation unique porte-parole — zéro communication sauvage",
            "Préparation dossier de preuves contradictoires si allégations inexactes",
            "Alerte légale si nécessaire (droit de réponse, voie judiciaire en dernier recours)",
            "Suivi des mentions en temps réel — War Room médiatique",
        ],
    },
    "WHISTLEBLOWER_REPORT": {
        "label": "Signalement lanceur d'alerte",
        "severity": "P1",
        "avg_duration_days": 90,
        "reputation_impact_score": -10,
        "recovery_time_months": 24,
        "first_24h_actions": [
            "Protection légale immédiate du lanceur d'alerte (conformité loi Sapin II)",
            "Ouverture enquête interne indépendante (cabinet externe mandaté)",
            "Séquestration et préservation de toutes preuves numériques",
            "Notification conseil d'administration et comité d'audit",
            "Communication interne transparente aux employés avant fuite externe",
        ],
    },
    "SOCIAL_MEDIA_VIRAL": {
        "label": "Viralité réseaux sociaux",
        "severity": "P3",
        "avg_duration_days": 7,
        "reputation_impact_score": -5,
        "recovery_time_months": 3,
        "first_24h_actions": [
            "Monitoring intensif — tracking hashtags, mentions, sentiment en temps réel",
            "Réponse empathique et humaine dans les 2h sur les plateformes concernées",
            "Identification et engagement des influenceurs clés relayant l'information",
            "Contenu de clarification — thread explicatif ou vidéo de dirigeant",
            "Évaluation viralité secondaire — anticipation reprise médias traditionnels",
        ],
    },
    "INVESTOR_DIVESTMENT": {
        "label": "Désinvestissement investisseurs",
        "severity": "P2",
        "avg_duration_days": 180,
        "reputation_impact_score": -7,
        "recovery_time_months": 15,
        "first_24h_actions": [
            "Identification investisseurs désinvestisseurs et dialogue direct immédiat",
            "Présentation plan d'action ESG renforcé avec jalons mesurables",
            "Roadshow investisseurs ESG pour attirer remplaçants responsables",
            "Publication engagement amélioré sur objectifs Net Zero et droits humains",
            "Rapport de progrès ESG trimestriel accéléré",
        ],
    },
    "EMPLOYEE_STRIKE": {
        "label": "Grève ou mouvement social interne",
        "severity": "P3",
        "avg_duration_days": 14,
        "reputation_impact_score": -5,
        "recovery_time_months": 6,
        "first_24h_actions": [
            "Ouverture immédiate dialogue avec représentants syndicaux",
            "Déclaration DG d'écoute et d'engagement vers résolution rapide",
            "Communication interne authentique aux équipes non-grévistes",
            "Suspension toute communication externe positive — cohérence de posture",
            "Médiation externe si blocage — désignation médiateur neutre agréé",
        ],
    },
}

REPUTATION_ASSETS = {
    "CSDDD_CERTIFICATION": {
        "label": "Certification CSDD (Corporate Sustainability Due Diligence)",
        "trust_boost": 10,
        "acquisition_cost_EUR": 85000,
        "maintenance_annual_EUR": 25000,
        "renewal_years": 3,
        "csddd_alignment_benefit": "Conformité directe — certification reconnue par la Commission Européenne",
    },
    "B_CORP_STATUS": {
        "label": "Statut B Corp",
        "trust_boost": 9,
        "acquisition_cost_EUR": 12000,
        "maintenance_annual_EUR": 8000,
        "renewal_years": 3,
        "csddd_alignment_benefit": "Fort alignement — processus B Impact Assessment couvre les exigences CSDD",
    },
    "UN_GLOBAL_COMPACT": {
        "label": "Adhésion UN Global Compact",
        "trust_boost": 8,
        "acquisition_cost_EUR": 15000,
        "maintenance_annual_EUR": 15000,
        "renewal_years": 1,
        "csddd_alignment_benefit": "Alignement principes directeurs ONU sur les entreprises et les droits de l'homme",
    },
    "ISO_26000_ALIGNMENT": {
        "label": "Alignement ISO 26000 (Responsabilité Sociétale)",
        "trust_boost": 7,
        "acquisition_cost_EUR": 35000,
        "maintenance_annual_EUR": 10000,
        "renewal_years": 5,
        "csddd_alignment_benefit": "Cadre de référence pour la diligence raisonnable en matière de droits humains",
    },
    "WAVE_REPORT_PUBLICATION": {
        "label": "Publication Wave Report CaelumSwarm™",
        "trust_boost": 8,
        "acquisition_cost_EUR": 18000,
        "maintenance_annual_EUR": 18000,
        "renewal_years": 1,
        "csddd_alignment_benefit": "Transparence proactive renforcée — démonstration de diligence raisonnable documentée",
    },
    "TRANSPARENCY_INDEX_RANKING": {
        "label": "Classement Indice de Transparence (Transparency International)",
        "trust_boost": 6,
        "acquisition_cost_EUR": 5000,
        "maintenance_annual_EUR": 3000,
        "renewal_years": 1,
        "csddd_alignment_benefit": "Signal anti-corruption et gouvernance — critère CSDD gouvernance",
    },
    "AWARD_ESG_LEADER": {
        "label": "Prix Leader ESG Sectoriel",
        "trust_boost": 7,
        "acquisition_cost_EUR": 8000,
        "maintenance_annual_EUR": 2000,
        "renewal_years": 1,
        "csddd_alignment_benefit": "Reconnaissance externe indépendante — crédibilité narrative ESG renforcée",
    },
}

STAKEHOLDER_PERCEPTION_MAP = {
    "INVESTORS": {
        "current_perception": "NEUTRAL",
        "influence_score": 10,
        "key_concerns": [
            "Matérialité des risques ESG sur les valorisations",
            "Conformité SFDR et taxonomie verte",
            "Objectifs Net Zero crédibles et chiffrés",
            "Gouvernance anti-corruption",
        ],
        "engagement_frequency": "Trimestrielle (appels résultats + roadshows ESG)",
        "reputation_lever": "Publications d'objectifs ESG chiffrés, notation MSCI AA minimum",
    },
    "REGULATORS": {
        "current_perception": "NEUTRAL",
        "influence_score": 10,
        "key_concerns": [
            "Respect délais de transposition CSDD",
            "Qualité des rapports de diligence raisonnable",
            "Traçabilité chaîne d'approvisionnement",
            "Mécanismes de plainte accessibles",
        ],
        "engagement_frequency": "Mensuelle (veille réglementaire + consultation proactive)",
        "reputation_lever": "Dialogue proactif, signalement volontaire, dépasser les exigences minimales",
    },
    "NGOS": {
        "current_perception": "NEUTRAL",
        "influence_score": 8,
        "key_concerns": [
            "Droits des travailleurs chaîne d'approvisionnement",
            "Impact communautés locales opérations",
            "Déforestation et droits des peuples autochtones",
            "Accès aux recours pour victimes",
        ],
        "engagement_frequency": "Bimensuelle (partenariats + dialogue parties prenantes)",
        "reputation_lever": "Partenariats formels, co-construction mécanismes de plainte, rapports Wave transparents",
    },
    "MEDIA": {
        "current_perception": "NEUTRAL",
        "influence_score": 7,
        "key_concerns": [
            "Greenwashing et écart engagements/réalité",
            "Scandales sociaux ou environnementaux",
            "Opacité sur les pratiques chaîne d'approvisionnement",
            "Cohérence communication interne/externe",
        ],
        "engagement_frequency": "Hebdomadaire (veille médias + relations presse proactives)",
        "reputation_lever": "Transparence radicale, accès journalistes, preuves documentées des engagements",
    },
    "EMPLOYEES": {
        "current_perception": "POSITIVE",
        "influence_score": 6,
        "key_concerns": [
            "Culture d'entreprise inclusive et respectueuse",
            "Alignement valeurs personnelles/valeurs entreprise",
            "Politique de dénonciation sécurisée",
            "Développement compétences et équité salariale",
        ],
        "engagement_frequency": "Continue (canal interne, enquêtes trimestrielles)",
        "reputation_lever": "Programme ambassadeurs internes, politique RSE authentique, engagement sustainability",
    },
    "CUSTOMERS": {
        "current_perception": "POSITIVE",
        "influence_score": 7,
        "key_concerns": [
            "Éthique des produits et services",
            "Traçabilité et origine des matières",
            "Engagement climatique concret",
            "Politique de données personnelles et vie privée",
        ],
        "engagement_frequency": "Continue (enquêtes NPS, réseaux sociaux, service client)",
        "reputation_lever": "Labels et certifications visibles, storytelling authentique, rapports impact annuels",
    },
}

# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

def calculate_reputation_score(client: dict, dimension_scores: dict) -> dict:
    """
    Calcule l'indice de réputation pondéré (0-100) sur 7 dimensions.

    Args:
        client: dict avec au moins 'name', 'industry', 'size'
        dimension_scores: dict {dimension_key: score (0-100)}

    Returns:
        dict avec overall_score, grade, dimension_breakdown, vs_sector_benchmark,
        trend, alerts
    """
    total_weighted = 0.0
    dimension_breakdown = {}
    alerts = []
    total_benchmark = 0.0

    for dim_key, config in REPUTATION_DIMENSIONS.items():
        raw_score = dimension_scores.get(dim_key, 50)
        weight = config["weight"]
        weighted = raw_score * weight
        total_weighted += weighted
        benchmark = config["benchmark_leader_score"]
        total_benchmark += benchmark * weight
        gap_to_leader = benchmark - raw_score

        dimension_breakdown[dim_key] = {
            "label": config["label"],
            "score": round(raw_score, 1),
            "weight_pct": round(weight * 100, 1),
            "weighted_contribution": round(weighted, 2),
            "benchmark_leader": benchmark,
            "gap_to_leader": round(gap_to_leader, 1),
            "measurement_frequency": config["measurement_frequency"],
            "impact_on_csddd": config["impact_on_csddd_compliance"],
        }

        # Alertes par dimension
        if raw_score < 30:
            alerts.append({
                "level": "CRITIQUE",
                "dimension": config["label"],
                "score": raw_score,
                "message": (
                    f"Score critique ({raw_score}/100) en {config['label']} — "
                    "intervention immédiate requise"
                ),
            })
        elif raw_score < 50:
            alerts.append({
                "level": "ATTENTION",
                "dimension": config["label"],
                "score": raw_score,
                "message": (
                    f"Score insuffisant ({raw_score}/100) en {config['label']} — "
                    "plan d'amélioration prioritaire"
                ),
            })

    overall_score = round(total_weighted, 2)
    sector_benchmark_avg = round(total_benchmark, 2)
    vs_benchmark = round(overall_score - sector_benchmark_avg, 2)

    # Grade
    if overall_score >= 90:
        grade = "A+"
    elif overall_score >= 80:
        grade = "A"
    elif overall_score >= 65:
        grade = "B"
    elif overall_score >= 50:
        grade = "C"
    elif overall_score >= 35:
        grade = "D"
    else:
        grade = "F"

    # Tendance simulée basée sur le score et le secteur
    if overall_score >= sector_benchmark_avg + 5:
        trend = "IMPROVING"
    elif overall_score <= sector_benchmark_avg - 10:
        trend = "DECLINING"
    else:
        trend = "STABLE"

    # Alerte globale si score très bas
    if overall_score < 40:
        alerts.insert(0, {
            "level": "CRITIQUE GLOBAL",
            "dimension": "Réputation globale",
            "score": overall_score,
            "message": (
                f"Score de réputation global critique ({overall_score}/100) — "
                "activation protocole de gestion de crise recommandée"
            ),
        })

    return {
        "client_name": client.get("name", "Inconnu"),
        "industry": client.get("industry", "Non spécifié"),
        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
        "overall_score": overall_score,
        "grade": grade,
        "grade_label": {
            "A+": "Excellence ESG — Leader sectoriel",
            "A": "Très bonne réputation — Au-dessus des standards",
            "B": "Bonne réputation — Conforme aux attentes",
            "C": "Réputation moyenne — Axes d'amélioration identifiés",
            "D": "Réputation fragile — Vulnérabilités significatives",
            "F": "Réputation en crise — Intervention urgente requise",
        }.get(grade, "Non classé"),
        "dimension_breakdown": dimension_breakdown,
        "vs_sector_benchmark": {
            "sector_avg_score": sector_benchmark_avg,
            "gap": vs_benchmark,
            "position": "AU-DESSUS" if vs_benchmark > 0 else "EN-DESSOUS",
        },
        "trend": trend,
        "trend_label": {
            "IMPROVING": "Tendance positive — momentum à consolider",
            "STABLE": "Tendance stable — vigilance maintenue",
            "DECLINING": "Tendance négative — actions correctives urgentes",
        }.get(trend, "Indéterminé"),
        "alerts": alerts,
        "alerts_count": len(alerts),
        "caelumswarm_recommendation": (
            "Publication Wave Report recommandée — renforcement transparence proactive"
            if overall_score < 70
            else "Maintien programme Wave Reports — consolidation position de leader ESG"
        ),
    }


def design_crisis_response_plan(crisis_type: str, client: dict, severity: int) -> dict:
    """
    Crée un plan de réponse à la crise en 5 phases.

    Args:
        crisis_type: clé dans CRISIS_TYPES
        client: dict avec 'name', 'industry', 'size', 'headquarters'
        severity: entier 1-4 (1 = le plus grave)

    Returns:
        dict avec 5 phases : Detect, Assess, Respond, Monitor, Recover
    """
    crisis_config = CRISIS_TYPES.get(crisis_type, CRISIS_TYPES["MEDIA_INVESTIGATION"])
    client_name = client.get("name", "Client")
    industry = client.get("industry", "Secteur non spécifié")
    headquarters = client.get("headquarters", "France")

    severity_label = {1: "P1 — Critique", 2: "P2 — Élevé", 3: "P3 — Modéré", 4: "P4 — Faible"}.get(
        severity, "P2 — Élevé"
    )
    impact = crisis_config["reputation_impact_score"]
    recovery_months = crisis_config["recovery_time_months"]

    now = datetime.now()

    phases = {
        "PHASE_1_DETECT": {
            "name": "Phase 1 — Détection & Alerte",
            "timeline_hours": "0-2h",
            "deadline": (now + timedelta(hours=2)).strftime("%H:%M — %d/%m/%Y"),
            "actions": [
                "Activation système de veille multicanal (médias, réseaux sociaux, régulateurs)",
                "Notification immédiate DirCom + DG + Conseil Juridique",
                f"Ouverture War Room crise — {client_name} — salle dédiée ou Teams/Zoom sécurisé",
                "Collecte premières données : origine, périmètre, acteurs impliqués",
                "Activation monitoring CaelumSwarm™ — tableau de bord réputation temps réel",
            ],
            "spokespersons": ["Directeur Communication (DirCom)", "Responsable Veille Stratégique"],
            "key_messages": [
                "Aucune déclaration publique avant validation cellule de crise",
                "Message interne CEO : 'Nous prenons la situation très au sérieux'",
            ],
            "channels": ["Interne uniquement — Teams/email sécurisé"],
            "success_criteria": [
                "Cellule de crise activée dans les 2h",
                "Périmètre de la crise délimité",
                "Porte-parole unique désigné",
            ],
        },
        "PHASE_2_ASSESS": {
            "name": "Phase 2 — Évaluation & Décision",
            "timeline_hours": "2-6h",
            "deadline": (now + timedelta(hours=6)).strftime("%H:%M — %d/%m/%Y"),
            "actions": [
                f"Évaluation impact financier préliminaire — modélisation scénarios A/B/C",
                f"Scoring réputationnel : impact estimé {impact}/10 pts de réputation",
                "Analyse juridique : obligations légales de communication (AMF, CSDD, RGPD)",
                "Inventaire parties prenantes impactées par ordre de priorité",
                "Sélection stratégie de réponse : proactive / réactive / silence calculé",
                crisis_config["first_24h_actions"][0] if crisis_config["first_24h_actions"] else "",
            ],
            "spokespersons": [
                "DG ou Directeur Général Délégué",
                "DirCom",
                "Directeur Juridique",
                "DRH (si impact social)",
            ],
            "key_messages": [
                f"{client_name} prend connaissance de la situation avec la plus grande attention",
                "Une enquête interne indépendante a été immédiatement diligentée",
                f"Nos équipes travaillent à établir les faits avec rigueur et transparence",
            ],
            "channels": [
                "Communiqué de presse initial (si P1/P2)",
                "Site institutionnel — page dédiée crise",
                "Email direct aux investisseurs clés",
            ],
            "success_criteria": [
                "Stratégie de réponse validée par DG + Conseil Juridique",
                "Messages clés approuvés",
                "Plan d'actions 48h formalisé",
            ],
        },
        "PHASE_3_RESPOND": {
            "name": "Phase 3 — Réponse Publique & Gestion Narrative",
            "timeline_hours": "6-48h",
            "deadline": (now + timedelta(hours=48)).strftime("%H:%M — %d/%m/%Y"),
            "actions": [
                "Publication déclaration officielle — ton : empathique, responsable, engagé",
                f"Activation {len(crisis_config['first_24h_actions'])} actions prioritaires 24h",
                "Briefing personnalisé top 5 médias + agences de presse",
                "Notification proactive régulateurs sectoriels ({})".format(
                    "AMF + DIRECCTE" if headquarters == "France" else "Régulateurs locaux"
                ),
                "Communication interne renforcée — FAQ employés, message CEO vidéo",
                "Engagement ONG partenaires pour dialogue constructif",
                "Publication page FAQ dédiée sur site web institutionnel",
                "Rapport de situation toutes les 6h à la cellule de crise",
            ],
            "spokespersons": [
                f"DG {client_name} — voix principale, responsabilité assumée",
                "Expert externe indépendant (crédibilité tierce partie)",
                f"Directeur RSE/ESG — expertise technique",
            ],
            "key_messages": [
                f"{client_name} assume l'entière responsabilité de la situation",
                "Des mesures concrètes et immédiates sont mises en place",
                "Nous nous engageons à une totale transparence tout au long du processus",
                "Un rapport Wave CaelumSwarm™ indépendant sera publié dans les 60 jours",
            ],
            "channels": [
                "Conférence de presse (si P1)",
                "Site web — espace dédié mis à jour toutes les 24h",
                "LinkedIn officiel + Twitter/X",
                "Email direct actionnaires",
                "Intranet employés",
            ],
            "success_criteria": [
                "Sentiment médiatique stabilisé (pas d'aggravation)",
                "Zéro déclaration contradictoire de l'entreprise",
                "Dialogue ouvert avec ONG et régulateurs",
                "Engagement public avec plan d'actions daté",
            ],
        },
        "PHASE_4_MONITOR": {
            "name": "Phase 4 — Surveillance & Ajustement",
            "timeline_hours": f"48h — {crisis_config['avg_duration_days']} jours",
            "deadline": (now + timedelta(days=crisis_config["avg_duration_days"])).strftime(
                "%d/%m/%Y"
            ),
            "actions": [
                "Monitoring sentiment médias 24/7 — alertes en temps réel",
                "Suivi indicateurs réputation : score ESG, mentions, sentiment ONG",
                "Rapports de situation hebdomadaires au Comité Exécutif",
                "Ajustement narratif si nouveaux éléments émergent",
                "Mise à jour régulière page dédiée crise — preuves de progrès",
                "Engagement continu parties prenantes — newsletter mensuelle de suivi",
                "Veille concurrentielle — comparaison gestion crise secteur",
                "Préparation rapport post-crise CaelumSwarm™ Wave Analysis",
            ],
            "spokespersons": [
                "DirCom — pilotage quotidien",
                "Responsable Relations Investisseurs — suivi marchés",
                "Responsable Affaires Publiques — suivi régulateurs",
            ],
            "key_messages": [
                "Rapport de progrès concret : [X actions complétées sur Y]",
                "Transparence continue — prochaine mise à jour : [date]",
                f"Engagement de publication Wave Report CaelumSwarm™ indépendant",
            ],
            "channels": [
                "Dashboard public de suivi (site web)",
                "Rapports mensuels investisseurs",
                "Newsletters parties prenantes",
                "Social listening + engagement",
            ],
            "success_criteria": [
                "Score médiatique en amélioration constante",
                "Zéro escalade réglementaire supplémentaire",
                "Maintien notation ESG (pas de dégradation)",
                "Dialogue productif avec parties prenantes critiques",
            ],
        },
        "PHASE_5_RECOVER": {
            "name": "Phase 5 — Rétablissement & Renforcement",
            "timeline_hours": f"Mois 1 — Mois {recovery_months}",
            "deadline": (now + timedelta(days=recovery_months * 30)).strftime("%d/%m/%Y"),
            "actions": [
                f"Lancement programme de reconstruction réputation — objectif score +{abs(impact)} pts",
                "Publication Wave Report CaelumSwarm™ complet — transparence totale sur les actions menées",
                "Certification ESG renforcée — acquisition CSDDD ou B Corp si non détenu",
                "Campagne 'Preuves de transformation' — storytelling basé sur données factuelles",
                f"Roadshow investisseurs ESG — re-engagement fonds ISR après {recovery_months//2} mois",
                "Partenariats ONG formalisés — comité consultatif parties prenantes",
                "Formation intensive équipes — culture RSE et prévention des risques",
                "Rapport annuel renforcé — section dédiée leçons apprises et engagements",
                "Objectif : retour score réputation pré-crise + 5 points bonus leadership",
            ],
            "spokespersons": [
                "DG — engagement personnel long terme",
                "Ambassadeurs internes formés",
                "Partenaires ONG co-signataires",
                "Analystes ESG indépendants (validation externe)",
            ],
            "key_messages": [
                f"{client_name} est sorti(e) de cette crise transformé(e) et renforcé(e)",
                "La transparence et la responsabilité sont désormais inscrites dans notre ADN",
                "Nos Wave Reports CaelumSwarm™ garantissent une surveillance indépendante continue",
                "Nous sommes devenus un modèle sectoriel de gestion responsable",
            ],
            "channels": [
                "Rapport annuel RSE/CSDD dédié",
                "Campagne communication institutionnelle",
                "Conférence sectorielle — témoignage transformation",
                "Médias spécialisés ESG et droits humains",
                "LinkedIn thought leadership DG",
            ],
            "success_criteria": [
                f"Score réputation global ≥ score pré-crise dans les {recovery_months} mois",
                "Notation ESG améliorée vs avant-crise",
                "Couverture médiatique redevenue positive (>70% positif)",
                "Certifications ESG nouvelles obtenues",
                "Publication Wave Report CaelumSwarm™ citée comme référence sectorielle",
            ],
        },
    }

    return {
        "plan_id": f"CRP-{client_name[:3].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "client_name": client_name,
        "industry": industry,
        "crisis_type": crisis_config["label"],
        "crisis_type_key": crisis_type,
        "severity_level": severity_label,
        "estimated_reputation_impact": f"{impact} points (score /100)",
        "estimated_recovery_time": f"{recovery_months} mois",
        "avg_crisis_duration": f"{crisis_config['avg_duration_days']} jours",
        "plan_created_at": now.strftime("%Y-%m-%d %H:%M"),
        "phases": phases,
        "total_phases": 5,
        "guiding_principle": (
            "Transparence radicale + responsabilité assumée + preuves concrètes = "
            "récupération réputationnelle accélérée. Les Wave Reports CaelumSwarm™ "
            "constituent la preuve de diligence raisonnable la plus crédible disponible."
        ),
        "caelumswarm_asset": {
            "wave_report_role": "Preuve externe indépendante de transformation — Phase 3 à 5",
            "publication_timeline": "J+60 maximum après déclenchement crise",
            "expected_trust_boost": "+8 points de confiance parties prenantes",
        },
    }


def build_reputation_protection_strategy(
    client: dict, current_score: float, target_score: float
) -> dict:
    """
    Conçoit un bouclier de réputation proactif pour atteindre le score cible.

    Args:
        client: dict avec 'name', 'industry', 'size', 'annual_revenue_EUR'
        current_score: score actuel (0-100)
        target_score: score visé (0-100)

    Returns:
        dict avec assets prioritarisés, piliers narratifs, calendrier contenu,
        ambassadeurs, plan relations réglementaires
    """
    client_name = client.get("name", "Client")
    industry = client.get("industry", "Secteur")
    revenue = client.get("annual_revenue_EUR", 50_000_000)
    gap = round(target_score - current_score, 1)

    # Budget réputation suggéré : 0.15-0.3% du CA selon le gap
    budget_pct = 0.002 if gap > 20 else 0.0015
    suggested_budget = round(revenue * budget_pct)

    # Prioritisation des assets par ROI (trust_boost / coût total 3 ans)
    assets_with_roi = []
    for asset_key, asset in REPUTATION_ASSETS.items():
        total_cost_3y = asset["acquisition_cost_EUR"] + (asset["maintenance_annual_EUR"] * 3)
        roi_score = round((asset["trust_boost"] * 100000) / max(total_cost_3y, 1), 2)
        assets_with_roi.append({
            "asset_key": asset_key,
            "label": asset["label"],
            "trust_boost": asset["trust_boost"],
            "acquisition_cost_EUR": asset["acquisition_cost_EUR"],
            "maintenance_annual_EUR": asset["maintenance_annual_EUR"],
            "total_cost_3y_EUR": total_cost_3y,
            "renewal_years": asset["renewal_years"],
            "roi_score": roi_score,
            "csddd_alignment_benefit": asset["csddd_alignment_benefit"],
            "priority_rank": 0,
        })

    assets_with_roi.sort(key=lambda x: x["roi_score"], reverse=True)
    for i, asset in enumerate(assets_with_roi):
        asset["priority_rank"] = i + 1

    # Sélection des 4 assets prioritaires dans le budget
    cumulative_cost = 0
    prioritized_assets = []
    for asset in assets_with_roi:
        if cumulative_cost + asset["acquisition_cost_EUR"] <= suggested_budget:
            prioritized_assets.append(asset)
            cumulative_cost += asset["acquisition_cost_EUR"]
            if len(prioritized_assets) >= 4:
                break

    # Piliers narratifs (3 messages clés)
    narrative_pillars = [
        {
            "pillar_id": 1,
            "name": "Leader de Transparence Droits Humains",
            "core_message": (
                f"{client_name} publie chaque trimestre un Wave Report CaelumSwarm™ indépendant "
                "démontrant notre diligence raisonnable sur toute la chaîne de valeur — "
                "au-delà des obligations légales CSDD."
            ),
            "proof_points": [
                "Rapports Wave CaelumSwarm™ publics et vérifiables",
                "Mécanisme de plainte accessible à toutes les parties prenantes",
                "Score transparence chaîne d'approvisionnement publié annuellement",
            ],
            "target_audiences": ["Régulateurs", "ONG", "Médias spécialisés ESG"],
            "channels": ["Site web — hub transparence", "LinkedIn", "Rapports réglementaires"],
        },
        {
            "pillar_id": 2,
            "name": "Partenaire de Confiance Investisseurs ESG",
            "core_message": (
                f"Avec une notation ESG cible de {target_score}/100 et des certifications "
                "internationales reconnues, {client_name} offre le profil de risque ESG "
                "le plus solide de son secteur.".format(client_name=client_name)
            ),
            "proof_points": [
                f"Objectif score ESG {target_score}/100 dans 18 mois",
                "Certifications CSDDD + B Corp en cours d'acquisition",
                "Rapport Climate TCFD publié annuellement",
            ],
            "target_audiences": ["Investisseurs institutionnels", "Fonds ISR", "Proxy advisors"],
            "channels": ["Roadshow investisseurs", "Rapports trimestriels", "IR website"],
        },
        {
            "pillar_id": 3,
            "name": "Employeur Responsable & Culture ESG Authentique",
            "core_message": (
                f"Chez {client_name}, la responsabilité n'est pas un département — "
                "c'est notre culture. Nos employés sont les premiers ambassadeurs "
                "de notre engagement pour les droits humains et la durabilité."
            ),
            "proof_points": [
                "Programme Ambassadeurs RSE internes — 100 employés formés",
                "Score eNPS (engagement employés) publié en transparence",
                "Plan formation droits humains pour 100% des managers d'ici 12 mois",
            ],
            "target_audiences": ["Candidats", "Employés actuels", "Médias RH et sociaux"],
            "channels": ["Glassdoor", "LinkedIn", "Campus recruitment", "Intranet"],
        },
    ]

    # Calendrier éditorial thématique (12 mois)
    content_calendar_themes = [
        {"month": "Janvier", "theme": "Bilan ESG annuel & objectifs", "format": "Rapport annuel + conférence presse", "pillar": 2},
        {"month": "Février", "theme": "Droits humains chaîne approvisionnement", "format": "Wave Report CaelumSwarm™ Q4", "pillar": 1},
        {"month": "Mars", "theme": "Égalité & inclusion (Journée 8 mars)", "format": "Étude interne + engagement public", "pillar": 3},
        {"month": "Avril", "theme": "Transparence fournisseurs", "format": "Cartographie chaîne publiée", "pillar": 1},
        {"month": "Mai", "theme": "Résultats AG & vote ESG actionnaires", "format": "Rapport développement durable", "pillar": 2},
        {"month": "Juin", "theme": "Ambitions climatiques (avant COP)", "format": "Wave Report CaelumSwarm™ Q1 + roadmap Net Zero", "pillar": 2},
        {"month": "Juillet", "theme": "Bilan mi-année & progrès certifications", "format": "Rapport mi-parcours", "pillar": 1},
        {"month": "Août", "theme": "Communautés locales & impact territorial", "format": "Témoignages & données impact", "pillar": 3},
        {"month": "Septembre", "theme": "Rentrée RSE — engagement employés", "format": "Wave Report CaelumSwarm™ Q2 + forum interne", "pillar": 3},
        {"month": "Octobre", "theme": "Mois de l'engagement (tendances ESG)", "format": "Tribune CEO + position paper", "pillar": 2},
        {"month": "Novembre", "theme": "Droits humains (avant Journée 10 déc.)", "format": "Wave Report CaelumSwarm™ Q3 + étude impact", "pillar": 1},
        {"month": "Décembre", "theme": "Engagements 2026 & vision long terme", "format": "Lettre ouverte DG aux parties prenantes", "pillar": 3},
    ]

    # Programme ambassadeurs
    ambassador_activations = [
        {
            "type": "Ambassadeurs Internes",
            "nombre_cible": 50,
            "profils": ["Managers middle", "Experts ESG", "Représentants syndicaux volontaires"],
            "formation": "Programme 2 jours : droits humains, CSDD, communication responsable",
            "missions": ["Témoignages LinkedIn", "Forums sectoriels", "Accueil visites parties prenantes"],
            "kpis": ["Posts LinkedIn mensuels", "Score perception interne", "Candidatures reçues via ambassadeurs"],
        },
        {
            "type": "Partenaires ONG Co-signataires",
            "nombre_cible": 3,
            "profils": ["ONG droits humains reconnue", "Association environnementale crédible", "Think tank ESG"],
            "formation": "Co-construction mécanisme de plainte et indicateurs de suivi",
            "missions": ["Co-publication rapports", "Validation indépendante engagements", "Participation comité consultatif"],
            "kpis": ["Déclarations positives publiées", "Score perception ONG", "Rapports co-signés"],
        },
        {
            "type": "Experts Académiques & Think Tanks",
            "nombre_cible": 5,
            "profils": ["Chercheurs droits humains", "Économistes ESG", "Juristes CSDD"],
            "formation": "N/A — consultation rémunérée",
            "missions": ["Validation méthodologique Wave Reports", "Tribunes académiques", "Conférences sectorielles"],
            "kpis": ["Citations académiques", "Invitations conférences", "Score crédibilité narrative"],
        },
    ]

    # Plan relations réglementaires
    regulatory_relationship_plan = {
        "philosophy": "Dépasser les obligations — être acteur de la co-construction réglementaire",
        "target_regulators": [
            "Commission Européenne (DG JUST — CSDD)",
            "AMF (si entité cotée)",
            "ADEME (environnement)",
            "DIRECCTE / DREETS (droit social)",
            "AFA (Agence Française Anticorruption)",
        ],
        "engagement_actions": [
            "Consultation proactive sur projets de textes — position papers",
            "Participation groupes de travail sectoriels CSDD",
            "Partage volontaire de données Wave Reports aux autorités",
            "Organisation table ronde annuelle 'Pratiques de diligence raisonnable'",
            "Rapport de conformité CSDD publié avant délai légal",
        ],
        "quarterly_milestones": {
            "Q1": "Mapping complet obligations réglementaires + audit gap CSDD",
            "Q2": "Premier rapport CSDD publié + notification régulateurs",
            "Q3": "Participation consultation publique CSDD Commission Européenne",
            "Q4": "Bilan conformité + engagement objectifs N+1 avec régulateurs",
        },
    }

    return {
        "strategy_id": f"RPS-{client_name[:3].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "client_name": client_name,
        "industry": industry,
        "current_score": current_score,
        "target_score": target_score,
        "gap_to_close": gap,
        "estimated_timeframe_months": 18 if gap > 20 else 12,
        "suggested_annual_budget_EUR": suggested_budget,
        "reputation_assets_to_acquire": prioritized_assets,
        "total_assets_acquisition_cost_EUR": cumulative_cost,
        "narrative_pillars": narrative_pillars,
        "content_calendar_themes": content_calendar_themes,
        "ambassador_activations": ambassador_activations,
        "regulatory_relationship_plan": regulatory_relationship_plan,
        "wave_report_centrality": {
            "role": "Colonne vertébrale de la stratégie — preuve de transparence proactive",
            "frequency": "Trimestrielle — 4 Wave Reports CaelumSwarm™ par an",
            "expected_trust_delta": "+8 points de score de confiance sur 12 mois",
            "unique_value": (
                "La publication proactive de Wave Reports avant toute obligation légale "
                "positionne le client comme leader de la transparence — non comme suiveur réglementaire"
            ),
        },
        "expected_outcomes_12m": {
            "score_projection": round(current_score + gap * 0.65, 1),
            "media_sentiment_improvement": "+25 pts de sentiment positif",
            "investor_esg_interest": "+30% d'intérêt fonds ISR",
            "regulatory_risk_reduction": "-40% de probabilité de mise en cause réglementaire",
        },
    }


def monitor_reputation_signals(client_name: str, industry: str) -> dict:
    """
    Simule la surveillance en temps réel des signaux de réputation.

    Args:
        client_name: nom du client
        industry: secteur d'activité

    Returns:
        dict avec signal_summary, trending_topics, risk_alerts, recommended_actions,
        next_monitoring_check_hours
    """
    random.seed(hash(client_name + industry) % 10000)

    # Simulation de signaux par canal
    channels_data = {
        "Médias traditionnels": {
            "volume": random.randint(8, 45),
            "positive": random.randint(3, 20),
            "negative": random.randint(0, 12),
            "neutral": 0,
        },
        "Réseaux sociaux (LinkedIn/Twitter)": {
            "volume": random.randint(25, 200),
            "positive": random.randint(10, 80),
            "negative": random.randint(2, 40),
            "neutral": 0,
        },
        "Forums ONG & Rapports OSC": {
            "volume": random.randint(2, 15),
            "positive": random.randint(0, 5),
            "negative": random.randint(0, 8),
            "neutral": 0,
        },
        "Publications réglementaires": {
            "volume": random.randint(1, 8),
            "positive": random.randint(0, 3),
            "negative": random.randint(0, 4),
            "neutral": 0,
        },
        "Glassdoor & avis employés": {
            "volume": random.randint(3, 25),
            "positive": random.randint(1, 12),
            "negative": random.randint(0, 8),
            "neutral": 0,
        },
    }

    for channel in channels_data.values():
        channel["neutral"] = max(0, channel["volume"] - channel["positive"] - channel["negative"])

    # Agrégation
    total_positive = sum(c["positive"] for c in channels_data.values())
    total_negative = sum(c["negative"] for c in channels_data.values())
    total_neutral = sum(c["neutral"] for c in channels_data.values())
    total_volume = total_positive + total_negative + total_neutral

    sentiment_score = round((total_positive - total_negative) / max(total_volume, 1) * 100, 1)

    # Sujets tendance simulés selon le secteur
    trending_topic_pool = {
        "Manufacturing": [
            ("Droits des travailleurs usines sous-traitants Asie du Sud", -6),
            (f"{client_name} publie son bilan carbone 2025", +4),
            ("Tensions syndicales secteur manufacturier Europe", -3),
            (f"Rapport Wave CaelumSwarm™ {client_name} : score transparence 82/100", +7),
            ("Nouvelle réglementation CSDD — impact chaîne approvisionnement", -2),
        ],
        "Finance": [
            ("Greenwashing accusations fonds ESG européens", -5),
            (f"{client_name} rejoint UN Global Compact", +5),
            ("Dégradation notation ESG acteurs financiers traditionnels", -4),
            (f"Rapport ESG {client_name} salué par PRI", +6),
            ("Exigences SFDR Niveau 2 — adaptation en cours secteur", -1),
        ],
        "Retail": [
            ("Conditions travail fournisseurs fast fashion — enquête", -8),
            (f"{client_name} publie cartographie complète fournisseurs", +6),
            ("Plastiques et emballages — pression consommateurs", -3),
            (f"B Corp certification {client_name} — réaction positive clients", +7),
            ("Inflation et achats responsables : enquête consommateurs", -2),
        ],
    }

    industry_topics = trending_topic_pool.get(
        industry,
        [
            (f"{client_name} — couverture ESG positive", +4),
            ("Droits humains chaîne valeur — tendance réglementaire", -2),
            (f"Wave Report CaelumSwarm™ {client_name} publié", +6),
            ("Pressions syndicales secteur", -3),
            ("Investisseurs ISR renforcent critères ESG", -1),
        ],
    )

    # Sélection aléatoire de 3-4 sujets actifs
    n_topics = random.randint(3, min(5, len(industry_topics)))
    selected_topics = random.sample(industry_topics, n_topics)
    trending_topics = [
        {
            "topic": topic,
            "signal_score": score,
            "sentiment": "POSITIF" if score > 0 else ("NEUTRE" if score == 0 else "NÉGATIF"),
            "urgency": "ÉLEVÉE" if score <= -5 else ("MODÉRÉE" if score < 0 else "FAIBLE"),
            "source_channels": random.sample(
                ["Twitter/X", "LinkedIn", "Médias ESG", "ONG", "Presse économique"], k=2
            ),
        }
        for topic, score in selected_topics
    ]

    # Alertes de risque (si score signal <= -5)
    risk_alerts = []
    for topic_data in trending_topics:
        if topic_data["signal_score"] <= -5:
            crisis_type_suggestion = (
                "SUPPLY_CHAIN_SCANDAL" if "fournisseur" in topic_data["topic"].lower() or "chaîne" in topic_data["topic"].lower()
                else "MEDIA_INVESTIGATION" if "enquête" in topic_data["topic"].lower()
                else "NGO_CAMPAIGN" if "ONG" in topic_data["topic"].lower() or "droits" in topic_data["topic"].lower()
                else "REGULATORY_FINE"
            )
            risk_alerts.append({
                "alert_id": f"ALERT-{client_name[:3].upper()}-{random.randint(1000, 9999)}",
                "level": "P1" if topic_data["signal_score"] <= -8 else "P2",
                "topic": topic_data["topic"],
                "signal_score": topic_data["signal_score"],
                "suggested_crisis_type": crisis_type_suggestion,
                "immediate_action": (
                    "Activation cellule de crise dans l'heure — "
                    "consulter plan de réponse CaelumSwarm™"
                ),
                "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    # Actions recommandées
    recommended_actions = []
    if sentiment_score < -10:
        recommended_actions.append({
            "priority": 1,
            "action": "Activation protocole de gestion de crise — sentiment global dégradé",
            "timeline": "Immédiat — 0-2h",
            "owner": "DirCom + DG",
        })
    if any(t["signal_score"] <= -5 for t in trending_topics):
        recommended_actions.append({
            "priority": 2,
            "action": f"Monitoring intensifié sur topics à risque identifiés",
            "timeline": "Dans les 4h",
            "owner": "Équipe Veille Réputation",
        })
    recommended_actions.append({
        "priority": len(recommended_actions) + 1,
        "action": f"Publication prochaine mise à jour Wave Report CaelumSwarm™ — renforcement narratif positif",
        "timeline": "Prochains 15 jours",
        "owner": "Directeur RSE + CaelumSwarm™",
    })
    recommended_actions.append({
        "priority": len(recommended_actions) + 1,
        "action": "Engagement proactif partie prenante à influence élevée",
        "timeline": "Cette semaine",
        "owner": "Directeur Relations Institutionnelles",
    })

    # Fréquence de la prochaine vérification
    if risk_alerts:
        next_check = 1
        monitoring_intensity = "CRITIQUE — surveillance horaire activée"
    elif sentiment_score < 0:
        next_check = 6
        monitoring_intensity = "RENFORCÉE — vérification toutes les 6h"
    else:
        next_check = 24
        monitoring_intensity = "STANDARD — vérification quotidienne"

    return {
        "monitoring_id": f"MON-{client_name[:3].upper()}-{datetime.now().strftime('%Y%m%d%H%M')}",
        "client_name": client_name,
        "industry": industry,
        "monitored_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "monitoring_window": "Dernières 24h",
        "signal_summary": {
            "total_signals": total_volume,
            "positive": total_positive,
            "negative": total_negative,
            "neutral": total_neutral,
            "sentiment_score": sentiment_score,
            "sentiment_label": (
                "TRÈS POSITIF" if sentiment_score > 20
                else "POSITIF" if sentiment_score > 5
                else "NEUTRE" if sentiment_score >= -5
                else "NÉGATIF" if sentiment_score >= -20
                else "TRÈS NÉGATIF"
            ),
            "by_channel": channels_data,
        },
        "trending_topics": trending_topics,
        "risk_alerts": risk_alerts,
        "risk_alerts_count": len(risk_alerts),
        "recommended_actions": sorted(recommended_actions, key=lambda x: x["priority"]),
        "next_monitoring_check_hours": next_check,
        "monitoring_intensity": monitoring_intensity,
        "wave_report_status": {
            "last_published": (datetime.now() - timedelta(days=random.randint(15, 90))).strftime("%Y-%m-%d"),
            "next_scheduled": (datetime.now() + timedelta(days=random.randint(5, 45))).strftime("%Y-%m-%d"),
            "recommendation": (
                "Publication accélérée recommandée — contexte médiatique sensible"
                if risk_alerts
                else "Publication selon calendrier standard"
            ),
        },
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète de l'Agent Gestion & Réputation Clients CaelumSwarm™.
    """
    separator = "=" * 70

    print(separator)
    print("  AGENT GESTION & RÉPUTATION CLIENTS — CaelumSwarm™")
    print("  Démonstration complète — " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print(separator)

    # ------------------------------------------------------------------
    # 1. SCORES DE RÉPUTATION — 3 PROFILS CLIENTS
    # ------------------------------------------------------------------
    print("\n" + separator)
    print("  MODULE 1 — CALCUL DES SCORES DE RÉPUTATION (3 CLIENTS)")
    print(separator)

    clients_demo = [
        {
            "profile": "CLIENT EXCELLENT — Leader ESG sectoriel",
            "client": {
                "name": "GreenSphere Industries",
                "industry": "Manufacturing",
                "size": "ETI",
                "headquarters": "France",
                "annual_revenue_EUR": 250_000_000,
            },
            "scores": {
                "ESG_RATING_SCORE": 91,
                "MEDIA_SENTIMENT": 85,
                "NGO_PERCEPTION": 82,
                "REGULATORY_STANDING": 97,
                "INVESTOR_CONFIDENCE": 88,
                "EMPLOYEE_PERCEPTION": 80,
                "SUPPLY_CHAIN_TRANSPARENCY": 78,
            },
        },
        {
            "profile": "CLIENT MOYEN — Acteur en progression",
            "client": {
                "name": "Horizons Retail Group",
                "industry": "Retail",
                "size": "Grande entreprise",
                "headquarters": "France",
                "annual_revenue_EUR": 800_000_000,
            },
            "scores": {
                "ESG_RATING_SCORE": 62,
                "MEDIA_SENTIMENT": 55,
                "NGO_PERCEPTION": 48,
                "REGULATORY_STANDING": 72,
                "INVESTOR_CONFIDENCE": 58,
                "EMPLOYEE_PERCEPTION": 65,
                "SUPPLY_CHAIN_TRANSPARENCY": 40,
            },
        },
        {
            "profile": "CLIENT EN CRISE — Réputation fragilisée",
            "client": {
                "name": "CapitalNord Finance",
                "industry": "Finance",
                "size": "Grande entreprise",
                "headquarters": "Luxembourg",
                "annual_revenue_EUR": 1_200_000_000,
            },
            "scores": {
                "ESG_RATING_SCORE": 28,
                "MEDIA_SENTIMENT": 22,
                "NGO_PERCEPTION": 18,
                "REGULATORY_STANDING": 35,
                "INVESTOR_CONFIDENCE": 30,
                "EMPLOYEE_PERCEPTION": 42,
                "SUPPLY_CHAIN_TRANSPARENCY": 25,
            },
        },
    ]

    reputation_results = []
    for demo in clients_demo:
        result = calculate_reputation_score(demo["client"], demo["scores"])
        reputation_results.append(result)
        print(f"\n{'—' * 50}")
        print(f"  {demo['profile']}")
        print(f"{'—' * 50}")
        print(f"  Client          : {result['client_name']} ({result['industry']})")
        print(f"  Score global    : {result['overall_score']}/100")
        print(f"  Grade           : {result['grade']} — {result['grade_label']}")
        print(f"  Tendance        : {result['trend']} — {result['trend_label']}")
        print(f"  Vs benchmark    : {result['vs_sector_benchmark']['position']} ({result['vs_sector_benchmark']['gap']:+.1f} pts)")
        print(f"  Alertes actives : {result['alerts_count']}")
        if result["alerts"]:
            print(f"\n  TOP ALERTES :")
            for alert in result["alerts"][:3]:
                print(f"    [{alert['level']}] {alert['message'][:65]}...")
        print(f"\n  Recommandation CaelumSwarm™ :")
        print(f"    → {result['caelumswarm_recommendation']}")

    # ------------------------------------------------------------------
    # 2. PLAN DE RÉPONSE À LA CRISE — SCANDALE CHAÎNE D'APPROVISIONNEMENT P1
    # ------------------------------------------------------------------
    print("\n\n" + separator)
    print("  MODULE 2 — PLAN DE CRISE : SCANDALE CHAÎNE D'APPROVISIONNEMENT (P1)")
    print(separator)

    crisis_client = clients_demo[1]["client"]  # Horizons Retail Group
    crisis_plan = design_crisis_response_plan("SUPPLY_CHAIN_SCANDAL", crisis_client, severity=1)

    print(f"\n  Plan ID         : {crisis_plan['plan_id']}")
    print(f"  Client          : {crisis_plan['client_name']}")
    print(f"  Type de crise   : {crisis_plan['crisis_type']}")
    print(f"  Sévérité        : {crisis_plan['severity_level']}")
    print(f"  Impact estimé   : {crisis_plan['estimated_reputation_impact']}")
    print(f"  Durée moy. crise: {crisis_plan['avg_crisis_duration']}")
    print(f"  Temps récupérat.: {crisis_plan['estimated_recovery_time']}")

    print(f"\n  PLAN EN 5 PHASES :")
    for phase_key, phase in crisis_plan["phases"].items():
        print(f"\n  ┌─ {phase['name'].upper()}")
        print(f"  │  Délai       : {phase['timeline_hours']}")
        print(f"  │  Deadline    : {phase['deadline']}")
        print(f"  │  Actions clés:")
        for action in phase["actions"][:3]:
            if action:
                print(f"  │    • {action[:65]}")
        print(f"  │  Porte-parole : {', '.join(phase['spokespersons'][:2])}")
        print(f"  └─ Critère succès : {phase['success_criteria'][0]}")

    print(f"\n  Principe directeur :")
    print(f"    → {crisis_plan['guiding_principle'][:80]}...")
    print(f"\n  Rôle Wave Report CaelumSwarm™ :")
    print(f"    → {crisis_plan['caelumswarm_asset']['wave_report_role']}")
    print(f"    → Publication : {crisis_plan['caelumswarm_asset']['publication_timeline']}")
    print(f"    → Impact confiance : {crisis_plan['caelumswarm_asset']['expected_trust_boost']}")

    # ------------------------------------------------------------------
    # 3. STRATÉGIE DE PROTECTION RÉPUTATIONNELLE
    # ------------------------------------------------------------------
    print("\n\n" + separator)
    print("  MODULE 3 — STRATÉGIE DE PROTECTION RÉPUTATIONNELLE")
    print(separator)

    protection_client = clients_demo[1]["client"]
    current_s = reputation_results[1]["overall_score"]
    target_s = 80.0

    strategy = build_reputation_protection_strategy(protection_client, current_s, target_s)

    print(f"\n  Client          : {strategy['client_name']} ({strategy['industry']})")
    print(f"  Score actuel    : {strategy['current_score']}/100")
    print(f"  Cible           : {strategy['target_score']}/100")
    print(f"  Gap à combler   : +{strategy['gap_to_close']} points")
    print(f"  Durée estimée   : {strategy['estimated_timeframe_months']} mois")
    print(f"  Budget suggéré  : {strategy['suggested_annual_budget_EUR']:,} € / an")

    print(f"\n  ASSETS PRIORITAIRES (par ROI) :")
    for asset in strategy["reputation_assets_to_acquire"]:
        print(
            f"    #{asset['priority_rank']} — {asset['label'][:50]}"
        )
        print(
            f"         Trust boost : +{asset['trust_boost']}/10 | "
            f"Coût acquisition : {asset['acquisition_cost_EUR']:,} € | "
            f"ROI score : {asset['roi_score']}"
        )

    print(f"\n  3 PILIERS NARRATIFS :")
    for pillar in strategy["narrative_pillars"]:
        print(f"\n  [{pillar['pillar_id']}] {pillar['name']}")
        print(f"      Message : {pillar['core_message'][:70]}...")
        print(f"      Audiences : {', '.join(pillar['target_audiences'])}")

    print(f"\n  CALENDRIER CONTENU — THÈMES CLÉS :")
    for month_data in strategy["content_calendar_themes"][:6]:
        print(
            f"    {month_data['month']:<12} — {month_data['theme']:<45} "
            f"[Pilier {month_data['pillar']}]"
        )

    print(f"\n  PROJECTION 12 MOIS :")
    outcomes = strategy["expected_outcomes_12m"]
    print(f"    Score projeté     : {outcomes['score_projection']}/100")
    print(f"    Sentiment médias  : {outcomes['media_sentiment_improvement']}")
    print(f"    Intérêt ISR       : {outcomes['investor_esg_interest']}")
    print(f"    Risque réglementaire : {outcomes['regulatory_risk_reduction']}")

    print(f"\n  CENTRALITÉ WAVE REPORTS CaelumSwarm™ :")
    wave = strategy["wave_report_centrality"]
    print(f"    Rôle    : {wave['role']}")
    print(f"    Rythme  : {wave['frequency']}")
    print(f"    Impact  : {wave['expected_trust_delta']}")
    print(f"    Valeur unique : {wave['unique_value'][:70]}...")

    # ------------------------------------------------------------------
    # 4. RAPPORT DE SURVEILLANCE EN TEMPS RÉEL
    # ------------------------------------------------------------------
    print("\n\n" + separator)
    print("  MODULE 4 — RAPPORT DE SURVEILLANCE RÉPUTATION EN TEMPS RÉEL")
    print(separator)

    monitoring_clients = [
        ("GreenSphere Industries", "Manufacturing"),
        ("Horizons Retail Group", "Retail"),
        ("CapitalNord Finance", "Finance"),
    ]

    for client_name, industry in monitoring_clients:
        report = monitor_reputation_signals(client_name, industry)
        print(f"\n  {'—' * 50}")
        print(f"  Client : {report['client_name']} ({report['industry']})")
        print(f"  {'—' * 50}")

        sig = report["signal_summary"]
        print(f"  Signaux captés  : {sig['total_signals']} ({sig['positive']} pos. / {sig['negative']} nég. / {sig['neutral']} neutre)")
        print(f"  Sentiment global: {sig['sentiment_score']:+.1f} — {sig['sentiment_label']}")

        print(f"\n  SUJETS EN TENDANCE :")
        for topic in report["trending_topics"]:
            indicator = "+" if topic["signal_score"] > 0 else ("-" if topic["signal_score"] < 0 else "~")
            print(f"    [{indicator}{abs(topic['signal_score'])}] {topic['topic'][:60]} — {topic['urgency']}")

        if report["risk_alerts"]:
            print(f"\n  ⚠  ALERTES RISQUE ({report['risk_alerts_count']}) :")
            for alert in report["risk_alerts"]:
                print(f"    [{alert['level']}] {alert['alert_id']}")
                print(f"    → {alert['immediate_action']}")
        else:
            print(f"\n  Aucune alerte de risque critique détectée.")

        print(f"\n  ACTIONS RECOMMANDÉES :")
        for action in report["recommended_actions"][:3]:
            print(f"    #{action['priority']} [{action['timeline']}] {action['action'][:60]}")

        print(f"\n  Prochaine vérification : dans {report['next_monitoring_check_hours']}h")
        print(f"  Intensité monitoring   : {report['monitoring_intensity']}")
        print(f"  Wave Report — Prochain : {report['wave_report_status']['next_scheduled']}")
        print(f"  Recommandation         : {report['wave_report_status']['recommendation']}")

    # ------------------------------------------------------------------
    # FIN
    # ------------------------------------------------------------------
    print("\n\n" + separator)
    print("  AGENT GESTION & RÉPUTATION CLIENTS — CaelumSwarm™")
    print("  Démonstration terminée avec succès.")
    print("  Les Wave Reports CaelumSwarm™ constituent l'actif de réputation")
    print("  le plus efficace : transparence proactive = confiance renforcée.")
    print(separator + "\n")

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()
