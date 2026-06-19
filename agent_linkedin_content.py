"""
AGENT LINKEDIN CONTENT [80] — Contenu LinkedIn Authority & Prospection
Calendrier de posts, articles d'expertise, séquences d'autorité pour Chaima/Caelum.

Usage : python agent_linkedin_content.py
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

IDENTITE = """# AGENT LINKEDIN CONTENT — Caelum Partners

## IDENTITÉ
Tu es l'expert contenu LinkedIn de Chaima Mhadbi, fondatrice de Caelum Partners.
Tu crées des posts qui construisent l'autorité, génèrent des leads et rendent Chaima incontournable sur LinkedIn Belgique.

## PROFIL CHAIMA
- Fondatrice Caelum Partners — automation IA pour PME belges
- Basée à Bruxelles, marché cible : dirigeants de PME belges
- Expertise : déploiement IA opérationnel rapide, conforme, rentable
- Ton personnel : direct, humain, expert — jamais corporate

## STRATÉGIE LINKEDIN (3 types de posts en rotation)
1. EXPERTISE (40%) : insight IA, erreur commune, conseil actionnable → établit l'autorité
2. PREUVE (30%) : avant/après, résultat client, cas concret → crée la confiance
3. PROSPECTION DOUCE (30%) : question au réseau, sondage, "qui connaît un X qui..." → génère leads

## RÈGLES RÉDACTION
- Hook sur les 2 premières lignes (doit arrêter le scroll)
- Paragraphes courts : 1-2 lignes max
- Emojis sparingly : 1-2 par post, pas de liste avec 10 emojis
- CTA final : toujours une action facile (commentaire, DM, lien)
- Longueur : 150-300 mots (pas de romans)
- Hashtags : 3-5 max, en français, ciblés (#IA #PMEBelge #AutomatisationIA)
- JAMAIS commencer par "Je" (algo LinkedIn pénalise)"""


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
                max_output_tokens=3000,
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
    os.makedirs("fichiers/linkedin", exist_ok=True)
    fichier = f"fichiers/linkedin/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def post_expertise():
    print("\n  Sujet du post (ex: 'les PME perdent 8h/semaine en tâches répétitives') :")
    sujet = input("  Sujet → ").strip()
    if not sujet:
        return
    r = streamer(
        f"""Écris un post LinkedIn d'EXPERTISE pour Chaima Mhadbi sur : {sujet}

Structure :
- Hook choc (stat, question provocante, ou affirmation contre-intuitive)
- Développement en 3-4 points courts
- Leçon / conseil actionnable
- CTA doux (question aux abonnés ou "DM moi si tu veux en savoir plus")
- 3-4 hashtags ciblés

Ton : expert mais accessible, pas arrogant.""",
        f"POST EXPERTISE — {sujet[:40]}"
    )
    sauvegarder(f"post_expertise_{sujet[:20].replace(' ', '_')}", r)


def calendrier_semaine():
    print("\n  Secteur prioritaire cette semaine (ex: HORECA, avocats, PME tech) :")
    secteur = input("  Secteur → ").strip() or "PME belges"
    r = streamer(
        f"""Crée un CALENDRIER LINKEDIN pour 1 semaine ciblant : {secteur}

Format pour chaque jour (Lundi → Vendredi) :
JOUR X — [Type : Expertise/Preuve/Prospection]
Titre/Hook : ...
Corps : ...
CTA : ...
Hashtags : ...

5 posts complets, prêts à copier-coller.
Variation des formats : texte court, liste, storytelling, question.""",
        f"CALENDRIER LINKEDIN — {secteur}"
    )
    sauvegarder(f"calendrier_{secteur.replace(' ', '_')}", r)


def message_prospection():
    print("\n  Profil du prospect (ex: directeur cabinet comptable 15 personnes) :")
    profil = input("  Profil → ").strip()
    if not profil:
        return
    r = streamer(
        f"""Écris 3 variantes de MESSAGE DE CONNEXION LinkedIn pour contacter : {profil}

Règles :
- Max 300 caractères (limite LinkedIn)
- Personalisation visible (pas de copier-coller générique)
- Pas de pitch direct — créer la curiosité
- Propose une valeur immédiate (insight, question pertinente)
- Pas de "j'aimerais vous avoir dans mon réseau"

Format : Message 1 / Message 2 / Message 3 — avec explication de l'approche.""",
        f"MESSAGES CONNEXION — {profil[:40]}"
    )
    sauvegarder(f"msg_connexion_{profil[:20].replace(' ', '_')}", r)


def post_temoignage():
    print("\n  Décris le résultat obtenu pour un client (même fictif/simulé) :")
    resultat = input("  Résultat → ").strip()
    secteur = input("  Secteur client → ").strip() or "PME"
    if not resultat:
        return
    r = streamer(
        f"""Transforme ce résultat client en post LinkedIn PREUVE SOCIALE :
Résultat : {resultat}
Secteur : {secteur}

Structure narrative :
- Situation initiale (le problème, la douleur)
- Ce qu'on a fait (solution en 1-2 phrases)
- Résultat chiffré (temps, argent, erreurs)
- Leçon universelle pour les autres PME
- CTA : "Tu vis la même situation ? DM moi."

Humaniser sans nommer le client (anonymiser si besoin).""",
        f"POST TÉMOIGNAGE — {secteur}"
    )
    sauvegarder(f"post_temoignage_{secteur.replace(' ', '_')}", r)


def profil_linkedin():
    r = streamer(
        """Optimise le PROFIL LINKEDIN de Chaima Mhadbi, fondatrice Caelum Partners.

Génère :
1. TITRE OPTIMISÉ (220 caractères max) — percutant, avec mots-clés recherchés
2. RÉSUMÉ "À PROPOS" (2600 caractères max) — histoire + expertise + CTA
3. HEADLINE banner text (pour image de couverture)
4. 5 COMPÉTENCES à mettre en avant (pour apparaître dans les recherches)
5. URL personnalisée suggérée

Mots-clés cibles : automation IA, PME Belgique, intelligence artificielle, Bruxelles""",
        "OPTIMISATION PROFIL LINKEDIN"
    )
    sauvegarder("profil_linkedin_optimise", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  LINKEDIN CONTENT — Caelum Partners")
    print("  Posts autorité · Prospection · Calendrier éditorial")
    print("═"*65)

    while True:
        print("\n  1. Post d'expertise (insight IA)")
        print("  2. Calendrier 1 semaine complet")
        print("  3. Messages de connexion prospect")
        print("  4. Post témoignage / preuve sociale")
        print("  5. Optimiser le profil LinkedIn")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            post_expertise()
        elif choix == "2":
            calendrier_semaine()
        elif choix == "3":
            message_prospection()
        elif choix == "4":
            post_temoignage()
        elif choix == "5":
            profil_linkedin()
        else:
            print("  Choix invalide.")
