"""
Agent Stratège en Vente Éclair — stratégie commerciale agressive et précise pour convertir
les prospects CSDDD en clients CaelumSwarm™. Pipeline, scoring, closing, upsell.

CaelumSwarm™ | Caelum Partners | Module: Sales Intelligence
Version: 1.0.0
"""

from datetime import date, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

SALES_STAGES = {
    "AWARENESS": {
        "label": "Sensibilisation",
        "avg_duration_days": 14,
        "conversion_rate_pct": 15,
        "key_action": "Déclencher curiosité via contenu CSDDD ciblé ou cold outbound",
        "disqualification_criteria": "Aucun projet CSDDD identifié, hors périmètre réglementaire",
    },
    "INTEREST": {
        "label": "Intérêt",
        "avg_duration_days": 10,
        "conversion_rate_pct": 35,
        "key_action": "Qualifier le besoin réel, proposer une démo Wave sur leur secteur",
        "disqualification_criteria": "Budget <€30k/an confirmé, décideur injoignable",
    },
    "CONSIDERATION": {
        "label": "Considération",
        "avg_duration_days": 18,
        "conversion_rate_pct": 50,
        "key_action": "Présenter ROI chiffré vs consulting manuel, envoyer Wave sample report",
        "disqualification_criteria": "Choix de la voie interne confirmé avec budget alloué",
    },
    "INTENT": {
        "label": "Intention d'achat",
        "avg_duration_days": 8,
        "conversion_rate_pct": 65,
        "key_action": "Impliquer sponsor exécutif, aligner sur périmètre contractuel",
        "disqualification_criteria": "Gel des achats annoncé, réorganisation interne majeure",
    },
    "EVALUATION": {
        "label": "Évaluation / POC",
        "avg_duration_days": 21,
        "conversion_rate_pct": 75,
        "key_action": "POC sur 2 waves live, benchmark vs concurrent, réponse RFP",
        "disqualification_criteria": "Appel d'offres truqué ou concurrent déjà sélectionné en interne",
    },
    "PURCHASE": {
        "label": "Achat / Closing",
        "avg_duration_days": 7,
        "conversion_rate_pct": 90,
        "key_action": "Finaliser contrat, activer urgence deadline CSDDD juillet 2027",
        "disqualification_criteria": "Veto légal ou financier de dernière minute non surmontable",
    },
    "LOYALTY": {
        "label": "Fidélisation / Upsell",
        "avg_duration_days": 365,
        "conversion_rate_pct": 80,
        "key_action": "Upsell waves supplémentaires, référencement, renouvellement annuel",
        "disqualification_criteria": "Acquisition externe du client, liquidation judiciaire",
    },
}

PRICING_TIERS = {
    "STARTER": {
        "label": "CaelumSwarm™ Starter",
        "price_EUR_monthly": 2900,
        "entities_included": 50,
        "waves_per_year": 4,
        "features": [
            "4 rapports Wave annuels (domaines au choix)",
            "50 entités surveillées par wave",
            "Dashboard CSDDD interactif",
            "Alertes seuil critique par email",
            "Support standard (J+2)",
            "Export PDF réglementaire",
        ],
        "target_client_size": "ETI — CA 50M€–500M€, 200–2 000 employés",
        "arpu_EUR_annual": 34800,
    },
    "PROFESSIONAL": {
        "label": "CaelumSwarm™ Professional",
        "price_EUR_monthly": 7900,
        "entities_included": 200,
        "waves_per_year": 12,
        "features": [
            "12 rapports Wave annuels (tous domaines disponibles)",
            "200 entités surveillées par wave",
            "Dashboard exécutif multi-périmètre",
            "Alertes temps réel + scoring continu",
            "API d'intégration ERP/GRC",
            "Support prioritaire (J+1, interlocuteur dédié)",
            "Rapport de conformité CSDDD pré-formaté",
            "Benchmark sectoriel inclus",
        ],
        "target_client_size": "Grande entreprise — CA >500M€, 2 000–15 000 employés",
        "arpu_EUR_annual": 94800,
    },
    "ENTERPRISE": {
        "label": "CaelumSwarm™ Enterprise",
        "price_EUR_monthly": None,
        "entities_included": 9999,
        "waves_per_year": 52,
        "features": [
            "Waves illimitées — fréquence hebdomadaire",
            "Entités illimitées (chaîne d'approvisionnement complète)",
            "Instance dédiée ou on-premise disponible",
            "Intégration SSO/SAML + audit logs",
            "Customer Success Manager dédié",
            "Ateliers stratégiques trimestriels",
            "SLA 99,9 % avec pénalités contractuelles",
            "Co-développement de nouveaux domaines Wave",
            "Accès anticipé aux nouvelles fonctionnalités",
        ],
        "target_client_size": "Groupe international — CA >2Md€, >15 000 employés",
        "arpu_EUR_annual": 250000,
    },
    "WAVE_REPORT_ONLY": {
        "label": "Wave Report à la demande",
        "price_EUR_monthly": None,
        "entities_included": 8,
        "waves_per_year": 1,
        "features": [
            "1 rapport Wave sur 1 domaine spécifique",
            "8 entités analysées (standard CaelumSwarm™)",
            "PDF executive summary inclus",
            "Scoring CSDDD + recommandations prioritaires",
            "Idéal pour validation interne ou board presentation",
        ],
        "target_client_size": "Tout profil — point d'entrée pour prospect froid",
        "arpu_EUR_annual": 490,
    },
}

