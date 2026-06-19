"""
AGENT TRADUCTEUR [87] — Traductions professionnelles FR/NL/EN/DE
Belgique bilingue : tous documents traduits avec adaptation culturelle.

Usage : python agent_traducteur.py
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

IDENTITE = """# AGENT TRADUCTEUR PROFESSIONNEL — Caelum Partners

## IDENTITÉ
Tu es le traducteur professionnel de Caelum Partners.
Belgique est un pays bilingue (FR/NL) avec un marché anglophone et germanophone important.
Tu traduis tous les documents commerciaux, légaux et marketing avec adaptation culturelle.

## LANGUES MAÎTRISÉES
- Français (Wallonie, Bruxelles, France, Luxembourg)
- Néerlandais (Flandre, Bruxelles, Pays-Bas)
- Anglais (clients internationaux, documentation technique)
- Allemand (Communauté germanophone Belgique, Suisse, Autriche)

## RÈGLES DE TRADUCTION
- FIDÉLITÉ : sens exact, pas de mot à mot
- ADAPTATION : registre approprié à la cible (formel/informel selon pays)
- TERMINOLOGIE BELGE : utiliser les termes légaux belges corrects en NL
- COHÉRENCE : même terme = même traduction sur tout le document
- NL/Belgique vs NL/Pays-Bas : signaler les différences importantes

## CONTEXTE BELGE
- Bruxelles : bilingue officiel, emails souvent envoyés FR + NL
- Flandre : NL obligatoire pour communications légales
- Wallonie : FR uniquement
- Documents légaux : adaptation aux formulations officielles belges"""


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
    os.makedirs("fichiers/traductions", exist_ok=True)
    fichier = f"fichiers/traductions/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def traduire_document():
    print("\n  Langue source (FR / NL / EN / DE) :")
    source = input("  Langue source → ").strip().upper() or "FR"
    print("  Langue cible (FR / NL / EN / DE) :")
    cible = input("  Langue cible → ").strip().upper() or "NL"
    print("  Type de document (email / contrat / site web / brochure / autre) :")
    doc_type = input("  Type → ").strip() or "email"
    print("\n  Colle le texte à traduire (termine par une ligne vide + ENTRÉE) :")
    lignes = []
    while True:
        ligne = input()
        if ligne == "":
            break
        lignes.append(ligne)
    texte = "\n".join(lignes)
    if not texte:
        return
    r = streamer(
        f"""Traduis ce {doc_type} de {source} vers {cible} pour le contexte belge.

TEXTE À TRADUIRE :
{texte}

Instructions :
1. Traduction professionnelle fidèle et naturelle
2. Adaptation culturelle selon la cible ({cible})
3. Signaler en [NOTE] les termes avec nuance culturelle importante
4. Si {cible} = NL : utiliser terminologie belge (pas toujours identique aux Pays-Bas)

Format : texte traduit complet, puis notes éventuelles.""",
        f"TRADUCTION {source} → {cible} — {doc_type}"
    )
    sauvegarder(f"traduction_{source}_{cible}_{doc_type}", r)


def email_bilingue():
    print("\n  Sujet de l'email :")
    sujet = input("  Sujet → ").strip()
    print("  Contexte (ex: proposition commerciale à un notaire flamand) :")
    contexte = input("  Contexte → ").strip() or "email commercial"
    if not sujet:
        return
    r = streamer(
        f"""Crée un EMAIL BILINGUE FR/NL pour Caelum Partners.
Sujet : {sujet}
Contexte : {contexte}

Format :
--- VERSION FRANÇAISE ---
[Email complet professionnel]

--- NEDERLANDSE VERSIE ---
[Volledige professionele e-mail]

Les deux versions doivent être adaptées culturellement (pas juste traduites).
En NL : utiliser "u" (vouvoyer) sauf si contexte informel explicite.""",
        f"EMAIL BILINGUE FR/NL — {sujet[:40]}"
    )
    sauvegarder(f"email_bilingue_{sujet[:20].replace(' ', '_')}", r)


def glossaire_technique():
    print("\n  Domaine du glossaire (ex: IA, comptabilité, juridique, immobilier) :")
    domaine = input("  Domaine → ").strip() or "automation IA"
    r = streamer(
        f"""Crée un GLOSSAIRE TECHNIQUE FR/NL/EN pour le domaine : {domaine}

30 termes clés avec :
TERME FR | TERME NL | TERME EN | DÉFINITION COURTE FR

Prioriser les termes qui :
1. N'ont pas d'équivalent direct (risque de confusion)
2. Ont une traduction NL différente entre Belgique et Pays-Bas
3. Sont fréquemment mal traduits dans ce secteur

Format tableau.""",
        f"GLOSSAIRE — {domaine}"
    )
    sauvegarder(f"glossaire_{domaine.replace(' ', '_')}", r)


def site_web_nl():
    r = streamer(
        """Traduis les éléments CLE du site caelumpartners.agency en NÉERLANDAIS belge.

Éléments à traduire :
1. SLOGAN PRINCIPAL : "L'IA qui travaille pour votre entreprise"
2. TAGLINE : "Automation IA pour PME belges — résultats en 7 jours"
3. OFFRES (3 packages — titres et descriptions courtes)
4. CTA PRINCIPAL : "Demander un audit gratuit"
5. FOOTER légal : "Caelum Partners — contact@caelumpartners.agency — Bruxelles, Belgique"
6. META TITLE et META DESCRIPTION pour le SEO NL

Adapter le ton pour le marché flamand (plus direct, moins élaboré qu'en FR).""",
        "SITE WEB EN NÉERLANDAIS BELGE"
    )
    sauvegarder("site_web_nl", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  TRADUCTEUR — Caelum Partners")
    print("  FR · NL · EN · DE — Belgique bilingue")
    print("═"*65)

    while True:
        print("\n  1. Traduire un document (FR/NL/EN/DE)")
        print("  2. Email bilingue FR + NL (prêt à envoyer)")
        print("  3. Glossaire technique bilingue")
        print("  4. Traduire le site web en NL (marché flamand)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            traduire_document()
        elif choix == "2":
            email_bilingue()
        elif choix == "3":
            glossaire_technique()
        elif choix == "4":
            site_web_nl()
        else:
            print("  Choix invalide.")
