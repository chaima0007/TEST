"""
AGENT PITCH DECK [79] — Présentations & Argumentaires Caelum Partners
Crée des pitch decks clients, one-pagers investisseurs, scripts de présentation.

Usage : python agent_pitch_deck.py
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

IDENTITE = """# AGENT PITCH DECK — Caelum Partners

## IDENTITÉ
Tu es l'expert en présentation et argumentaire de Caelum Partners (Bruxelles, Belgique).
Tu crées des pitch decks percutants, des one-pagers convaincants et des scripts de présentation.

## CAELUM PARTNERS
- Services : 500€ (site web, 7j) · 1 500€ (automation IA, 14j) · 3 000€ (pack complet, 30j)
- Marché cible : PME belges, Bruxelles, puis Wallonie, France, Luxembourg
- Différenciateur : IA sur mesure + conformité légale belge + livraison rapide garantie
- Fondatrice : Chaima Mhadbi — experte IA opérationnelle

## RÈGLES PITCH
- Aller direct au problème client (douleur réelle, coût de l'inaction)
- Chiffrer le ROI avant/après (temps économisé, CA généré, erreurs évitées)
- Social proof : même sans client, utiliser les cas d'usage sectoriels
- CTA unique et clair à la fin (appel de 30 min, pas de décision compliquée)
- Ton : professionnel mais humain, jamais corporate pompeux
- Prix jamais négociables vers le bas — toujours justifier la valeur

## FORMAT PITCH DECK (10 slides max)
1. Le problème (1 stat choc)
2. La solution (en 1 phrase)
3. Comment ça marche (3 étapes max)
4. Résultats concrets (chiffres)
5. Pourquoi Caelum (différenciateurs)
6. Offres & Tarifs
7. CTA (prochaine étape)"""


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
                temperature=0.35,
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
    os.makedirs("fichiers/pitch_deck", exist_ok=True)
    fichier = f"fichiers/pitch_deck/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def pitch_client():
    print("\n  Secteur du client (ex: HORECA, avocat, comptable, PME tech) :")
    secteur = input("  Secteur → ").strip()
    print("  Problème principal du client (ex: trop de temps sur la paperasse) :")
    probleme = input("  Problème → ").strip()
    if not secteur:
        return
    r = streamer(
        f"""Crée un pitch deck COMPLET pour vendre l'automation IA Caelum Partners à :
- Secteur : {secteur}
- Problème identifié : {probleme}

FORMAT : 7 slides numérotées avec titre + contenu + conseil de présentation orale.
Inclure : 1 statistique choc sur le secteur, ROI estimé (temps économisé/semaine), prix recommandé parmi nos 3 offres.""",
        f"PITCH DECK — {secteur}"
    )
    sauvegarder(f"pitch_{secteur.replace(' ', '_')}", r)


def one_pager():
    print("\n  Pour qui est ce one-pager ? (ex: directeur PME, investisseur, partenaire) :")
    cible = input("  Cible → ").strip()
    if not cible:
        return
    r = streamer(
        f"""Crée un ONE-PAGER A4 percutant pour Caelum Partners, destiné à : {cible}

FORMAT :
HEADER : Caelum Partners — L'IA qui travaille pour vous
COLONNE GAUCHE (problème + solution)
COLONNE DROITE (résultats + offres + contact)
FOOTER : contact@caelumpartners.agency | caelumpartners.agency

Max 300 mots. Dense, lisible, convaincant.""",
        f"ONE-PAGER — {cible}"
    )
    sauvegarder(f"one_pager_{cible.replace(' ', '_')}", r)


def script_presentation():
    print("\n  Durée de la présentation (ex: 5 min, 15 min, 30 min) :")
    duree = input("  Durée → ").strip() or "15 min"
    print("  Contexte (ex: appel cold, réunion in situ, démo en ligne) :")
    contexte = input("  Contexte → ").strip() or "appel téléphonique"
    r = streamer(
        f"""Crée un SCRIPT DE PRÉSENTATION de {duree} pour Caelum Partners.
Contexte : {contexte}

FORMAT :
- Introduction accroche (15 sec)
- Découverte problème client (questions à poser)
- Présentation solution (pitch principal)
- Objections fréquentes + réponses
- Closing (comment conclure la prochaine étape)

Style : naturel, conversationnel, pas robotique.""",
        f"SCRIPT {duree} — {contexte}"
    )
    sauvegarder(f"script_{duree.replace(' ', '_')}", r)


def argumentaire_prix():
    print("\n  L'offre concernée (500€ / 1500€ / 3000€) :")
    offre = input("  Offre → ").strip()
    print("  Objection du client (ex: 'c'est trop cher', 'je dois réfléchir') :")
    objection = input("  Objection → ").strip()
    if not objection:
        return
    r = streamer(
        f"""Le client dit : "{objection}" face à notre offre {offre}.

Génère un argumentaire de DÉFENSE DE VALEUR (pas de réduction de prix) :
1. Reformulation empathique
2. Recadrage par le coût de l'inaction (ce que ça lui coûte de NE PAS acheter)
3. Décomposition ROI (combien ça rapporte sur 6 mois)
4. Proof point sectoriel
5. Proposition de prochaine étape (pas de décision forcée)

Ton : confiant, jamais défensif.""",
        f"DÉFENSE PRIX — {offre}"
    )
    sauvegarder(f"argumentaire_prix_{offre.replace('€', 'e')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  PITCH DECK — Caelum Partners")
    print("  Présentations & argumentaires qui convertissent")
    print("═"*65)

    while True:
        print("\n  1. Créer un pitch deck secteur")
        print("  2. Générer un one-pager A4")
        print("  3. Script de présentation orale")
        print("  4. Argumentaire de défense du prix")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            pitch_client()
        elif choix == "2":
            one_pager()
        elif choix == "3":
            script_presentation()
        elif choix == "4":
            argumentaire_prix()
        else:
            print("  Choix invalide.")
