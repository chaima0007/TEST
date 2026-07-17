"""
Agent amplificateur bouche-à-oreille & viralité organique — stimule le partage naturel,
le referral et la notoriété organique pour CaelumSwarm™

Caelum Partners — CaelumSwarm™ Intelligence
Domaine : Stratégie de croissance organique B2B, programmes ambassadeurs,
          coefficient viral et amplification de notoriété.
"""

import math
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

REFERRAL_PROGRAMS = {
    "AMBASSADOR_B2B": {
        "label": "Programme Ambassadeur B2B",
        "reward_type": "credit_abonnement",
        "reward_value": 1500,  # EUR par lead qualifié converti
        "expected_conversion_rate": 0.28,
        "target_profiles": [
            "DSI / CDO grandes entreprises",
            "Directeurs RSE CAC 40 / SBF 120",
            "Compliance Officers secteur financier",
        ],
        "activation_touchpoints": [
            "Onboarding J+30 : invitation personnalisée",
            "Premier succès mesurable : déclenchement email ambassadeur",
            "NPS 9-10 reçu : appel relationship manager",
            "Renouvellement contrat : upgrade statut ambassadeur",
            "Participation webinar Caelum : badge ambassadeur LinkedIn",
        ],
    },
    "EXPERT_REFERRAL": {
        "label": "Programme Referral Expert & Conseil",
        "reward_type": "commission_recurrente",
        "reward_value": 0.12,  # 12 % des revenus récurrents année 1
        "expected_conversion_rate": 0.35,
        "target_profiles": [
            "Cabinets d'avocats d'affaires spécialisés ESG",
            "Cabinets de conseil en stratégie (RSE, compliance)",
            "Associations professionnelles sectorielles",
        ],
        "activation_touchpoints": [
            "Signature accord partenariat officiel",
            "Formation certifiante CaelumSwarm™ (2h)",
            "Accès portail partenaire avec ressources co-brandées",
            "Revue trimestrielle des leads et commissions",
            "Co-présentation lors d'événements sectoriels",
        ],
    },
    "CLIENT_ADVOCATE": {
        "label": "Programme Client Advocate",
        "reward_type": "avantages_premium",
        "reward_value": 2000,  # EUR équivalent avantages (accès bêta, formation, etc.)
        "expected_conversion_rate": 0.18,
        "target_profiles": [
            "Clients PME ETI satisfaits (NPS ≥ 9)",
            "Clients ayant présenté des cas d'usage en conférence",
            "Clients ayant publié un témoignage ou étude de cas",
        ],
        "activation_touchpoints": [
            "Publication étude de cas co-brandée",
            "Invitation à la CaelumSwarm™ Advisory Board",
            "Accès anticipé aux nouvelles Waves (bêta)",
            "Mention dans le rapport annuel Caelum Partners",
            "Participation à des tables rondes presse",
        ],
    },
}

NPS_SEGMENTS = {
    "PROMOTERS": {
        "label": "Promoteurs (NPS 9-10)",
        "score_range": (9, 10),
        "action_plan": (
            "Activation immédiate : contacter sous 48h après réception du NPS. "
            "Proposer le programme ambassadeur, solliciter témoignage vidéo, "
            "inviter à co-présenter lors d'un webinar ou événement sectoriel. "
            "Fournir kit de partage LinkedIn clé-en-main."
        ),
        "word_of_mouth_multiplier": 4.2,
        "conversion_to_ambassador_rate": 0.41,
    },
    "PASSIVES": {
        "label": "Passifs (NPS 7-8)",
        "score_range": (7, 8),
        "action_plan": (
            "Nurturing ciblé : identifier le point de friction résiduel et adresser "
            "proactivement. Partager des success stories similaires à leur secteur. "
            "Inviter à des événements exclusifs clients. Objectif : faire monter le "
            "score NPS à 9+ dans les 60 jours suivants."
        ),
        "word_of_mouth_multiplier": 1.8,
        "conversion_to_ambassador_rate": 0.12,
    },
    "DETRACTORS": {
        "label": "Détracteurs (NPS 0-6)",
        "score_range": (0, 6),
        "action_plan": (
            "Récupération prioritaire : escalade Customer Success sous 24h. "
            "Plan de remédiation personnalisé avec engagement de résultat. "
            "Suivi hebdomadaire pendant 30 jours. Objectif : neutraliser avant "
            "toute propagation négative et transformer en success story de récupération."
        ),
        "word_of_mouth_multiplier": -2.1,
        "conversion_to_ambassador_rate": 0.03,
    },
}

ORGANIC_CHANNELS = {
    "LINKEDIN_ORGANIC": {
        "label": "LinkedIn Organique (contenus & thought leadership)",
        "trust_score": 7,
        "reach_multiplier": 3.5,
        "cost_EUR": 0,
        "time_to_impact_months": 2,
    },
    "CONFERENCE_SPEAKING": {
        "label": "Prises de parole en conférence sectorielle",
        "trust_score": 9,
        "reach_multiplier": 6.0,
        "cost_EUR": 3500,
        "time_to_impact_months": 3,
    },
    "MEDIA_CITATIONS": {
        "label": "Citations & tribunes dans la presse spécialisée",
        "trust_score": 9,
        "reach_multiplier": 8.5,
        "cost_EUR": 0,
        "time_to_impact_months": 4,
    },
    "AWARDS_RECOGNITION": {
        "label": "Prix & distinctions sectorielles (RSE, legaltech, ESG)",
        "trust_score": 10,
        "reach_multiplier": 12.0,
        "cost_EUR": 800,
        "time_to_impact_months": 6,
    },
    "ACADEMIC_PARTNERSHIPS": {
        "label": "Partenariats académiques & publications de recherche",
        "trust_score": 10,
        "reach_multiplier": 5.0,
        "cost_EUR": 2000,
        "time_to_impact_months": 9,
    },
    "PODCAST_APPEARANCES": {
        "label": "Apparitions podcast (droit, RSE, innovation, tech)",
        "trust_score": 8,
        "reach_multiplier": 4.2,
        "cost_EUR": 0,
        "time_to_impact_months": 1,
    },
    "INDUSTRY_REPORTS": {
        "label": "Rapports & études sectorielles publiés par Caelum",
        "trust_score": 9,
        "reach_multiplier": 7.0,
        "cost_EUR": 5000,
        "time_to_impact_months": 5,
    },
}

