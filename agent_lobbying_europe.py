"""
AGENT LOBBYING & AFFAIRES PUBLIQUES EUROPE [94]
Influence et anticipation réglementaire à Bruxelles et capitales européennes.
Assure que la législation favorise ou protège les intérêts de Caelum Partners.

Usage : python agent_lobbying_europe.py
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

IDENTITE = """# AGENT LOBBYING & AFFAIRES PUBLIQUES EUROPE — Caelum Partners

## IDENTITÉ
Tu es l'expert en affaires publiques et stratégie réglementaire de Caelum Partners.
Tu surveilles les évolutions législatives européennes sur l'IA, la data et le numérique.
Tu identifies les opportunités de subventions, les risques réglementaires et les alliances stratégiques.

## RADAR RÉGLEMENTAIRE ACTUEL
- AI Act (EU) : entré en vigueur 2024, déploiement progressif jusqu'à 2026-2027
- RGPD / ePrivacy : en évolution constante, spécificités belges APD
- Digital Markets Act (DMA) : obligations plateformes systémiques
- Digital Services Act (DSA) : modération contenu, responsabilité
- Cyber Resilience Act : sécurité produits IA et logiciels
- Directive NIS2 : sécurité réseaux et systèmes d'information

## OPPORTUNITÉS RÉGLEMENTAIRES (AVANTAGES CAELUM)
- AI Act : PME bénéficient d'exemptions et de délais — avantage compétitif vs grandes entreprises
- Subventions EU : Horizon Europe, Digital Europe Programme
- Label "IA de confiance" : certification différenciante sur le marché belge/européen
- RGPD compliance = argument de vente premium face aux concurrents non-conformes

## ACTEURS CLÉS À SURVEILLER
- Parlement européen : Comité ITRE (IA) et LIBE (données)
- Commission européenne : DG CONNECT, DG CNECT
- SPF Économie Belge : transposition des directives EU
- Hub Brussels : guichet entreprises et innovation Bruxelles
- Innoviris : fonds R&D innovation Bruxelles"""


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
                temperature=0.15,
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
    os.makedirs("fichiers/lobbying", exist_ok=True)
    fichier = f"fichiers/lobbying/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def analyse_ai_act():
    r = streamer(
        """ANALYSE AI ACT — IMPACT CAELUM PARTNERS

Analyse complète de l'AI Act européen pour Caelum Partners (PME prestataire IA Belgique) :

1. CLASSIFICATION DES SYSTÈMES IA DE CAELUM
   - Quels systèmes IA développés pour clients sont à haut risque / faible risque ?
   - Exemptions applicables aux PME

2. OBLIGATIONS SPÉCIFIQUES
   - Documentation technique requise
   - Transparence envers les utilisateurs
   - Enregistrement dans la base de données EU

3. CALENDRIER D'APPLICATION
   - Quelles règles s'appliquent maintenant vs dans 12/24 mois ?

4. AVANTAGES COMPÉTITIFS
   - Comment la conformité AI Act devient un argument de vente ?
   - Label "IA de confiance" : comment l'obtenir ?

5. RISQUES ET SANCTIONS
   - Amendes potentielles si non-conformité
   - Comment se protéger

6. PLAN D'ACTION CAELUM (90 jours)""",
        "ANALYSE AI ACT — CAELUM PARTNERS"
    )
    sauvegarder("analyse_ai_act", r)


def veille_reglementaire():
    print("\n  Domaine réglementaire à surveiller (ex: IA, données, cybersécurité, TVA numérique) :")
    domaine = input("  Domaine → ").strip() or "IA et données"
    r = streamer(
        f"""VEILLE RÉGLEMENTAIRE — {domaine.upper()}

Analyse l'état actuel et les évolutions prévues concernant : {domaine}

Pour Caelum Partners (PME IA belge) :
1. TEXTES EN VIGUEUR : quelles règles s'appliquent aujourd'hui ?
2. EN COURS D'ADOPTION : textes européens ou belges en discussion
3. IMPACT SUR CAELUM : risques et opportunités pour nos services
4. CALENDRIER : quand agir et sur quoi ?
5. SUBVENTIONS LIÉES : existe-t-il des aides pour accompagner la mise en conformité ?
6. PARTENAIRES INSTITUTIONNELS à contacter (agences, ministères, hubs)""",
        f"VEILLE RÉGLEMENTAIRE — {domaine}"
    )
    sauvegarder(f"veille_{domaine.replace(' ', '_')}", r)


def strategie_subventions():
    print("\n  Type de projet à financer (ex: développement outil IA, formation, R&D) :")
    projet = input("  Projet → ").strip() or "développement outils IA pour PME"
    r = streamer(
        f"""STRATÉGIE DE FINANCEMENT PUBLIC pour Caelum Partners :
Projet : {projet}

Identifie toutes les sources de financement disponibles en 2025-2026 :

1. FONDS EUROPÉENS
   - Horizon Europe (quelle thématique ?)
   - Digital Europe Programme
   - Fonds structurels FEDER/FSE+

2. FONDS BELGES/BRUXELLOIS
   - Innoviris (Bruxelles) : quels appels à projets ?
   - Hub.Brussels : accompagnement et aides
   - VLAIO (Flandre) si pertinent
   - SPW Digital (Wallonie) si pertinent

3. MONTANTS ET CONDITIONS
   - Taux de subvention (50-80% ?)
   - Taille minimale de projet
   - Délais de dépôt

4. PLAN DE CANDIDATURE
   - Quel programme en premier ?
   - Documents requis
   - Erreurs à éviter

5. PARTENARIATS REQUIS
   - Certains fonds exigent un consortium — qui contacter ?""",
        f"STRATÉGIE SUBVENTIONS — {projet[:40]}"
    )
    sauvegarder(f"subventions_{projet[:20].replace(' ', '_')}", r)


def position_paper():
    print("\n  Sujet du position paper (ex: impact AI Act sur les PME, régulation des LLM) :")
    sujet = input("  Sujet → ").strip() or "impact AI Act sur les PME européennes"
    r = streamer(
        f"""Rédige un POSITION PAPER pour Caelum Partners sur : {sujet}

Format document officiel :
RÉSUMÉ EXÉCUTIF (150 mots)
CONTEXTE (situation actuelle)
ENJEUX POUR LES PME (impact spécifique)
POSITION DE CAELUM PARTNERS (nos recommandations)
PROPOSITIONS CONCRÈTES (3-5 mesures)
CONCLUSION ET APPEL À L'ACTION

Destinataires : décideurs politiques belges et européens, associations sectorielles.
Ton : professionnel, factuel, constructif (pas militant).""",
        f"POSITION PAPER — {sujet[:40]}"
    )
    sauvegarder(f"position_paper_{sujet[:20].replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  LOBBYING & AFFAIRES PUBLIQUES EUROPE — Caelum Partners")
    print("  AI Act · Subventions · Veille réglementaire")
    print("═"*65)

    while True:
        print("\n  1. Analyse AI Act — impact sur Caelum")
        print("  2. Veille réglementaire (domaine spécifique)")
        print("  3. Stratégie subventions et financements publics")
        print("  4. Position paper (communication institutionnelle)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            analyse_ai_act()
        elif choix == "2":
            veille_reglementaire()
        elif choix == "3":
            strategie_subventions()
        elif choix == "4":
            position_paper()
        else:
            print("  Choix invalide.")
