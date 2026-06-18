"""
AGENT RÉPUTATION & GESTION DE CRISE — AgentClaude Solutions
Répond aux avis, gère les crises, surveille l'e-réputation,
construit le storytelling de marque et pilote la stratégie LinkedIn.
Tout ça. En français. Sans excuses.

Usage : python agent_reputation.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types
from memoire import incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

# ─── Dossier de sauvegarde ────────────────────────────────────
REPUTATION_DIR = os.path.join("fichiers", "reputation")
os.makedirs(REPUTATION_DIR, exist_ok=True)

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Spécialité : Automatisation par agents IA (Claude, Gemini)
Services :
  - Agents autonomes sur mesure pour entreprises
  - Migration et modernisation de code legacy
  - Sécurité et audit IA
  - Formation équipes sur agents IA
  - Orchestrateurs autonomes clé en main
Valeurs : Réactivité, transparence, excellence technique, accompagnement humain
Positionnement : Référence francophone en agents IA pour PME et ETI
Site : agentclaude.solutions
"""


# ─── Utilitaires ──────────────────────────────────────────────

def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def creer_agent(instructions, temperature=0.7):
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=4096
        ),
    )


def executer_stream(model, prompt, label):
    print(f"\n{'═' * 62}")
    print(f"  ► {label}")
    print(f"{'═' * 62}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur agent : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_fichier(prefixe, contenu, suffixe=""):
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom = f"{prefixe}_{horodatage}{suffixe}.txt"
    chemin = os.path.join(REPUTATION_DIR, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"=== AgentClaude Solutions — {prefixe.upper()} ===\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 62 + "\n\n")
        f.write(contenu)
    print(f"\n  ✅ Document sauvegardé → {chemin}")
    return chemin


# ─── AGENT 1 : Réponse aux avis clients ───────────────────────

def agent_reponse_avis(avis_texte, note, plateforme):
    """
    Génère une réponse professionnelle parfaite à un avis client.
    Adapte le ton selon la note (1-5 étoiles) et la plateforme.
    """
    incrementer_stat("agent_reponse_avis")

    instructions = f"""
Tu es le Directeur de l'Expérience Client d'AgentClaude Solutions.
Tu rédiges des réponses aux avis en ligne qui sont de véritables modèles du genre.

{ENTREPRISE_PROFIL}

RÈGLES ABSOLUES :
- Jamais défensif, jamais d'excuses vides, jamais de copié-collé générique.
- Toujours personnalisé selon le contenu exact de l'avis.
- Ton adapté à la plateforme ({plateforme}) et à la note ({note}/5).
- Réponse en français, professionnelle et authentique.
- Maximum 200 mots pour ne pas noyer le message.

LOGIQUE PAR NOTE :
★★★★★ (5/5) → Chaleur sincère + renforcement de la proposition de valeur + invitation à revenir / recommander. Partager l'enthousiasme sans en faire trop.
★★★★☆ (4/5) → Remerciement + reconnaissance du point d'amélioration mentionné + engagement concret d'amélioration.
★★★☆☆ (3/5) → Reconnaître l'expérience mitigée + montrer les améliorations en cours + proposer un échange direct.
★★☆☆☆ (1-2/5) → Désescalade empathique + prise de responsabilité sans excuse creuse + invitation à résoudre hors ligne avec contact direct + offre de résolution concrète. Ne jamais se justifier publiquement sur les détails.

FORMAT DE RÉPONSE :
1. La réponse rédigée et prête à publier
2. Note stratégique (2-3 lignes sur pourquoi ce choix de ton/angle)
"""

    agent = creer_agent(instructions, temperature=0.65)

    note_int = int(note)
    if note_int == 5:
        niveau = "5 étoiles — satisfaction totale"
        contexte_ton = "chaleureux, enthousiaste mais professionnel"
    elif note_int == 4:
        niveau = "4 étoiles — très satisfait avec réserve mineure"
        contexte_ton = "reconnaissant et proactif sur l'amélioration"
    elif note_int == 3:
        niveau = "3 étoiles — expérience mitigée"
        contexte_ton = "compréhensif, ouvert au dialogue"
    else:
        niveau = f"{note_int} étoile(s) — insatisfaction sérieuse"
        contexte_ton = "empathique, désescalade, orienté solution"

    prompt = f"""
Rédige la réponse parfaite à cet avis {plateforme} ({niveau}).

AVIS DU CLIENT :
« {avis_texte} »

NOTE : {note}/5
PLATEFORME : {plateforme}
TON REQUIS : {contexte_ton}

Génère :
1. ✉️ RÉPONSE PUBLIABLE (prête à copier-coller)
2. 🎯 NOTE STRATÉGIQUE (pourquoi cet angle)
3. 📌 ACTIONS INTERNES RECOMMANDÉES (ce que l'équipe doit faire en coulisses)
"""

    label = f"Réponse avis {note}/5 étoile(s) — {plateforme}"
    reponse = executer_stream(agent, prompt, label)

    contenu = f"PLATEFORME : {plateforme}\nNOTE : {note}/5\n\nAVIS CLIENT :\n{avis_texte}\n\n{'─'*50}\n\nRÉPONSE GÉNÉRÉE :\n{reponse}"
    sauvegarder_fichier("reponse_avis", contenu, f"_{note}etoiles")
    return reponse


# ─── AGENT 2 : Gestion de crise ───────────────────────────────

def agent_gestion_crise(situation, canal):
    """
    Protocole complet de gestion de crise réputationnelle.
    Produit un plan d'action immédiat + communication multi-audience.
    """
    incrementer_stat("agent_gestion_crise")

    instructions = f"""
Tu es un expert en communication de crise de niveau C-suite, spécialisé en entreprises tech et IA.
Tu travailles pour AgentClaude Solutions et tu dois produire un protocole de crise opérationnel immédiatement.

{ENTREPRISE_PROFIL}

PRINCIPES DE GESTION DE CRISE :
- Vitesse + transparence = confiance préservée.
- Chaque heure sans réponse = amplification de la crise x2.
- Jamais de mensonge, jamais de minimisation, jamais d'attaque.
- Prendre le contrôle du récit sans le déformer.
- Séparer les faits, les émotions et les actions.

TA MISSION : Produire un plan de crise complet, structuré, utilisable MAINTENANT.
Tout en français. Tout orienté action.
"""

    agent = creer_agent(instructions, temperature=0.5)

    prompt = f"""
SITUATION DE CRISE : {situation}
CANAL D'ÉMERGENCE : {canal}
DATE/HEURE : {datetime.now().strftime('%d/%m/%Y à %H:%M')}

Génère le PROTOCOLE DE CRISE COMPLET :

## 🚨 1. RÉPONSE IMMÉDIATE (dans les 2 premières heures)
- Actions prioritaires minute par minute (0-30min / 30min-1h / 1h-2h)
- Qui fait quoi (désignation des rôles)
- Première déclaration publique (prête à publier)

## 📣 2. PLAN DE COMMUNICATION PAR AUDIENCE
Pour chaque audience, un message adapté et prêt à envoyer :
- **Clients existants** : email + message direct
- **Équipe interne** : note interne
- **Presse / Journalistes** : communiqué
- **Réseaux sociaux** : post {canal} + commentaires types

## ⏱️ 3. TIMELINE DES ACTIONS (J0 à J14)
Tableau : Jour | Action | Responsable | Canal | Indicateur de succès

## ❌ 4. CE QU'IL NE FAUT ABSOLUMENT PAS DIRE OU FAIRE
Liste des 10 erreurs fatales à éviter dans cette crise précise.

## 🔧 5. PLAN DE RÉPARATION RÉPUTATIONNELLE (post-crise J15 à J60)
- Actions de reconstruction de confiance
- Contenu positif à produire et diffuser
- Indicateurs de sortie de crise
- KPIs à surveiller

## 📋 6. MESSAGES TYPES PRÊTS À L'EMPLOI
Templates complets pour chaque canal, personnalisables en 2 minutes.
"""

    label = f"Protocole de crise — {canal}"
    reponse = executer_stream(agent, prompt, label)

    contenu = f"SITUATION : {situation}\nCANAL : {canal}\nDATE : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n{'─'*50}\n\nPROTOCOLE GÉNÉRÉ :\n{reponse}"
    sauvegarder_fichier("gestion_crise", contenu)
    return reponse


# ─── AGENT 3 : Veille e-réputation ────────────────────────────

def agent_veille_reputation(nom_entreprise, secteur):
    """
    Stratégie complète de monitoring de la réputation en ligne.
    Plateformes, mots-clés, alertes gratuites, réponses aux mentions.
    """
    incrementer_stat("agent_veille_reputation")

    instructions = f"""
Tu es un expert en e-réputation et community management B2B, spécialisé dans le secteur tech/IA.
Tu vas créer une stratégie de veille complète et opérationnelle.

{ENTREPRISE_PROFIL}

TON APPROCHE :
- Pragmatique : outils gratuits d'abord, payants si indispensables.
- Actionnables : chaque recommandation doit pouvoir se mettre en place cette semaine.
- Proactif : la meilleure défense c'est une bonne réputation construite avant la crise.
- Tout en français, structuré et prêt à utiliser.
"""

    agent = creer_agent(instructions, temperature=0.6)

    prompt = f"""
Crée la stratégie de veille e-réputation complète pour :
ENTREPRISE : {nom_entreprise}
SECTEUR : {secteur}

## 📡 1. CARTOGRAPHIE DES PLATEFORMES À SURVEILLER
Pour chaque plateforme : priorité (haute/moyenne/faible) + fréquence de vérification + quoi surveiller exactement.
Liste exhaustive : Google Business, Trustpilot, LinkedIn, Twitter/X, Facebook, YouTube, Reddit, Glassdoor, forums spécialisés IA, blogs tech, podcasts, presse en ligne.

## 🔑 2. MOTS-CLÉS ET EXPRESSIONS À SURVEILLER
- Nom de l'entreprise et variantes (fautes d'orthographe incluses)
- Noms des dirigeants
- Produits / services
- Expressions concurrentielles
- Termes négatifs combinés (arnaque, problème, déçu...)
- Termes sectoriels (agents IA, automatisation, Claude, Gemini...)

## 🔔 3. CONFIGURATION DES GOOGLE ALERTS (guide pas à pas)
Instructions précises pour configurer 10 alertes gratuites stratégiques.
Syntaxe exacte des requêtes, fréquence, format email.

## 📱 4. OUTILS GRATUITS ET FREEMIUM RECOMMANDÉS
Pour chaque outil : nom, usage, plan gratuit disponible, lien, note /5.

## 💬 5. PROTOCOLE DE RÉPONSE AUX MENTIONS
- Mentions positives : comment réagir pour amplifier
- Mentions neutres : comment engager
- Mentions négatives : arbre de décision (répondre / ignorer / escalader)
- Temps de réponse cible par plateforme

## 🏆 6. STRATÉGIE DE THOUGHT LEADERSHIP PROACTIF
- 5 types de contenus à produire pour construire la réputation
- Calendrier de publication recommandé
- 3 partenariats ou collaborations à rechercher dans le secteur IA
- Comment transformer les clients satisfaits en ambassadeurs
"""

    label = f"Veille e-réputation — {nom_entreprise} / {secteur}"
    reponse = executer_stream(agent, prompt, label)

    contenu = f"ENTREPRISE : {nom_entreprise}\nSECTEUR : {secteur}\n\n{'─'*50}\n\nSTRATÉGIE DE VEILLE :\n{reponse}"
    sauvegarder_fichier("veille_reputation", contenu, f"_{nom_entreprise.lower().replace(' ', '_')}")
    return reponse


# ─── AGENT 4 : Storytelling de marque ─────────────────────────

def agent_storytelling_marque(valeurs, histoire, differenciateur):
    """
    Construit le récit de marque complet et le positionnement.
    Origin story, mission/vision, pitchs multi-durées, tone of voice.
    """
    incrementer_stat("agent_storytelling_marque")

    instructions = f"""
Tu es un expert en brand strategy et storytelling d'entreprise, spécialisé dans les scale-ups tech B2B.
Tu vas construire le récit complet d'AgentClaude Solutions pour qu'il résonne avec ses cibles.

{ENTREPRISE_PROFIL}

PRINCIPES DU BON STORYTELLING :
- Les faits informent, les histoires persuadent.
- Le "pourquoi" avant le "quoi" (Simon Sinek).
- Authenticité > perfection. Les failles humanisent.
- Chaque audience veut entendre sa propre histoire dans la vôtre.
- La cohérence entre tous les supports construit la confiance.

Rédige tout en français, avec un style vivant et professionnel.
"""

    agent = creer_agent(instructions, temperature=0.8)

    prompt = f"""
Construis le STORYTELLING DE MARQUE COMPLET pour AgentClaude Solutions.

MATIÈRE PREMIÈRE :
- Valeurs : {valeurs}
- Histoire / Origine : {histoire}
- Différenciateur clé : {differenciateur}

## 📖 1. ORIGIN STORY (récit fondateur)
L'histoire de création en 300 mots, avec tension dramatique, moment de bascule et résolution. Style narratif, pas corporatif.

## 🧭 2. MISSION / VISION / VALEURS
- Mission (ce qu'on fait et pour qui — 1 phrase percutante)
- Vision (le monde qu'on veut créer — 1 phrase inspirante)
- Valeurs (5 valeurs avec leur manifestation concrète au quotidien — pas de mots creux)

## 🎤 3. PITCHS MULTI-FORMATS
- **Elevator pitch 30 secondes** : pour un ascenseur ou un cocktail
- **Pitch 2 minutes** : pour une réunion ou un appel découverte
- **Pitch 5 minutes** : pour une conférence ou un investisseur

## 🎯 4. MESSAGES CLÉS PAR AUDIENCE
Pour chaque cible, le message principal + l'angle émotionnel + la preuve :
- **Client PME/ETI** : ce qui le rassure et le convainc
- **Investisseur** : ce qui excite et crédibilise
- **Candidat (recrutement)** : ce qui donne envie de rejoindre
- **Partenaire** : ce qui crée l'envie de collaborer
- **Presse tech** : l'angle qui fait une bonne histoire

## 🗣️ 5. GUIDE DE TON DE VOIX
- Personnalité de marque (5 adjectifs et leur contraire interdit)
- Ce qu'on dit / Ce qu'on ne dit jamais
- Exemples de reformulations (avant → après)
- Niveau de formalité par canal
- Notre rapport à l'humour, à la technique, à la vulgarisation
"""

    label = "Construction du Storytelling de Marque"
    reponse = executer_stream(agent, prompt, label)

    contenu = f"VALEURS : {valeurs}\nHISTOIRE : {histoire}\nDIFFÉRENCIATEUR : {differenciateur}\n\n{'─'*50}\n\nSTORYTELLING :\n{reponse}"
    sauvegarder_fichier("storytelling_marque", contenu)
    return reponse


# ─── AGENT 5 : Stratégie LinkedIn ─────────────────────────────

def agent_linkedin_strategy():
    """
    Stratégie LinkedIn complète pour AgentClaude Solutions.
    Optimisation profil, calendrier, templates de posts, thought leadership.
    """
    incrementer_stat("agent_linkedin_strategy")

    instructions = f"""
Tu es un expert LinkedIn B2B avec 10 ans d'expérience dans la croissance de marques tech.
Tu vas construire la stratégie LinkedIn complète d'AgentClaude Solutions pour en faire
LA référence francophone sur les agents IA.

{ENTREPRISE_PROFIL}

TA PHILOSOPHIE LINKEDIN :
- LinkedIn n'est pas un CV géant, c'est une scène de conférence permanente.
- Le contenu éducatif surperforme le contenu promotionnel x5.
- La régularité bat l'inspiration occasionnelle.
- Les gens achètent à des personnes, pas à des logos — humaniser la marque.
- L'objectif : être PENSÉ EN PREMIER quand quelqu'un a besoin d'agents IA.

Tout en français, concret, immédiatement applicable.
"""

    agent = creer_agent(instructions, temperature=0.75)

    prompt = f"""
Génère la STRATÉGIE LINKEDIN COMPLÈTE pour AgentClaude Solutions.

## ✅ 1. CHECKLIST D'OPTIMISATION DU PROFIL PAGE ENTREPRISE
Tous les champs à remplir, avec exemples et formules copywriting prêtes à l'emploi.
Section par section : bannière, slogan, description, spécialités, URL personnalisée, CTA.

## 📅 2. CALENDRIER ÉDITORIAL (4 semaines type)
Tableau : Semaine | Jour | Type de post | Sujet | Format | Hashtags | Heure optimale
- Fréquence recommandée et justification
- Meilleurs jours/heures pour notre cible B2B en France
- Mix optimal entre types de contenu

## 📝 3. 10 TEMPLATES DE POSTS PRÊTS À L'EMPLOI
Pour chaque template : titre accrocheur, structure complète, exemple rédigé, call-to-action.
Couvrir : Carrousel éducatif | Sondage | Témoignage client (anonymisé) | Coulisse / Behind the scenes | Insight sectoriel choc | Fail & leçon apprise | Checklist pratique | Annonce produit/service | Post recrutement | Post célébration équipe

## 🤝 4. TACTIQUES D'ENGAGEMENT ET DE CROISSANCE
- Comment commenter stratégiquement pour gagner en visibilité
- Avec qui interagir (influenceurs IA, médias tech, clients potentiels)
- Comment transformer les vues en leads sans être pushy
- Stratégie de hashtags (liste des 20 hashtags prioritaires FR/EN)
- Comment utiliser les articles LinkedIn vs posts courts

## 🧠 5. CONSTRUIRE LE THOUGHT LEADERSHIP IA EN FRANCE
- 5 sujets sur lesquels AgentClaude Solutions doit prendre position
- Comment structurer un point de vue qui fait autorité
- Comment réagir aux tendances IA (ChatGPT, Gemini, réglementations EU AI Act...)
- Plan pour devenir source citée par les journalistes tech FR
- KPIs pour mesurer la progression (portée, followers, leads LinkedIn)

## 🎯 6. STRATÉGIE DE CONTENU PERSONAL BRANDING (pour le/les fondateur·s)
Le profil perso performe 5x mieux que la page entreprise.
Recommandations spécifiques pour humaniser la marque via le fondateur.
"""

    label = "Stratégie LinkedIn Complète — AgentClaude Solutions"
    reponse = executer_stream(agent, prompt, label)

    contenu = f"DATE : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n{'─'*50}\n\nSTRATÉGIE LINKEDIN :\n{reponse}"
    sauvegarder_fichier("linkedin_strategy", contenu)
    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def afficher_menu():
    print("\n" + "╔" + "═" * 60 + "╗")
    print("║" + "  🎯 AGENT RÉPUTATION — AgentClaude Solutions".center(60) + "║")
    print("║" + "  Online Reputation & Crisis Management".center(60) + "║")
    print("╠" + "═" * 60 + "╣")
    print("║  1. Répondre à un avis client (Google / Trustpilot / LinkedIn)  ║")
    print("║  2. Gérer une crise réputationnelle                             ║")
    print("║  3. Stratégie de veille e-réputation                            ║")
    print("║  4. Construire le storytelling de marque                        ║")
    print("║  5. Stratégie LinkedIn complète                                 ║")
    print("║  0. Quitter                                                     ║")
    print("╚" + "═" * 60 + "╝")
    print(f"\n  📁 Fichiers sauvegardés dans : fichiers/reputation/")


def main():
    print("\n  Démarrage de l'agent réputation...")
    print(f"  Modèle : {MODEL}")
    print(f"  Entreprise : AgentClaude Solutions")

    while True:
        afficher_menu()

        try:
            choix = input("\n  Votre choix (0-5) : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Au revoir !\n")
            break

        if choix == "0":
            print("\n  Au revoir !\n")
            break

        elif choix == "1":
            print("\n  ── Répondre à un avis client ──")
            avis = input("  Collez le texte de l'avis : ").strip()
            if not avis:
                print("  [ERREUR] L'avis ne peut pas être vide.")
                continue
            note_str = input("  Note donnée par le client (1 à 5) : ").strip()
            try:
                note = int(note_str)
                if note < 1 or note > 5:
                    raise ValueError
            except ValueError:
                print("  [ERREUR] Note invalide. Entrez un chiffre entre 1 et 5.")
                continue
            print("  Plateformes disponibles : Google, Trustpilot, LinkedIn, Autres")
            plateforme = input("  Plateforme : ").strip() or "Google"
            agent_reponse_avis(avis, note, plateforme)

        elif choix == "2":
            print("\n  ── Gestion de crise réputationnelle ──")
            situation = input("  Décrivez la situation de crise : ").strip()
            if not situation:
                print("  [ERREUR] La description de la situation est requise.")
                continue
            canal = input("  Canal d'émergence (Twitter/X, LinkedIn, Presse, Forum, Email...) : ").strip() or "Réseaux sociaux"
            agent_gestion_crise(situation, canal)

        elif choix == "3":
            print("\n  ── Stratégie de veille e-réputation ──")
            nom = input("  Nom de l'entreprise [AgentClaude Solutions] : ").strip() or "AgentClaude Solutions"
            secteur = input("  Secteur d'activité [IA & Automatisation B2B] : ").strip() or "IA & Automatisation B2B"
            agent_veille_reputation(nom, secteur)

        elif choix == "4":
            print("\n  ── Storytelling de marque ──")
            valeurs = input("  Valeurs de l'entreprise (ex: transparence, excellence, humain) : ").strip()
            if not valeurs:
                valeurs = "transparence, excellence technique, accompagnement humain, innovation responsable"
                print(f"  Valeurs par défaut utilisées : {valeurs}")
            histoire = input("  Histoire / contexte de création (quelques phrases) : ").strip()
            if not histoire:
                histoire = "Née de la frustration face aux agents IA trop génériques, AgentClaude Solutions a été fondée pour offrir des solutions sur mesure aux entreprises françaises."
                print(f"  Histoire par défaut utilisée.")
            differenciateur = input("  Différenciateur clé vs concurrents : ").strip()
            if not differenciateur:
                differenciateur = "L'unique acteur francophone qui combine expertise Claude + Gemini avec un accompagnement humain de A à Z."
                print(f"  Différenciateur par défaut utilisé.")
            agent_storytelling_marque(valeurs, histoire, differenciateur)

        elif choix == "5":
            print("\n  ── Stratégie LinkedIn complète ──")
            print("  Génération de la stratégie LinkedIn pour AgentClaude Solutions...")
            agent_linkedin_strategy()

        else:
            print(f"\n  [ERREUR] Choix invalide : '{choix}'. Entrez un chiffre entre 0 et 5.")

        input("\n  Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
