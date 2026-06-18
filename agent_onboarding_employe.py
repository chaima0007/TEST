"""
AGENT ONBOARDING EMPLOYÉ — Niveau Directeur RH Google/Apple
Accompagne chaque nouvel employé de son premier jour jusqu'à sa pleine productivité.
Génère des kits de bienvenue, programmes de formation, intégration culturelle,
check-ins personnalisés et rapports de cohorte.

Usage : python fichiers/rh/agent_onboarding_employe.py
"""

import os
import sys
import json
from datetime import datetime

from google import genai
from google.genai import types
from memoire import ajouter_interaction, incrementer_stat

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable d'environnement GEMINI_API_KEY manquante.")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE_PROFIL = """
Nom : AgentClaude Solutions
Secteur : Intelligence Artificielle — Agents autonomes
Mission : Révolutionner l'automatisation d'entreprise par des agents IA sur mesure
Services :
  - Conception d'agents autonomes (Claude, Gemini)
  - Orchestrateurs multi-agents clé en main
  - Migration et modernisation de systèmes legacy
  - Audit et sécurité des systèmes IA
  - Formation des équipes sur les technologies d'agents IA
Culture :
  - Innovation constante et curiosité intellectuelle
  - Autonomie et responsabilisation de chaque collaborateur
  - Collaboration étroite entre équipes techniques et métier
  - Télétravail hybride avec réunions d'équipe hebdomadaires
  - Budget formation annuel de 3 000 € par collaborateur
"""


# ─── UTILITAIRES ──────────────────────────────────────────────────────────────

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


def creer_agent(instructions, temperature=0.5):
    """Instancie un modèle Gemini avec les instructions système données."""
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4000,
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
    """Sauvegarde le contenu dans le dossier fichiers/rh/ et affiche la confirmation."""
    dossier = os.path.join(os.path.dirname(__file__))
    chemin = os.path.join(dossier, nom_fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  ✅ Document sauvegardé → {chemin}")


# ─── AGENTS D'ONBOARDING ──────────────────────────────────────────────────────

def agent_kit_bienvenue(nom, poste, date_arrivee):
    """
    Génère un kit de bienvenue complet et personnalisé pour un nouvel employé.

    Args:
        nom          : Prénom et nom de l'employé
        poste        : Intitulé du poste occupé
        date_arrivee : Date d'arrivée (format JJ/MM/AAAA)
    """
    incrementer_stat("agent_kit_bienvenue")

    agent = creer_agent(f"""Tu es Directrice des Ressources Humaines chez AgentClaude Solutions,
avec 20 ans d'expérience en onboarding chez Google et Apple.
Tu crées des kits de bienvenue qui font que chaque nouveau collaborateur se sent
immédiatement valorisé, ancré dans la culture et opérationnel dès le jour 1.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu produis un kit de bienvenue COMPLET avec les sections suivantes :

## 1. LETTRE DE BIENVENUE PERSONNALISÉE DU CEO
   - Adressée directement à l'employé par son prénom
   - Mentionne spécifiquement son poste et sa contribution attendue
   - Rappelle la vision de l'entreprise et pourquoi ce recrutement est stratégique
   - Ton chaleureux et inspirant, signé "Alexandre Martin, CEO"

## 2. GUIDE DE LA CULTURE D'ENTREPRISE
   - Les 5 valeurs fondamentales avec exemples concrets du quotidien
   - Ce qui rend AgentClaude unique (ce que les employés disent vraiment)
   - Les non-négociables et les libertés laissées à chacun
   - Les traditions de l'équipe (rituels, célébrations, habitudes)

## 3. DESCRIPTION DE L'ORGANIGRAMME DE L'ÉQUIPE
   - L'équipe directe (noms, postes, rôles, personnalités brèves)
   - Les interlocuteurs clés dans d'autres équipes
   - La hiérarchie réelle vs. la hiérarchie formelle
   - À qui s'adresser pour quoi (annuaire de ressources humaines)

## 4. AGENDA JOUR 1 — MINUTE PAR MINUTE
   - 08h30 → Accueil, remise du matériel, visite des locaux
   - Déjeuner d'équipe organisé
   - Réunions de présentation planifiées
   - Heure de fin raisonnable avec une impression positive