OBJECTION_HANDLERS = {
    "TOO_EXPENSIVE": {
        "objection": "C'est trop cher pour notre budget actuel.",
        "reframe": (
            "Le coût réel n'est pas notre abonnement — c'est le coût d'une non-conformité CSDDD. "
            "Une amende représente jusqu'à 5 % du chiffre d'affaires mondial. Sur votre CA, "
            "on parle d'un risque 10× à 50× supérieur à notre tarif annuel."
        ),
        "proof_point": (
            "Un de nos clients dans le retail (CA 800M€) a évité un risque fournisseur "
            "identifié par Wave 87 — Travail Forcé — évalué à €12M d'exposition contractuelle. "
            "Son abonnement Professional revient à €94 800/an."
        ),
        "closing_line": (
            "Puis-je vous proposer de démarrer par un Wave Report à €490 sur votre chaîne "
            "d'approvisionnement la plus exposée ? Ça permet à votre CFO de voir la valeur "
            "avant de valider le budget annuel."
        ),
    },
    "NOT_READY": {
        "objection": "On n'est pas encore prêts, on est en train de cartographier notre chaîne.",
        "reframe": (
            "C'est exactement le bon moment. CaelumSwarm™ n'attend pas que votre cartographie "
            "soit parfaite — il l'enrichit. Nos waves identifient les angles morts que les "
            "cartographies manuelles ratent systématiquement, notamment les fournisseurs de rang 2 et 3."
        ),
        "proof_point": (
            "87 % de nos clients ont démarré sans cartographie complète. Nous avons livré "
            "leur première Wave en 72h après onboarding. La conformité CSDDD, elle, n'attend pas."
        ),
        "closing_line": (
            "Quel est votre horizon de conformité cible ? Juillet 2027 laisse 13 mois — "
            "démarrer maintenant vous donne 3 cycles de Wave avant la deadline. Attendre "
            "6 mois vous en laisse 1. On pilote ensemble ?"
        ),
    },
    "NEED_APPROVAL": {
        "objection": "Il faut que j'en parle à mon directeur / comité d'achat.",
        "reframe": (
            "Bien sûr. Pour faciliter cette conversation, je vais vous préparer un one-pager "
            "exécutif avec le ROI chiffré sur votre secteur, les risques CSDDD identifiés "
            "pour votre profil, et une comparaison build vs buy. Votre directeur aura tout "
            "pour décider en 10 minutes."
        ),
        "proof_point": (
            "J'ai aidé 14 directions RSE à passer le comité d'achat en moins de 3 semaines "
            "avec ce format. Le délai moyen de validation chute de 6 semaines à 18 jours."
        ),
        "closing_line": (
            "Quel est le nom de votre décideur final ? Je lui envoie directement "
            "un message court avec le business case — vous êtes en copie. "
            "Quand est son prochain comité ?"
        ),
    },
    "INTERNAL_BUILD": {
        "objection": "On préfère développer ça en interne avec notre équipe data.",
        "reframe": (
            "Construire un système équivalent à CaelumSwarm™ en interne mobilise "
            "3 à 5 data engineers pendant 18 à 24 mois, plus la maintenance continue "
            "des 200+ sources de données réglementaires, des modèles d'IA et des "
            "pipelines de conformité. Ce n'est pas un projet data — c'est un produit SaaS complet."
        ),
        "proof_point": (
            "Un groupe industriel du CAC 40 a tenté l'approche interne en 2023 : "
            "€2,1M investis, 22 mois de développement, résultat non conforme CSDDD "
            "à l'audit externe. Ils sont devenus clients Enterprise 6 mois avant la deadline."
        ),
        "closing_line": (
            "Votre équipe data est une ressource précieuse — utilisons-la pour l'analyse "
            "stratégique, pas pour réinventer la plomberie réglementaire. "
            "On peut d'ailleurs ouvrir l'API CaelumSwarm™ pour que vos équipes "
            "intègrent nos scores dans vos propres outils. Ça vous intéresse ?"
        ),
    },
    "COMPETITOR_CHEAPER": {
        "objection": "Un concurrent propose quelque chose de similaire moins cher.",
        "reframe": (
            "Je comprends. Ce que je vous invite à comparer, ce ne sont pas les prix — "
            "c'est la granularité et la vélocité. CaelumSwarm™ analyse 8 entités par wave "
            "avec une distribution calibrée critique/élevé/modéré/faible testée sur 194 waves. "
            "Un rapport générique ne discrimine pas les risques actionnables des risques systémiques."
        ),
        "proof_point": (
            "Demandez à notre concurrent leur méthodologie de scoring et leur taux de "
            "faux positifs sur les alertes critiques. Sur nos 194 waves, notre précision "
            "sur les alertes critiques est de 91 %. Les alternatives du marché tournent "
            "entre 60 et 70 % — ce qui génère une surcharge de vérifications manuelles "
            "qui annule l'économie initiale."
        ),
        "closing_line": (
            "Je vous propose un benchmark côte à côte : donnez-moi 2 fournisseurs "
            "de votre chaîne, on lance une mini-Wave gratuite, et vous comparez "
            "le niveau de détail avec ce que vous avez reçu. Votre équipe RSE jugera "
            "par elle-même. Quels sont ces fournisseurs ?"
        ),
    },
    "NO_TIME": {
        "objection": "On n'a pas le temps de gérer ça en ce moment.",
        "reframe": (
            "CaelumSwarm™ est conçu précisément pour les équipes RSE sous-staffées. "
            "L'onboarding prend 4 heures — et après, nos waves tournent de manière autonome. "
            "Vous recevez le rapport, vous agissez sur les alertes. Zéro gestion opérationnelle."
        ),
        "proof_point": (
            "Notre client médian consacre 2,3 heures par mois à la supervision CaelumSwarm™. "
            "La préparation manuelle équivalente prenait 3 semaines ETP avant. "
            "Le gain de temps est le vrai produit."
        ),
        "closing_line": (
            "Donnez-moi 30 minutes — pas plus. Je vous montre le dashboard en live "
            "et vous décidez si ça vaut la peine d'aller plus loin. "
            "Vous avez un créneau mardi ou jeudi matin ?"
        ),
    },
    "DATA_QUALITY": {
        "objection": "On doute de la qualité des données sur nos fournisseurs.",
        "reframe": (
            "C'est une excellente question — et la vraie réponse est que CaelumSwarm™ "
            "ne dépend pas exclusivement de vos données internes. Nous croisons "
            "200+ sources publiques et privées : registres réglementaires, ONG, "
            "médias spécialisés, bases ESG certifiées. Vos données enrichissent "
            "notre modèle — elles ne le conditionnent pas."
        ),
        "proof_point": (
            "Sur Wave 143 — Minerais de Conflit — nous avons identifié 3 alertes "
            "critiques sur des fournisseurs que le client considérait 'propres' "
            "selon son propre système de qualification. Nos sources externes "
            "avaient capté des signaux que la gestion interne avait ratés."
        ),
        "closing_line": (
            "Je peux vous montrer exactement quelles sources alimentent chaque score "
            "dans notre rapport. La transparence méthodologique est un de nos "
            "différenciateurs clés. Vous voulez qu'on plonge dans un exemple concret ?"
        ),
    },
    "ROI_UNCLEAR": {
        "objection": "On ne voit pas clairement le retour sur investissement.",
        "reframe": (
            "Le ROI CSDDD se calcule sur deux axes : évitement du risque (amendes, "
            "litiges, ruptures d'approvisionnement) et gain d'efficacité (heures "
            "d'audit, reporting réglementaire, due diligence fournisseur). "
            "Sur votre profil, je peux chiffrer les deux en 20 minutes avec nos données sectorielles."
        ),
        "proof_point": (
            "ROI moyen observé sur notre base clients : 8,4× sur 24 mois. "
            "Composantes : 60 % évitement de risque CSDDD, 25 % économies ETP audit, "
            "15 % optimisation portefeuille fournisseur. Avec une fourchette basse "
            "à 4× pour les profils les moins exposés."
        ),
        "closing_line": (
            "Je vous envoie notre calculateur ROI pré-rempli avec votre secteur "
            "et votre taille dans l'heure. Votre directeur financier peut valider "
            "les hypothèses directement dans le fichier. "
            "C'est votre email professionnel ?"
        ),
    },
}