AMBASSADOR_PROFILES = {
    "RSE_DIRECTOR": {
        "label": "Directeur / Directrice RSE",
        "network_size_est": 1800,
        "credibility_multiplier": 3.8,
        "activation_incentive": (
            "Co-rédaction du baromètre RSE annuel Caelum Partners, "
            "invitation aux think tanks ESG exclusifs, certification "
            "Ambassadeur CaelumSwarm™ visible sur LinkedIn."
        ),
        "content_types_preferred": [
            "Études de cas impact mesurable",
            "Comparatifs réglementaires (CSRD, SFDR, Taxonomie)",
            "Infographies données ESG",
            "Témoignages vidéo 2-3 min",
        ],
    },
    "COMPLIANCE_LAWYER": {
        "label": "Avocat(e) Compliance & Droit des affaires",
        "network_size_est": 950,
        "credibility_multiplier": 4.5,
        "activation_incentive": (
            "Accès anticipé aux analyses réglementaires Wave, co-authoring "
            "de livres blancs juridiques, invitation aux conférences droit & "
            "conformité en qualité d'expert CaelumSwarm™."
        ),
        "content_types_preferred": [
            "Analyses réglementaires détaillées",
            "Veille jurisprudentielle",
            "Guides pratiques conformité",
            "Webinars techniques droit & ESG",
        ],
    },
    "ESG_JOURNALIST": {
        "label": "Journaliste / Rédacteur ESG & Finance durable",
        "network_size_est": 12000,
        "credibility_multiplier": 5.2,
        "activation_incentive": (
            "Accès exclusif aux données CaelumSwarm™ avant publication, "
            "briefings analytiques confidentiels, interview des experts "
            "Caelum en avant-première sur les nouvelles Waves."
        ),
        "content_types_preferred": [
            "Données exclusives et exclusivités",
            "Accès aux experts pour citations",
            "Visualisations de données prêtes à l'emploi",
            "Communiqués de presse structurés",
        ],
    },
    "ACADEMIC_RESEARCHER": {
        "label": "Chercheur(se) / Enseignant-chercheur droits humains & ESG",
        "network_size_est": 2200,
        "credibility_multiplier": 4.8,
        "activation_incentive": (
            "Accès API aux données CaelumSwarm™ pour la recherche, "
            "co-publication d'articles académiques, financement partiel "
            "de programmes de recherche appliquée."
        ),
        "content_types_preferred": [
            "Méthodologies et frameworks analytiques",
            "Données longitudinales et séries temporelles",
            "Accès aux datasets anonymisés",
            "Collaborations publications peer-reviewed",
        ],
    },
}

# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------


def calculate_viral_coefficient(
    initial_users: int,
    invites_per_user: float,
    conversion_rate: float,
) -> dict:
    """
    Calcule le coefficient viral (K-factor) et les projections de croissance.

    Formule : K = invites_per_user × conversion_rate
    Projection : users_n = initial_users × Σ K^i  pour i de 0 à n_cycles

    Args:
        initial_users: Nombre d'utilisateurs initiaux (seed).
        invites_per_user: Nombre moyen d'invitations envoyées par utilisateur.
        conversion_rate: Taux de conversion des invitations (0.0 à 1.0).

    Returns:
        dict avec K-factor, projections 30j / 90j, temps de cycle viral, statut viral.
    """
    if initial_users <= 0:
        raise ValueError("initial_users doit être strictement positif.")
    if not (0.0 <= conversion_rate <= 1.0):
        raise ValueError("conversion_rate doit être compris entre 0.0 et 1.0.")
    if invites_per_user < 0:
        raise ValueError("invites_per_user ne peut pas être négatif.")

    k_factor = round(invites_per_user * conversion_rate, 4)
    is_viral = k_factor > 1.0

    # Cycle viral moyen en B2B SaaS : ~14 jours (décision d'achat plus longue)
    viral_cycle_time_days = 14

    cycles_30d = 30 / viral_cycle_time_days  # 2.14 cycles
    cycles_90d = 90 / viral_cycle_time_days  # 6.43 cycles

    def project_users(n_cycles: float) -> int:
        """Calcule les utilisateurs cumulés après n_cycles cycles viraux."""
        if k_factor == 1.0:
            # Cas limite : croissance linéaire
            return int(initial_users * (1 + n_cycles))
        # Somme géométrique : Σ K^i de 0 à floor(n_cycles)
        n = math.floor(n_cycles)
        total = initial_users * (1 - k_factor ** (n + 1)) / (1 - k_factor)
        # Fraction partielle du dernier cycle
        frac = n_cycles - n
        total += initial_users * k_factor ** (n + 1) * frac
        return max(initial_users, int(total))

    projected_30d = project_users(cycles_30d)
    projected_90d = project_users(cycles_90d)

    growth_rate_30d = round((projected_30d / initial_users - 1) * 100, 1)
    growth_rate_90d = round((projected_90d / initial_users - 1) * 100, 1)

    status = "VIRAL" if is_viral else ("EN CROISSANCE" if k_factor >= 0.7 else "SUB-VIRAL")
    recommendation = (
        "Excellent — amplifier les canaux d'invitation existants et maintenir la boucle."
        if is_viral
        else (
            "Potentiel réel — optimiser les incitations et simplifier le flux d'invitation."
            if k_factor >= 0.7
            else "Action requise — revoir la proposition de valeur du referral et les récompenses."
        )
    )

    return {
        "k_factor": k_factor,
        "is_viral": is_viral,
        "status": status,
        "viral_cycle_time_days": viral_cycle_time_days,
        "inputs": {
            "initial_users": initial_users,
            "invites_per_user": invites_per_user,
            "conversion_rate": conversion_rate,
        },
        "projections": {
            "projected_users_30d": projected_30d,
            "projected_users_90d": projected_90d,
            "growth_rate_30d_pct": growth_rate_30d,
            "growth_rate_90d_pct": growth_rate_90d,
            "new_users_30d": projected_30d - initial_users,
            "new_users_90d": projected_90d - initial_users,
        },
        "recommendation": recommendation,
    }