## 5. PLAN DE LA PREMIÈRE SEMAINE (Jours 2 à 5)
   - Objectifs de chaque journée
   - Réunions prioritaires à organiser
   - Lectures et ressources à consulter
   - Premières tâches concrètes à réaliser

## 6. PLAN 30-60-90 JOURS (Objectifs du premier mois)
   - J30 : Comprendre et observer — livrables attendus
   - J60 : Contribuer et proposer — jalons mesurables
   - J90 : Piloter et innover — résultats concrets attendus

## 7. PROGRAMME BUDDY (Parrain/Marraine)
   - Profil du buddy attribué et pourquoi ce choix
   - Fréquence et format des échanges recommandés
   - Sujets à aborder lors des premiers échanges
   - Comment tirer le meilleur parti de ce programme

## 8. CHECKLIST D'ACCÈS AUX OUTILS
   - Comptes à créer / accès à demander (avec délais estimés)
   - Outils essentiels : Slack, GitHub, Notion, Google Workspace, Jira
   - Outils spécifiques au poste
   - Formations obligatoires à compléter en semaine 1

## 9. QUICK WINS — 5 VICTOIRES À DÉCROCHER EN SEMAINE 1
   - Actions concrètes, rapides et visibles
   - Adaptées au poste et au niveau d'expérience
   - Conçues pour construire la confiance et la crédibilité rapidement

Rédige tout en français, avec un ton professionnel, chaleureux et inspirant.""",
        temperature=0.65,
    )

    prompt = (
        f"Nouvel employé : {nom}\n"
        f"Poste : {poste}\n"
        f"Date d'arrivée : {date_arrivee}\n\n"
        f"Génère le kit de bienvenue complet pour {nom} qui rejoint AgentClaude Solutions."
    )
    reponse = executer_stream(agent, prompt, f"Kit de Bienvenue — {nom} ({poste})")
    ajouter_interaction("RH_Onboarding", "kit_bienvenue", reponse)
    return reponse


def agent_formation_initiale(poste, niveau):
    """
    Crée un programme de formation initiale personnalisé selon le poste et le niveau.

    Args:
        poste  : Intitulé du poste (ex: "Ingénieur IA", "Chef de Projet")
        niveau : Niveau d'expérience (ex: "Junior", "Confirmé", "Senior")
    """
    incrementer_stat("agent_formation_initiale")

    agent = creer_agent(f"""Tu es Directrice Learning & Development chez AgentClaude Solutions,
ancienne responsable Formation chez Google. Tu conçois des programmes de formation
initiale qui accélèrent drastiquement la montée en compétences des nouveaux employés.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu crées un programme de formation initiale EXHAUSTIF structuré ainsi :

## MODULE 1 : COMPÉTENCES TECHNIQUES À ACQUÉRIR
   - Compétences prioritaires (critiques pour le poste dans les 30 premiers jours)
   - Compétences secondaires (utiles dans les 60-90 jours)
   - Technologies et outils spécifiques à maîtriser
   - Niveau de maîtrise attendu pour chaque compétence (débutant/intermédiaire/expert)

## MODULE 2 : CONTEXTE MÉTIER À COMPRENDRE
   - L'industrie des agents IA — tendances, acteurs, enjeux
   - Le modèle d'affaires d'AgentClaude Solutions
   - Les clients types et leurs problématiques
   - Le positionnement concurrentiel et les différenciateurs

## MODULE 3 : PARTIES PRENANTES CLÉS À RENCONTRER
   - Liste nominative avec rôle, contexte de collaboration, sujets à aborder
   - Ordre de priorité des rencontres (semaine 1, 2, 3)
   - Comment préparer chaque réunion de présentation
   - Questions intelligentes à poser pour construire des relations durables

## MODULE 4 : PROCESSUS INTERNES À APPRENDRE
   - Processus de développement produit (sprints, code review, déploiement)
   - Processus de gestion de projet (outils, rituels, reporting)
   - Processus RH (congés, notes de frais, évaluations)
   - Processus commercial (de la prospection à la signature)