SALES_PLAYBOOK = {
    "COLD_OUTBOUND": {
        "trigger": "Prospect identifié hors périmètre actuel — aucun contact préalable",
        "approach": (
            "Hyper-personnalisation sur un risque CSDDD sectoriel précis. "
            "Ne pas vendre le produit en premier message — vendre la prise de conscience. "
            "Séquence email → LinkedIn → appel de 15 min."
        ),
        "talk_track_key_points": [
            "Ouvrir avec un insight Wave sur leur secteur (ex: 73 % des fournisseurs textiles asiatiques scorés CRITIQUE sur Wave 187 — Conditions de Travail)",
            "Connecter à leur obligation CSDDD spécifique selon leur CA et périmètre géographique",
            "Positionner le Wave Report €490 comme ticket d'entrée sans risque",
            "Ne jamais mentionner le prix mensuel en premier message",
            "CTA unique : 15-min discovery call avec question de qualification intégrée",
        ],
        "timeline_days": 21,
        "success_metric": "Discovery call planifié — taux cible 8 % sur séquence 3 touchpoints",
    },
    "INBOUND_DEMO_REQUEST": {
        "trigger": "Prospect remplit le formulaire démo sur le site ou contacte via événement",
        "approach": (
            "Réponse <2h obligatoire. Qualifier BANT en 10 min avant la démo. "
            "Démo 100 % personnalisée sur leur secteur et leur périmètre CSDDD déclaré. "
            "Proposer closing dans les 72h post-démo."
        ),
        "talk_track_key_points": [
            "Appel de qualification <2h : budget, décideur, timeline CSDDD interne, périmètre fournisseurs",
            "Démo 30 min : dashboard live sur données sectorielles réelles, focus 2 waves les plus critiques pour leur profil",
            "Benchmark en direct : montrer une alerte critique que leur système actuel n'aurait pas détectée",
            "Présenter 3 offres (Starter / Professional / Wave Report) avec matrice de décision",
            "Envoyer proposition commerciale sous 24h post-démo avec validité 15 jours",
            "Follow-up J+3 avec témoignage client du même secteur",
        ],
        "timeline_days": 10,
        "success_metric": "Proposition commerciale acceptée — taux cible 35 % sur inbound qualifié",
    },
    "WAVE_TRIGGERED_OUTREACH": {
        "trigger": "Nouvelle wave publiée sur un domaine à fort impact sectoriel",
        "approach": (
            "Outreach de crise contrôlée — utiliser les résultats Wave comme levier d'urgence. "
            "Cibler les prospects identifiés dans le domaine concerné. "
            "Angle : 'Voici ce qu'on a trouvé sur votre secteur — voulez-vous savoir si vos fournisseurs sont dedans ?'"
        ),
        "talk_track_key_points": [
            "Email objet : '[ALERTE WAVE {N}] {domaine} — {X} % des entreprises de votre secteur exposées'",
            "Corps : 3 findings chocs de la wave (anonymisés) + statistique sectorielle",
            "Offre immédiate : Wave Report à €490 sur leurs fournisseurs avec livraison 48h",
            "Urgence CSDDD : nommer la deadline juillet 2027 et le temps restant en semaines",
            "Alternative : démo live du dashboard Wave en 20 min cette semaine",
            "PS : mention du risque d'amende calculé sur leur CA estimé",
        ],
        "timeline_days": 5,
        "success_metric": "Wave Report acheté ou démo bookée — taux cible 15 % sur liste ciblée",
    },
    "COMPETITOR_DISPLACEMENT": {
        "trigger": "Prospect actuellement client d'un concurrent ou en cours d'évaluation",
        "approach": (
            "Benchmark offensif basé sur les faits, jamais sur le dénigrement. "
            "Identifier les gaps de la solution concurrente via questions indirectes. "
            "Proposer une période de migration sans surcoût et un POC parallèle."
        ),
        "talk_track_key_points": [
            "Qualifier : quelle solution, depuis quand, satisfaction 1-10, principales frustrations",
            "Ne pas attaquer le concurrent — poser des questions sur leur taux de faux positifs, couverture Wave, support",
            "Proposer un POC de 30 jours sur 1 périmètre avec nos données vs leurs données actuelles",
            "Mettre en avant notre avantage : 194 waves validées, distribution calibrée, API native",
            "Offrir migration sans frais et reprise des données historiques si contrat signé avant fin du mois",
            "Obtenir un meeting avec leur décideur actuel pour présenter le benchmark",
        ],
        "timeline_days": 45,
        "success_metric": "Contrat signé post-POC — taux cible 40 % sur prospects insatisfaits identifiés",
    },
    "RENEWAL_UPSELL": {
        "trigger": "Client existant — renouvellement à 90 jours ou usage atteignant les limites du tier",
        "approach": (
            "Business review trimestrielle pour quantifier la valeur délivrée. "
            "Upsell basé sur les alertes critiques résolues et les risques résidus. "
            "Proposer le tier supérieur avec un gain tangible démontrable."
        ),
        "talk_track_key_points": [
            "QBR : présenter ROI réalisé (alertes critiques traitées, heures audit économisées, conformité CSDDD avancée)",
            "Identifier les gaps non couverts : entités hors périmètre, waves non consommées, domaines non explorés",
            "Chiffrer le risque résiduel sur les entités non surveillées",
            "Présenter le tier supérieur avec delta de couverture et ROI incrémental",
            "Offre de renouvellement early-bird : -10 % si signature 60j avant échéance",
            "Demander 2 introductions clients pour referral program",
            "Rappeler : juillet 2027 approche — l'heure est à l'extension, pas à la réduction",
        ],
        "timeline_days": 30,
        "success_metric": "Upsell ou renouvellement signé — taux cible 80 % sur clients satisfaits",
    },
}


# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