def design_referral_program(
    program_type: str,
    budget_EUR: float,
    target_leads: int,
) -> dict:
    """
    Conçoit un programme de referral complet avec mécanique, récompenses et ROI attendu.

    Args:
        program_type: Clé dans REFERRAL_PROGRAMS (ex. "AMBASSADOR_B2B").
        budget_EUR: Budget disponible en euros.
        target_leads: Nombre de leads qualifiés visés.

    Returns:
        dict complet avec mécaniques, templates communication, ROI, break-even.
    """
    if program_type not in REFERRAL_PROGRAMS:
        raise ValueError(
            f"Type de programme invalide. Options : {list(REFERRAL_PROGRAMS.keys())}"
        )
    if budget_EUR <= 0:
        raise ValueError("Le budget doit être strictement positif.")
    if target_leads <= 0:
        raise ValueError("Le nombre de leads cibles doit être strictement positif.")

    program = REFERRAL_PROGRAMS[program_type]
    conversion_rate = program["expected_conversion_rate"]
    reward_value = program["reward_value"]

    # Calcul du coût par lead et du break-even
    if program_type == "EXPERT_REFERRAL":
        # Modèle commission : reward_value est un taux (12 %)
        avg_contract_value_EUR = 18000  # valeur contrat annuel moyen Caelum B2B
        reward_per_conversion_EUR = avg_contract_value_EUR * reward_value
    else:
        reward_per_conversion_EUR = float(reward_value)

    # Coûts totaux = récompenses + coûts d'activation (estimation 20 % du budget)
    activation_cost_pct = 0.20
    activation_budget = budget_EUR * activation_cost_pct
    rewards_budget = budget_EUR * (1 - activation_cost_pct)

    max_conversions_from_budget = int(rewards_budget / reward_per_conversion_EUR)
    referrals_needed_for_target = math.ceil(target_leads / conversion_rate)
    break_even_referrals = math.ceil(
        (budget_EUR * 0.15) / reward_per_conversion_EUR
    )  # ROI positif à partir de 15 % de retour minimum

    expected_conversions = min(
        int(referrals_needed_for_target * conversion_rate),
        max_conversions_from_budget,
    )
    expected_conversions = max(expected_conversions, 1)

    # Estimation revenus générés (contrat moyen 18 000 EUR, LTV x3)
    avg_contract_EUR = 18000
    ltv_multiplier = 3.0
    expected_revenue_EUR = expected_conversions * avg_contract_EUR
    expected_ltv_EUR = expected_conversions * avg_contract_EUR * ltv_multiplier
    roi_pct = round((expected_revenue_EUR - budget_EUR) / budget_EUR * 100, 1)

    # Templates de communication
    communication_templates = {
        "email_invitation": (
            f"Objet : [Confidentiel] Rejoignez le {program['label']} — CaelumSwarm™\n\n"
            "Bonjour [Prénom],\n\n"
            "Votre expérience avec CaelumSwarm™ et votre expertise sur les enjeux "
            "droits humains & ESG font de vous un partenaire idéal pour notre programme "
            f"{program['label']}.\n\n"
            "En recommandant CaelumSwarm™ à un confrère ou partenaire qualifié, "
            f"vous bénéficiez de : {_format_reward(program_type, program)}.\n\n"
            "Prochaine étape : 15 minutes d'appel pour vous présenter les détails.\n\n"
            "Cordialement,\nL'équipe Caelum Partners"
        ),
        "linkedin_message": (
            f"Bonjour [Prénom], j'ai pensé à vous pour notre {program['label']} "
            "chez Caelum Partners. CaelumSwarm™ analyse les risques droits humains "
            "en temps réel — je serais ravi(e) de vous en dire plus. Disponible pour "
            "un échange rapide ?"
        ),
        "onboarding_prompt": (
            "🎯 Vous avez transformé votre approche des risques ESG avec CaelumSwarm™. "
            "Partagez cette valeur avec un collègue et soyez récompensé(e). "
            "[Bouton : Devenir Ambassadeur]"
        ),
        "success_notification": (
            f"Félicitations ! Votre recommandation a abouti. "
            f"Votre récompense {program['reward_type'].replace('_', ' ')} "
            "est en cours de traitement. Merci pour votre confiance !"
        ),
    }

    # Mécaniques du programme
    mechanics = {
        "tracking": "Lien de referral unique + code ambassadeur personnalisé",
        "attribution_window_days": 90,
        "qualification_criteria": [
            "Lead accepte une démonstration CaelumSwarm™",
            "Lead répond aux critères ICP (taille, secteur, budget)",
            "Pas de contact commercial Caelum actif sur ce lead",
        ],
        "reward_trigger": "Signature contrat + paiement première facture",
        "payment_delay_days": 30,
        "portal": "dashboard.caelum-partners.com/ambassadeurs",
        "support_contact": "ambassadeurs@caelum-partners.com",
    }

    return {
        "program_type": program_type,
        "program_label": program["label"],
        "budget_EUR": budget_EUR,
        "target_leads": target_leads,
        "mechanics": mechanics,
        "rewards": {
            "reward_type": program["reward_type"],
            "reward_value_display": _format_reward(program_type, program),
            "reward_per_conversion_EUR": round(reward_per_conversion_EUR, 2),
        },
        "communication_templates": communication_templates,
        "financial_projections": {
            "referrals_needed": referrals_needed_for_target,
            "expected_conversion_rate_pct": round(conversion_rate * 100, 1),
            "expected_conversions": expected_conversions,
            "expected_revenue_EUR": expected_revenue_EUR,
            "expected_ltv_EUR": expected_ltv_EUR,
            "roi_pct": roi_pct,
            "break_even_referrals": break_even_referrals,
            "activation_budget_EUR": round(activation_budget, 2),
            "rewards_budget_EUR": round(rewards_budget, 2),
        },
        "activation_touchpoints": program["activation_touchpoints"],
        "target_profiles": program["target_profiles"],
    }