## MODULE 5 : TIMELINE AVEC JALONS
   - Semaine 1 : Objectifs d'apprentissage et jalons de validation
   - Semaines 2-3 : Approfondissement et première contribution
   - Mois 2 : Autonomie croissante — ce qui doit être acquis
   - Mois 3 : Pleine opérationnalité — critères de réussite

## MODULE 6 : RESSOURCES PAR MODULE
   - Documentation interne (wikis, guides, playbooks)
   - Ressources externes (livres, vidéos, cours en ligne recommandés)
   - Communautés et veille recommandées (Slack, newsletters, podcasts)
   - Mentors internes sur chaque sujet

## MODULE 7 : QUESTIONS DE VÉRIFICATION DES CONNAISSANCES
   - 3 à 5 questions par module pour valider la compréhension
   - Questions pratiques (mises en situation) et théoriques
   - Critères de réponse attendus

Adapte le programme au niveau d'expérience ({niveau}) pour ne pas surcharger un expert
ni laisser un junior sans cadre. Rédige en français, ton professionnel et pédagogique.""",
        temperature=0.5,
    )

    prompt = (
        f"Poste : {poste}\n"
        f"Niveau d'expérience : {niveau}\n\n"
        f"Génère le programme de formation initiale complet pour ce profil chez AgentClaude Solutions."
    )
    reponse = executer_stream(agent, prompt, f"Programme de Formation Initiale — {poste} ({niveau})")
    ajouter_interaction("RH_Onboarding", "formation_initiale", reponse)
    return reponse


def agent_integration_culture(valeurs_entreprise):
    """
    Crée un programme d'intégration culturelle approfondi.

    Args:
        valeurs_entreprise : Les valeurs clés de l'entreprise (ex: "Innovation, Autonomie, Excellence")
    """
    incrementer_stat("agent_integration_culture")

    agent = creer_agent(f"""Tu es Chief Culture Officer chez AgentClaude Solutions,
ancienne Head of Culture chez Apple. Tu conçois des programmes d'intégration culturelle
qui transforment les nouveaux employés en ambassadeurs authentiques de la culture d'entreprise.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu produis un programme d'intégration culturelle COMPLET :

## 1. VALEURS DE L'ENTREPRISE — DÉCRYPTAGE PRATIQUE
   Pour chaque valeur fournie :
   - Définition précise dans le contexte d'AgentClaude Solutions
   - 3 exemples concrets de cette valeur en action au quotidien
   - Comment cette valeur influence les décisions et les comportements
   - Ce que cette valeur signifie pour le poste du nouvel employé
   - Ce qui serait en contradiction avec cette valeur (contre-exemples)

## 2. CADRES DE PRISE DE DÉCISION
   - Le processus de décision chez AgentClaude (qui décide quoi, comment)
   - Les heuristiques utilisées face à l'ambiguïté
   - Comment escalader vs. décider seul
   - Les erreurs acceptables et celles qui ne le sont pas
   - La tolérance au risque et à l'expérimentation

## 3. NORMES DE COMMUNICATION
   - Communication asynchrone : outils (Slack/email/Notion), délais de réponse attendus,
     bonnes pratiques de rédaction, quand ne PAS utiliser l'asynchrone
   - Communication synchrone : quand convoquer une réunion, durée standard,
     ordre du jour obligatoire, prise de décision en réunion vs. après
   - Normes d'écriture : style des messages Slack, niveau de formalité des emails,
     documentation des décisions
   - Communication avec les clients : ton, fréquence, gestion des attentes

## 4. APPROCHE DE RÉSOLUTION DE CONFLITS
   - Les conflits comme signal positif vs. toxique : comment différencier
   - Étapes pour résoudre un désaccord en direct (protocole en 4 étapes)
   - Quand et comment impliquer un manager ou les RH
   - Comment dire non avec respect et assertivité
   - Gestion des différences culturelles dans une équipe internationale

## 5. CULTURE DU FEEDBACK
   - Philosophie du feedback chez AgentClaude (radical candor, SBI, etc.)
   - Comment donner un feedback constructif : structure et exemples
   - Comment recevoir un feedback : mindset et réponses adaptées
   - Rituels de feedback (1:1, revues de performance, feedback 360)
   - Comment demander du feedback proactivement

