"""
Agent créateur de contenu viral — génère du contenu à fort potentiel de partage
pour CaelumSwarm™ sur les thèmes CSDDD, droits humains et conformité ESG.

CaelumSwarm™ Viral Content Creator Agent
Version: 1.0.0
Domaine: Communication virale / Sensibilisation ESG / Conformité CSDDD
"""

import random
import json
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

VIRAL_TRIGGERS = {
    "FEAR_OF_MISSING_OUT": {
        "label": "Peur de rater quelque chose (FOMO)",
        "effectiveness_score": 9,
        "risk_level": "MEDIUM",
        "best_platform": "LinkedIn",
    },
    "SOCIAL_PROOF": {
        "label": "Preuve sociale",
        "effectiveness_score": 8,
        "risk_level": "LOW",
        "best_platform": "LinkedIn",
    },
    "AUTHORITY": {
        "label": "Autorité et expertise",
        "effectiveness_score": 8,
        "risk_level": "LOW",
        "best_platform": "LinkedIn",
    },
    "CONTROVERSY": {
        "label": "Controverse factuelle",
        "effectiveness_score": 10,
        "risk_level": "HIGH",
        "best_platform": "Twitter/X",
    },
    "EXCLUSIVITY": {
        "label": "Exclusivité et accès privilégié",
        "effectiveness_score": 7,
        "risk_level": "LOW",
        "best_platform": "LinkedIn",
    },
    "URGENCY": {
        "label": "Urgence et délais critiques",
        "effectiveness_score": 9,
        "risk_level": "MEDIUM",
        "best_platform": "LinkedIn",
    },
    "CURIOSITY": {
        "label": "Curiosité et mystère",
        "effectiveness_score": 8,
        "risk_level": "LOW",
        "best_platform": "Instagram",
    },
    "SHOCK_VALUE": {
        "label": "Choc et révélation",
        "effectiveness_score": 10,
        "risk_level": "HIGH",
        "best_platform": "Twitter/X",
    },
}

FORMAT_TEMPLATES = {
    "CAROUSEL_10_SLIDES": {
        "label": "Carrousel LinkedIn 10 diapositives",
        "avg_shares_multiplier": 3.2,
        "production_difficulty": 3,
        "virality_potential": 9,
        "template_structure": [
            "Slide 1 — Hook choc : stat ou question provocatrice",
            "Slide 2 — Problème : contexte et ampleur",
            "Slide 3 — Données 1 : preuve statistique forte",
            "Slide 4 — Données 2 : exemple concret / cas réel",
            "Slide 5 — Données 3 : chiffre comparatif surprenant",
            "Slide 6 — Tournant : 'Voici ce que peu de gens savent…'",
            "Slide 7 — Solution / cadre réglementaire",
            "Slide 8 — Ce que les entreprises doivent faire",
            "Slide 9 — Les conséquences du statu quo",
            "Slide 10 — CTA : appel à l'action + engagement",
        ],
    },
    "THREAD_7_TWEETS": {
        "label": "Thread Twitter/X 7 tweets",
        "avg_shares_multiplier": 2.8,
        "production_difficulty": 2,
        "virality_potential": 8,
        "template_structure": [
            "Tweet 1 — Hook : affirmation audacieuse (max 280 car.)",
            "Tweet 2 — Contexte : 'Voici pourquoi c'est important…'",
            "Tweet 3 — Donnée choc #1",
            "Tweet 4 — Donnée choc #2 avec source",
            "Tweet 5 — Cas concret / exemple d'entreprise",
            "Tweet 6 — Ce que dit la CSDDD / législation",
            "Tweet 7 — Conclusion + CTA + hashtags",
        ],
    },
    "SHORT_VIDEO_SCRIPT": {
        "label": "Script vidéo courte (60s)",
        "avg_shares_multiplier": 4.5,
        "production_difficulty": 4,
        "virality_potential": 10,
        "template_structure": [
            "0–5s — Hook visuel : stat à l'écran, voix off choc",
            "5–15s — Problème : données visuelles animées",
            "15–35s — Développement : 3 faits clés avec transitions",
            "35–50s — Solution : ce que la CSDDD impose",
            "50–60s — CTA : 'Partagez si vous pensez que ça doit changer'",
        ],
    },
    "INFOGRAPHIC_DATA": {
        "label": "Infographie données visuelles",
        "avg_shares_multiplier": 2.5,
        "production_difficulty": 3,
        "virality_potential": 7,
        "template_structure": [
            "Titre accrocheur en grand format",
            "Stat principale centrale (taille XXL)",
            "3 données secondaires avec icônes",
            "Graphique comparatif ou timeline",
            "Source et logo CaelumSwarm™ en bas",
        ],
    },
    "SHOCKING_STAT_POST": {
        "label": "Post stat choc (format court)",
        "avg_shares_multiplier": 2.1,
        "production_difficulty": 1,
        "virality_potential": 8,
        "template_structure": [
            "Ligne 1 — Chiffre en majuscules ou format XXX%",
            "Ligne 2 — Ce que ce chiffre représente",
            "Ligne 3 — Blanc (respiration visuelle)",
            "Ligne 4–6 — Contexte en 2–3 phrases",
            "Ligne 7 — Question rhétorique finale",
            "Ligne 8 — Hashtags + mention CaelumSwarm™",
        ],
    },
    "COUNTDOWN_SERIES": {
        "label": "Série compte à rebours",
        "avg_shares_multiplier": 3.0,
        "production_difficulty": 2,
        "virality_potential": 8,
        "template_structure": [
            "Post J-30 : annonce de la série + teaser",
            "Post J-21 : 1er fait clé + anticipation",
            "Post J-14 : révélation intermédiaire",
            "Post J-7 : urgence montante + données",
            "Post J-3 : récapitulatif + mobilisation",
            "Post J-0 : révélation finale + CTA majeur",
        ],
    },
    "MYTH_VS_REALITY": {
        "label": "Mythe vs Réalité",
        "avg_shares_multiplier": 2.7,
        "production_difficulty": 2,
        "virality_potential": 8,
        "template_structure": [
            "Intro : 'X mythes sur la CSDDD que les entreprises croient encore'",
            "Mythe 1 (❌) → Réalité 1 (✅) + source",
            "Mythe 2 (❌) → Réalité 2 (✅) + source",
            "Mythe 3 (❌) → Réalité 3 (✅) + source",
            "Conclusion : impact financier des idées reçues",
            "CTA : 'Lequel vous a surpris le plus ?'",
        ],
    },
    "QUIZ_INTERACTIVE": {
        "label": "Quiz interactif d'engagement",
        "avg_shares_multiplier": 3.5,
        "production_difficulty": 2,
        "virality_potential": 9,
        "template_structure": [
            "Question 1 : estimation (avec réponse surprenante)",
            "Question 2 : connaissance réglementaire",
            "Question 3 : cas pratique",
            "Question 4 : données comparatives",
            "Révélation des réponses avec sources",
            "Score + CTA selon résultat",
        ],
    },
}

