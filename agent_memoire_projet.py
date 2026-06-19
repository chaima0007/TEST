"""
AGENT MÉMOIRE DU PROJET — Rappel complet de tout ce qu'on a construit ensemble
Éviter la répétition · Contexte permanent · Directives mémorisées
Mission : Chaima ne répète jamais deux fois la même directive

Usage : python agent_memoire_projet.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

CONTEXTE_FILE = "CONTEXTE_CAELUM.md"


def charger_contexte() -> str:
    if os.path.exists(CONTEXTE_FILE):
        with open(CONTEXTE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "Fichier CONTEXTE_CAELUM.md introuvable."


CONTEXTE = charger_contexte()

IDENTITE = f"""# AGENT MÉMOIRE DU PROJET CAELUM PARTNERS

## IDENTITÉ
Tu es la Mémoire du Projet de Caelum Partners.
Tu contiens tout ce qui a été construit, décidé et configuré.
Quand Chaima pose une question sur ce qu'on a fait, tu réponds avec précision.
Quand elle donne une nouvelle directive, tu la mémorises et l'intègres.

## TA BASE DE CONNAISSANCE COMPLÈTE
{CONTEXTE}

## MISSION
1. Répondre à toute question sur ce qui a été fait ("est-ce qu'on a déjà un agent pour X ?")
2. Rappeler les directives permanentes quand elles sont pertinentes
3. Éviter que Chaima répète deux fois la même instruction
4. Synthétiser rapidement l'état du projet pour reprendre une session

## DIRECTIVE DE COMPORTEMENT
- Réponses courtes et précises (pas de blabla)
- Si l'agent existe : donner son numéro + nom de fichier exact
- Si quelque chose n'est pas encore fait : le dire clairement + suggérer quel agent créer
- Rappeler les contraintes légales belges si pertinent (ONEM, ASBL, TVA)"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE,
                temperature=0.1,
                max_output_tokens=2000,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/memoire_projet", exist_ok=True)
    fichier = f"fichiers/memoire_projet/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def poser_question():
    """Pose une question sur ce qui a été fait."""
    print("\n  Ta question sur le projet (ex: 'est-ce qu'on a un agent pour les avocats ?')\n")
    question = input("  Question → ").strip()[:500]
    if not question:
        return
    streamer(
        f"Question de Chaima : {question}\n\nRéponds précisément en te basant sur la mémoire du projet.",
        f"MÉMOIRE — {question[:50]}"
    )


def resume_complet():
    """Affiche un résumé complet de tout ce qui a été construit."""
    streamer(
        """Génère un résumé exécutif complet de tout ce qui a été construit pour Caelum Partners.

FORMAT :
1. QUI EST CHAIMA (contexte en 3 lignes)
2. ÉTAT ACTUEL DE LA FLOTTE (combien d'agents, quels blocs)
3. DIRECTIVES PERMANENTES (les règles à toujours respecter)
4. CE QUI EST PRÊT À UTILISER MAINTENANT
5. CE QUI RESTE À FAIRE (priorité : premier client)

Réponse courte, dense, actionnable.""",
        "RÉSUMÉ COMPLET DU PROJET CAELUM"
    )


def chercher_agent():
    """Cherche si un agent pour un besoin spécifique existe déjà."""
    print("\n  Pour quel besoin cherches-tu un agent ?\n")
    besoin = input("  Besoin → ").strip()[:300]
    if not besoin:
        return
    streamer(
        f"""Chaima cherche un agent pour : {besoin}

Vérifie dans la mémoire du projet :
1. Est-ce qu'un agent qui couvre ce besoin existe déjà ? Si oui : numéro + fichier exact
2. Quel agent est le plus proche si pas de correspondance exacte ?
3. Si rien n'existe : suggérer comment créer cet agent (en une phrase)""",
        f"RECHERCHE AGENT — {besoin[:40]}"
    )


def rappel_directives():
    """Rappelle toutes les directives permanentes."""
    streamer(
        """Liste toutes les directives permanentes du projet Caelum Partners.
Ce sont les règles que Claude doit toujours respecter quand il crée de nouveaux agents.

Format : liste numérotée, une directive par ligne, courte et précise.""",
        "DIRECTIVES PERMANENTES — À respecter toujours"
    )


def ajouter_directive():
    """Ajoute une nouvelle directive permanente dans CONTEXTE_CAELUM.md."""
    print("\n  Nouvelle directive à mémoriser :\n")
    directive = input("  Directive → ").strip()[:500]
    if not directive:
        return

    with open(CONTEXTE_FILE, "r", encoding="utf-8") as f:
        contenu = f.read()

    nouvelle_ligne = f"\n{len([l for l in contenu.split('\\n') if l.startswith('8. ') or l.startswith('9. ')])+8}. **{directive}**"
    contenu_mis_a_jour = contenu.replace(
        "## DIRECTIVES PERMANENTES",
        f"## DIRECTIVES PERMANENTES\n{len(contenu.split('---')[0])}. **AJOUTÉ LE {datetime.now().strftime('%d/%m/%Y')}** : {directive}\n"
    )

    with open(CONTEXTE_FILE, "w", encoding="utf-8") as f:
        f.write(contenu_mis_a_jour)

    print(f"  ✅ Directive mémorisée dans {CONTEXTE_FILE}")
    print(f"  → Fais un 'git add {CONTEXTE_FILE} && git commit' pour la sauvegarder définitivement")


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  MÉMOIRE DU PROJET — Caelum Partners")
    print(f"  {len([l for l in CONTEXTE.split(chr(10)) if l.startswith('|') and 'agent' in l.lower()])} agents en mémoire · Directives · Contexte complet")
    print("═"*65)

    while True:
        print("\n  1. Poser une question sur ce qui a été fait")
        print("  2. Résumé complet du projet (reprendre une session)")
        print("  3. Chercher si un agent pour un besoin existe déjà")
        print("  4. Rappel des directives permanentes")
        print("  5. Ajouter une nouvelle directive à mémoriser")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            poser_question()
        elif choix == "2":
            resume_complet()
        elif choix == "3":
            chercher_agent()
        elif choix == "4":
            rappel_directives()
        elif choix == "5":
            ajouter_directive()
        else:
            print("  Choix invalide.")
