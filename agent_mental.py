"""
AGENT MENTAL — Coach entrepreneurial et gestion des blocages psychologiques
Syndrome de l'imposteur · Peur d'échouer · Motivation · Résilience fondatrice

Usage : python agent_mental.py
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

IDENTITE = """Tu es un coach entrepreneurial et psychologue du travail spécialisé dans l'accompagnement de fondateurs de startups.
Tu as coaché 500+ entrepreneurs, dont beaucoup de femmes fondatrices en tech.

CONTEXTE CHAIMA :
- Fondatrice de Caelum Partners, Bruxelles
- Phase de lancement — 0 clients encore
- Présidente d'une ASBL en parallèle
- Secteur IA et tech (parfois intimidant)
- Objectif : premier client à 500€ dès que possible

LES BLOCAGES QUE TU AIDES À SURMONTER :
1. Syndrome de l'imposteur ("je ne suis pas légitime")
2. Peur du rejet / de prospecter ("et s'ils disent non ?")
3. Perfectionnisme paralysant ("c'est pas encore parfait")
4. Surcharge mentale ("je sais pas par où commencer")
5. Doute sur les prix ("c'est trop cher pour ce que je fais ?")
6. Comparaison aux autres ("les autres avancent plus vite")
7. Fatigue du fondateur / burnout précoce

TON APPROCHE :
- Empathique mais pas complaisant
- Toujours ramener à l'action concrète — pas juste du soutien
- Outils pratiques : journaling, routines, techniques de vente émotionnelle
- Rappel constant : le doute est normal, l'action guérit le doute
- Pas de psychologie de comptoir — conseils basés sur des méthodes éprouvées"""


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
                temperature=0.4,
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
    os.makedirs("fichiers/mental", exist_ok=True)
    fichier = f"fichiers/mental/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def debloquer_imposteur():
    r = streamer(
        """Chaima a parfois le syndrome de l'imposteur sur Caelum Partners.
Elle se demande si elle est "assez légitime" pour vendre des services IA à des PME.
Aide-la à :
1. Comprendre pourquoi le syndrome de l'imposteur est particulièrement fort chez les femmes tech
2. Identifier ses vraies compétences (ce qu'elle sait faire mieux que 95% des gens)
3. Recadrer la légitimité : tu n'as pas besoin d'être experte de tout, tu dois résoudre un problème
4. Un exercice pratique à faire maintenant pour reprendre confiance
5. La phrase à se répéter quand le doute revient
6. Pourquoi le premier client guérit plus l'imposteur que 100 séances de coaching""",
        "SYNDROME DE L'IMPOSTEUR — Débloquer la confiance"
    )
    sauvegarder("imposteur", r)


def routine_fondatrice():
    r = streamer(
        """Crée la routine quotidienne optimale pour Chaima en phase de lancement.
Elle doit prospecter, construire, gérer l'ASBL et garder de l'énergie.
Concevoir une routine réaliste (pas une routine de guru Instagram) :
- Matin (avant 9h) : routine mentale + priorité du jour
- Journée : blocs de travail (prospection / construction / admin)
- Soir : débrief et déconnexion
- Hebdomadaire : revue des métriques + rechargement
Inclure : techniques anti-procrastination, gestion de l'énergie, règles non-négociables.""",
        "ROUTINE FONDATRICE — Journée optimale en phase lancement"
    )
    sauvegarder("routine_fondatrice", r)


def gerer_le_refus():
    r = streamer(
        """Chaima va prospecter et va recevoir des refus. C'est inévitable.
Prépare-la mentalement et pratiquement :
1. La vérité sur les taux de conversion en B2B (combien de refus pour 1 oui ?)
2. Pourquoi un refus n'est PAS un rejet personnel
3. Les 5 types de refus et ce qu'ils signalent vraiment
4. Comment analyser un refus pour s'améliorer (sans ruminer)
5. La règle des 100 refus (pourquoi chercher les refus accélère le succès)
6. Ce qu'il faut se dire immédiatement après un refus
7. Comment rebondir en moins de 5 minutes et reprendre la prospection""",
        "GÉRER LE REFUS — Mental de fer pour prospecter"
    )
    sauvegarder("gerer_refus", r)


def session_coaching(sujet: str):
    streamer(
        f"""Chaima a besoin de coaching sur ce sujet : {sujet}
Réponds comme un coach bienveillant mais direct.
Structure : écoute → recadrage → outil pratique → action immédiate.""",
        f"SESSION COACHING — {sujet[:40]}"
    )


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT MENTAL — Coach entrepreneurial Caelum Partners")
    print("  Confiance · Résilience · Routine · Blocages")
    print("═"*65)

    while True:
        print("\n  1. Syndrome de l'imposteur — débloquer la confiance")
        print("  2. Routine quotidienne optimale pour fondatrice")
        print("  3. Gérer les refus — mental de fer")
        print("  4. Session coaching libre — parle de ce qui te bloque")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            debloquer_imposteur()
        elif choix == "2":
            routine_fondatrice()
        elif choix == "3":
            gerer_le_refus()
        elif choix == "4":
            sujet = input("\n  Ce qui te bloque en ce moment → ").strip()
            if sujet:
                session_coaching(sujet)
        else:
            print("  Choix invalide.")