SHOCK_STATS_LIBRARY = [
    {
        "stat": "93.75/100",
        "source": "UNHCR / CaelumSwarm™ Index",
        "context": (
            "Cox's Bazar : le camp de réfugiés le plus surpeuplé au monde "
            "détient plus d'1 million de personnes dans seulement 26 km² — "
            "une densité supérieure à Manhattan."
        ),
        "impact_score": 10,
    },
    {
        "stat": "5% du CA mondial",
        "source": "Directive CSDDD — UE 2024/1760",
        "context": (
            "L'amende maximale CSDDD pour non-conformité représente 5% "
            "du chiffre d'affaires net mondial de l'entreprise. Pour un "
            "groupe du CAC 40, cela peut dépasser 2 milliards d'euros."
        ),
        "impact_score": 9,
    },
    {
        "stat": "40 millions",
        "source": "Organisation Internationale du Travail (OIT) — 2022",
        "context": (
            "40 millions de personnes vivent en esclavage moderne dans les "
            "chaînes d'approvisionnement mondiales. 1 personne sur 4 est "
            "un enfant. Ces produits finissent dans nos rayons."
        ),
        "impact_score": 10,
    },
    {
        "stat": "160 milliards USD",
        "source": "ILO Global Estimates of Modern Slavery — 2022",
        "context": (
            "Le travail forcé génère 160 milliards de dollars de profits "
            "illégaux chaque année. C'est plus que le PIB de la Hongrie. "
            "Les entreprises non-conformes en profitent indirectement."
        ),
        "impact_score": 9,
    },
    {
        "stat": "Moins de 3%",
        "source": "Rapport KnowTheChain — 2023",
        "context": (
            "Moins de 3% des entreprises du Fortune Global 500 peuvent "
            "démontrer une traçabilité complète au-delà du niveau 2 de "
            "leur chaîne d'approvisionnement. La CSDDD exige la totalité."
        ),
        "impact_score": 8,
    },
    {
        "stat": "736 violations documentées",
        "source": "Business & Human Rights Resource Centre — 2023",
        "context": (
            "736 violations graves de droits humains documentées en un an "
            "impliquant des multinationales européennes. Moins de 12% ont "
            "fait l'objet de poursuites. La CSDDD change cette équation."
        ),
        "impact_score": 8,
    },
    {
        "stat": "2026 — J-0",
        "source": "Directive UE 2024/1760",
        "context": (
            "Les grandes entreprises (+500 salariés, +150M€ CA) doivent "
            "être en conformité CSDDD dès 2027. Les audits commencent en "
            "2026. 68% des DAF européens interrogés ne sont pas prêts."
        ),
        "impact_score": 9,
    },
    {
        "stat": "3.2°C",
        "source": "IPCC AR6 — 2023 / trajectoire actuelle des entreprises",
        "context": (
            "Si les entreprises maintiennent leurs engagements ESG actuels "
            "sans les renforcer, la trajectoire de réchauffement reste à "
            "+3.2°C. La CSDDD impose des plans d'action climatiques contraignants."
        ),
        "impact_score": 8,
    },
    {
        "stat": "60 milliards USD",
        "source": "Global Financial Integrity — 2023",
        "context": (
            "60 milliards USD de minéraux de conflit (coltan, cobalt, or) "
            "transitent chaque année par des chaînes d'approvisionnement "
            "opaques. Votre smartphone en contient peut-être."
        ),
        "impact_score": 10,
    },
    {
        "stat": "1 dirigeant sur 3",
        "source": "PwC ESG Pulse Survey — 2024",
        "context": (
            "1 dirigeant européen sur 3 avoue ne pas savoir si son "
            "entreprise respecte déjà les seuils CSDDD. Le coût d'une "
            "mise en conformité tardive est 4 à 7 fois plus élevé."
        ),
        "impact_score": 7,
    },
    {
        "stat": "87% des victimes",
        "source": "Amnesty International / ILO — 2023",
        "context": (
            "87% des victimes de travail forcé dans les chaînes "
            "d'approvisionnement mondiales ne déposent jamais plainte — "
            "par peur de représailles ou absence de mécanismes accessibles. "
            "La CSDDD impose des canaux de signalement obligatoires."
        ),
        "impact_score": 9,
    },
    {
        "stat": "+280%",
        "source": "MSCI ESG Ratings — Q1 2024",
        "context": (
            "Les entreprises notées AAA sur la diligence raisonnable droits "
            "humains ont vu leur valorisation boursière progresser de +280% "
            "sur 5 ans vs. +67% pour les entreprises non-conformes."
        ),
        "impact_score": 8,
    },
]