def _format_reward(program_type: str, program: dict) -> str:
    """Formate l'affichage de la récompense selon le type de programme."""
    if program_type == "EXPERT_REFERRAL":
        return f"{int(program['reward_value'] * 100)} % de commission récurrente (année 1)"
    elif program_type == "AMBASSADOR_B2B":
        return f"{program['reward_value']:,} EUR de crédit abonnement par lead converti"
    else:
        return f"{program['reward_value']:,} EUR d'avantages premium (accès bêta, formation, advisory board)"


def identify_ambassadors(client_database: list, nps_scores: dict) -> dict:
    """
    Segmente la base clients en tiers ambassadeurs selon NPS, taille et influence.

    La segmentation utilise un score composite :
        score = (nps * 0.40) + (company_tier * 0.30) + (industry_influence * 0.30)

    Tiers :
        PLATINUM : score ≥ 8.0 → activation immédiate, programme complet
        GOLD     : score ≥ 6.0 → nurturing prioritaire, invitation sélective
        SILVER   : score ≥ 4.5 → programme automatisé, contenu clé-en-main

    Args:
        client_database: Liste de dicts client avec au minimum :
            {id, name, company, industry, company_size_employees, contract_value_EUR}
        nps_scores: Dict {client_id: nps_score (0-10)}

    Returns:
        dict avec ambassador_candidates par tier, statistiques et plans d'activation.
    """
    if not client_database:
        raise ValueError("La base clients ne peut pas être vide.")

    # Mapping secteur → influence (score 1-10)
    industry_influence_map = {
        "finance": 9,
        "assurance": 8,
        "energie": 8,
        "pharmaceutique": 9,
        "technologie": 7,
        "conseil": 8,
        "juridique": 9,
        "immobilier": 6,
        "industrie": 7,
        "retail": 5,
        "agroalimentaire": 6,
        "transport": 6,
        "sante": 8,
        "media": 7,
        "default": 5,
    }

    def company_tier_score(employees: int) -> float:
        """Score entreprise sur 10 selon la taille."""
        if employees >= 10000:
            return 10.0
        elif employees >= 5000:
            return 9.0
        elif employees >= 1000:
            return 7.5
        elif employees >= 500:
            return 6.0
        elif employees >= 100:
            return 4.5
        else:
            return 3.0

    candidates = []
    for client in client_database:
        client_id = client.get("id", "")
        nps = nps_scores.get(client_id, None)
        if nps is None:
            continue  # Ignorer les clients sans NPS

        # Normaliser NPS sur 10
        nps_normalized = nps  # déjà sur 10

        # Score entreprise
        employees = client.get("company_size_employees", 100)
        c_tier = company_tier_score(employees)

        # Score influence sectorielle
        industry_key = client.get("industry", "default").lower()
        influence = industry_influence_map.get(
            industry_key, industry_influence_map["default"]
        )

        # Score composite
        composite = (nps_normalized * 0.40) + (c_tier * 0.30) + (influence * 0.30)
        composite = round(composite, 2)

        # Déterminer le segment NPS
        if nps >= 9:
            nps_segment = "PROMOTERS"
        elif nps >= 7:
            nps_segment = "PASSIVES"
        else:
            nps_segment = "DETRACTORS"

        # Tier ambassadeur
        if composite >= 8.0 and nps_segment == "PROMOTERS":
            tier = "PLATINUM"
            priority = 1
        elif composite >= 6.0 and nps_segment in ("PROMOTERS", "PASSIVES"):
            tier = "GOLD"
            priority = 2
        elif composite >= 4.5:
            tier = "SILVER"
            priority = 3
        else:
            tier = None  # Non éligible
            priority = 99

        if tier is None:
            continue

        nps_info = NPS_SEGMENTS[nps_segment]
        wom_multiplier = nps_info["word_of_mouth_multiplier"]
        conversion_rate = nps_info["conversion_to_ambassador_rate"]

        # Plan d'activation personnalisé
        if tier == "PLATINUM":
            activation_plan = (
                f"Contact direct du CEO Caelum sous 48h. "
                f"Invitation au CaelumSwarm™ Advisory Board. "
                f"Proposition co-authoring étude de cas (NPS={nps}). "
                f"Programme AMBASSADOR_B2B complet activé."
            )
            recommended_program = "AMBASSADOR_B2B"
        elif tier == "GOLD":
            activation_plan = (
                f"Appel Relationship Manager sous 1 semaine. "
                f"Invitation webinar exclusif clients ambassadeurs. "
                f"Kit de partage LinkedIn fourni (NPS={nps}). "
                f"Éligible au programme CLIENT_ADVOCATE."
            )
            recommended_program = "CLIENT_ADVOCATE"
        else:
            activation_plan = (
                f"Séquence email automatisée (J+7, J+30). "
                f"Accès portail ambassadeur self-service (NPS={nps}). "
                f"Récompenses automatiques sur référence validée."
            )
            recommended_program = "CLIENT_ADVOCATE"

        # Profil ambassadeur le plus proche
        industry_to_profile = {
            "finance": "COMPLIANCE_LAWYER",
            "assurance": "RSE_DIRECTOR",
            "energie": "RSE_DIRECTOR",
            "conseil": "COMPLIANCE_LAWYER",
            "juridique": "COMPLIANCE_LAWYER",
            "default": "RSE_DIRECTOR",
        }
        matched_profile = industry_to_profile.get(
            industry_key, industry_to_profile["default"]
        )

        candidates.append(
            {
                "client_id": client_id,
                "name": client.get("name", "Inconnu"),
                "company": client.get("company", "N/A"),
                "industry": client.get("industry", "N/A"),
                "company_size_employees": employees,
                "contract_value_EUR": client.get("contract_value_EUR", 0),
                "nps_score": nps,
                "nps_segment": nps_segment,
                "composite_score": composite,
                "tier": tier,
                "priority": priority,
                "wom_multiplier": wom_multiplier,
                "conversion_to_ambassador_rate_pct": round(conversion_rate * 100, 1),
                "activation_plan": activation_plan,
                "recommended_program": recommended_program,
                "matched_ambassador_profile": matched_profile,
            }
        )

    # Tri par priorité puis score composite décroissant
    candidates.sort(key=lambda x: (x["priority"], -x["composite_score"]))

    # Statistiques par tier
    platinum = [c for c in candidates if c["tier"] == "PLATINUM"]
    gold = [c for c in candidates if c["tier"] == "GOLD"]
    silver = [c for c in candidates if c["tier"] == "SILVER"]

    total_wom_potential = sum(c["wom_multiplier"] for c in candidates)
    avg_nps = round(sum(c["nps_score"] for c in candidates) / len(candidates), 2) if candidates else 0

    return {
        "total_eligible": len(candidates),
        "tiers": {
            "PLATINUM": {
                "count": len(platinum),
                "candidates": platinum,
                "description": "Ambassadeurs prioritaires — activation immédiate CEO",
                "target_activation_days": 2,
            },
            "GOLD": {
                "count": len(gold),
                "candidates": gold,
                "description": "Ambassadeurs à fort potentiel — nurturing prioritaire",
                "target_activation_days": 7,
            },
            "SILVER": {
                "count": len(silver),
                "candidates": silver,
                "description": "Ambassadeurs programme automatisé — self-service",
                "target_activation_days": 30,
            },
        },
        "statistics": {
            "avg_nps_eligible": avg_nps,
            "total_wom_potential_multiplier": round(total_wom_potential, 2),
            "estimated_new_leads_90d": int(
                sum(c["wom_multiplier"] * c["conversion_to_ambassador_rate_pct"] / 100 for c in candidates) * 10
            ),
        },
        "ambassador_candidates": candidates,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def generate_wom_campaign(trigger_event: str, wave: int) -> dict:
    """
    Crée une campagne de bouche-à-oreille autour d'une release Wave CaelumSwarm™.

    La campagne coordonne : seeding auprès d'influenceurs, points de discussion presse,
    assets de preuve sociale et stratégie de distribution organique.

    Args:
        trigger_event: Description de l'événement déclencheur (ex. "Lancement Wave 194").
        wave: Numéro de la Wave CaelumSwarm™.

    Returns:
        dict complet avec stratégie de seeding, influenceurs, talking points, assets, reach.
    """
    if wave <= 0:
        raise ValueError("Le numéro de Wave doit être positif.")
    if not trigger_event or not trigger_event.strip():
        raise ValueError("Le trigger_event ne peut pas être vide.")

    launch_date = datetime.now()
    campaign_end = launch_date + timedelta(days=60)

    # Sélection des canaux organiques les plus pertinents pour une Wave
    top_channels = sorted(
        ORGANIC_CHANNELS.items(),
        key=lambda x: (x[1]["trust_score"] * x[1]["reach_multiplier"]),
        reverse=True,
    )[:4]

    # Influenceurs clés à contacter par profil ambassadeur
    key_influencers_to_contact = []
    for profile_key, profile in AMBASSADOR_PROFILES.items():
        influencers_for_profile = {
            "profile_type": profile["label"],
            "network_size": profile["network_size_est"],
            "credibility_multiplier": profile["credibility_multiplier"],
            "outreach_message": (
                f"Bonjour, dans le cadre du lancement de notre Wave {wave} "
                f"({trigger_event}), nous souhaitons partager en avant-première "
                f"nos résultats avec des experts comme vous. "
                f"Seriez-vous disponible pour un briefing confidentiel de 20 minutes ?"
            ),
            "preferred_content": profile["content_types_preferred"][0],
            "activation_incentive": profile["activation_incentive"],
            "estimated_reach": int(
                profile["network_size_est"] * profile["credibility_multiplier"] * 0.15
            ),
        }
        key_influencers_to_contact.append(influencers_for_profile)

    # Stratégie de seeding en 3 phases
    seeding_strategy = {
        "phase_1_pre_launch": {
            "label": "Pré-lancement (J-14 à J-1)",
            "duration_days": 14,
            "actions": [
                f"Briefings confidentiels avec 5 influenceurs clés sur les résultats Wave {wave}",
                "Envoi d'embargo press kit aux journalistes ESG partenaires",
                "Teaser LinkedIn : 'Quelque chose de grand arrive sur les droits humains...'",
                "Activation ambassadeurs PLATINUM : accès preview dashboard",
                "Préparation des threads analytiques LinkedIn (3 contenus différenciés)",
            ],
            "target_seeds": 12,
        },
        "phase_2_launch": {
            "label": "Lancement (J0 à J+7)",
            "duration_days": 7,
            "actions": [
                f"Publication officielle : rapport Wave {wave} + communiqué de presse",
                "Posts LinkedIn coordonnés ambassadeurs (même jour, messages personnalisés)",
                "Envoi newsletter CaelumSwarm™ à 2 400 abonnés avec data exclusive",
                f"Webinar de lancement Wave {wave} — 200 invités clients + prospects",
                "Pitch proactif à 10 journalistes ESG et podcasts sectoriels",
                "Thread Twitter/X analytique avec les 3 insights les plus surprenants",
            ],
            "target_seeds": 45,
        },
        "phase_3_amplification": {
            "label": "Amplification (J+8 à J+60)",
            "duration_days": 52,
            "actions": [
                "Relance des non-répondants presse avec angle différent",
                f"Article de fond : 'Ce que révèle Wave {wave} sur [thématique]' (Medium + LinkedIn)",
                "Data visualization interactives partagées sur les réseaux",
                "Soumission aux prix sectoriels ESG et innovation",
                "Co-présentation conference avec 2 ambassadeurs PLATINUM",
                "Publication synthèse académique en partenariat universitaire",
            ],
            "target_shares": 280,
        },
    }

    # Points de discussion presse
    press_talking_points = [
        {
            "angle": "Primeur data",
            "headline": f"CaelumSwarm™ Wave {wave} : les entreprises françaises face aux nouveaux risques droits humains",
            "key_stat": f"Wave {wave} analyse {wave * 8} entités mondiales sur {wave * 4} indicateurs ESG",
            "audience": "Presse économique et financière",
        },
        {
            "angle": "Alerte réglementaire",
            "headline": f"CSRD 2025 : ce que révèle Wave {wave} sur l'écart entre reporting et réalité terrain",
            "key_stat": "67 % des entreprises analysées présentent des risques critiques non divulgués",
            "audience": "Presse juridique et compliance",
        },
        {
            "angle": "Innovation technologique",
            "headline": f"CaelumSwarm™ : comment l'IA analyse en temps réel les droits humains à l'échelle mondiale",
            "key_stat": f"Wave {wave} — 24h pour analyser ce qui prenait 6 mois à des équipes humaines",
            "audience": "Presse tech et IA",
        },
        {
            "angle": "Impact investissement",
            "headline": f"Wave {wave} : les données qui font bouger les décisions d'investissement ESG",
            "key_stat": "82 % des investisseurs institutionnels interrogés intègreront ces données en 2025",
            "audience": "Presse finance & investissement",
        },
    ]

    # Assets de preuve sociale
    social_proof_assets = [
        {
            "type": "Étude de cas vidéo",
            "description": "Témoignage 2 min d'un Directeur RSE CAC 40 sur l'impact CaelumSwarm™",
            "channel": "LinkedIn + Site web",
            "production_effort": "Moyen (1 journée de tournage)",
        },
        {
            "type": "Infographie données",
            "description": f"Top 5 insights Wave {wave} en infographie partageable",
            "channel": "LinkedIn + Newsletter",
            "production_effort": "Faible (demi-journée design)",
        },
        {
            "type": "Citation expert",
            "description": "3 citations d'experts indépendants sur la méthodologie Wave",
            "channel": "Communiqué de presse + Site web",
            "production_effort": "Faible (interviews email)",
        },
        {
            "type": "Score benchmark",
            "description": "Outil interactif : 'Comparez votre secteur aux résultats Wave'",
            "channel": "Site web + LinkedIn",
            "production_effort": "Élevé (développement 5 jours)",
        },
        {
            "type": "Rapport synthèse",
            "description": f"PDF executive summary Wave {wave} — 8 pages, design premium",
            "channel": "Lead magnet + Newsletter + Presse",
            "production_effort": "Moyen (2 jours rédaction + design)",
        },
    ]

    # Calcul du reach organique attendu
    total_reach_direct = sum(
        profile["network_size_est"] for profile in AMBASSADOR_PROFILES.values()
    )
    avg_credibility = sum(
        p["credibility_multiplier"] for p in AMBASSADOR_PROFILES.values()
    ) / len(AMBASSADOR_PROFILES)

    estimated_organic_reach = {
        "direct_reach_influencers": total_reach_direct,
        "amplified_reach_2nd_degree": int(total_reach_direct * avg_credibility * 0.08),
        "press_coverage_readers_est": 45000,
        "newsletter_reach": 2400,
        "webinar_attendees_target": 200,
        "total_estimated_reach": int(
            total_reach_direct
            + total_reach_direct * avg_credibility * 0.08
            + 45000
            + 2400
            + 200
        ),
        "estimated_leads_generated": int(
            (total_reach_direct * avg_credibility * 0.08 + 45000) * 0.008
        ),
        "estimated_media_value_EUR": int(
            (total_reach_direct * avg_credibility * 0.08 + 45000) * 0.02
        ),
    }

    # KPIs de la campagne
    kpis = {
        "shares_target_30d": 150,
        "mentions_linkedin_target": 85,
        "media_pickups_target": 8,
        "webinar_registrations_target": 200,
        "demo_requests_from_wom": 25,
        "new_newsletter_subscribers": 300,
        "ambassador_activations": 5,
    }

    return {
        "campaign_name": f"WOM Wave {wave} — {trigger_event}",
        "wave": wave,
        "trigger_event": trigger_event,
        "launch_date": launch_date.strftime("%Y-%m-%d"),
        "campaign_end_date": campaign_end.strftime("%Y-%m-%d"),
        "seeding_strategy": seeding_strategy,
        "key_influencers_to_contact": key_influencers_to_contact,
        "press_talking_points": press_talking_points,
        "social_proof_assets": social_proof_assets,
        "top_organic_channels": [
            {
                "key": ch[0],
                "label": ch[1]["label"],
                "trust_score": ch[1]["trust_score"],
                "reach_multiplier": ch[1]["reach_multiplier"],
                "cost_EUR": ch[1]["cost_EUR"],
            }
            for ch in top_channels
        ],
        "expected_organic_reach": estimated_organic_reach,
        "kpis": kpis,
        "total_estimated_budget_EUR": sum(
            ch[1]["cost_EUR"] for ch in top_channels
        ),
        "generated_at": launch_date.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démonstration complète de l'agent bouche-à-oreille & viralité organique.

    Enchaîne :
      1. Calcul du coefficient viral CaelumSwarm™
      2. Conception du programme de referral AMBASSADOR_B2B
      3. Identification des ambassadeurs depuis 5 clients fictifs
      4. Génération de la campagne WOM pour la Wave 194

    Returns:
        True si la démo s'est exécutée sans erreur.
    """
    separator = "=" * 70

    print(separator)
    print("  CAELUMSWARM™ — AGENT BOUCHE-À-OREILLE & VIRALITÉ ORGANIQUE")
    print(f"  Exécution : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separator)

    # ------------------------------------------------------------------
    # 1. COEFFICIENT VIRAL
    # ------------------------------------------------------------------
    print("\n[1/4] CALCUL DU COEFFICIENT VIRAL — CaelumSwarm™\n")

    viral_result = calculate_viral_coefficient(
        initial_users=120,
        invites_per_user=2.4,
        conversion_rate=0.38,
    )

    print(f"  Utilisateurs initiaux  : {viral_result['inputs']['initial_users']}")
    print(f"  Invitations / utilisateur : {viral_result['inputs']['invites_per_user']}")
    print(f"  Taux de conversion     : {viral_result['inputs']['conversion_rate'] * 100:.0f} %")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  K-Factor (coeff. viral): {viral_result['k_factor']}")
    print(f"  Statut                 : {viral_result['status']}")
    print(f"  Est viral (K > 1)      : {'OUI ✓' if viral_result['is_viral'] else 'NON'}")
    print(f"  Cycle viral            : {viral_result['viral_cycle_time_days']} jours")
    print(f"  Projection J+30        : {viral_result['projections']['projected_users_30d']} utilisateurs"
          f" (+{viral_result['projections']['growth_rate_30d_pct']} %)")
    print(f"  Projection J+90        : {viral_result['projections']['projected_users_90d']} utilisateurs"
          f" (+{viral_result['projections']['growth_rate_90d_pct']} %)")
    print(f"  Nouveaux utilisateurs 90j : {viral_result['projections']['new_users_90d']}")
    print(f"\n  Recommandation : {viral_result['recommendation']}")

    # ------------------------------------------------------------------
    # 2. PROGRAMME DE REFERRAL
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("\n[2/4] CONCEPTION PROGRAMME DE REFERRAL — AMBASSADOR_B2B\n")

    referral_result = design_referral_program(
        program_type="AMBASSADOR_B2B",
        budget_EUR=25000.0,
        target_leads=40,
    )

    fp = referral_result["financial_projections"]
    print(f"  Programme              : {referral_result['program_label']}")
    print(f"  Budget total           : {referral_result['budget_EUR']:,.0f} EUR")
    print(f"  Leads cibles           : {referral_result['target_leads']}")
    print(f"  Récompense             : {referral_result['rewards']['reward_value_display']}")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  Referrals nécessaires  : {fp['referrals_needed']}")
    print(f"  Taux de conversion     : {fp['expected_conversion_rate_pct']} %")
    print(f"  Conversions attendues  : {fp['expected_conversions']}")
    print(f"  Revenus attendus       : {fp['expected_revenue_EUR']:,} EUR")
    print(f"  LTV projetée (x3)      : {fp['expected_ltv_EUR']:,} EUR")
    print(f"  ROI estimé             : {fp['roi_pct']:+.1f} %")
    print(f"  Break-even referrals   : {fp['break_even_referrals']}")
    print(f"  Budget activation      : {fp['activation_budget_EUR']:,.0f} EUR")
    print(f"  Budget récompenses     : {fp['rewards_budget_EUR']:,.0f} EUR")
    print(f"\n  Template email (extrait) :")
    email_preview = referral_result["communication_templates"]["email_invitation"]
    for line in email_preview.split("\n")[:5]:
        print(f"    {line}")
    print(f"    [...]")

    # ------------------------------------------------------------------
    # 3. IDENTIFICATION DES AMBASSADEURS
    # ------------------------------------------------------------------
    print(f"\n{separator}")
    print("\n[3/4] IDENTIFICATION DES AMBASSADEURS — 5 CLIENTS FICTIFS\n")

    mock_clients = [
        {
            "id": "CLI-001",
            "name": "Sophie Marchand",
            "company": "Groupe Énergie Transition SA",
            "industry": "energie",
            "company_size_employees": 8500,
            "contract_value_EUR": 42000,
        },
        {
            "id": "CLI-002",
            "name": "Marc Delacroix",
            "company": "Cabimet Delacroix & Associés",
            "industry": "juridique",
            "company_size_employees": 85,
            "contract_value_EUR": 18000,
        },
        {
            "id": "CLI-003",
            "name": "Isabelle Fontaine",
            "company": "AXA France",
            "industry": "assurance",
            "company_size_employees": 23000,
            "contract_value_EUR": 95000,
        },
        {
            "id": "CLI-004",
            "name": "Thomas Renard",
            "company": "PME Techno Solutions",
            "industry": "technologie",
            "company_size_employees": 45,
            "contract_value_EUR": 8500,
        },
        {
            "id": "CLI-005",
            "name": "Céline Moreau",
            "company": "BNP Paribas Asset Management",
            "industry": "finance",
            "company_size_employees": 35000,
            "contract_value_EUR": 120000,
        },
    ]

    mock_nps = {
        "CLI-001": 9,
        "CLI-002": 8,
        "CLI-003": 10,
        "CLI-004": 6,
        "CLI-005": 9,
    }

    ambassador_result = identify_ambassadors(mock_clients, mock_nps)

    print(f"  Clients analysés       : {len(mock_clients)}")
    print(f"  Clients éligibles      : {ambassador_result['total_eligible']}")
    print(f"  NPS moyen éligibles    : {ambassador_result['statistics']['avg_nps_eligible']}")
    print(f"  WOM potentiel total    : x{ambassador_result['statistics']['total_wom_potential_multiplier']}")
    print(f"  Leads estimés 90j      : {ambassador_result['statistics']['estimated_new_leads_90d']}")
    print()

    for tier_key in ["PLATINUM", "GOLD", "SILVER"]:
        tier_data = ambassador_result["tiers"][tier_key]
        print(f"  Tier {tier_key} ({tier_data['count']} client(s)) — {tier_data['description']}")
        for c in tier_data["candidates"]:
            print(f"    • {c['name']} ({c['company']}) — NPS {c['nps_score']}"
                  f" — Score {c['composite_score']} — Programme : {c['recommended_program']}")
            print(f"      Plan : {c['activation_plan'][:90]}...")
        print()

    # ------------------------------------------------------------------
    # 4. CAMPAGNE WOM WAVE 194
    # ------------------------------------------------------------------
    print(f"{separator}")
    print("\n[4/4] CAMPAGNE WOM — WAVE 194 CAELUMSWARM™\n")

    wom_result = generate_wom_campaign(
        trigger_event="Lancement Wave 194 — Droits des travailleurs migrants & chaînes d'approvisionnement",
        wave=194,
    )

    reach = wom_result["expected_organic_reach"]
    print(f"  Campagne               : {wom_result['campaign_name']}")
    print(f"  Période                : {wom_result['launch_date']} → {wom_result['campaign_end_date']}")
    print(f"  Budget canaux organiques : {wom_result['total_estimated_budget_EUR']:,} EUR")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  Reach direct influenceurs  : {reach['direct_reach_influencers']:,} contacts")
    print(f"  Reach amplifié 2ème degré  : {reach['amplified_reach_2nd_degree']:,} contacts")
    print(f"  Readers presse estimés     : {reach['press_coverage_readers_est']:,}")
    print(f"  Newsletter                 : {reach['newsletter_reach']:,} abonnés")
    print(f"  TOTAL REACH ESTIMÉ         : {reach['total_estimated_reach']:,} personnes")
    print(f"  Leads générés estimés      : {reach['estimated_leads_generated']}")
    print(f"  Valeur médias équivalente  : {reach['estimated_media_value_EUR']:,} EUR")

    print(f"\n  Phases de seeding :")
    for phase_key, phase in wom_result["seeding_strategy"].items():
        print(f"    [{phase['label']}]")
        print(f"      → {phase['actions'][0]}")
        print(f"      → {phase['actions'][1]}")

    print(f"\n  Canaux organiques prioritaires :")
    for ch in wom_result["top_organic_channels"]:
        print(f"    • {ch['label']}")
        print(f"      Trust: {ch['trust_score']}/10 | Reach x{ch['reach_multiplier']} | Coût: {ch['cost_EUR']} EUR")

    print(f"\n  Angles presse :")
    for pt in wom_result["press_talking_points"][:3]:
        print(f"    [{pt['angle'].upper()}] {pt['headline'][:65]}...")

    print(f"\n  KPIs cibles 60 jours :")
    for kpi_key, val in wom_result["kpis"].items():
        print(f"    • {kpi_key.replace('_', ' ').title():40s} : {val}")

    print(f"\n{separator}")
    print("  DÉMO TERMINÉE — Tous les modules opérationnels.")
    print(f"  CaelumSwarm™ Organic Virality Agent — {datetime.now().strftime('%Y-%m-%d')}")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        exit(0)
    else:
        exit(1)
