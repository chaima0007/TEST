"""
AGENT BIEN-ÊTRE ÉQUIPE — Prévention burnout, résilience et joie au travail
Garde le cap humain dans une entreprise IA en croissance rapide.

Usage : python agent_bienetre_equipe.py
"""

import os
import sys
import json
from datetime import datetime

import google.generativeai as genai
from memoire import charger_memoire, sauvegarder_memoire, incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable d'environnement GEMINI_API_KEY manquante.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Secteur : Intelligence Artificielle — Agents autonomes
Mission : Révolutionner l'automatisation d'entreprise par des agents IA sur mesure
Culture :
  - Innovation constante et curiosité intellectuelle
  - Autonomie et responsabilisation de chaque collaborateur
  - Collaboration étroite entre équipes techniques et métier
  - Télétravail hybride avec réunions d'équipe hebdomadaires
  - Croissance rapide — équipe en pleine expansion
Contexte bien-être :
  - Charge mentale élevée liée à l'innovation permanente
  - Pression des délais et des attentes clients
  - Risque de surinvestissement émotionnel dans le travail
  - Importance capitale de préserver l'énergie et la créativité à long terme
"""

MOTS_CLES_BURNOUT = [
    "épuisé", "épuisement", "à bout", "plus la force", "plus envie",
    "saturé", "débordé", "submergé", "vide", "sans énergie", "fatigue extrême",
    "déprimé", "démotivé", "plus de sens", "inutile", "détaché", "indifférent",
    "insomnies", "anxiété", "stress constant", "craquer", "tenir plus",
    "abandon", "démissionner", "partir", "ras le bol", "ras-le-bol",
]


# ─── UTILITAIRES ──────────────────────────────────────────────────────────────

def creer_agent(instructions, temperature=0.7):
    """Instancie un modèle Gemini avec les instructions système données."""
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=4096,
        ),
    )


def executer_stream(model, prompt, label):
    """Exécute une requête en streaming et retourne la réponse complète."""
    print(f"\n{'─' * 66}")
    print(f"  ► {label}")
    print(f"{'─' * 66}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur de génération : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_fichier(contenu, nom_fichier):
    """Sauvegarde dans fichiers/bienetre/ et affiche la confirmation."""
    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fichiers", "bienetre")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  ✅ Document sauvegardé → {chemin}")
    return chemin


def detecter_signal_burnout(humeur, charge, sens, note_libre):
    """Retourne True si des signaux de burnout sont détectés."""
    scores_bas = sum(1 for s in [humeur, charge, sens] if s < 5)
    note_lower = note_libre.lower() if note_libre else ""
    mot_detecte = any(mot in note_lower for mot in MOTS_CLES_BURNOUT)
    # Signal si 2+ dimensions en dessous de 5, ou score très bas + mot-clé
    return scores_bas >= 2 or (scores_bas >= 1 and mot_detecte)


def obtenir_donnees_bienetre():
    """Charge toutes les données bien-être depuis la mémoire."""
    memoire = charger_memoire()
    return memoire.get("bienetre", {})


def horodatage():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ─── AGENT 1 : CHECK-IN BIEN-ÊTRE ─────────────────────────────────────────────

def agent_check_in_bienetre(membre, humeur_1_10, charge_travail_1_10, sens_1_10, note_libre):
    """
    Check-in bien-être personnel pour un membre de l'équipe.

    Args:
        membre             : Prénom du membre de l'équipe
        humeur_1_10        : Score d'humeur générale (1 = très bas, 10 = excellent)
        charge_travail_1_10: Score de charge de travail (1 = écrasant, 10 = équilibré)
        sens_1_10          : Score de sens et motivation (1 = aucun, 10 = pleinement aligné)
        note_libre         : Message libre, ressenti du moment (peut être vide)
    """
    incrementer_stat("agent_check_in_bienetre")

    signal_burnout = detecter_signal_burnout(humeur_1_10, charge_travail_1_10, sens_1_10, note_libre)
    alerte_manager = signal_burnout

    agent = creer_agent(f"""Tu es le responsable bien-être d'AgentClaude Solutions.
