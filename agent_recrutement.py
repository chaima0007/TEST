"""
AGENT RECRUTEMENT AUTONOME
Gère l'intégralité du processus de recrutement : fiches de poste,
analyse de CV, emails candidats, questions d'entretien et rapports.

Usage : python agent_recrutement.py
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
            max_output_tokens=3000,
        ),
    )


def executer_stream(model, prompt, label):
    """Exécute une requête en streaming et retourne la réponse complète."""
    print(f"\n{'─' * 62}")
    print(f"  ► {label}")
    print(f"{'─' * 62}\n")
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
    """Sauvegarde le contenu dans un fichier texte et affiche la confirmation."""
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  ✅ Rapport sauvegardé → {nom_fichier}")


# ─── AGENTS DE RECRUTEMENT ────────────────────────────────────────────────────

def agent_fiche_poste(titre, competences, niveau):
    """
    Génère une fiche de poste complète et attractive.

    Args:
        titre       : Intitulé du poste (ex: "Ingénieur IA Senior")
        competences : Compétences clés requises (ex: "Python, LLM, RAG")
        niveau      : Niveau d'expérience requis (ex: "Junior", "Senior", "Lead")
    """
    incrementer_stat("agent_fiche_poste")

    agent = creer_agent(f"""Tu es un expert RH spécialisé dans le recrutement tech et IA.
Tu rédiges des fiches de poste engageantes, précises et conformes aux meilleures pratiques RH.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Pour chaque fiche de poste, tu produis obligatoirement les sections suivantes :
1. 🎯 Mission principale (3-4 phrases percutantes)
2. 📋 Responsabilités détaillées (8 à 10 points)
3. ✅ Compétences requises (techniques et comportementales)
4. ➕ Compétences appréciées (nice-to-have)
5. 💰 Fourchette salariale réaliste selon le marché français
6. 🏢 Culture et environnement de travail
7. 🚀 Pourquoi nous rejoindre (3 arguments différenciants)

Le ton est professionnel mais humain, moderne, sans jargon inutile.""",
        temperature=0.6,
    )

    prompt = (
        f"Poste : {titre}\n"
        f"Compétences principales : {competences}\n"
        f"Niveau d'expérience : {niveau}\n\n"
        f"Génère la fiche de poste complète pour AgentClaude Solutions."
    )
    reponse = executer_stream(agent, prompt, f"Fiche de Poste — {titre}")
    ajouter_interaction("RH_Recrutement", "fiche_poste", reponse)
    return reponse


def agent_analyser_cv(cv_texte, poste):
    """
    Analyse un CV par rapport à un poste et produit une évaluation structurée.

    Args:
        cv_texte : Contenu textuel du CV du candidat
        poste    : Intitulé et description du poste ciblé
    """
    incrementer_stat("agent_analyser_cv")

    agent = creer_agent(f"""Tu es un recruteur expert et évaluateur de talents techniques.
Tu analyses les CV avec rigueur, objectivité et bienveillance.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Pour chaque analyse de CV, tu fournis impérativement :
1. 🎯 Score de correspondance global (0-100) avec justification
2. 💪 Points forts du candidat (au moins 4 éléments concrets)
3. ⚠️ Écarts par rapport au poste (compétences manquantes ou insuffisantes)
4. 🚩 Signaux d'alerte éventuels (trous dans le CV, incohérences, etc.)
5. ❓ 5 questions d'entretien spécifiques à poser à ce candidat
6. 📊 Recommandation finale : Entretien / À reconsidérer / Refus

Sois factuel et bienveillant. Base-toi uniquement sur ce qui est écrit dans le CV.""",
        temperature=0.3,
    )

    prompt = (
        f"Poste visé : {poste}\n\n"
        f"CV du candidat :\n{cv_texte}\n\n"
        f"Analyse ce CV pour le poste indiqué chez AgentClaude Solutions."
    )
    reponse = executer_stream(agent, prompt, f"Analyse CV — {poste}")
    ajouter_interaction("RH_Recrutement", "analyse_cv", reponse)
    return reponse


def agent_email_candidat(nom, statut, poste):
    """
    Rédige un email personnalisé pour un candidat selon son statut.

    Args:
        nom    : Prénom du candidat
        statut : Type d'email — "convocation", "refus" ou "offre"
        poste  : Intitulé du poste concerné
    """
    incrementer_stat("agent_email_candidat")

    types_email = {
        "convocation": "convocation à un entretien (date et heure à compléter)",
        "refus": "refus bienveillant en valorisant le candidat",
        "offre": "offre d'emploi formelle avec félicitations",
    }
    description_email = types_email.get(
        statut.lower(),
        f"communication de type '{statut}'"
    )

    agent = creer_agent(f"""Tu es un responsable RH bienveillant et professionnel chez AgentClaude Solutions.