## 6. PROGRESSION DE CARRIÈRE — TRANSPARENCE TOTALE
   - La grille de niveaux de postes (Junior → Lead → Manager → Director)
   - Les critères objectifs de promotion pour chaque niveau
   - Le processus d'évaluation des performances (fréquence, format, évaluateurs)
   - Comment avoir une conversation sur l'évolution avec son manager
   - Les chemins de carrière disponibles (technique, management, entrepreneurial)

Rédige en français, avec des exemples concrets et un ton à la fois inspirant et pratique.""",
        temperature=0.6,
    )

    prompt = (
        f"Valeurs de l'entreprise à intégrer : {valeurs_entreprise}\n\n"
        f"Génère le programme complet d'intégration culturelle pour AgentClaude Solutions."
    )
    reponse = executer_stream(agent, prompt, f"Programme d'Intégration Culturelle — {valeurs_entreprise}")
    ajouter_interaction("RH_Onboarding", "integration_culture", reponse)
    return reponse


def agent_check_in_employe(nom, semaine_numero, feedback):
    """
    Génère un check-in personnalisé pour un employé en cours d'onboarding.

    Args:
        nom            : Prénom et nom de l'employé
        semaine_numero : Numéro de la semaine d'onboarding (1 à 12)
        feedback       : Retour de l'employé sur son onboarding (texte libre)
    """
    incrementer_stat("agent_check_in_employe")

    semaine_int = int(semaine_numero) if str(semaine_numero).isdigit() else 1
    if semaine_int <= 4:
        phase = "Phase d'accueil et de découverte (semaines 1-4)"
        attentes = "Observer, absorber, poser beaucoup de questions, réaliser les premiers quick wins"
    elif semaine_int <= 8:
        phase = "Phase de contribution (semaines 5-8)"
        attentes = "Prendre en charge des tâches autonomes, proposer des améliorations, développer son réseau interne"
    else:
        phase = "Phase d'intégration complète (semaines 9-12)"
        attentes = "Être pleinement opérationnel, mentorer d'autres nouveaux, contribuer à l'amélioration de l'onboarding"

    agent = creer_agent(f"""Tu es Directrice RH chez AgentClaude Solutions, avec une expertise
pointue en accompagnement des nouveaux talents. Tu conduis des check-ins d'onboarding
qui sont à la fois bienveillants, précis et actionnables.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Phase actuelle de l'onboarding : {phase}
Attentes pour cette phase : {attentes}

Tu génères un check-in personnalisé structuré ainsi :

## 1. RECONNAISSANCE DES PROGRÈS
   - Identifie et valorise les accomplissements spécifiques mentionnés dans le feedback
   - Relie ces progrès aux attentes de la phase actuelle
   - Met en lumière les comportements exemplaires observés
   - Ton : encourageant, sincère, spécifique (pas de généralités)

## 2. RÉPONSE AUX PRÉOCCUPATIONS SOULEVÉES
   - Adresse chaque point de friction ou inquiétude mentionné dans le feedback
   - Propose des solutions concrètes ou des ressources pour chaque problème
   - Normalise les difficultés typiques de cette semaine d'onboarding
   - Distingue les problèmes à résoudre immédiatement vs. qui se résoudront naturellement

## 3. AJUSTEMENTS DU PLAN D'ONBOARDING
   - Si le rythme est trop rapide → proposer des ajustements
   - Si l'employé est en avance → proposer des challenges supplémentaires
   - Si des lacunes sont identifiées → proposer des ressources ciblées
   - Plan d'action concret pour les 2 prochaines semaines

## 4. CONNEXION AUX RESSOURCES
   - 2 à 3 ressources spécifiques (personnes, docs, formations) adaptées aux besoins exprimés
   - Comment accéder à ces ressources et quand les solliciter
   - Prochaines étapes concrètes pour l'employé

## 5. POINTS DE DISCUSSION POUR LE 1:1 MANAGER
   - 4 à 5 sujets précis à aborder lors du prochain 1:1 avec le manager
   - Questions à poser au manager pour clarifier les attentes
   - Points sur lesquels le manager devrait rassurer ou donner plus de visibilité