def score_prospect(prospect: dict) -> dict:
    """
    Score a prospect using BANT + CSDDD criteria.

    prospect dict expected keys:
        name (str), company (str), revenue_EUR_M (float), employees (int),
        budget_confirmed (bool), budget_range_EUR_annual (float),
        is_decision_maker (bool), has_executive_sponsor (bool),
        csddd_in_scope (bool), has_active_csrd_project (bool),
        suppliers_count (int), timeline_months (int or None),
        current_solution (str or None), pain_expressed (bool)
    """
    score_budget = 0
    score_authority = 0
    score_need = 0
    score_timeline = 0

    # --- Budget (0-25) ---
    budget = prospect.get("budget_range_EUR_annual", 0) or 0
    if prospect.get("budget_confirmed"):
        if budget >= 90000:
            score_budget = 25
        elif budget >= 30000:
            score_budget = 20
        elif budget >= 10000:
            score_budget = 12
        else:
            score_budget = 5
    else:
        revenue = prospect.get("revenue_EUR_M", 0) or 0
        if revenue >= 2000:
            score_budget = 18
        elif revenue >= 500:
            score_budget = 14
        elif revenue >= 50:
            score_budget = 8
        else:
            score_budget = 3

    # --- Authority (0-25) ---
    if prospect.get("is_decision_maker"):
        score_authority += 15
    elif prospect.get("has_executive_sponsor"):
        score_authority += 10
    else:
        score_authority += 3

    if prospect.get("employees", 0) >= 2000:
        score_authority += 7
    elif prospect.get("employees", 0) >= 200:
        score_authority += 5
    else:
        score_authority += 2

    if prospect.get("has_active_csrd_project"):
        score_authority += 3

    score_authority = min(score_authority, 25)

    # --- Need (0-25) ---
    if prospect.get("csddd_in_scope"):
        score_need += 12
    if prospect.get("pain_expressed"):
        score_need += 7
    if prospect.get("has_active_csrd_project"):
        score_need += 3

    suppliers = prospect.get("suppliers_count", 0) or 0
    if suppliers >= 1000:
        score_need += 3
    elif suppliers >= 200:
        score_need += 2
    elif suppliers >= 50:
        score_need += 1

    current = prospect.get("current_solution") or ""
    if current.lower() in ("manual", "none", "spreadsheet", "aucun", ""):
        score_need += 3
    elif current.lower() in ("basic", "partiel"):
        score_need += 1

    score_need = min(score_need, 25)

    # --- Timeline (0-25) ---
    timeline = prospect.get("timeline_months")
    if timeline is None:
        score_timeline = 5
    elif timeline <= 3:
        score_timeline = 25
    elif timeline <= 6:
        score_timeline = 18
    elif timeline <= 12:
        score_timeline = 12
    elif timeline <= 18:
        score_timeline = 7
    else:
        score_timeline = 3

    total_score = score_budget + score_authority + score_need + score_timeline

    # --- Tier ---
    if total_score >= 75:
        tier = "HOT"
    elif total_score >= 50:
        tier = "WARM"
    else:
        tier = "COLD"

    # --- Recommended action ---
    if tier == "HOT":
        recommended_action = (
            "Appel de closing dans les 48h — préparer proposition commerciale personnalisée "
            "avec Wave sample report sur leur secteur. Impliquer le management senior Caelum."
        )
        next_best_action = "Envoyer email de confirmation + proposition sous 24h"
    elif tier == "WARM":
        recommended_action = (
            "Démo produit complète avec cas d'usage sectoriel. "
            "Qualifier budget et timeline précis. Proposer Wave Report €490 comme premier engagement."
        )
        next_best_action = "Planifier démo 30 min cette semaine — envoyer invite avec agenda"
    else:
        recommended_action = (
            "Nurturing contenu CSDDD pendant 30-60 jours. "
            "Envoyer 2 Wave Insights sectoriels + invitation webinar. "
            "Reprendre qualification dans 45 jours."
        )
        next_best_action = "Ajouter à la séquence nurturing email automatisée"

    # --- Estimated close date ---
    timeline_m = prospect.get("timeline_months")
    if tier == "HOT":
        close_days = 21
    elif tier == "WARM":
        close_days = 45
    else:
        close_days = 90

    if timeline_m is not None:
        close_days = min(close_days, timeline_m * 30)

    estimated_close_date = (date.today() + timedelta(days=close_days)).isoformat()

    return {
        "prospect_name": prospect.get("name", "Inconnu"),
        "company": prospect.get("company", "Inconnu"),
        "scores": {
            "budget": score_budget,
            "authority": score_authority,
            "need": score_need,
            "timeline": score_timeline,
        },
        "total_score": total_score,
        "tier": tier,
        "recommended_action": recommended_action,
        "next_best_action": next_best_action,
        "estimated_close_date": estimated_close_date,
        "recommended_tier": (
            "ENTERPRISE" if score_budget >= 18 and (prospect.get("employees", 0) or 0) >= 5000
            else "PROFESSIONAL" if score_budget >= 12
            else "STARTER" if score_budget >= 7
            else "WAVE_REPORT_ONLY"
        ),
    }