Tu rédiges des emails candidats qui reflètent les valeurs humaines de l'entreprise.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Règles de rédaction :
- Ton chaleureux, professionnel et personnalisé
- Prénom du candidat utilisé dès la première ligne
- Contenu clair et structuré (objet + corps + signature)
- Signature : "L'équipe Recrutement — AgentClaude Solutions"
- Pour la convocation : préciser le format (visio/présentiel), la durée estimée
- Pour le refus : encourager et laisser la porte ouverte pour de futurs postes
- Pour l'offre : féliciter chaleureusement et indiquer les prochaines étapes""",
        temperature=0.7,
    )

    prompt = (
        f"Candidat : {nom}\n"
        f"Poste : {poste}\n"
        f"Type d'email à rédiger : {description_email}\n\n"
        f"Rédige l'email complet avec l'objet et le corps du message."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Email Candidat — {nom} ({statut.capitalize()})"
    )
    ajouter_interaction("RH_Recrutement", f"email_{statut}", reponse)
    return reponse


def agent_questions_entretien(poste, profil):
    """
    Génère 10 questions techniques + 5 comportementales pour un entretien.

    Args:
        poste  : Intitulé et description du poste
        profil : Description du profil recherché / niveau d'expérience
    """
    incrementer_stat("agent_questions_entretien")

    agent = creer_agent(f"""Tu es un expert en recrutement technique spécialisé dans l'IA et le développement logiciel.
Tu conçois des entretiens rigoureux, pertinents et respectueux des candidats.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire de ta réponse :

## QUESTIONS TECHNIQUES (10 questions)
Pour chaque question :
- La question précise
- Critères de réponse attendue (ce qu'un bon candidat doit mentionner)
- Niveau de difficulté : Facile / Intermédiaire / Avancé

## QUESTIONS COMPORTEMENTALES (5 questions)
Pour chaque question :
- La question (format STAR recommandé)
- Comportements positifs à détecter
- Signaux d'alerte à surveiller

Les questions doivent être adaptées au niveau du profil et au contexte d'AgentClaude Solutions.""",
        temperature=0.4,
    )

    prompt = (
        f"Poste : {poste}\n"
        f"Profil recherché : {profil}\n\n"
        f"Génère le guide d'entretien complet (10 questions techniques + 5 comportementales)."
    )
    reponse = executer_stream(
        agent, prompt,
        f"Guide d'Entretien — {poste}"
    )
    ajouter_interaction("RH_Recrutement", "questions_entretien", reponse)
    return reponse


def agent_rapport_recrutement(candidats):
    """
    Génère un rapport complet de campagne de recrutement.

    Args:
        candidats : Liste de dicts avec les clés :
                    nom, poste, score (0-100), statut, notes (optionnel)
    """
    incrementer_stat("agent_rapport_recrutement")

    # Calcul des statistiques du funnel
    total = len(candidats)
    retenus = [c for c in candidats if c.get("score", 0) >= 70]
    a_reconsiderer = [c for c in candidats if 40 <= c.get("score", 0) < 70]
    refuses = [c for c in candidats if c.get("score", 0) < 40]

    # Classement par score décroissant
    classement = sorted(candidats, key=lambda c: c.get("score", 0), reverse=True)

    stats_json = json.dumps(
        {
            "total_candidats": total,
            "retenus_entretien": len(retenus),
            "a_reconsiderer": len(a_reconsiderer),
            "refuses": len(refuses),
            "taux_conversion": f"{round(len(retenus) / total * 100, 1) if total else 0}%",
            "classement_top5": [
                {"nom": c["nom"], "poste": c["poste"], "score": c.get("score", 0)}
                for c in classement[:5]
            ],
        },
        ensure_ascii=False,
        indent=2,
    )

    details_candidats = "\n".join(
        f"- {c['nom']} | Poste : {c['poste']} | Score : {c.get('score', 'N/A')}/100 "
        f"| Statut : {c.get('statut', 'N/A')} | Notes : {c.get('notes', 'aucune')}"
        for c in classement
    )

    agent = creer_agent(f"""Tu es un Directeur des Ressources Humaines senior chez AgentClaude Solutions.
Tu rédiges des rapports de recrutement complets, analytiques et actionnables.

Profil de l'entreprise :
{ENTREPRISE_PROFIL}

Structure obligatoire du rapport :

# RAPPORT DE CAMPAGNE DE RECRUTEMENT
Date : {datetime.now().strftime('%d/%m/%Y')}

## 1. Résumé Exécutif
## 2. Analyse du Funnel de Recrutement (avec commentaire sur les taux)
## 3. Classement et Présentation des Top Candidats
## 4. Recommandation d'Embauche (1 ou 2 candidats maximum, avec justification)
## 5. Points d'Amélioration pour la Prochaine Campagne
## 6. Prochaines Étapes Recommandées

Le rapport doit être précis, professionnel et directement utilisable par la direction.""",
        temperature=0.3,
    )

    prompt = (
        f"Statistiques de la campagne :\n{stats_json}\n\n"
        f"Détail des candidats :\n{details_candidats}\n\n"
        f"Génère le rapport de recrutement complet."
    )
    reponse = executer_stream(agent, prompt, "Rapport de Campagne de Recrutement")
    ajouter_interaction("RH_Recrutement", "rapport_recrutement", reponse)
    return reponse