Tu accompagnes les membres de l'équipe avec chaleur, bienveillance et une vraie présence humaine.
Tu n'es ni un robot ni un coach trop lisse — tu es quelqu'un de sincère, qui voit vraiment les gens.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Ton rôle dans ce check-in :
- Accueillir ce que la personne ressent, sans minimiser ni dramatiser
- Générer une réponse empathique et personnalisée (pas de formules génériques)
- Proposer 3 micro-actions concrètes de 5 minutes maximum pour aujourd'hui
- Fournir une insight motivationnelle taillée sur mesure pour sa situation réelle
- Tout est confidentiel et bienveillant

Structure ta réponse ainsi :

## 💙 Réponse personnalisée pour {membre}
[Réponse empathique et sincère, directement adressée à la personne, qui reconnaît ce qu'elle vit]

## ⚡ 3 micro-actions pour aujourd'hui (5 min chacune)
[Actions très concrètes, réalisables maintenant, adaptées à ses scores et son message]

## ✨ Insight du moment
[Une perspective motivationnelle unique, pas générique, ancrée dans sa situation spécifique
et dans le contexte d'une entreprise IA en construction]

{"## ⚠️ Note discrète pour le manager" + chr(10) + "[Formule discrète et respectueuse de la vie privée, qui signale l'attention nécessaire sans alarmer]" if alerte_manager else ""}
""", temperature=0.75)

    prompt = f"""Voici le check-in bien-être de {membre} :

Scores (sur 10) :
- Humeur générale : {humeur_1_10}/10
- Charge de travail (1=écrasant, 10=équilibré) : {charge_travail_1_10}/10
- Sentiment de sens et motivation : {sens_1_10}/10

Message libre :
« {note_libre if note_libre else "Pas de message libre partagé."} »

Signaux détectés : {"⚠️ Attention requise — plusieurs indicateurs de tension élevée" if signal_burnout else "✅ Situation globalement stable"}

Génère une réponse complète, chaleureuse et utile."""

    label = f"Check-in bien-être — {membre}"
    reponse = executer_stream(agent, prompt, label)

    # Sauvegarde en mémoire
    memoire = charger_memoire()
    if "bienetre" not in memoire:
        memoire["bienetre"] = {}
    if "check_ins" not in memoire["bienetre"]:
        memoire["bienetre"]["check_ins"] = []

    entree = {
        "date": datetime.now().isoformat(),
        "membre": membre,
        "scores": {
            "humeur": humeur_1_10,
            "charge_travail": charge_travail_1_10,
            "sens": sens_1_10,
            "moyenne": round((humeur_1_10 + charge_travail_1_10 + sens_1_10) / 3, 1),
        },
        "note_libre": note_libre,
        "signal_burnout": signal_burnout,
        "alerte_manager": alerte_manager,
        "reponse_extrait": reponse[:300],
    }
    memoire["bienetre"]["check_ins"].append(entree)

    # Mise à jour du profil individuel
    if "membres" not in memoire["bienetre"]:
        memoire["bienetre"]["membres"] = {}
    if membre not in memoire["bienetre"]["membres"]:
        memoire["bienetre"]["membres"][membre] = {"check_ins": [], "alertes": 0}
    memoire["bienetre"]["membres"][membre]["check_ins"].append(entree)
    if alerte_manager:
        memoire["bienetre"]["membres"][membre]["alertes"] = (
            memoire["bienetre"]["membres"][membre].get("alertes", 0) + 1
        )
    memoire["bienetre"]["membres"][membre]["dernier_check_in"] = datetime.now().isoformat()

    sauvegarder_memoire(memoire)

    # Sauvegarde fichier
    ts = horodatage()
    nom_fichier = f"checkin_{membre.lower().replace(' ', '_')}_{ts}.txt"
    contenu = f"""CHECK-IN BIEN-ÊTRE
═══════════════════════════════════════════════════════════════════
Membre       : {membre}
Date         : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Humeur       : {humeur_1_10}/10
Charge       : {charge_travail_1_10}/10
Sens         : {sens_1_10}/10
Moyenne      : {round((humeur_1_10 + charge_travail_1_10 + sens_1_10) / 3, 1)}/10
Alerte       : {"OUI — Attention requise" if alerte_manager else "Non"}
Note libre   : {note_libre or "(aucune)"}
═══════════════════════════════════════════════════════════════════

{reponse}
"""
    sauvegarder_fichier(contenu, nom_fichier)

    if alerte_manager:
        print("\n  ⚠️  Un signal d'alerte a été discrètement enregistré pour ce membre.")

    return reponse


# ─── AGENT 2 : RITUEL D'ÉQUIPE ────────────────────────────────────────────────

def agent_rituel_equipe(type_rituel, nb_personnes, duree_minutes):
    """
    Conçoit un rituel d'équipe adapté au besoin du moment.

    Args:
        type_rituel   : "energisant" | "cohesion" | "celebration" | "reset" | "créativité"
        nb_personnes  : Nombre de participants
        duree_minutes : Durée totale disponible en minutes
    """
    incrementer_stat("agent_rituel_equipe")

    descriptions_rituels = {
        "energisant": "Kickoff du lundi matin — recharger les batteries et lancer la semaine avec élan",
        "cohesion": "Activité de cohésion — renforcer les liens et la confiance entre les membres",
        "celebration": "Célébration des victoires — reconnaître les succès collectifs et individuels",
        "reset": "Reset après une semaine difficile — déposer le poids et retrouver de l'espace",
        "créativité": "Session d'innovation — libérer la créativité et générer des idées nouvelles",
    }

    description = descriptions_rituels.get(type_rituel, type_rituel)

    agent = creer_agent(f"""Tu es expert en facilitation d'équipe et en psychologie organisationnelle.
Tu crées des rituels qui transforment vraiment l'énergie d'un groupe — pas des animations superficielles.
Chaque rituel que tu conçois est ancré dans la réalité d'une équipe IA en croissance rapide,
fonctionne aussi bien en présentiel qu'en remote, et respecte le temps de chacun.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire de ton guide de facilitation :

## 🎯 Objectif du rituel
[Ce que ce rituel accomplit vraiment, pourquoi maintenant]

## 🛠️ Préparation (avant la session)
### Matériels nécessaires
[Liste précise pour présentiel ET remote — outils Miro, Jamboard, Zoom, etc.]
### Configuration de l'espace
[Disposition physique ou setup digital idéal]
### Ce que le/la facilitateur·ice doit préparer

## 🌟 Icebreaker d'ouverture ({max(2, duree_minutes // 6)} minutes)
[Activité courte pour créer la sécurité psychologique et l'énergie]
[Instructions étape par étape, mot pour mot si besoin]

## 🎪 Activité principale ({duree_minutes - max(2, duree_minutes // 6) - max(3, duree_minutes // 5)} minutes)
[L'activité cœur du rituel — détaillée, avec variantes remote/présentiel]
[Instructions facilitateur, questions clés, gestion des dynamiques de groupe]

## 🌙 Clôture ({max(3, duree_minutes // 5)} minutes)
[Ritual de fermeture qui ancre l'énergie et crée un souvenir positif]
[Mot de conclusion suggéré pour le/la facilitateur·ice]

## 💡 Conseils de facilitation
[3-5 conseils pour que ce rituel réussisse vraiment]
[Comment gérer les situations délicates]

## 📋 Fiche récap en un coup d'œil
[Tableau Timing | Activité | Rôle facilitateur]
""", temperature=0.8)

    prompt = f"""Conçois un rituel d'équipe pour AgentClaude Solutions :

Type de rituel : {type_rituel} — {description}
Nombre de participants : {nb_personnes} personnes
Durée totale : {duree_minutes} minutes

Contexte : L'équipe est composée de développeurs IA, de consultants et de managers.
Certains sont en télétravail, d'autres au bureau. Le rituel doit fonctionner pour les deux.
L'équipe est jeune, dynamique, et apprécie l'authenticité plus que la formalité.

Crée un guide de facilitation complet que quelqu'un peut utiliser directement,
sans formation préalable en facilitation."""

    label = f"Rituel {type_rituel} — {nb_personnes} personnes — {duree_minutes} min"
    reponse = executer_stream(agent, prompt, label)

    ts = horodatage()
    nom_fichier = f"rituel_{type_rituel}_{nb_personnes}p_{duree_minutes}min_{ts}.txt"
    contenu = f"""GUIDE DE FACILITATION — RITUEL D'ÉQUIPE
═══════════════════════════════════════════════════════════════════
Type         : {type_rituel.upper()} — {description}
Participants : {nb_personnes} personnes
Durée        : {duree_minutes} minutes
Généré le    : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
═══════════════════════════════════════════════════════════════════

{reponse}
"""
    sauvegarder_fichier(contenu, nom_fichier)

    # Trace en mémoire
    memoire = charger_memoire()
    if "bienetre" not in memoire:
        memoire["bienetre"] = {}
    if "rituels" not in memoire["bienetre"]:
        memoire["bienetre"]["rituels"] = []
    memoire["bienetre"]["rituels"].append({
        "date": datetime.now().isoformat(),
        "type": type_rituel,
        "nb_personnes": nb_personnes,
        "duree_minutes": duree_minutes,
    })
    sauvegarder_memoire(memoire)

    return reponse


# ─── AGENT 3 : PRÉVENTION BURNOUT ─────────────────────────────────────────────

def agent_prevention_burnout():
    """
    Analyse toutes les données bien-être en mémoire.
    Calcule un score de risque burnout par membre et génère un plan d'action.
    """
    incrementer_stat("agent_prevention_burnout")

    donnees = obtenir_donnees_bienetre()
    membres = donnees.get("membres", {})

    if not membres:
        print("\n  ℹ️  Aucune donnée de check-in disponible en mémoire.")
        print("     Commencez par faire des check-ins avec l'agent 1.\n")
        return None

    # Calcul des scores de risque par membre
    scores_risque = {}
    for nom, data in membres.items():
        check_ins = data.get("check_ins", [])
        if not check_ins:
            continue

        recents = check_ins[-5:]  # 5 derniers check-ins
        alertes = data.get("alertes", 0)

        moyennes = [ci["scores"]["moyenne"] for ci in recents if "scores" in ci]
        moy_globale = sum(moyennes) / len(moyennes) if moyennes else 5.0

        # Score de risque 0-100 (100 = risque maximal)
        risque_base = max(0, (10 - moy_globale) * 10)  # 0-100 selon moyenne
        bonus_alertes = min(30, alertes * 10)  # +10 par alerte, max 30
        tendance_baisse = 0
        if len(moyennes) >= 3:
            if moyennes[-1] < moyennes[-3]:
                tendance_baisse = 15  # tendance à la baisse

        score_risque = min(100, round(risque_base + bonus_alertes + tendance_baisse))
        scores_risque[nom] = {
            "score": score_risque,
            "niveau": "CRITIQUE" if score_risque >= 70 else "ÉLEVÉ" if score_risque >= 50 else "MODÉRÉ" if score_risque >= 30 else "FAIBLE",
            "nb_check_ins": len(check_ins),
            "moyenne_actuelle": round(moy_globale, 1),
            "alertes": alertes,
        }

    # Résumé des données pour le prompt
    resume_equipe = json.dumps(scores_risque, ensure_ascii=False, indent=2)
    check_ins_recents = []
    for nom, data in membres.items():
        for ci in data.get("check_ins", [])[-3:]:
            check_ins_recents.append(ci)

    agent = creer_agent(f"""Tu es psychologue du travail et expert en prévention des risques psychosociaux (RPS).
Tu as 15 ans d'expérience dans les entreprises tech en forte croissance.
Tu identifies les patterns de burnout avant qu'ils ne deviennent irréversibles.
Tu génères des plans d'action concrets, humains et réalistes — pas du jargon RH.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire de ton analyse :

## 🔍 TABLEAU DE BORD BIEN-ÊTRE ÉQUIPE
[Tableau récapitulatif : Membre | Score risque | Niveau | Tendance | Points d'attention]

## 👤 ANALYSE INDIVIDUELLE PAR MEMBRE
[Pour chaque membre, en commençant par les plus à risque :]
### [Prénom] — Risque [NIVEAU] ([score]/100)
**Patterns détectés :** [Surcharge / Perte de sens / Isolement / Manque de reconnaissance / Ambiguïté de rôle]
**Recommandations personnalisées :**
  - Action immédiate (cette semaine)
  - Action court terme (ce mois)
  - Action moyen terme (3 mois)

## 🏢 INTERVENTIONS AU NIVEAU ÉQUIPE
[3-5 actions collectives pour améliorer le bien-être global]

## 🗓️ PLAN DE RÉCUPÉRATION 30 JOURS
[Pour les membres à risque élevé/critique uniquement]
[Semaine par semaine : actions concrètes, conversations à avoir, ajustements de charge]

## 🔧 CHANGEMENTS SYSTÉMIQUES RECOMMANDÉS
[Ce qui doit changer structurellement pour prévenir la récurrence]
[Processus, rituels, pratiques managériales, charge de travail, culture]

## 📊 INDICATEURS DE SUIVI
[Comment mesurer les progrès dans les 30 prochains jours]
""", temperature=0.6)

    prompt = f"""Analyse les données bien-être de l'équipe AgentClaude Solutions :

SCORES DE RISQUE CALCULÉS :
{resume_equipe}

DÉTAIL DES DERNIERS CHECK-INS :
{json.dumps(check_ins_recents, ensure_ascii=False, indent=2)}

Génère une analyse complète et un plan d'action pour prévenir le burnout.
Sois précis, humain et utile. Nomme les personnes directement (avec leur prénom).
Prioritise les cas les plus urgents."""

    label = "Analyse prévention burnout — Équipe complète"
    reponse = executer_stream(agent, prompt, label)

    ts = horodatage()
    nom_fichier = f"prevention_burnout_{ts}.txt"
    contenu = f"""ANALYSE PRÉVENTION BURNOUT — ÉQUIPE AGENTCLAUDE
═══════════════════════════════════════════════════════════════════
Date d'analyse  : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Membres analysés: {len(scores_risque)}
═══════════════════════════════════════════════════════════════════

SCORES DE RISQUE :
{json.dumps(scores_risque, ensure_ascii=False, indent=2)}

═══════════════════════════════════════════════════════════════════

{reponse}
"""
    sauvegarder_fichier(contenu, nom_fichier)

    return reponse


# ─── AGENT 4 : RECONNAISSANCE ─────────────────────────────────────────────────

def agent_reconnaissance(membre, accomplissement):
    """
    Génère un système de reconnaissance personnalisé et mémorable.

    Args:
        membre         : Prénom et nom du membre à reconnaître
        accomplissement: Description précise de ce qu'il/elle a accompli
    """
    incrementer_stat("agent_reconnaissance")

    agent = creer_agent(f"""Tu es DRH et expert en culture d'entreprise chez AgentClaude Solutions.
Tu crois profondément que la reconnaissance sincère est un des actes managériaux les plus puissants.
Tu ne fais jamais dans le générique ou le copier-coller — chaque reconnaissance est unique,
ancrée dans ce que la personne a vraiment accompli, et dit quelque chose de vrai sur qui elle est.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire :

## 💫 MESSAGE DE RECONNAISSANCE PERSONNALISÉ
[Message direct à la personne, sincère et spécifique.
Pas de formules vides. Dis ce que cet accomplissement révèle de sa valeur réelle.
Ton : chaleureux, authentique, inspirant. 150-200 mots.]

## 👥 PROMPT DE RECONNAISSANCE PAR LES PAIRS
[Ce que les collègues peuvent dire/écrire — version courte (3-4 phrases)
pour Slack, standup, ou réunion d'équipe]

## 🎉 FORMAT DE CÉLÉBRATION PUBLIQUE
### Version Slack
[Message prêt à envoyer dans le channel #victoires ou #équipe]
### Version email (all-hands ou manager)
[Email complet, avec objet, prêt à envoyer]
### Version mention en réunion
[Script de 1 minute pour célébrer en réunion d'équipe]

## 📜 CARTE HÉRITAGE — Impact dans 5 ans
[Texte court (100 mots) qui raconte comment cet accomplissement aura marqué
l'histoire d'AgentClaude Solutions dans 5 ans — ce qu'il aura rendu possible,
les décisions qu'il aura influencées, l'équipe qu'il aura inspirée]
""", temperature=0.8)

    prompt = f"""Génère une reconnaissance complète et mémorable pour :

Membre de l'équipe : {membre}
Accomplissement : {accomplissement}

Contexte : AgentClaude Solutions est une entreprise IA en forte croissance.
Chaque accomplissement compte et mérite d'être célébré avec sincérité.

Crée des messages qui touchent vraiment, qui seront relus avec fierté dans 10 ans."""

    label = f"Reconnaissance — {membre}"
    reponse = executer_stream(agent, prompt, label)

    # Sauvegarde en mémoire (archives des succès)
    memoire = charger_memoire()
    if "bienetre" not in memoire:
        memoire["bienetre"] = {}
    if "reconnaissances" not in memoire["bienetre"]:
        memoire["bienetre"]["reconnaissances"] = []

    entree = {
        "date": datetime.now().isoformat(),
        "membre": membre,
        "accomplissement": accomplissement,
        "reponse_extrait": reponse[:300],
    }
    memoire["bienetre"]["reconnaissances"].append(entree)

    # Registre des succès par membre
    if "membres" not in memoire["bienetre"]:
        memoire["bienetre"]["membres"] = {}
    if membre not in memoire["bienetre"]["membres"]:
        memoire["bienetre"]["membres"][membre] = {"check_ins": [], "alertes": 0}
    if "succes" not in memoire["bienetre"]["membres"][membre]:
        memoire["bienetre"]["membres"][membre]["succes"] = []
    memoire["bienetre"]["membres"][membre]["succes"].append({
        "date": datetime.now().isoformat(),
        "accomplissement": accomplissement,
    })

    sauvegarder_memoire(memoire)

    ts = horodatage()
    prenom = membre.split()[0].lower() if membre else "membre"
    nom_fichier = f"reconnaissance_{prenom}_{ts}.txt"
    contenu = f"""RECONNAISSANCE — {membre.upper()}
═══════════════════════════════════════════════════════════════════
Membre       : {membre}
Date         : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Accomplissement : {accomplissement}
═══════════════════════════════════════════════════════════════════

{reponse}
"""
    sauvegarder_fichier(contenu, nom_fichier)

    return reponse


# ─── AGENT 5 : ÉNERGIE COLLECTIVE ─────────────────────────────────────────────

def agent_energie_collective():
    """
    Optimise les rythmes de l'équipe pour une énergie durable.
    Analyse les patterns de charge et recommande une organisation hebdomadaire saine.
    """
    incrementer_stat("agent_energie_collective")

    donnees = obtenir_donnees_bienetre()
    membres = donnees.get("membres", {})
    check_ins = donnees.get("check_ins", [])

    # Analyse des patterns de charge et d'énergie
    patterns = {
        "nb_membres": len(membres),
        "nb_check_ins": len(check_ins),
        "charges_par_membre": {},
        "tendances": {},
        "alertes_recentes": 0,
    }

    for nom, data in membres.items():
        recents = data.get("check_ins", [])[-10:]
        if recents:
            charges = [ci["scores"]["charge_travail"] for ci in recents if "scores" in ci]
            humeurs = [ci["scores"]["humeur"] for ci in recents if "scores" in ci]
            patterns["charges_par_membre"][nom] = {
                "charge_moyenne": round(sum(charges) / len(charges), 1) if charges else 5,
                "humeur_moyenne": round(sum(humeurs) / len(humeurs), 1) if humeurs else 5,
                "nb_alertes": data.get("alertes", 0),
                "nb_succes": len(data.get("succes", [])),
            }
            patterns["alertes_recentes"] += data.get("alertes", 0)

    if not membres:
        print("\n  ℹ️  Données limitées disponibles. Génération de recommandations générales.")

    agent = creer_agent(f"""Tu es expert en design organisationnel et en gestion de l'énergie collective.
Tu as accompagné des dizaines de startups tech en phase de croissance rapide.
Tu sais que l'énergie d'une équipe est une ressource précieuse et non-renouvelable à court terme.
Tu conçois des rythmes de travail qui maximisent la créativité, la concentration ET la durabilité.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire :

## ⚡ DIAGNOSTIC ÉNERGÉTIQUE DE L'ÉQUIPE
[Analyse de l'état énergétique actuel basée sur les données disponibles]
[Points forts, zones de tension, patterns préoccupants]

## 📅 CARTOGRAPHIE ÉNERGIE DE LA SEMAINE
[Pour chaque jour de la semaine :]
### [Lundi à Vendredi]
- Niveau d'énergie naturel : [Montant / Plateau / Descente]
- Type de travail recommandé : [Travail profond / Réunions / Créativité / Admin]
- À éviter absolument : [...]
- Rituel recommandé : [court et concret]

## 🎯 RECOMMANDATIONS PAR TYPE DE TRAVAIL
### Travail profond (deep work)
[Quand, combien de temps, comment protéger ces créneaux]
### Réunions et synchronisation
[Quand regrouper les réunions, durée maximale, anti-patterns]
### Sessions créatives et innovation
[Moments optimaux, comment créer les conditions]
### Récupération et recharge
[Micro-pauses, déjeuner, fin de journée — rituels de décompression]

## 🔄 RYTHME HEBDOMADAIRE DURABLE
[Proposition de planning type pour une semaine saine chez AgentClaude Solutions]
[Tableau : Horaire | Lundi | Mardi | Mercredi | Jeudi | Vendredi]

## 🚨 PATTERNS INSOUTENABLES À CORRIGER
[Ce qui doit changer avant que ça devienne un problème — soyez spécifique]
[Pour chaque pattern : le risque si inchangé, la correction recommandée]

## 🌱 ACTIVITÉS DE RECHARGE COLLECTIVE
[5 activités concrètes pour recharger l'énergie de l'équipe — durée, format, pourquoi ça marche]
""", temperature=0.7)

    prompt = f"""Analyse les patterns énergétiques de l'équipe AgentClaude Solutions
et conçois un plan pour optimiser l'énergie collective de manière durable.

DONNÉES DISPONIBLES :
{json.dumps(patterns, ensure_ascii=False, indent=2)}

Contexte supplémentaire :
- L'équipe travaille en mode hybride (télétravail + présentiel)
- Les semaines sont intenses, avec des deadlines fréquentes
- L'innovation et la créativité sont au cœur du métier
- L'équipe grandit rapidement — nouveaux arrivants réguliers
- Le risque de burnout dans les startups IA est réel et documenté

Génère des recommandations précises, actionnables dès cette semaine."""

    label = "Optimisation énergie collective — Analyse complète"
    reponse = executer_stream(agent, prompt, label)

    ts = horodatage()
    nom_fichier = f"energie_collective_{ts}.txt"
    contenu = f"""OPTIMISATION ÉNERGIE COLLECTIVE — AGENTCLAUDE SOLUTIONS
═══════════════════════════════════════════════════════════════════
Date d'analyse  : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Membres suivis  : {patterns['nb_membres']}
Check-ins total : {patterns['nb_check_ins']}
═══════════════════════════════════════════════════════════════════

DONNÉES D'ANALYSE :
{json.dumps(patterns, ensure_ascii=False, indent=2)}

═══════════════════════════════════════════════════════════════════

{reponse}
"""
    sauvegarder_fichier(contenu, nom_fichier)

    return reponse


# ─── MENU PRINCIPAL ────────────────────────────────────────────────────────────

def afficher_menu():
    print("\n" + "═" * 66)
    print("  💙  AGENT BIEN-ÊTRE ÉQUIPE — AgentClaude Solutions")
    print("═" * 66)
    print("  Prévenir le burnout · Construire la résilience · Cultiver la joie")
    print("─" * 66)
    print("  1. Check-in bien-être personnel")
    print("  2. Concevoir un rituel d'équipe")
    print("  3. Analyse prévention burnout (données équipe)")
    print("  4. Reconnaissance & célébration")
    print("  5. Optimiser l'énergie collective")
    print("  0. Quitter")
    print("─" * 66)


def saisir_score(label, min_val=1, max_val=10):
    """Saisit un score entier validé entre min_val et max_val."""
    while True:
        try:
            val = int(input(f"  {label} ({min_val}-{max_val}) : "))
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠️  Veuillez entrer un nombre entre {min_val} et {max_val}.")
        except ValueError:
            print("  ⚠️  Veuillez entrer un nombre entier.")


def menu_check_in():
    print("\n  ─── CHECK-IN BIEN-ÊTRE PERSONNEL ───")
    membre = input("  Prénom du membre : ").strip()
    if not membre:
        print("  ⚠️  Prénom requis.")
        return
    print(f"\n  Bonjour {membre} ! Quelques questions rapides sur comment tu vas. 💙")
    print("  (Tout est confidentiel et bienveillant)\n")
    humeur = saisir_score("Humeur générale (1=très bas, 10=excellent)")
    charge = saisir_score("Charge de travail (1=écrasant, 10=bien équilibrée)")
    sens = saisir_score("Sentiment de sens et motivation (1=aucun, 10=plein)")
    print("\n  Un message libre ? (ce qui te pèse, ce qui te fait sourire — ou rien du tout)")
    note = input("  → ").strip()
    agent_check_in_bienetre(membre, humeur, charge, sens, note)


def menu_rituel():
    print("\n  ─── RITUEL D'ÉQUIPE ───")
    print("  Types disponibles :")
    print("    energisant  → Kickoff du lundi, recharge d'énergie")
    print("    cohesion    → Renforcer les liens et la confiance")
    print("    celebration → Célébrer les victoires ensemble")
    print("    reset       → Décompresser après une semaine difficile")
    print("    créativité  → Session d'innovation et d'idées")
    type_rituel = input("\n  Type de rituel : ").strip().lower()
    types_valides = ["energisant", "cohesion", "celebration", "reset", "créativité"]
    if type_rituel not in types_valides:
        print(f"  ⚠️  Type invalide. Choisissez parmi : {', '.join(types_valides)}")
        return
    try:
        nb = int(input("  Nombre de participants : ").strip())
        duree = int(input("  Durée en minutes : ").strip())
    except ValueError:
        print("  ⚠️  Veuillez entrer des nombres valides.")
        return
    agent_rituel_equipe(type_rituel, nb, duree)


def menu_burnout():
    print("\n  ─── ANALYSE PRÉVENTION BURNOUT ───")
    print("  Analyse en cours des données bien-être de l'équipe...")
    agent_prevention_burnout()


def menu_reconnaissance():
    print("\n  ─── RECONNAISSANCE & CÉLÉBRATION ───")
    membre = input("  Prénom et nom du membre à reconnaître : ").strip()
    if not membre:
        print("  ⚠️  Nom requis.")
        return
    print(f"\n  Qu'est-ce que {membre} a accompli ? (soyez précis·e — plus c'est concret, plus la reconnaissance sera puissante)")
    accomplissement = input("  → ").strip()
    if not accomplissement:
        print("  ⚠️  Description de l'accomplissement requise.")
        return
    agent_reconnaissance(membre, accomplissement)


def menu_energie():
    print("\n  ─── OPTIMISATION ÉNERGIE COLLECTIVE ───")
    print("  Analyse des rythmes et patterns de l'équipe en cours...")
    agent_energie_collective()


def main():
    while True:
        afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "0":
            print("\n  💙 Prenez soin de vous et de votre équipe. À bientôt !\n")
            break
        elif choix == "1":
            menu_check_in()
        elif choix == "2":
            menu_rituel()
        elif choix == "3":
            menu_burnout()
        elif choix == "4":
            menu_reconnaissance()
        elif choix == "5":
            menu_energie()
        else:
            print("  ⚠️  Choix invalide. Veuillez entrer un chiffre entre 0 et 5.")

        input("\n  [Appuyez sur Entrée pour revenir au menu]")


if __name__ == "__main__":
    main()