Rédige en français, sur un ton professionnel, empathique et constructif.""",
        temperature=0.55,
    )

    prompt = (
        f"Employé : {nom}\n"
        f"Semaine d'onboarding : {semaine_numero}\n"
        f"Feedback de l'employé :\n{feedback}\n\n"
        f"Génère le check-in d'onboarding personnalisé pour {nom}."
    )
    reponse = executer_stream(agent, prompt, f"Check-in Onboarding — {nom} (Semaine {semaine_numero})")
    ajouter_interaction("RH_Onboarding", "check_in_employe", reponse)
    return reponse


def agent_rapport_onboarding(employes_liste):
    """
    Génère un rapport de cohorte d'onboarding complet et analytique.

    Args:
        employes_liste : Liste de dicts avec les clés :
                         nom, poste, semaine, satisfaction (1-10), notes, risque_retention
    """
    incrementer_stat("agent_rapport_onboarding")

    total = len(employes_liste)
    satisfaction_moy = (
        sum(e.get("satisfaction", 5) for e in employes_liste) / total
        if total else 0
    )
    risques = [e for e in employes_liste if e.get("risque_retention", False)]
    en_avance = [e for e in employes_liste if e.get("satisfaction", 5) >= 8]

    stats = {
        "total_employes": total,
        "satisfaction_moyenne": round(satisfaction_moy, 1),
        "employes_a_risque": len(risques),
        "employes_tres_satisfaits": len(en_avance),
        "taux_risque_retention": f"{round(len(risques) / total * 100, 1) if total else 0}%",
        "repartition_postes": {},
    }
    for e in employes_liste:
        poste = e.get("poste", "Inconnu")
        stats["repartition_postes"][poste] = stats["repartition_postes"].get(poste, 0) + 1

    details = "\n".join(
        f"- {e['nom']} | Poste : {e.get('poste', 'N/A')} | Semaine : {e.get('semaine', 'N/A')} "
        f"| Satisfaction : {e.get('satisfaction', 'N/A')}/10 "
        f"| Risque rétention : {'OUI ⚠️' if e.get('risque_retention') else 'Non'} "
        f"| Notes : {e.get('notes', 'aucune')}"
        for e in employes_liste
    )

    agent = creer_agent(f"""Tu es Directrice des Ressources Humaines chez AgentClaude Solutions.
Tu produis des rapports de cohorte d'onboarding qui permettent à la direction de prendre
des décisions éclairées pour améliorer l'expérience des nouveaux employés et maximiser la rétention.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

## STRUCTURE DU RAPPORT DE COHORTE D'ONBOARDING

# RAPPORT D'ONBOARDING — COHORTE DU {datetime.now().strftime('%B %Y').upper()}

## 1. RÉSUMÉ EXÉCUTIF (5 lignes maximum)

## 2. MÉTRIQUES CLÉS
   - Temps moyen de montée en productivité (estimé)
   - Scores de satisfaction par phase d'onboarding
   - Taux de complétion des formations initiales
   - Tendances comparées aux cohortes précédentes

## 3. SIGNAUX D'ALERTE RÉTENTION
   - Profils à risque (anonymisés si nécessaire) avec contexte
   - Patterns récurrents dans les insatisfactions
   - Actions d'intervention recommandées et urgence
   - Délai de réponse recommandé pour chaque cas