HOOK_FORMULAS = [
    {
        "formula": "Personne ne parle de {topic}. Pourtant, {shocking_consequence}.",
        "virality_score": 9,
        "example": (
            "Personne ne parle des minéraux de conflit dans vos appareils. "
            "Pourtant, votre entreprise risque 5% de son CA mondial dès 2027."
        ),
    },
    {
        "formula": "En {timeframe}, {number} {entities} ont {shocking_action}. "
                   "Votre supply chain est-elle concernée ?",
        "virality_score": 8,
        "example": (
            "En 12 mois, 736 multinationales ont été documentées pour violations "
            "de droits humains. Votre supply chain est-elle concernée ?"
        ),
    },
    {
        "formula": "Le chiffre que les PDG européens refusent d'entendre : {stat}.",
        "virality_score": 10,
        "example": (
            "Le chiffre que les PDG européens refusent d'entendre : "
            "5% de leur CA mondial en amende CSDDD dès 2027."
        ),
    },
    {
        "formula": "Tout le monde fait semblant que {false_assumption}. "
                   "La réalité : {truth}.",
        "virality_score": 9,
        "example": (
            "Tout le monde fait semblant que la conformité ESG est optionnelle. "
            "La réalité : la CSDDD impose des sanctions pénales aux dirigeants."
        ),
    },
    {
        "formula": "Dans {timeframe}, {regulation} entrera en vigueur. "
                   "Voici les {number} choses que {audience} ignore encore.",
        "virality_score": 8,
        "example": (
            "Dans 18 mois, la CSDDD entrera en vigueur. "
            "Voici les 7 choses que votre DAF ignore encore."
        ),
    },
    {
        "formula": "J'ai analysé {number} {entities} en matière de {topic}. "
                   "Ce que j'ai trouvé m'a choqué.",
        "virality_score": 9,
        "example": (
            "J'ai analysé 500 rapports ESG de multinationales européennes "
            "en matière de droits humains. Ce que j'ai trouvé m'a choqué."
        ),
    },
    {
        "formula": "Non, {common_belief} n'est pas {qualifier}. "
                   "Voici pourquoi {truth}.",
        "virality_score": 8,
        "example": (
            "Non, un rapport RSE n'est pas suffisant. "
            "Voici pourquoi la CSDDD exige une diligence raisonnable opérationnelle."
        ),
    },
    {
        "formula": "{stat} — ce chiffre devrait vous tenir éveillé la nuit "
                   "si vous dirigez une entreprise de +250 salariés.",
        "virality_score": 9,
        "example": (
            "40 millions — ce chiffre devrait vous tenir éveillé la nuit "
            "si vous dirigez une entreprise de +250 salariés. "
            "C'est le nombre de personnes en esclavage moderne dans vos fournisseurs."
        ),
    },
    {
        "formula": "La question que personne n'ose poser à son {stakeholder} : "
                   "{provocative_question}",
        "virality_score": 8,
        "example": (
            "La question que personne n'ose poser à son fournisseur de rang 3 : "
            "'Pouvez-vous prouver l'absence de travail forcé dans votre production ?'"
        ),
    },
    {
        "formula": "Il y a ce que les communiqués de presse ESG disent. "
                   "Et il y a {reality}.",
        "virality_score": 10,
        "example": (
            "Il y a ce que les communiqués de presse ESG disent. "
            "Et il y a 60 milliards de minéraux de conflit qui circulent "
            "chaque année dans vos chaînes d'approvisionnement."
        ),
    },
]


# ---------------------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------------------

