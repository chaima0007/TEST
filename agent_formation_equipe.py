"""
AGENT FORMATION ÉQUIPE — Niveau Directeur L&D Entreprise
Évalue les compétences, crée des formations sur mesure, recommande des certifications,
construit des plans de développement individuels et bâtit une culture apprenante.

Usage : python fichiers/rh/agent_formation_equipe.py
"""

import os
import sys
import json
from datetime import datetime

import google.generativeai as genai
from memoire import ajouter_interaction, incrementer_stat

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

def creer_agent(instructions, temperature=0.5):
    """Instancie un modèle Gemini avec les instructions système données."""
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(
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


# ─── AGENTS DE FORMATION ──────────────────────────────────────────────────────

def agent_evaluer_competences(membre_equipe, poste_actuel, evolution_souhaitee):
    """
    Réalise une analyse des écarts de compétences (skills gap analysis) personnalisée.

    Args:
        membre_equipe      : Prénom et nom du membre de l'équipe
        poste_actuel       : Intitulé du poste actuel avec niveau
        evolution_souhaitee: Rôle ou poste cible souhaité
    """
    incrementer_stat("agent_evaluer_competences")

    agent = creer_agent(f"""Tu es Directeur Learning & Development chez AgentClaude Solutions,
avec 20 ans d'expérience dans les grandes entreprises tech (Amazon, Microsoft, Capgemini).
Tu réalises des analyses de compétences rigoureuses, objectives et constructives,
qui donnent aux collaborateurs un chemin clair vers leur évolution professionnelle.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu produis une analyse des écarts de compétences COMPLÈTE :

## 1. INVENTAIRE DES COMPÉTENCES ACTUELLES
   ### Compétences Techniques
   - Liste des compétences techniques estimées pour le poste actuel
   - Niveau présumé pour chacune (Débutant / Intermédiaire / Avancé / Expert)
   - Compétences transférables identifiées

   ### Compétences Comportementales (Soft Skills)
   - Leadership, communication, collaboration, gestion du stress, etc.
   - Points forts comportementaux associés au poste actuel

   ### Compétences Sectorielles
   - Connaissance du secteur des agents IA
   - Compréhension du contexte métier d'AgentClaude Solutions

## 2. COMPÉTENCES REQUISES POUR LE RÔLE CIBLE
   ### Compétences Techniques Indispensables
   - Technologies et outils critiques pour le rôle cible
   - Niveau de maîtrise requis pour chacune

   ### Compétences de Leadership et Management (si applicable)
   - Compétences managériales nécessaires
   - Capacités de prise de décision et de vision stratégique

   ### Compétences Relationnelles Avancées
   - Influence, négociation, communication exécutive, etc.

## 3. ANALYSE DES ÉCARTS — GAP ANALYSIS
   ### Écarts Critiques (à combler en priorité absolue)
   - Compétences totalement absentes et indispensables
   - Impact sur la performance si non comblées

   ### Écarts Significatifs (à développer dans les 6 mois)
   - Compétences présentes mais insuffisantes
   - Niveau actuel vs. niveau cible

   ### Écarts Mineurs (à développer dans les 12 mois)
   - Améliorations souhaitables mais non bloquantes

## 4. COMPÉTENCES PRIORITAIRES À DÉVELOPPER
   Classement des 5 compétences les plus impactantes à développer,
   avec pour chacune :
   - Justification de la priorité
   - Bénéfices concrets attendus
   - Délai réaliste pour atteindre le niveau requis

## 5. PARCOURS D'APPRENTISSAGE PERSONNALISÉ
   ### Phase 1 — Fondations (Mois 1-3)
   - Actions concrètes (formations, lectures, projets pratiques)
   - Ressources recommandées avec liens ou références
   - Jalons de progression à atteindre

   ### Phase 2 — Développement (Mois 4-6)
   - Montée en compétences progressive
   - Projets réels pour pratiquer les nouvelles compétences
   - Mentorat recommandé

   ### Phase 3 — Maîtrise (Mois 7-12)
   - Validation des compétences acquises
   - Prise de responsabilités croissante
   - Indicateurs de réussite mesurables

Rédige en français, avec un ton analytique, encourageant et orienté action.""",
        temperature=0.45,
    )

    prompt = (
        f"Membre de l'équipe : {membre_equipe}\n"
        f"Poste actuel : {poste_actuel}\n"
        f"Évolution souhaitée : {evolution_souhaitee}\n\n"
        f"Réalise l'analyse complète des écarts de compétences pour {membre_equipe}."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Analyse des Compétences — {membre_equipe} → {evolution_souhaitee}"
    )
    ajouter_interaction("RH_Formation", "evaluer_competences", reponse)
    return reponse


def agent_creer_formation(sujet, niveau, duree):
    """
    Crée un module de formation complet, prêt à déployer.

    Args:
        sujet  : Sujet de la formation (ex: "Conception d'agents IA avec Gemini")
        niveau : Niveau du public cible (ex: "Débutant", "Intermédiaire", "Avancé")
        duree  : Durée totale de la formation (ex: "1 jour", "3 heures", "2 semaines")
    """
    incrementer_stat("agent_creer_formation")

    agent = creer_agent(f"""Tu es Ingénieur Pédagogique Senior chez AgentClaude Solutions,
spécialisé dans la formation aux technologies d'agents IA et à l'IA générative.
Tu conçois des formations engageantes, pratiques et mesurables selon les meilleures
méthodologies (instructional design, 70-20-10, apprentissage par l'expérience).

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu crées un module de formation COMPLET et DÉPLOYABLE :

## 1. OBJECTIFS PÉDAGOGIQUES (SMART)
   Pour chaque objectif :
   - Formulation précise (verbe d'action + résultat mesurable)
   - Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini
   - Niveau taxonomique de Bloom visé (mémoriser, comprendre, appliquer, analyser, créer)
   - 5 à 7 objectifs au total, du plus simple au plus complexe

## 2. PLAN DE CONTENU DÉTAILLÉ
   Pour chaque module/chapitre :
   - Titre et durée estimée
   - Concepts clés couverts
   - Points d'attention pédagogique
   - Transition vers le module suivant

## 3. EXERCICES ET ACTIVITÉS PRATIQUES
   - Au moins 4 exercices pratiques progressifs
   - Pour chaque exercice : description, objectif, durée, consignes, critères de réussite
   - Mix de formats : individuel, en binôme, en groupe
   - Au moins 1 exercice de mise en situation réelle

## 4. ÉTUDES DE CAS — CONTEXTE AGENTS IA
   - 2 études de cas ancrées dans le contexte d'AgentClaude Solutions
   - Scénarios réalistes issus des services de l'entreprise
   - Questions d'analyse et de réflexion pour chaque cas
   - Corrigés indicatifs pour le formateur

## 5. QUESTIONS D'ÉVALUATION
   - 10 questions QCM pour valider la compréhension théorique
   - 3 questions ouvertes pour évaluer la réflexion et l'application
   - Critères de notation détaillés
   - Seuil de réussite recommandé

## 6. GUIDE DU FORMATEUR
   - Conseils de facilitation pour chaque module
   - Gestion des questions difficiles (FAQ anticipée)
   - Adaptation selon le profil des participants
   - Timing recommandé et points de pause
   - Matériel nécessaire (salle, outils, logiciels)

## 7. CAHIER DU PARTICIPANT
   - Résumé structuré de chaque module
   - Espaces de prise de notes guidés
   - Fiches mémo des concepts clés
   - Plan d'action personnel post-formation

## 8. RESSOURCES DE SUIVI
   - 5 ressources complémentaires (livres, articles, vidéos, cours)
   - Communautés à rejoindre pour continuer à apprendre
   - Projet de mise en pratique à réaliser dans les 30 jours suivants

Adapte tout le contenu au niveau {niveau} et à la durée de {duree}.
Rédige en français, ton pédagogique, clair et engageant.""",
        temperature=0.55,
    )

    prompt = (
        f"Sujet de la formation : {sujet}\n"
        f"Niveau des participants : {niveau}\n"
        f"Durée totale : {duree}\n\n"
        f"Crée le module de formation complet sur ce sujet pour AgentClaude Solutions."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Module de Formation — {sujet} ({niveau}, {duree})"
    )
    ajouter_interaction("RH_Formation", "creer_formation", reponse)
    return reponse


def agent_certifications_recommandees(poste):
    """
    Recommande les certifications professionnelles les plus pertinentes pour un poste.

    Args:
        poste : Intitulé du poste (ex: "Ingénieur IA", "Chef de Projet", "Commercial")
    """
    incrementer_stat("agent_certifications_recommandees")

    agent = creer_agent(f"""Tu es Directeur Learning & Development chez AgentClaude Solutions.
Tu conseilles les collaborateurs sur les certifications professionnelles qui maximisent
leur valeur sur le marché et leur contribution à l'entreprise.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Pour chaque certification recommandée, tu fournis OBLIGATOIREMENT :

Structure par catégorie :

## CERTIFICATIONS IA / CLOUD (Google, AWS, Azure, Anthropic)
   Pour chaque certification :
   - Nom officiel et organisme certificateur
   - Coût estimé (examen + préparation)
   - Durée de préparation réaliste
   - ROI concret pour le poste (compétences acquises, crédibilité, salaire)
   - Niveau de priorité : CRITIQUE / RECOMMANDÉ / OPTIONNEL
   - Lien officiel ou ressource de préparation recommandée

## CERTIFICATIONS SÉCURITÉ
   (CISSP, CEH, CompTIA Security+, ISO 27001 Lead Auditor, etc.)
   Même format détaillé

## CERTIFICATIONS GESTION DE PROJET
   (PMP, PRINCE2, CAPM, PMI-ACP, etc.)
   Même format détaillé

## CERTIFICATIONS AGILE / SCRUM
   (CSM, PSM, SAFe, PMI-ACP, etc.)
   Même format détaillé

## CERTIFICATIONS LINGUISTIQUES (pour l'expansion internationale)
   (TOEIC, TOEFL, IELTS, DELF/DALF, Goethe-Zertifikat, HSK, etc.)
   Même format détaillé

## CERTIFICATIONS SPÉCIFIQUES AU SECTEUR IA
   (Certifications IA éthique, MLOps, Data Engineering, etc.)
   Même format détaillé

## SYNTHÈSE ET PLAN DE CERTIFICATION
   - Top 3 certifications à prioriser absolument
   - Ordre de passage recommandé avec justification
   - Budget total estimé sur 2 ans
   - Planning réaliste sur 24 mois
   - Comment financer via le budget formation de 3 000 € annuels

Rédige en français, ton professionnel et factuel.""",
        temperature=0.4,
    )

    prompt = (
        f"Poste : {poste}\n\n"
        f"Recommande les certifications professionnelles les plus pertinentes pour ce poste "
        f"chez AgentClaude Solutions, une entreprise spécialisée dans les agents IA."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Certifications Recommandées — {poste}"
    )
    ajouter_interaction("RH_Formation", "certifications_recommandees", reponse)
    return reponse


def agent_plan_developpement_individuel(nom, ambition_carriere, forces, axes_amelioration):
    """
    Crée un Plan de Développement Individuel (PDI) complet et personnalisé.

    Args:
        nom                 : Prénom et nom du collaborateur
        ambition_carriere   : Vision et objectif de carrière à 3-5 ans
        forces              : Points forts principaux du collaborateur
        axes_amelioration   : Axes de développement identifiés ou souhaités
    """
    incrementer_stat("agent_plan_developpement_individuel")

    agent = creer_agent(f"""Tu es Directeur des Ressources Humaines et Coach de Carrière Senior
chez AgentClaude Solutions. Tu crées des Plans de Développement Individuels (PDI) qui
transforment les ambitions en réalité, en alliant vision long terme et actions concrètes.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu produis un PDI COMPLET, structuré et prêt à être utilisé en entretien annuel :

## 1. VISION DE CARRIÈRE ET ALIGNEMENT STRATÉGIQUE
   - La vision de carrière reformulée et amplifiée
   - Pourquoi cette ambition est réaliste et atteignable
   - Comment cette évolution crée de la valeur pour AgentClaude Solutions
   - Horizon temporel réaliste (1 an, 3 ans, 5 ans)
   - Les étapes jalons de la trajectoire

## 2. FORCES À EXPLOITER COMME LEVIERS
   Pour chaque force identifiée :
   - Comment capitaliser encore plus sur cette force
   - Opportunités concrètes pour l'exprimer davantage
   - Comment cette force contribue à l'atteinte de l'ambition
   - Risques de sur-utilisation à surveiller

## 3. AXES DE DÉVELOPPEMENT PRIORITAIRES
   Pour chaque axe d'amélioration :
   - Diagnostic précis de la situation actuelle
   - Impact sur la carrière si non développé
   - Niveau cible à atteindre et dans quel délai
   - 3 actions concrètes pour progresser sur cet axe
   - Indicateurs de progrès mesurables

## 4. PLAN D'ACTIONS DÉTAILLÉ AVEC CALENDRIER
   ### Court terme (0-3 mois) — Actions immédiates
   - Liste d'actions précises, réalisables rapidement
   - Responsable de chaque action (le collaborateur / le manager / les RH)
   - Ressources nécessaires (temps, budget, accès)

   ### Moyen terme (3-12 mois) — Développement progressif
   - Missions stretch à viser
   - Formations et certifications à planifier
   - Réseau à construire (mentors, sponsors, pairs)

   ### Long terme (12-36 mois) — Vision et transformation
   - Jalons de carrière clés
   - Expériences indispensables à acquérir
   - Positionnement visé (interne et sur le marché)

## 5. MÉTRIQUES DE SUCCÈS
   - 5 à 7 indicateurs clés de progression (KPIs de développement)
   - Fréquence de mesure recommandée
   - Seuils de succès définis objectivement
   - Revue trimestrielle : questions à se poser

## 6. SOUTIEN NÉCESSAIRE
   ### Du Manager
   - Opportunités à créer (projets, visibilité, délégation)
   - Feedback régulier sur les axes de développement
   - Connexions à faciliter dans l'entreprise

   ### D'un Mentor ou Coach
   - Profil du mentor idéal à rechercher
   - Sujets prioritaires à travailler avec le mentor
   - Fréquence recommandée des sessions

## 7. BUDGET ET RESSOURCES
   - Estimation du budget formation nécessaire (vs. budget disponible de 3 000 €/an)
   - Ressources gratuites à exploiter en priorité
   - Investissements à prioriser avec le plus grand ROI

Rédige en français, sur un ton inspirant, structuré et professionnel.""",
        temperature=0.6,
    )

    prompt = (
        f"Collaborateur : {nom}\n"
        f"Ambition de carrière : {ambition_carriere}\n"
        f"Forces identifiées : {forces}\n"
        f"Axes d'amélioration : {axes_amelioration}\n\n"
        f"Crée le Plan de Développement Individuel complet pour {nom}."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Plan de Développement Individuel — {nom}"
    )
    ajouter_interaction("RH_Formation", "plan_developpement_individuel", reponse)
    return reponse


def agent_culture_apprentissage():
    """
    Bâtit une stratégie complète d'organisation apprenante pour l'entreprise.
    Aucun argument requis — génère la stratégie complète pour AgentClaude Solutions.
    """
    incrementer_stat("agent_culture_apprentissage")

    agent = creer_agent(f"""Tu es Chief Learning Officer (CLO) chez AgentClaude Solutions,
reconnu comme expert mondial en organisation apprenante et culture du développement continu.
Tu t'inspires des meilleures pratiques de Google, Netflix, Spotify, Atlassian et Amazon.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Tu conçois une stratégie d'organisation apprenante EXHAUSTIVE et DÉPLOYABLE :

## 1. RITUELS DE PARTAGE DES CONNAISSANCES
   ### Lunch & Learn
   - Format recommandé (durée, fréquence, présentateurs)
   - Processus de sélection des sujets (vote, rotation, thèmes trimestriels)
   - Gestion de la participation (volontariat vs. obligation)
   - Archivage et diffusion des enregistrements

   ### Tech Talks Internes
   - Format (courte démo 15 min vs. conférence approfondie 45 min)
   - Qui peut présenter et comment candidater
   - Lien avec la veille technologique et l'innovation

   ### Clubs de Lecture
   - Comment lancer un club de lecture IA/Tech/Business
   - Fréquence des réunions et format de discussion
   - Liste de 10 livres fondateurs recommandés pour AgentClaude Solutions
   - Comment relier les lectures aux projets en cours

## 2. CULTURE DE LA DOCUMENTATION
   - Principes fondateurs (écrire pour être relu dans 1 an)
   - Ce qui DOIT être documenté (décisions, post-mortems, onboarding, processus)
   - Templates standardisés recommandés (ADR, post-mortem, guide technique)
   - Rituels de mise à jour (documentation comme critère de "Definition of Done")
   - Gamification de la documentation (badges, reconnaissance)

## 3. STRUCTURE DU WIKI INTERNE
   - Architecture de l'information recommandée (arborescence complète)
   - Responsables de sections (ownership clair)
   - Processus de contribution et de review
   - Moteur de recherche et découvrabilité
   - Intégration avec les outils existants (Notion, Confluence, etc.)

## 4. PROCESSUS DE RETOURS D'EXPÉRIENCE (REX / POST-MORTEMS)
   - Quand déclencher un post-mortem (seuils : incidents, projets terminés, échecs)
   - Format du post-mortem blameless (agenda, facilitateur, participants)
   - Template de rapport de post-mortem
   - Comment partager les apprentissages à toute l'entreprise
   - Suivi des actions correctives (ownership, délais, vérification)

## 5. TEMPS D'INNOVATION (20% TIME / HACKATHONS)
   - Politique de temps dédié à l'exploration (format recommandé pour une PME IA)
   - Critères de sélection des projets d'innovation
   - Hackathon interne trimestriel : format, durée, thèmes, prix
   - Comment transformer une idée en projet réel
   - Gestion de la propriété intellectuelle des innovations internes

## 6. POLITIQUE DE CONFÉRENCES ET ÉVÉNEMENTS EXTERNES
   - Budget annuel recommandé par niveau de poste
   - Conférences prioritaires dans le secteur des agents IA (liste)
   - Processus de demande et d'approbation
   - Obligation de restitution post-conférence (format, délai)
   - Comment maximiser le ROI d'une participation à une conférence

## 7. PROGRAMME DE MENTORAT STRUCTURÉ
   - Design du programme (durée, fréquence, format des sessions)
   - Matching mentor/mentoré (algorithme ou critères de sélection)
   - Formation des mentors (compétences et posture du mentor)
   - Contrat de mentorat (objectifs, confidentialité, engagement)
   - Évaluation de l'impact du programme (KPIs, satisfaction)

## 8. FEUILLE DE ROUTE D'IMPLÉMENTATION
   - Mois 1-3 : Quick wins à lancer immédiatement
   - Mois 4-6 : Programmes structurés à déployer
   - Mois 7-12 : Mesure de l'impact et ajustements
   - KPIs de la culture apprenante à suivre dans le temps

Rédige en français, ton visionnaire et pratique, avec des exemples concrets à chaque étape.""",
        temperature=0.65,
    )

    prompt = (
        f"Entreprise : AgentClaude Solutions\n"
        f"Date : {datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"Conçois la stratégie complète d'organisation apprenante pour AgentClaude Solutions, "
        f"une entreprise de 20 à 50 personnes spécialisée dans les agents IA."
    )
    reponse = executer_stream(
        agent, prompt,
        "Stratégie d'Organisation Apprenante — AgentClaude Solutions"
    )
    ajouter_interaction("RH_Formation", "culture_apprentissage", reponse)
    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────────────────────

def menu():
    print("\n" + "═" * 66)
    print("  AGENT FORMATION ÉQUIPE — AgentClaude Solutions")
    print("  Niveau Directeur Learning & Development")
    print("═" * 66)

    while True:
        print("\n  1. Analyser les compétences (skills gap analysis)")
        print("  2. Créer un module de formation complet")
        print("  3. Recommander des certifications professionnelles")
        print("  4. Élaborer un Plan de Développement Individuel (PDI)")
        print("  5. Construire la stratégie d'organisation apprenante")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir !\n")
            break

        elif choix == "1":
            membre = input("  Prénom et nom du collaborateur → ").strip()
            poste_actuel = input("  Poste actuel (ex: Développeur Python Senior) → ").strip()
            evolution = input("  Évolution souhaitée (ex: Lead Technique, Manager IA) → ").strip()
            analyse = agent_evaluer_competences(membre, poste_actuel, evolution)
            nom_fichier = f"gap_analysis_{membre.replace(' ', '_').lower()}.txt"
            sauvegarder_fichier(analyse, nom_fichier)

        elif choix == "2":
            sujet = input("  Sujet de la formation → ").strip()
            niveau = input("  Niveau du public cible (Débutant / Intermédiaire / Avancé) → ").strip()
            duree = input("  Durée totale (ex: 1 jour, 3 heures, 2 semaines) → ").strip()
            formation = agent_creer_formation(sujet, niveau, duree)
            nom_fichier = f"formation_{sujet.replace(' ', '_').lower()}_{niveau.lower()}.txt"
            sauvegarder_fichier(formation, nom_fichier)

        elif choix == "3":
            poste = input("  Intitulé du poste → ").strip()
            certifs = agent_certifications_recommandees(poste)
            nom_fichier = f"certifications_{poste.replace(' ', '_').lower()}.txt"
            sauvegarder_fichier(certifs, nom_fichier)

        elif choix == "4":
            nom = input("  Prénom et nom du collaborateur → ").strip()
            ambition = input("  Ambition de carrière (ex: Devenir CTO d'une startup IA) → ").strip()
            forces = input("  Forces principales (ex: Leadership, Python expert, communication) → ").strip()
            axes = input("  Axes d'amélioration (ex: Prise de parole en public, gestion du stress) → ").strip()
            pdi = agent_plan_developpement_individuel(nom, ambition, forces, axes)
            nom_fichier = f"pdi_{nom.replace(' ', '_').lower()}.txt"
            sauvegarder_fichier(pdi, nom_fichier)

        elif choix == "5":
            print("\n  Génération de la stratégie complète d'organisation apprenante...")
            print("  (Aucune information supplémentaire requise)\n")
            strategie = agent_culture_apprentissage()
            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"strategie_organisation_apprenante_{horodatage}.txt"
            sauvegarder_fichier(strategie, nom_fichier)

        else:
            print("  Choix invalide. Veuillez saisir un numéro entre 0 et 5.")


if __name__ == "__main__":
    menu()