# ─── MENU PRINCIPAL ───────────────────────────────────────────────────────────

def menu():
    print("\n" + "═" * 62)
    print("  AGENT RECRUTEMENT AUTONOME — AgentClaude Solutions")
    print("═" * 62)

    while True:
        print("\n  1. Générer une fiche de poste")
        print("  2. Analyser un CV candidat")
        print("  3. Rédiger un email candidat")
        print("  4. Créer un guide d'entretien")
        print("  5. Générer un rapport de campagne")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  Au revoir !\n")
            break

        elif choix == "1":
            titre = input("  Intitulé du poste → ").strip()
            competences = input("  Compétences clés (ex: Python, LLM, API) → ").strip()
            niveau = input("  Niveau requis (Junior / Confirmé / Senior / Lead) → ").strip()
            fiche = agent_fiche_poste(titre, competences, niveau)
            nom_fichier = f"fiche_poste_{titre.replace(' ', '_')}.txt"
            sauvegarder_fichier(fiche, nom_fichier)

        elif choix == "2":
            print("  Collez le texte du CV (terminez par une ligne contenant uniquement 'FIN') :")
            lignes = []
            while True:
                ligne = input()
                if ligne.strip().upper() == "FIN":
                    break
                lignes.append(ligne)
            cv_texte = "\n".join(lignes)
            poste = input("  Poste ciblé → ").strip()
            agent_analyser_cv(cv_texte, poste)

        elif choix == "3":
            nom = input("  Prénom du candidat → ").strip()
            poste = input("  Poste concerné → ").strip()
            print("  Type d'email :")
            print("    a. Convocation à entretien")
            print("    b. Refus bienveillant")
            print("    c. Offre d'emploi")
            type_choix = input("  Choix (a/b/c) → ").strip().lower()
            mapping = {"a": "convocation", "b": "refus", "c": "offre"}
            statut = mapping.get(type_choix, "convocation")
            agent_email_candidat(nom, statut, poste)

        elif choix == "4":
            poste = input("  Poste → ").strip()
            profil = input("  Profil recherché (ex: Senior 5 ans exp., autonome) → ").strip()
            guide = agent_questions_entretien(poste, profil)
            nom_fichier = f"guide_entretien_{poste.replace(' ', '_')}.txt"
            sauvegarder_fichier(guide, nom_fichier)

        elif choix == "5":
            print("  Saisie des candidats (entrez 'FIN' comme nom pour terminer)")
            candidats = []
            while True:
                nom = input(f"\n  Candidat {len(candidats) + 1} — Nom → ").strip()
                if nom.upper() == "FIN":
                    break
                poste = input("  Poste → ").strip()
                score_str = input("  Score (0-100) → ").strip()
                try:
                    score = int(score_str)
                except ValueError:
                    score = 0
                statut = input("  Statut (retenu / refusé / en attente) → ").strip()
                notes = input("  Notes (optionnel, appuyez sur Entrée pour passer) → ").strip()
                candidats.append({
                    "nom": nom,
                    "poste": poste,
                    "score": score,
                    "statut": statut,
                    "notes": notes,
                })

            if not candidats:
                print("  Aucun candidat saisi.")
                continue

            rapport = agent_rapport_recrutement(candidats)
            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"rapport_recrutement_{horodatage}.txt"
            sauvegarder_fichier(rapport, nom_fichier)

        else:
            print("  Choix invalide. Veuillez saisir un numéro entre 0 et 5.")


if __name__ == "__main__":
    menu()