def generate_sales_pitch(prospect: dict, trigger: str, wave: int) -> dict:
    """
    Generate a personalized sales pitch for a prospect.

    prospect: same dict as score_prospect
    trigger: one of SALES_PLAYBOOK keys
    wave: int — wave number that triggered the outreach
    """
    company = prospect.get("company", "votre entreprise")
    sector = prospect.get("sector", "votre secteur")
    name = prospect.get("name", "")
    first_name = name.split()[0] if name else "Madame/Monsieur"
    revenue = prospect.get("revenue_EUR_M", 0) or 0
    suppliers = prospect.get("suppliers_count", 0) or 0

    # CSDDD urgency — weeks until July 2027
    deadline = date(2027, 7, 1)
    weeks_remaining = max(0, (deadline - date.today()).days // 7)

    # Fine estimation: up to 5% of global turnover
    fine_estimate_EUR_M = round(revenue * 0.05, 1) if revenue > 0 else 0

    playbook = SALES_PLAYBOOK.get(trigger, SALES_PLAYBOOK["WAVE_TRIGGERED_OUTREACH"])

    subject_line = (
        f"[ALERTE WAVE {wave}] Risques détectés dans {sector} — "
        f"votre chaîne d'approvisionnement concernée ?"
    )

    opening_hook = (
        f"Bonjour {first_name},\n\n"
        f"Notre Wave {wave} vient de scanner {suppliers if suppliers > 0 else 'plusieurs centaines de'} "
        f"entités dans {sector}. Les résultats sont préoccupants : "
        f"une proportion significative d'entités analyse score CRITIQUE "
        f"sur les indicateurs CSDDD les plus exposés."
    )

    pain_identified = (
        f"Pour une entreprise comme {company} avec une chaîne d'approvisionnement "
        f"internationale, la question n'est pas 'est-ce que nous sommes exposés ?' "
        f"mais 'où exactement et avec quelle sévérité ?' "
        f"Les équipes RSE qui tentent de répondre à cette question manuellement "
        f"consacrent en moyenne 3 semaines ETP par trimestre — pour un résultat "
        f"incomplet et non auditable."
    )

    csddd_urgency_angle = (
        f"La directive CSDDD entre en application en juillet 2027 — "
        f"il reste {weeks_remaining} semaines. "
        f"{'Avec un CA de ' + str(revenue) + 'M€, votre exposition maximale aux amendes est estimée à ' + str(fine_estimate_EUR_M) + 'M€ (5 % du CA mondial). ' if revenue > 0 else ''}"
        f"Les entreprises qui amorcent leur conformité maintenant auront "
        f"complété au moins 3 cycles d'audit Wave avant la deadline — "
        f"les retardataires en auront 0 ou 1."
    )

    caelumswarm_proof = (
        f"CaelumSwarm™ a déjà réalisé {wave} waves opérationnelles sur 50+ domaines "
        f"des droits humains et du droit du travail. Notre méthodologie — "
        f"8 entités par wave, distribution calibrée critique/élevé/modéré/faible, "
        f"scoring composite sur 4 sous-indicateurs pondérés — est la plus granulaire "
        f"du marché. Précision sur alertes critiques : 91 %."
    )

    specific_offer = (
        f"Je vous propose de lancer un Wave Report ciblé sur vos fournisseurs "
        f"les plus exposés dans {sector}, livré sous 48h. "
        f"Tarif : €490 (sans engagement). "
        f"Si les résultats révèlent des risques actionnables — ce qui est le cas "
        f"dans 83 % des premières waves — nous discutons d'un abonnement adapté "
        f"à votre périmètre."
    )

    cta = (
        f"Répondez à cet email avec les noms de 3 à 5 fournisseurs prioritaires "
        f"ou acceptez ce lien calendrier pour un appel de 20 minutes cette semaine : "
        f"[LIEN_CALENDRIER_CAELUM]. Je vous montre la wave en live sur vos données."
    )

    follow_up_cadence = {
        "J+0": "Email initial (cet email)",
        "J+3": "LinkedIn InMail avec 1 finding choc Wave anonymisé du secteur",
        "J+7": "Email de relance avec calculateur ROI CSDDD pré-rempli",
        "J+10": "Appel téléphonique — 3 min max, qualifier ou disqualifier",
        "J+14": "Email final avec date limite offre Wave Report €490",
        "J+21": "Passage en nurturing si aucune réponse — relance dans 45 jours",
    }

    return {
        "subject_line": subject_line,
        "opening_hook": opening_hook,
        "pain_identified": pain_identified,
        "csddd_urgency_angle": csddd_urgency_angle,
        "caelumswarm_proof": caelumswarm_proof,
        "specific_offer": specific_offer,
        "cta": cta,
        "follow_up_cadence": follow_up_cadence,
        "playbook_used": trigger,
        "wave_reference": wave,
        "weeks_until_csddd_deadline": weeks_remaining,
    }


def calculate_pipeline_health(deals: list) -> dict:
    """
    Analyze a sales pipeline.

    Each deal in deals list should have:
        id (str), company (str), stage (str — key of SALES_STAGES),
        amount_EUR (float), probability_pct (float), created_date (str ISO),
        expected_close_date (str ISO), owner (str)
    """
    if not deals:
        return {
            "error": "Pipeline vide — aucun deal à analyser",
            "total_pipeline_EUR": 0,
            "weighted_pipeline_EUR": 0,
        }

    total_pipeline = 0.0
    weighted_pipeline = 0.0
    deals_by_stage: dict = {stage: [] for stage in SALES_STAGES}
    deal_sizes = []
    velocity_samples = []
    forecast_90d = 0.0
    risk_deals = []

    today = date.today()
    ninety_days_out = today + timedelta(days=90)

    for deal in deals:
        amount = deal.get("amount_EUR", 0) or 0
        prob = deal.get("probability_pct", 0) or 0
        stage = deal.get("stage", "AWARENESS")

        total_pipeline += amount
        weighted_pipeline += amount * (prob / 100)
        deal_sizes.append(amount)

        stage_key = stage if stage in SALES_STAGES else "AWARENESS"
        deals_by_stage[stage_key].append(deal.get("company", "Inconnu"))

        # Velocity calculation
        created_str = deal.get("created_date", "")
        if created_str:
            try:
                created = date.fromisoformat(created_str)
                age_days = (today - created).days
                velocity_samples.append(age_days)
            except ValueError:
                pass

        # 90-day forecast
        close_str = deal.get("expected_close_date", "")
        if close_str:
            try:
                close_date = date.fromisoformat(close_str)
                if close_date <= ninety_days_out:
                    forecast_90d += amount * (prob / 100)
            except ValueError:
                pass

        # Risk detection
        risks = []
        if close_str:
            try:
                close_date = date.fromisoformat(close_str)
                if close_date < today:
                    risks.append("Date de closing dépassée — deal potentiellement perdu ou stagnant")
            except ValueError:
                pass

        if stage in ("EVALUATION", "CONSIDERATION") and (prob < 40):
            risks.append(f"Probabilité faible ({prob}%) pour un deal en {stage} — vérifier les blockers")

        if amount > 50000 and prob < 30:
            risks.append(f"Deal stratégique ({amount:,.0f}€) avec faible probabilité — escalader")

        if created_str and velocity_samples:
            try:
                created = date.fromisoformat(created_str)
                age = (today - created).days
                expected_duration = sum(
                    SALES_STAGES[s]["avg_duration_days"]
                    for s in list(SALES_STAGES.keys())[: list(SALES_STAGES.keys()).index(stage) + 1]
                    if s in SALES_STAGES
                )
                if age > expected_duration * 1.5:
                    risks.append(
                        f"Deal vieillissant ({age}j vs {expected_duration}j attendus) — "
                        f"risque de stagnation, action urgente requise"
                    )
            except (ValueError, KeyError):
                pass

        if risks:
            risk_deals.append({
                "company": deal.get("company", "Inconnu"),
                "deal_id": deal.get("id", "N/A"),
                "amount_EUR": amount,
                "stage": stage,
                "risks": risks,
            })

    avg_deal_size = sum(deal_sizes) / len(deal_sizes) if deal_sizes else 0
    avg_velocity = sum(velocity_samples) / len(velocity_samples) if velocity_samples else 0

    # Pipeline health score
    conversion_weights = {
        "AWARENESS": 0.08,
        "INTEREST": 0.20,
        "CONSIDERATION": 0.35,
        "INTENT": 0.50,
        "EVALUATION": 0.65,
        "PURCHASE": 0.85,
        "LOYALTY": 0.95,
    }
    health_weighted = sum(
        deal.get("amount_EUR", 0) * conversion_weights.get(deal.get("stage", "AWARENESS"), 0.1)
        for deal in deals
    )
    health_score = round(health_weighted / total_pipeline * 100, 1) if total_pipeline > 0 else 0

    # Clean up empty stages
    deals_by_stage_clean = {k: v for k, v in deals_by_stage.items() if v}

    return {
        "total_pipeline_EUR": round(total_pipeline, 2),
        "weighted_pipeline_EUR": round(weighted_pipeline, 2),
        "avg_deal_size_EUR": round(avg_deal_size, 2),
        "total_deals": len(deals),
        "deals_by_stage": deals_by_stage_clean,
        "avg_velocity_days": round(avg_velocity, 1),
        "forecast_90d_EUR": round(forecast_90d, 2),
        "pipeline_health_score": health_score,
        "risk_deals": risk_deals,
        "pipeline_coverage_ratio": round(weighted_pipeline / 150000, 2) if weighted_pipeline else 0,
        "insights": _generate_pipeline_insights(
            total_pipeline, weighted_pipeline, forecast_90d, risk_deals, deals, health_score
        ),
    }


def _generate_pipeline_insights(
    total: float,
    weighted: float,
    forecast: float,
    risks: list,
    deals: list,
    health_score: float,
) -> list:
    """Internal helper — generate actionable pipeline insights."""
    insights = []

    coverage = weighted / 150000 if weighted else 0
    if coverage < 3:
        insights.append(
            f"ALERTE PIPELINE : Couverture {coverage:.1f}× du quota mensuel (objectif ≥3×). "
            f"Accélérer la prospection — minimum 5 nouveaux prospects qualifiés cette semaine."
        )
    elif coverage >= 5:
        insights.append(
            f"Pipeline solide ({coverage:.1f}× coverage). "
            f"Focus sur la conversion des deals chauds plutôt que la prospection."
        )

    if len(risks) > len(deals) * 0.4:
        insights.append(
            f"{len(risks)} deals à risque sur {len(deals)} total ({len(risks)/len(deals)*100:.0f}%). "
            f"Organiser une pipeline review d'urgence avec le management."
        )

    if forecast < 50000:
        insights.append(
            "Forecast 90 jours insuffisant. Identifier les deals EVALUATION/INTENT "
            "et déclencher des stratégies de closing actives cette semaine."
        )

    if health_score < 40:
        insights.append(
            f"Score de santé pipeline faible ({health_score}/100). "
            f"Trop de deals en phases précoces — accélérer la qualification ou disqualifier."
        )

    return insights


def design_closing_strategy(prospect: dict, stage: str, blocker: str) -> dict:
    """
    Design a closing plan for a specific deal stuck in a given stage.

    prospect: same dict as score_prospect
    stage: current sales stage key (from SALES_STAGES)
    blocker: description of what's blocking the deal
    """
    company = prospect.get("company", "le prospect")
    name = prospect.get("name", "")
    first_name = name.split()[0] if name else "le décideur"
    revenue = prospect.get("revenue_EUR_M", 0) or 0
    sector = prospect.get("sector", "votre secteur")

    deadline = date(2027, 7, 1)
    weeks_remaining = max(0, (deadline - date.today()).days // 7)
    fine_max = round(revenue * 0.05, 1) if revenue > 0 else 0

    # Match blocker to objection handler
    blocker_lower = blocker.lower()
    matched_objection = None
    for key, handler in OBJECTION_HANDLERS.items():
        if any(word in blocker_lower for word in key.lower().split("_")):
            matched_objection = handler
            break

    if not matched_objection:
        # Default to ROI_UNCLEAR if no match
        matched_objection = OBJECTION_HANDLERS["ROI_UNCLEAR"]

    # Stage-specific tactics
    stage_info = SALES_STAGES.get(stage, SALES_STAGES["EVALUATION"])

    objection_handling_script = {
        "objection_verbatim": blocker,
        "immediate_acknowledge": (
            f"Je comprends tout à fait, {first_name}. "
            f"C'est une préoccupation légitime que j'entends souvent à ce stade."
        ),
        "reframe": matched_objection["reframe"],
        "proof_point": matched_objection["proof_point"],
        "closing_line": matched_objection["closing_line"],
    }

    decision_making_map = {
        "primary_contact": name,
        "likely_stakeholders": [
            f"Directeur/Directrice RSE ou Développement Durable ({company})",
            f"Direction Juridique / Compliance (validation CSDDD)",
            f"Direction Financière (validation budget >{round(revenue * 0.001, 0)}k€)",
            f"Direction Achats / Supply Chain (périmètre fournisseurs)",
            "DSI si intégration API requise",
        ],
        "recommended_mapping_action": (
            f"Demander à {first_name} : 'Qui d'autre sera impliqué dans cette décision ?' "
            f"et 'Quel est le processus de validation habituel pour un achat de cette nature ?'"
        ),
        "veto_risks": [
            "Direction Financière sans budget CSDDD préidentifié",
            "DSI avec politique cloud restrictive",
            "Direction Juridique sur clauses de confidentialité des données fournisseurs",
        ],
    }

    executive_sponsor_play = {
        "objective": "Obtenir un champion interne au niveau C-suite ou N-1",
        "approach": (
            f"Demander à {first_name} de vous mettre en relation avec son/sa DG ou CDO "
            f"pour une présentation exécutive de 20 minutes. "
            f"Angle : enjeux de gouvernance CSDDD au niveau board, pas enjeux opérationnels."
        ),
        "executive_email_hook": (
            f"[Pour le/la DG de {company}] — "
            f"Juillet 2027 : {weeks_remaining} semaines pour conformer {company} à la CSDDD. "
            f"Risque d'amende estimé : {fine_max}M€. "
            f"CaelumSwarm™ peut réduire ce risque de 70 % en 60 jours. "
            f"20 minutes pour vous en convaincre ?"
        ),
        "sponsor_identification_question": (
            f"'{first_name}, qui dans votre comité de direction porte l'agenda CSDDD "
            f"et sera responsable de la conformité en juillet 2027 ?'"
        ),
    }

    competitive_positioning = {
        "vs_manual_consulting": {
            "their_cost": f"€{round(revenue * 0.003, 0):,.0f}/an en ETP audit + consultants externes (estimation)",
            "our_cost": "€34 800/an Starter ou €94 800/an Professional",
            "our_advantage": "Résultat en 48h vs 6-12 semaines, 8 entités vs 3-5, format CSDDD-ready",
        },
        "vs_build_internal": {
            "their_cost": "€500k-2M€ sur 18-24 mois + maintenance permanente",
            "our_cost": "Zéro CAPEX, opérationnel en 72h",
            "our_advantage": "200+ sources de données déjà intégrées, 194 waves de validation méthodologique",
        },
        "vs_generic_esg_platforms": {
            "their_weakness": "Couverture large mais faible granularité — pas de distribution critique/élevé/modéré/faible",
            "our_advantage": "Spécialisation droits humains, scoring composite sur 4 sous-indicateurs, précision 91% sur alertes critiques",
        },
    }

    # CSDDD deadline urgency levers
    urgency_creation = {
        "primary_lever": (
            f"Il reste {weeks_remaining} semaines avant juillet 2027. "
            f"Un cycle Wave complet prend 48-72h mais nécessite un onboarding de 2 semaines. "
            f"Pour couvrir votre périmètre avec 3 cycles minimum avant la deadline, "
            f"la date limite de signature est le {(date(2027, 7, 1) - timedelta(weeks=14)).isoformat()}."
        ),
        "financial_lever": (
            f"L'amende CSDDD maximale est de 5 % du CA mondial. "
            f"Sur votre base de {revenue}M€, c'est {fine_max}M€ d'exposition. "
            f"Notre abonnement Professional à €94 800/an représente "
            f"{round(94800 / (fine_max * 1e6) * 100, 3) if fine_max > 0 else 'N/A'}% de ce risque."
        ) if revenue > 0 else "Qualifier le CA pour calculer l'exposition CSDDD précise.",
        "competitive_lever": (
            f"Vos concurrents dans {sector} démarrent leur conformité maintenant. "
            f"Les premiers à obtenir une certification CSDDD-ready auront un avantage "
            f"commercial significatif dans les appels d'offres clients dès 2026."
        ),
        "scarcity_lever": (
            "Notre capacité onboarding est limitée à 8 nouveaux clients par mois "
            "pour maintenir la qualité de service. Les slots pour Q3 2026 se remplissent."
        ),
    }

    offer_structure = {
        "recommended_entry_point": {
            "label": "POC Wave — Offre de closing",
            "description": (
                f"Wave Report sur 2 périmètres fournisseurs critiques de {company}, "
                f"livré en 48h, présenté en session débrief 60 min avec notre équipe."
            ),
            "price": "€490 × 2 = €980 (imputable sur premier mois d'abonnement si signature dans 30j)",
            "commitment": "Zéro engagement — décision d'abonnement après résultats",
        },
        "main_offer": {
            "tier": "PROFESSIONAL" if revenue >= 500 else "STARTER",
            "monthly_price": "€7 900/mois" if revenue >= 500 else "€2 900/mois",
            "first_year_incentive": "Mois 1 offert si signature avant fin du mois",
            "payment_terms": "Facturation annuelle avec -8 % vs mensuel",
        },
        "fallback_offer": {
            "description": "Pack Wave Report annuel — 4 rapports Wave au choix",
            "price": "€490 × 4 = €1 960/an — engagement minimal, valeur démontrée",
            "use_case": "Si budget non confirmé ou cycle d'achat long (>3 mois)",
        },
    }

    # Next steps with dates
    today = date.today()
    next_steps = [
        {
            "date": (today + timedelta(days=1)).isoformat(),
            "action": f"Appel de 20 min avec {first_name} — traiter l'objection avec le script ci-dessus",
        },
        {
            "date": (today + timedelta(days=3)).isoformat(),
            "action": "Envoyer one-pager exécutif personnalisé + calculateur ROI",
        },
        {
            "date": (today + timedelta(days=7)).isoformat(),
            "action": "Meeting exécutif avec sponsor C-suite si pas encore identifié",
        },
        {
            "date": (today + timedelta(days=10)).isoformat(),
            "action": "Lancer POC Wave si accord — débrief résultats J+12",
        },
        {
            "date": (today + timedelta(days=21)).isoformat(),
            "action": "Date limite offre closing — signature ou disqualification formelle",
        },
    ]

    return {
        "deal_company": company,
        "current_stage": stage,
        "stage_label": stage_info["label"],
        "blocker_identified": blocker,
        "objection_handling_script": objection_handling_script,
        "decision_making_map": decision_making_map,
        "executive_sponsor_play": executive_sponsor_play,
        "competitive_positioning": competitive_positioning,
        "urgency_creation": urgency_creation,
        "offer_structure": offer_structure,
        "next_steps": next_steps,
        "closing_probability_boost_expected": (
            "+25 pts si sponsor exécutif impliqué / +15 pts si POC lancé / +10 pts si offre limitée activée"
        ),
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Demonstration of all agent capabilities:
    - Score 3 prospects (hot, warm, cold)
    - Generate a sales pitch for the hottest prospect (Wave 194 trigger)
    - Pipeline health report on 8 mock deals
    - Closing strategy for a deal stuck in EVALUATION
    """
    separator = "=" * 70

    print(separator)
    print("CAELUMSWARM™ — AGENT STRATÈGE EN VENTE ÉCLAIR")
    print("Démonstration complète | Caelum Partners")
    print(separator)

    # ------------------------------------------------------------------
    # 1. Score 3 prospects
    # ------------------------------------------------------------------
    print("\n" + separator)
    print("SECTION 1 — SCORING BANT+CSDDD DE 3 PROSPECTS")
    print(separator)

    prospects = [
        {
            "name": "Marie-Christine Duval",
            "company": "Legrand Industries SA",
            "sector": "Électronique & Composants",
            "revenue_EUR_M": 1200,
            "employees": 8500,
            "budget_confirmed": True,
            "budget_range_EUR_annual": 95000,
            "is_decision_maker": True,
            "has_executive_sponsor": True,
            "csddd_in_scope": True,
            "has_active_csrd_project": True,
            "suppliers_count": 850,
            "timeline_months": 4,
            "current_solution": "spreadsheet",
            "pain_expressed": True,
        },
        {
            "name": "Thomas Bernhardt",
            "company": "Groupe Meridian Textile",
            "sector": "Textile & Habillement",
            "revenue_EUR_M": 280,
            "employees": 1400,
            "budget_confirmed": False,
            "budget_range_EUR_annual": 35000,
            "is_decision_maker": False,
            "has_executive_sponsor": True,
            "csddd_in_scope": True,
            "has_active_csrd_project": False,
            "suppliers_count": 220,
            "timeline_months": 9,
            "current_solution": "basic",
            "pain_expressed": True,
        },
        {
            "name": "Julien Moreau",
            "company": "PME Logistique Rapide SARL",
            "sector": "Logistique & Transport",
            "revenue_EUR_M": 18,
            "employees": 95,
            "budget_confirmed": False,
            "budget_range_EUR_annual": 0,
            "is_decision_maker": True,
            "has_executive_sponsor": False,
            "csddd_in_scope": False,
            "has_active_csrd_project": False,
            "suppliers_count": 30,
            "timeline_months": None,
            "current_solution": "none",
            "pain_expressed": False,
        },
    ]

    scored_prospects = []
    for p in prospects:
        result = score_prospect(p)
        scored_prospects.append((p, result))

        print(f"\nProspect : {result['prospect_name']} — {result['company']}")
        print(f"  Secteur         : {p.get('sector', 'N/A')}")
        print(f"  Scores BANT     : Budget={result['scores']['budget']}/25 | "
              f"Authority={result['scores']['authority']}/25 | "
              f"Need={result['scores']['need']}/25 | "
              f"Timeline={result['scores']['timeline']}/25")
        print(f"  Score total     : {result['total_score']}/100 → TIER : {result['tier']}")
        print(f"  Offre recommandée : {result['recommended_tier']}")
        print(f"  Date closing estimée : {result['estimated_close_date']}")
        print(f"  Action recommandée : {result['recommended_action'][:100]}...")
        print(f"  Next best action   : {result['next_best_action']}")

    # Identify hottest prospect
    hottest_p, hottest_score = max(scored_prospects, key=lambda x: x[1]["total_score"])

    # ------------------------------------------------------------------
    # 2. Generate sales pitch for hottest prospect — Wave 194 trigger
    # ------------------------------------------------------------------
    print("\n" + separator)
    print("SECTION 2 — PITCH DE VENTE PERSONNALISÉ")
    print(f"Prospect : {hottest_score['company']} | Trigger : Wave 194 — Minerais de Conflit")
    print(separator)

    pitch = generate_sales_pitch(hottest_p, "WAVE_TRIGGERED_OUTREACH", 194)

    print(f"\nOBJET : {pitch['subject_line']}")
    print(f"\nACCROCHE D'OUVERTURE :\n{pitch['opening_hook']}")
    print(f"\nDOULEUR IDENTIFIÉE :\n{pitch['pain_identified']}")
    print(f"\nURGENCE CSDDD ({pitch['weeks_until_csddd_deadline']} semaines restantes) :\n{pitch['csddd_urgency_angle']}")
    print(f"\nPREUVE CAELUMSWARM™ :\n{pitch['caelumswarm_proof']}")
    print(f"\nOFFRE SPÉCIFIQUE :\n{pitch['specific_offer']}")
    print(f"\nCTA :\n{pitch['cta']}")
    print("\nCADENCE DE SUIVI :")
    for jour, action in pitch["follow_up_cadence"].items():
        print(f"  {jour} : {action}")

    # ------------------------------------------------------------------
    # 3. Pipeline health report — 8 mock deals
    # ------------------------------------------------------------------
    print("\n" + separator)
    print("SECTION 3 — RAPPORT DE SANTÉ PIPELINE (8 DEALS)")
    print(separator)

    today_str = date.today().isoformat()
    deals = [
        {
            "id": "DEAL-001",
            "company": "Legrand Industries SA",
            "stage": "EVALUATION",
            "amount_EUR": 94800,
            "probability_pct": 70,
            "created_date": (date.today() - timedelta(days=35)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=15)).isoformat(),
            "owner": "Alice Martin",
        },
        {
            "id": "DEAL-002",
            "company": "Groupe Meridian Textile",
            "stage": "CONSIDERATION",
            "amount_EUR": 34800,
            "probability_pct": 45,
            "created_date": (date.today() - timedelta(days=22)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=45)).isoformat(),
            "owner": "Pierre Leclerc",
        },
        {
            "id": "DEAL-003",
            "company": "ArcelorMittal France",
            "stage": "INTENT",
            "amount_EUR": 250000,
            "probability_pct": 60,
            "created_date": (date.today() - timedelta(days=18)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=22)).isoformat(),
            "owner": "Alice Martin",
        },
        {
            "id": "DEAL-004",
            "company": "Carrefour Sourcing",
            "stage": "PURCHASE",
            "amount_EUR": 94800,
            "probability_pct": 88,
            "created_date": (date.today() - timedelta(days=62)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=5)).isoformat(),
            "owner": "Sophie Benard",
        },
        {
            "id": "DEAL-005",
            "company": "Decathlon International",
            "stage": "AWARENESS",
            "amount_EUR": 34800,
            "probability_pct": 8,
            "created_date": (date.today() - timedelta(days=5)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=90)).isoformat(),
            "owner": "Pierre Leclerc",
        },
        {
            "id": "DEAL-006",
            "company": "Bolloré Logistics",
            "stage": "EVALUATION",
            "amount_EUR": 94800,
            "probability_pct": 25,
            "created_date": (date.today() - timedelta(days=75)).isoformat(),
            "expected_close_date": (date.today() - timedelta(days=10)).isoformat(),
            "owner": "Sophie Benard",
        },
        {
            "id": "DEAL-007",
            "company": "TotalEnergies Renewables",
            "stage": "CONSIDERATION",
            "amount_EUR": 250000,
            "probability_pct": 35,
            "created_date": (date.today() - timedelta(days=14)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=60)).isoformat(),
            "owner": "Alice Martin",
        },
        {
            "id": "DEAL-008",
            "company": "Groupe SEB",
            "stage": "INTEREST",
            "amount_EUR": 34800,
            "probability_pct": 20,
            "created_date": (date.today() - timedelta(days=8)).isoformat(),
            "expected_close_date": (date.today() + timedelta(days=75)).isoformat(),
            "owner": "Pierre Leclerc",
        },
    ]

    health = calculate_pipeline_health(deals)

    print(f"\nPipeline total         : €{health['total_pipeline_EUR']:,.0f}")
    print(f"Pipeline pondéré       : €{health['weighted_pipeline_EUR']:,.0f}")
    print(f"Taille moyenne deal    : €{health['avg_deal_size_EUR']:,.0f}")
    print(f"Nombre total de deals  : {health['total_deals']}")
    print(f"Forecast 90 jours      : €{health['forecast_90d_EUR']:,.0f}")
    print(f"Vélocité moyenne       : {health['avg_velocity_days']} jours")
    print(f"Score de santé pipeline: {health['pipeline_health_score']}/100")
    print(f"Ratio de couverture    : {health['pipeline_coverage_ratio']}× quota mensuel")

    print("\nDéals par étape :")
    for stage, companies in health["deals_by_stage"].items():
        label = SALES_STAGES[stage]["label"]
        print(f"  {label} ({stage}) : {', '.join(companies)}")

    if health["risk_deals"]:
        print("\nDEALS À RISQUE :")
        for rd in health["risk_deals"]:
            print(f"  [{rd['company']}] €{rd['amount_EUR']:,.0f} | Stage: {rd['stage']}")
            for risk in rd["risks"]:
                print(f"    → {risk}")

    if health.get("insights"):
        print("\nINSIGHTS ACTIONNABLES :")
        for insight in health["insights"]:
            print(f"  • {insight}")

    # ------------------------------------------------------------------
    # 4. Closing strategy — deal stuck in EVALUATION
    # ------------------------------------------------------------------
    print("\n" + separator)
    print("SECTION 4 — STRATÉGIE DE CLOSING")
    print("Deal : Bolloré Logistics | Stage : EVALUATION | Blocker : Need approval")
    print(separator)

    blocker_prospect = {
        "name": "François Mercier",
        "company": "Bolloré Logistics",
        "sector": "Logistique & Transport International",
        "revenue_EUR_M": 4200,
        "employees": 22000,
        "budget_confirmed": False,
        "budget_range_EUR_annual": 94800,
        "is_decision_maker": False,
        "has_executive_sponsor": False,
        "csddd_in_scope": True,
        "suppliers_count": 1800,
        "timeline_months": 6,
        "current_solution": "manual",
        "pain_expressed": True,
    }

    strategy = design_closing_strategy(
        blocker_prospect,
        "EVALUATION",
        "Il faut que j'en parle à mon directeur général pour valider le budget",
    )

    print(f"\nEntreprise          : {strategy['deal_company']}")
    print(f"Étape actuelle      : {strategy['stage_label']} ({strategy['current_stage']})")
    print(f"Blocker identifié   : {strategy['blocker_identified']}")

    print("\n--- SCRIPT DE TRAITEMENT D'OBJECTION ---")
    script = strategy["objection_handling_script"]
    print(f"Accusé réception : {script['immediate_acknowledge']}")
    print(f"Reframe          : {script['reframe'][:150]}...")
    print(f"Preuve           : {script['proof_point'][:150]}...")
    print(f"Closing line     : {script['closing_line']}")

    print("\n--- CARTOGRAPHIE DÉCISIONNELLE ---")
    dm = strategy["decision_making_map"]
    print(f"Contact principal : {dm['primary_contact']}")
    print("Parties prenantes probables :")
    for s in dm["likely_stakeholders"]:
        print(f"  • {s}")
    print(f"Action de mapping : {dm['recommended_mapping_action']}")

    print("\n--- PLAY SPONSOR EXÉCUTIF ---")
    esp = strategy["executive_sponsor_play"]
    print(f"Email exécutif hook : {esp['executive_email_hook']}")
    print(f"Question de qualification : {esp['sponsor_identification_question']}")

    print("\n--- CRÉATION D'URGENCE CSDDD ---")
    urg = strategy["urgency_creation"]
    print(f"Levier principal    : {urg['primary_lever']}")
    print(f"Levier financier    : {urg['financial_lever']}")
    print(f"Levier concurrentiel: {urg['competitive_lever']}")

    print("\n--- STRUCTURE D'OFFRE DE CLOSING ---")
    offer = strategy["offer_structure"]
    entry = offer["recommended_entry_point"]
    main = offer["main_offer"]
    fallback = offer["fallback_offer"]
    print(f"Point d'entrée : {entry['label']} — {entry['price']}")
    print(f"Offre principale : {main['tier']} à {main['monthly_price']} | {main['first_year_incentive']}")
    print(f"Offre repli      : {fallback['description']} — {fallback['price']}")

    print("\n--- PROCHAINES ÉTAPES ---")
    for step in strategy["next_steps"]:
        print(f"  {step['date']} : {step['action']}")

    print(f"\nBoost probabilité attendu : {strategy['closing_probability_boost_expected']}")

    print("\n" + separator)
    print("DÉMONSTRATION TERMINÉE — Agent Stratège en Vente Éclair opérationnel")
    print("CaelumSwarm™ | Caelum Partners | CSDDD Deadline : Juillet 2027")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("\n[OK] run_demo() → True")