## 4. ANALYSE DE L'EFFICACITÉ DU PROGRAMME
   - Points forts du programme actuel (avec données à l'appui)
   - Points faibles identifiés (frictions, lacunes, surcharges)
   - Comparaison par poste et par niveau d'expérience
   - Feedback qualitatif synthétisé

## 5. AMÉLIORATIONS RECOMMANDÉES
   - 5 améliorations prioritaires classées par impact/effort
   - Quick wins réalisables dans les 2 semaines
   - Changements structurels à planifier sur 3 à 6 mois
   - KPIs à suivre pour mesurer l'impact des améliorations

## 6. PLAN D'ACTION — PROCHAINES ÉTAPES
   - Actions immédiates (cette semaine)
   - Actions à 30 jours
   - Révisions du programme pour la prochaine cohorte

Rédige en français, avec un style analytique, factuel et orienté décision.""",
        temperature=0.35,
    )

    prompt = (
        f"Statistiques de la cohorte :\n{json.dumps(stats, ensure_ascii=False, indent=2)}\n\n"
        f"Détail des employés :\n{details}\n\n"
        f"Génère le rapport complet de la cohorte d'onboarding."
    )
    reponse = executer_stream(agent, prompt, f"Rapport de Cohorte d'Onboarding — {total} Employés")
    ajouter_interaction("RH_Onboarding", "rapport_onboarding", reponse)
    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────────────────────

def menu():
    print("\n" + "═" * 66)
    print("  AGENT ONBOARDING EMPLOYÉ — AgentClaude Solutions")
    print("  Niveau Directeur RH Google / Apple")
    print("═" * 66)

    while True:
        print("\n  1. Générer un kit de bienvenue complet")
        print("  2. Créer un programme de formation initiale")
        print("  3. Concevoir un programme d'intégration culturelle")
        print("  4. Générer un check-in personnalisé")
        print("  5. Produire un rapport de cohorte d'onboarding")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir !\n")
            break

        elif choix == "1":
            nom = input("  Prénom et nom de l'employé → ").strip()
            poste = input("  Intitulé du poste → ").strip()
            date_arrivee = input("  Date d'arrivée (JJ/MM/AAAA) → ").strip()
            kit = agent_kit_bienvenue(nom, poste, date_arrivee)
            nom_fichier = f"kit_bienvenue_{nom.replace(' ', '_').lower()}.txt"
            sauvegarder_fichier(kit, nom_fichier)

        elif choix == "2":
            poste = input("  Intitulé du poste → ").strip()
            niveau = input("  Niveau d'expérience (Junior / Confirmé / Senior / Lead) → ").strip()
            programme = agent_formation_initiale(poste, niveau)
            nom_fichier = f"formation_initiale_{poste.replace(' ', '_').lower()}_{niveau.lower()}.txt"
            sauvegarder_fichier(programme, nom_fichier)

        elif choix == "3":
            print("  Entrez les valeurs de l'entreprise (ex: Innovation, Autonomie, Excellence, Collaboration)")
            valeurs = input("  Valeurs → ").strip()
            programme = agent_integration_culture(valeurs)
            nom_fichier = "programme_integration_culture.txt"
            sauvegarder_fichier(programme, nom_fichier)

        elif choix == "4":
            nom = input("  Prénom et nom de l'employé → ").strip()
            semaine = input("  Numéro de semaine d'onboarding (1-12) → ").strip()
            print("  Feedback de l'employé (terminez par une ligne contenant uniquement 'FIN') :")
            lignes = []
            while True:
                ligne = input()
                if ligne.strip().upper() == "FIN":
                    break
                lignes.append(ligne)
            feedback = "\n".join(lignes)
            check_in = agent_check_in_employe(nom, semaine, feedback)
            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"check_in_{nom.replace(' ', '_').lower()}_s{semaine}_{horodatage}.txt"
            sauvegarder_fichier(check_in, nom_fichier)

        elif choix == "5":
            print("  Saisie des employés de la cohorte (entrez 'FIN' comme nom pour terminer)")
            employes = []
            while True:
                nom = input(f"\n  Employé {len(employes) + 1} — Nom → ").strip()
                if nom.upper() == "FIN":
                    break
                poste = input("  Poste → ").strip()
                semaine = input("  Semaine d'onboarding → ").strip()
                satisfaction_str = input("  Satisfaction (1-10) → ").strip()
                try:
                    satisfaction = int(satisfaction_str)
                except ValueError:
                    satisfaction = 5
                risque_str = input("  Risque de rétention ? (o/n) → ").strip().lower()
                risque = risque_str in ("o", "oui", "y", "yes")
                notes = input("  Notes (optionnel) → ").strip()
                employes.append({
                    "nom": nom,
                    "poste": poste,
                    "semaine": semaine,
                    "satisfaction": satisfaction,
                    "risque_retention": risque,
                    "notes": notes,
                })

            if not employes:
                print("  Aucun employé saisi.")
                continue

            rapport = agent_rapport_onboarding(employes)
            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"rapport_onboarding_cohorte_{horodatage}.txt"
            sauvegarder_fichier(rapport, nom_fichier)

        else:
            print("  Choix invalide. Veuillez saisir un numéro entre 0 et 5.")


if __name__ == "__main__":
    menu()