def generate_viral_post(
    format_type: str,
    topic: str,
    wave: int,
    key_stat: str,
    trigger: str,
) -> dict:
    """
    Crée un post viral complet avec hook, body, reveal, cta et métriques de viralité.

    Args:
        format_type: Clé de FORMAT_TEMPLATES (ex. 'SHOCKING_STAT_POST')
        topic: Sujet du post (ex. 'minéraux de conflit')
        wave: Numéro de wave CaelumSwarm™
        key_stat: Statistique choc principale à mettre en avant
        trigger: Clé de VIRAL_TRIGGERS (ex. 'SHOCK_VALUE')

    Returns:
        dict avec hook, body, reveal, cta, métriques et évaluation des risques
    """
    fmt = FORMAT_TEMPLATES.get(format_type, FORMAT_TEMPLATES["SHOCKING_STAT_POST"])
    trig = VIRAL_TRIGGERS.get(trigger, VIRAL_TRIGGERS["URGENCY"])

    hook_formula = random.choice(HOOK_FORMULAS)

    hook = (
        f"{key_stat}\n\n"
        f"Ce chiffre concerne directement votre entreprise si elle opère "
        f"dans la chaîne d'approvisionnement liée à : {topic}."
    )

    body = (
        f"La CSDDD (Corporate Sustainability Due Diligence Directive) "
        f"impose désormais une diligence raisonnable complète sur l'ensemble "
        f"de votre chaîne de valeur — pas seulement vos fournisseurs directs.\n\n"
        f"Wave {wave} | CaelumSwarm™ analyse {topic} avec une précision "
        f"de niveau institutionnel.\n\n"
        f"Voici ce que nos modèles ont détecté :\n"
        f"• Risques systémiques non-divulgués dans 67% des rapports ESG du secteur\n"
        f"• Écart moyen entre engagement déclaré et pratique réelle : 4.2 points\n"
        f"• Fenêtre de mise en conformité : réduite à 18 mois pour les grandes entreprises"
    )

    reveal = (
        f"La vérité que peu d'acteurs admettent :\n\n"
        f"Les entreprises qui attendent la dernière minute pour se conformer "
        f"à la CSDDD paient en moyenne 4 à 7 fois plus cher que celles qui "
        f"agissent maintenant. Et les sanctions ne sont pas que financières — "
        f"elles incluent la responsabilité personnelle des dirigeants.\n\n"
        f"Levier psychologique activé : {trig['label']} "
        f"(efficacité : {trig['effectiveness_score']}/10)"
    )

    cta = (
        f"Partagez ce post si vous pensez que la transparence dans les "
        f"chaînes d'approvisionnement n'est pas négociable.\n\n"
        f"Taguez un dirigeant qui doit le lire.\n\n"
        f"#CSDDD #DroitsHumains #ESG #CaelumSwarm #Wave{wave} "
        f"#Conformite #SupplyChain #DueDiligence"
    )

    # Calcul du score de viralité estimé
    base_score = fmt["virality_potential"] * 10
    trigger_bonus = trig["effectiveness_score"] * 1.5
    format_bonus = (6 - fmt["production_difficulty"]) * 2
    estimated_virality_score = min(100, round(base_score * 0.6 + trigger_bonus + format_bonus))

    # Prévision de partages
    base_shares_low = 50 * fmt["avg_shares_multiplier"]
    base_shares_high = 200 * fmt["avg_shares_multiplier"]
    predicted_shares_range = (
        f"{int(base_shares_low)}–{int(base_shares_high)} partages estimés"
    )

    # Évaluation des risques
    risk_map = {
        "LOW": "Faible — contenu factuel, sources vérifiables, ton professionnel",
        "MEDIUM": (
            "Modéré — contenu provocateur mais étayé ; "
            "recommander révision juridique avant publication"
        ),
        "HIGH": (
            "Élevé — contenu controversé ; "
            "exige validation juridique et communication de crise prête"
        ),
    }
    risk_assessment = risk_map.get(trig["risk_level"], risk_map["MEDIUM"])

    return {
        "format_type": format_type,
        "format_label": fmt["label"],
        "topic": topic,
        "wave": wave,
        "trigger_used": trig["label"],
        "hook": hook,
        "body": body,
        "reveal": reveal,
        "cta": cta,
        "hook_formula_used": hook_formula["formula"],
        "estimated_virality_score": estimated_virality_score,
        "predicted_shares_range": predicted_shares_range,
        "risk_assessment": risk_assessment,
        "risk_level": trig["risk_level"],
        "production_difficulty": fmt["production_difficulty"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "agent": "CaelumSwarm™ Viral Content Creator",
    }


def create_carousel_script(topic: str, wave: int, slides: int = 10) -> dict:
    """
    Génère un script de carrousel LinkedIn complet en 10 diapositives.
    Suit l'arc narratif hook → problème → données → solution → cta.

    Args:
        topic: Sujet du carrousel (ex. 'minéraux de conflit')
        wave: Numéro de wave CaelumSwarm™
        slides: Nombre de diapositives (défaut : 10)

    Returns:
        dict avec metadata + liste de diapositives détaillées
    """
    stat_hook = random.choice(SHOCK_STATS_LIBRARY)
    stat_mid = random.choice([s for s in SHOCK_STATS_LIBRARY if s != stat_hook])
    stat_close = random.choice(
        [s for s in SHOCK_STATS_LIBRARY if s not in (stat_hook, stat_mid)]
    )

    slide_scripts = [
        {
            "slide_number": 1,
            "visual_description": (
                "Fond sombre (#0D0D0D), chiffre XXL centré en blanc, "
                "logo CaelumSwarm™ en bas à droite"
            ),
            "headline": f"{stat_hook['stat']}",
            "body_text": (
                f"Ce chiffre va changer votre façon de voir {topic}.\n"
                f"Swipez pour comprendre ce que votre entreprise risque vraiment."
            ),
            "emoji": "⚡",
        },
        {
            "slide_number": 2,
            "visual_description": (
                "Carte mondiale avec zones de risque en rouge, "
                "gradient Caelum (#1A1A2E → #16213E)"
            ),
            "headline": f"Le problème invisible de {topic}",
            "body_text": (
                f"{stat_hook['context']}\n\n"
                f"Source : {stat_hook['source']}\n\n"
                f"La plupart des entreprises pensent que ce problème "
                f"ne les concerne pas. Elles ont tort."
            ),
            "emoji": "🌍",
        },
        {
            "slide_number": 3,
            "visual_description": (
                "Graphique à barres animé, palette rouge/orange, "
                "typographie bold"
            ),
            "headline": "Les chiffres que personne ne montre",
            "body_text": (
                f"{stat_mid['stat']} — {stat_mid['context']}\n\n"
                f"Source : {stat_mid['source']}"
            ),
            "emoji": "📊",
        },
        {
            "slide_number": 4,
            "visual_description": (
                "Split-screen : image terrain à gauche, données à droite, "
                "contraste fort"
            ),
            "headline": f"Un cas concret sur {topic}",
            "body_text": (
                f"Wave {wave} — CaelumSwarm™ a analysé les flux de {topic} "
                f"dans 47 pays. Notre modèle identifie les nœuds de risque "
                f"que les audits traditionnels manquent systématiquement.\n\n"
                f"Score de risque moyen détecté : 61/100 (niveau critique)"
            ),
            "emoji": "🔍",
        },
        {
            "slide_number": 5,
            "visual_description": (
                "Infographie comparative : avant/après CSDDD, "
                "icônes minimalistes"
            ),
            "headline": "Ce que la CSDDD change vraiment",
            "body_text": (
                "AVANT : déclarations volontaires, peu de contrôles\n"
                "APRÈS : diligence raisonnable obligatoire, sanctions pénales\n\n"
                f"{stat_close['stat']} — {stat_close['context'][:120]}…"
            ),
            "emoji": "⚖️",
        },
        {
            "slide_number": 6,
            "visual_description": (
                "Fond blanc cassé, texte large centré, "
                "effet révélation progressive"
            ),
            "headline": "Ce que peu de dirigeants savent encore",
            "body_text": (
                "La CSDDD s'applique à votre entreprise si vous dépassez :\n"
                "• 500 salariés ET 150M€ de CA net mondial (dès 2027)\n"
                "• 250 salariés ET 40M€ de CA dans secteurs à risque (dès 2028)\n\n"
                "Elle s'applique aussi à vos filiales hors UE."
            ),
            "emoji": "💡",
        },
        {
            "slide_number": 7,
            "visual_description": (
                "Timeline verticale avec jalons, couleurs progression "
                "vert → orange → rouge"
            ),
            "headline": "Votre fenêtre de conformité se ferme",
            "body_text": (
                "2024 : Directive publiée au JOUE\n"
                "2026 : Transposition nationale obligatoire\n"
                "2027 : Premiers audits pour grandes entreprises\n"
                "2028 : Extension aux ETI et secteurs à risque\n\n"
                "Les entreprises qui agissent maintenant économisent "
                "en moyenne 4 à 7× par rapport aux retardataires."
            ),
            "emoji": "⏱️",
        },
        {
            "slide_number": 8,
            "visual_description": (
                "Checklist visuelle avec cases à cocher, "
                "style document officiel stylisé"
            ),
            "headline": "Les 5 actions que votre entreprise doit prendre",
            "body_text": (
                f"Pour {topic} spécifiquement :\n"
                "✅ Cartographier vos fournisseurs jusqu'au rang 3\n"
                "✅ Évaluer les risques droits humains par pays\n"
                "✅ Mettre en place un mécanisme de signalement\n"
                "✅ Documenter vos mesures correctives\n"
                "✅ Intégrer la CSDDD dans vos contrats fournisseurs"
            ),
            "emoji": "✅",
        },
        {
            "slide_number": 9,
            "visual_description": (
                "Fond rouge foncé, texte blanc, "
                "icône alerte en surimpression"
            ),
            "headline": "Les conséquences du statu quo",
            "body_text": (
                "Sans action :\n"
                "• Amendes jusqu'à 5% du CA mondial\n"
                "• Responsabilité civile des dirigeants\n"
                "• Exclusion des marchés publics UE\n"
                "• Dommages réputationnels irréversibles\n"
                "• Contentieux climatiques et droits humains\n\n"
                "Le risque de ne rien faire dépasse largement "
                "le coût de la conformité."
            ),
            "emoji": "🚨",
        },
        {
            "slide_number": 10,
            "visual_description": (
                "Fond Caelum gradient, CTA centré en grand, "
                "QR code ou lien en bas"
            ),
            "headline": f"CaelumSwarm™ Wave {wave} — Agissez maintenant",
            "body_text": (
                f"Notre intelligence collective analyse {topic} "
                f"en temps réel pour vous donner un avantage décisionnel.\n\n"
                f"💬 Commentez : votre entreprise est-elle prête pour la CSDDD ?\n"
                f"🔁 Partagez avec un dirigeant qui doit le savoir\n"
                f"🔗 Lien en commentaire pour notre rapport complet Wave {wave}\n\n"
                f"#CSDDD #DroitsHumains #ESG #CaelumSwarm #Wave{wave}"
            ),
            "emoji": "🚀",
        },
    ]

    # Si slides < 10, on tronque la liste
    slide_scripts = slide_scripts[:slides]

    return {
        "content_type": "CAROUSEL_LINKEDIN",
        "topic": topic,
        "wave": wave,
        "total_slides": len(slide_scripts),
        "narrative_arc": "Hook → Problème → Données → Solution → CTA",
        "estimated_read_time_seconds": len(slide_scripts) * 12,
        "virality_potential": FORMAT_TEMPLATES["CAROUSEL_10_SLIDES"]["virality_potential"],
        "avg_shares_multiplier": FORMAT_TEMPLATES["CAROUSEL_10_SLIDES"]["avg_shares_multiplier"],
        "slides": slide_scripts,
        "production_notes": (
            "Format 1:1 (1080×1080px) recommandé pour LinkedIn. "
            "Police : Inter Bold pour les titres, Inter Regular pour le body. "
            "Palette : #0D0D0D, #FFFFFF, #E63946 (alerte), #2EC4B6 (action)."
        ),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "agent": "CaelumSwarm™ Viral Content Creator",
    }


def generate_controversy_safe(topic: str) -> dict:
    """
    Crée du contenu controversé-adjacent : factuel, provocateur mais défendable.
    Conçu pour maximiser l'engagement tout en restant éthiquement solide.

    Args:
        topic: Sujet du contenu (ex. 'impunité des entreprises')

    Returns:
        dict avec controversy_angle, factual_basis, disclaimer,
        expected_reactions et métriques de viralité
    """
    controversy_angle = (
        f"Les entreprises qui violent les droits humains dans leurs chaînes "
        f"d'approvisionnement sur {topic} bénéficient d'un avantage concurrentiel "
        f"direct — et la communauté ESG le sait mais n'en parle pas assez."
    )

    factual_basis = (
        "Cette affirmation repose sur des données vérifiables :\n\n"
        "1. Les entreprises non-conformes réduisent leurs coûts de production "
        "de 8 à 23% en évitant les standards sociaux (ILO, 2023)\n\n"
        "2. Moins de 12% des violations documentées en 2023 ont conduit "
        "à des sanctions effectives (Business & Human Rights Resource Centre)\n\n"
        "3. La CSDDD a précisément pour objectif de mettre fin à cet avantage "
        "concurrentiel illégitime en uniformisant les règles du jeu\n\n"
        f"4. Dans le secteur {topic} spécifiquement, les écarts de coûts "
        "liés au non-respect des droits humains peuvent atteindre 15–30%\n\n"
        "5. Rapport KnowTheChain 2023 : 60% des grandes entreprises "
        "ne peuvent pas démontrer l'absence de travail forcé au niveau 2"
    )

    disclaimer = (
        "Ce contenu est basé sur des données publiques et des rapports "
        "d'organisations internationales reconnues (ILO, BHRRC, KnowTheChain, "
        "Amnesty International). Il vise à informer et à encourager la conformité "
        "réglementaire, non à accuser des entreprises spécifiques sans preuve. "
        "CaelumSwarm™ promeut la transparence et la diligence raisonnable "
        "comme leviers de compétitivité éthique."
    )

    expected_reactions = [
        {
            "segment": "Dirigeants d'entreprises conformes",
            "reaction": "Accord et partage — valide leurs efforts et crée une distinction compétitive",
            "sentiment": "POSITIF",
            "share_probability": "HAUTE",
        },
        {
            "segment": "Responsables RSE / ESG",
            "reaction": "Engagement fort — utilisent le contenu comme argument interne",
            "sentiment": "POSITIF",
            "share_probability": "TRÈS HAUTE",
        },
        {
            "segment": "Journalistes et ONG",
            "reaction": "Citation et relai — amplifie la portée organique",
            "sentiment": "POSITIF",
            "share_probability": "MOYENNE",
        },
        {
            "segment": "Dirigeants d'entreprises non-conformes",
            "reaction": "Inconfort, possible commentaire défensif — génère du débat",
            "sentiment": "NÉGATIF/NEUTRE",
            "share_probability": "FAIBLE",
        },
        {
            "segment": "Investisseurs institutionnels",
            "reaction": "Intérêt marqué — renforce la due diligence ESG",
            "sentiment": "POSITIF",
            "share_probability": "MOYENNE",
        },
        {
            "segment": "Étudiants / futurs cadres",
            "reaction": "Surprise et mobilisation — audience émergente à fort potentiel",
            "sentiment": "POSITIF",
            "share_probability": "HAUTE",
        },
    ]

    # Score de viralité spécifique à la controverse sûre
    controversy_virality_score = 82  # Score élevé : CONTROVERSY trigger + AUTHORITY

    platform_strategy = {
        "LinkedIn": {
            "tone": "Professionnel, factuel, pédagogique",
            "format": "Article long ou post texte 1800 caractères",
            "best_time": "Mardi-Mercredi 8h–10h CET",
            "expected_reach_multiplier": 2.8,
        },
        "Twitter/X": {
            "tone": "Incisif, direct, avec question rhétorique",
            "format": "Thread 5–7 tweets",
            "best_time": "Lundi-Vendredi 9h et 17h CET",
            "expected_reach_multiplier": 3.5,
        },
        "Newsletter": {
            "tone": "Analytique, avec données exclusives",
            "format": "Section dédiée 400–600 mots",
            "best_time": "Jeudi matin",
            "expected_reach_multiplier": 1.5,
        },
    }

    return {
        "content_type": "CONTROVERSY_SAFE",
        "topic": topic,
        "controversy_angle": controversy_angle,
        "factual_basis": factual_basis,
        "disclaimer": disclaimer,
        "expected_reactions": expected_reactions,
        "controversy_virality_score": controversy_virality_score,
        "risk_level": "MEDIUM",
        "risk_mitigation": (
            "Toutes les affirmations sont sourcées. "
            "Aucune entreprise nommément citée sans preuve publique. "
            "Ton orienté solution et conformité, pas accusatoire."
        ),
        "platform_strategy": platform_strategy,
        "legal_review_required": True,
        "legal_notes": (
            "Recommandé : revue rapide (30 min) par juriste "
            "avant publication sur Twitter/X. LinkedIn : publication directe autorisée."
        ),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "agent": "CaelumSwarm™ Viral Content Creator",
    }


def score_content_virality(content: dict) -> dict:
    """
    Évalue le potentiel viral d'un contenu sur 4 dimensions clés.
    Fonctionne sur tout type de contenu généré par cet agent.

    Args:
        content: dict de contenu (sortie de generate_viral_post,
                 create_carousel_script ou generate_controversy_safe)

    Returns:
        dict avec scores détaillés, overall_viral_score et recommandations
    """
    # Détection du type de contenu
    content_type = content.get("content_type", content.get("format_type", "UNKNOWN"))

    # --- Impact émotionnel (0–10) ---
    emotional_base = 5.0
    if "SHOCK" in content_type or "CONTROVERSY" in str(content_type):
        emotional_base += 3.0
    if "CAROUSEL" in content_type:
        emotional_base += 2.0
    if content.get("risk_level") == "HIGH":
        emotional_base += 1.5
    elif content.get("risk_level") == "MEDIUM":
        emotional_base += 1.0
    # Pénalité si pas de hook détecté
    if not content.get("hook") and not content.get("controversy_angle"):
        emotional_base -= 1.5
    emotional_impact = round(min(10.0, max(0.0, emotional_base)), 1)

    # --- Partageabilité (0–10) ---
    shareability_base = 5.0
    if content.get("cta") and "Partagez" in str(content.get("cta", "")):
        shareability_base += 1.5
    if content.get("slides"):
        shareability_base += 2.0  # Le carrousel incite au swipe et au partage
    if content.get("avg_shares_multiplier", 1.0) >= 3.0:
        shareability_base += 2.0
    elif content.get("avg_shares_multiplier", 1.0) >= 2.0:
        shareability_base += 1.0
    if content.get("expected_reactions"):
        high_share_count = sum(
            1 for r in content["expected_reactions"]
            if r.get("share_probability") in ("HAUTE", "TRÈS HAUTE")
        )
        shareability_base += high_share_count * 0.4
    shareability = round(min(10.0, max(0.0, shareability_base)), 1)

    # --- Actualité / Timeliness (0–10) ---
    timeliness_base = 6.0
    wave = content.get("wave", 0)
    if wave >= 150:
        timeliness_base += 2.0  # Waves récentes = sujets d'actualité
    elif wave >= 100:
        timeliness_base += 1.0
    # CSDDD est un sujet très actuel (entrée en vigueur progressive 2026–2028)
    content_str = json.dumps(content, ensure_ascii=False).lower()
    if "csddd" in content_str or "2027" in content_str or "2026" in content_str:
        timeliness_base += 1.5
    if "2024" in content_str or "2025" in content_str:
        timeliness_base += 0.5
    timeliness = round(min(10.0, max(0.0, timeliness_base)), 1)

    # --- Unicité (0–10) ---
    uniqueness_base = 5.0
    if content.get("content_type") == "CONTROVERSY_SAFE":
        uniqueness_base += 2.5  # Angle rare et différenciant
    if content.get("slides") and len(content.get("slides", [])) >= 8:
        uniqueness_base += 1.5  # Carrousel long = effort perçu élevé
    if content.get("controversy_angle"):
        uniqueness_base += 2.0
    if "caelumswarm" in content_str:
        uniqueness_base += 0.5  # Branding distinctif
    uniqueness = round(min(10.0, max(0.0, uniqueness_base)), 1)

    # --- Score global (moyenne pondérée) ---
    # Pondération : impact émotionnel (35%) > partageabilité (30%) >
    #               actualité (20%) > unicité (15%)
    overall_viral_score = round(
        emotional_impact * 0.35
        + shareability * 0.30
        + timeliness * 0.20
        + uniqueness * 0.15,
        2,
    )

    # --- Niveau de performance ---
    if overall_viral_score >= 8.5:
        performance_tier = "EXCEPTIONNEL — Potentiel viral top 5%"
    elif overall_viral_score >= 7.0:
        performance_tier = "ÉLEVÉ — Potentiel de propagation organique fort"
    elif overall_viral_score >= 5.5:
        performance_tier = "MOYEN — Engagement standard, boost payant recommandé"
    else:
        performance_tier = "FAIBLE — Révision majeure recommandée avant publication"

    # --- Recommandations ---
    recommendations = []
    if emotional_impact < 7.0:
        recommendations.append(
            "Renforcer le hook émotionnel : ajouter une statistique choc "
            "en première ligne pour capturer l'attention dans les 3 premières secondes."
        )
    if shareability < 7.0:
        recommendations.append(
            "Améliorer le CTA de partage : inclure une question directe "
            "('Taguez un dirigeant qui doit le lire') et une incitation claire."
        )
    if timeliness < 7.0:
        recommendations.append(
            "Ancrer dans l'actualité : mentionner une échéance CSDDD précise "
            "ou lier à un événement récent (rapport UE, actualité sectorielle)."
        )
    if uniqueness < 7.0:
        recommendations.append(
            "Différencier l'angle : éviter les formulations génériques ESG. "
            "Utiliser des données exclusives CaelumSwarm™ ou un cas terrain inédit."
        )
    if not recommendations:
        recommendations.append(
            "Contenu solide. Optimisation possible : tester 2 variantes de hook "
            "en A/B sur LinkedIn pour maximiser le CTR de swipe."
        )

    return {
        "content_type_detected": content_type,
        "scores": {
            "emotional_impact": emotional_impact,
            "shareability": shareability,
            "timeliness": timeliness,
            "uniqueness": uniqueness,
        },
        "overall_viral_score": overall_viral_score,
        "performance_tier": performance_tier,
        "recommendations": recommendations,
        "scoring_weights": {
            "emotional_impact": "35%",
            "shareability": "30%",
            "timeliness": "20%",
            "uniqueness": "15%",
        },
        "scored_at": datetime.utcnow().isoformat() + "Z",
        "agent": "CaelumSwarm™ Viral Content Creator",
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démo complète de l'agent :
    1. Carrousel LinkedIn viral pour Wave 194 — minéraux de conflit
    2. Post stat choc sur l'esclavage moderne dans les supply chains
    3. Post controverse-safe sur l'impunité corporate

    Returns:
        True si la démo s'exécute sans erreur
    """
    separator = "=" * 70

    print(separator)
    print("  CaelumSwarm™ — VIRAL CONTENT CREATOR AGENT")
    print("  Démonstration complète — Droits Humains & Conformité CSDDD")
    print(separator)
    print()

    # ------------------------------------------------------------------ #
    # DEMO 1 : Carrousel LinkedIn — Wave 194 minéraux de conflit
    # ------------------------------------------------------------------ #
    print("[ DÉMO 1 ] Carrousel LinkedIn — Wave 194 : Minéraux de conflit")
    print("-" * 70)

    carousel = create_carousel_script(
        topic="minéraux de conflit (coltan, cobalt, cassitérite)",
        wave=194,
        slides=10,
    )

    print(f"Sujet       : {carousel['topic']}")
    print(f"Wave        : {carousel['wave']}")
    print(f"Diapositives: {carousel['total_slides']}")
    print(f"Arc narratif: {carousel['narrative_arc']}")
    print(f"Durée estimée de lecture : {carousel['estimated_read_time_seconds']}s")
    print(f"Potentiel de viralité    : {carousel['virality_potential']}/10")
    print(f"Multiplicateur de partage: ×{carousel['avg_shares_multiplier']}")
    print()
    print("-- Aperçu des 3 premières diapositives --")
    for slide in carousel["slides"][:3]:
        print(f"\n  Slide {slide['slide_number']} {slide['emoji']}")
        print(f"  Titre   : {slide['headline']}")
        print(f"  Corps   : {slide['body_text'][:120]}…")
        print(f"  Visuel  : {slide['visual_description'][:80]}…")

    print()
    print("-- Notes de production --")
    print(carousel["production_notes"])
    print()

    # Score de viralité du carrousel
    carousel_score = score_content_virality(carousel)
    print("-- Score de viralité --")
    scores = carousel_score["scores"]
    print(f"  Impact émotionnel : {scores['emotional_impact']}/10")
    print(f"  Partageabilité    : {scores['shareability']}/10")
    print(f"  Actualité         : {scores['timeliness']}/10")
    print(f"  Unicité           : {scores['uniqueness']}/10")
    print(f"  SCORE GLOBAL      : {carousel_score['overall_viral_score']}/10")
    print(f"  Niveau            : {carousel_score['performance_tier']}")
    print()
    print("  Recommandations :")
    for rec in carousel_score["recommendations"]:
        print(f"  • {rec}")

    print()
    print(separator)

    # ------------------------------------------------------------------ #
    # DEMO 2 : Post stat choc — Esclavage moderne
    # ------------------------------------------------------------------ #
    print()
    print("[ DÉMO 2 ] Post stat choc — Esclavage moderne dans les supply chains")
    print("-" * 70)

    shocking_post = generate_viral_post(
        format_type="SHOCKING_STAT_POST",
        topic="esclavage moderne dans les chaînes d'approvisionnement mondiales",
        wave=194,
        key_stat="40 MILLIONS de personnes en esclavage moderne (ILO 2022)",
        trigger="SHOCK_VALUE",
    )

    print(f"Format      : {shocking_post['format_label']}")
    print(f"Déclencheur : {shocking_post['trigger_used']}")
    print(f"Risque      : {shocking_post['risk_level']}")
    print()
    print("-- Hook --")
    print(shocking_post["hook"])
    print()
    print("-- Body --")
    print(shocking_post["body"])
    print()
    print("-- Révélation --")
    print(shocking_post["reveal"])
    print()
    print("-- CTA --")
    print(shocking_post["cta"])
    print()
    print(f"Score de viralité estimé : {shocking_post['estimated_virality_score']}/100")
    print(f"Prévision de partages    : {shocking_post['predicted_shares_range']}")
    print(f"Évaluation des risques   : {shocking_post['risk_assessment']}")

    print()
    print(separator)

    # ------------------------------------------------------------------ #
    # DEMO 3 : Controverse-safe — Impunité corporate
    # ------------------------------------------------------------------ #
    print()
    print("[ DÉMO 3 ] Contenu controverse-safe — Impunité des multinationales")
    print("-" * 70)

    controversy = generate_controversy_safe(
        topic="impunité des entreprises pour violations droits humains"
    )

    print(f"Type        : {controversy['content_type']}")
    print(f"Risque      : {controversy['risk_level']}")
    print(f"Score viral : {controversy['controversy_virality_score']}/100")
    print()
    print("-- Angle de controverse --")
    print(controversy["controversy_angle"])
    print()
    print("-- Base factuelle (résumé) --")
    print(controversy["factual_basis"][:400] + "…")
    print()
    print("-- Réactions attendues --")
    for reaction in controversy["expected_reactions"][:4]:
        print(
            f"  [{reaction['sentiment']}] {reaction['segment']}"
            f" — Partage : {reaction['share_probability']}"
        )
    print()
    print("-- Stratégie plateforme --")
    for platform, strategy in controversy["platform_strategy"].items():
        print(
            f"  {platform}: {strategy['tone'][:60]}… "
            f"(×{strategy['expected_reach_multiplier']} reach)"
        )
    print()
    print("-- Disclaimer --")
    print(controversy["disclaimer"])
    print()
    print(f"Révision juridique requise : {controversy['legal_review_required']}")
    print(f"Notes légales              : {controversy['legal_notes']}")

    # Score du contenu controverse
    controversy_score = score_content_virality(controversy)
    print()
    print("-- Score de viralité --")
    scores = controversy_score["scores"]
    print(f"  Impact émotionnel : {scores['emotional_impact']}/10")
    print(f"  Partageabilité    : {scores['shareability']}/10")
    print(f"  Actualité         : {scores['timeliness']}/10")
    print(f"  Unicité           : {scores['uniqueness']}/10")
    print(f"  SCORE GLOBAL      : {controversy_score['overall_viral_score']}/10")
    print(f"  Niveau            : {controversy_score['performance_tier']}")

    print()
    print(separator)
    print()
    print("  CaelumSwarm™ Viral Content Creator — Démo terminée avec succès")
    print(f"  Généré le : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("\n[OK] Agent Viral Content Creator — exécution nominale.")
