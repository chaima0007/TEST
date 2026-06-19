"""
AGENT MARQUE — Expert branding et positionnement pour Caelum Partners
Identité de marque · Positionnement · Différenciation · Storytelling

Usage : python agent_marque.py
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

IDENTITE = """Tu es un expert en branding et stratégie de marque avec 20 ans d'expérience.
Tu as créé les identités de marque de startups tech devenues leaders européens.

CONTEXTE CAELUM PARTNERS :
- Nom : Caelum Partners (Caelum = "ciel" en latin)
- Fondatrice : Chaima Mhadbi, femme entrepreneuse, Bruxelles
- Secteur : IA et automatisation pour PME
- Valeurs fondamentales (à affiner) : ambition, protection, rigueur, innovation
- Différenciateur clé : 25+ agents IA spécialisés, livrés en 7 jours, prix accessibles
- Vision : devenir la référence européenne en IA pour PME
- Cible : dirigeants de PME, startups, indépendants — Belgique + Europe

PHILOSOPHIE BRANDING QUE TU APPLIQUES :
1. Une marque forte se construit sur UNE promesse claire (pas 10)
2. Le storytelling du fondateur EST la marque au stade startup
3. La différenciation n'est pas dans les features mais dans la façon de parler
4. L'identité visuelle amplifie le message — elle ne le remplace pas
5. La cohérence sur tous les canaux vaut plus que la perfection sur un seul"""


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
                max_output_tokens=2500,
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
    os.makedirs("fichiers/marque", exist_ok=True)
    fichier = f"fichiers/marque/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def identite_de_marque():
    r = streamer(
        """Crée l'identité de marque complète de Caelum Partners.
Inclure :
1. POSITIONNEMENT — En 1 phrase : "Caelum Partners est [quoi] pour [qui] qui [douleur]"
2. PROMESSE DE MARQUE — Ce qu'on promet et qu'on tient toujours
3. PERSONNALITÉ — Si Caelum Partners était une personne, comment serait-elle ? (5 adjectifs)
4. VOIX DE MARQUE — Comment Caelum parle (exemples de tournures à utiliser / à éviter)
5. VALEURS FONDAMENTALES — 3 valeurs avec leur signification concrète
6. TAGLINE — 3 propositions de slogan percutant
7. DIFFÉRENCIATION — Ce que personne d'autre ne peut dire avec autant de crédibilité""",
        "IDENTITÉ DE MARQUE — Caelum Partners complète"
    )
    sauvegarder("identite_marque", r)


def storytelling_fondatrice():
    r = streamer(
        """Crée le storytelling de Chaima Mhadbi — fondatrice de Caelum Partners.
Format : histoire en 3 actes (classique mais efficace)
Acte 1 — L'avant : qui était Chaima avant Caelum ? Quelle frustration ou vision ?
Acte 2 — Le déclic : qu'est-ce qui l'a poussée à créer Caelum Partners ?
Acte 3 — La mission : pourquoi elle fait ça et où elle veut emmener l'entreprise ?

Donner 3 versions :
- Version LinkedIn (150 mots, pour un post)
- Version "About" site web (250 mots)
- Version pitch oral (60 secondes, script exact)

Note : adapter en fonction de ce qu'on sait de Chaima — femme, Bruxelles, ASBL, IA""",
        "STORYTELLING FONDATRICE — L'histoire de Chaima"
    )
    sauvegarder("storytelling_fondatrice", r)


def messages_cles_par_cible():
    r = streamer(
        """Caelum Partners vend à des profils très différents.
Crée les messages clés adaptés à chaque cible :

CIBLE 1 — Dirigeant PME (10-50 employés), non-tech, veut gagner du temps
CIBLE 2 — Startup founder (5 employés), tech-friendly, budget serré
CIBLE 3 — Indépendant/freelancer, travaille seul, veut scaler sans recruter
CIBLE 4 — Responsable marketing PME, veut des résultats LinkedIn/SEO

Pour chaque cible :
- Leur douleur principale en leurs mots
- Ce qu'ils veulent vraiment (pas ce qu'on pense)
- L'argument Caelum qui les convainc le plus
- Les mots à utiliser / à éviter
- Un exemple de message LinkedIn d'accroche""",
        "MESSAGES CLÉS PAR CIBLE — Parler leur langue"
    )
    sauvegarder("messages_cles", r)


def audit_identite_visuelle():
    r = streamer(
        """Recommandations pour l'identité visuelle de Caelum Partners.
Sans voir le logo actuel, donner les principes directeurs :
1. PALETTE DE COULEURS — couleurs recommandées pour une agence IA premium belge
   (avec codes hex et justification psychologique de chaque couleur)
2. TYPOGRAPHIE — polices recommandées (titre / corps / accent)
3. STYLE VISUEL — moderne/minimaliste/tech/humain ? Comment combiner ?
4. LOGO — principes directeurs (formes, symboles à éviter/favoriser)
5. TEMPLATES — comment créer une cohérence sur LinkedIn / site / propositions
6. CE QU'IL FAUT ABSOLUMENT ÉVITER (clichés de l'IA : robots, cerveaux, circuits imprimés)""",
        "IDENTITÉ VISUELLE — Guidelines pour Caelum Partners"
    )
    sauvegarder("identite_visuelle", r)


def contenu_marque_linkedin():
    r = streamer(
        """Crée un guide de contenu LinkedIn pour bâtir la marque Caelum Partners.
Chaima doit poster 3-5 fois par semaine.
Inclure :
1. LES 5 PILIERS DE CONTENU — thèmes récurrents qui bâtissent l'autorité
2. FORMATS QUI FONCTIONNENT — carrousels, posts texte, vidéos, articles
3. 10 IDÉES DE POSTS prêts à rédiger (avec accroches)
4. LE FORMAT PARFAIT D'UN POST LINKEDIN (accroche / corps / CTA)
5. LES HASHTAGS À UTILISER systématiquement
6. LA FRÉQUENCE et le meilleur moment pour poster en Belgique
7. COMMENT RÉPONDRE AUX COMMENTAIRES pour maximiser la portée""",
        "CONTENU LINKEDIN — Bâtir la marque Caelum Partners"
    )
    sauvegarder("contenu_linkedin", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT MARQUE — Branding et positionnement Caelum Partners")
    print("  Identité · Storytelling · Messages · LinkedIn")
    print("═"*65)

    while True:
        print("\n  1. Identité de marque complète")
        print("  2. Storytelling de Chaima — 3 versions")
        print("  3. Messages clés par cible client")
        print("  4. Audit et recommandations identité visuelle")
        print("  5. Guide contenu LinkedIn — bâtir la marque")
        print("  7. Question libre sur le branding")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            identite_de_marque()
        elif choix == "2":
            storytelling_fondatrice()
        elif choix == "3":
            messages_cles_par_cible()
        elif choix == "4":
            audit_identite_visuelle()
        elif choix == "5":
            contenu_marque_linkedin()
        elif choix == "7":
            q = input("\n  Ta question → ").strip()
            if q:
                streamer(q, "QUESTION MARQUE")
        else:
            print("  Choix invalide.")
