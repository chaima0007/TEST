"""
AGENT NEWSLETTER [86] — Nurturing prospects & fidélisation clients
Newsletter hebdo, séquences de bienvenue, campagnes de relance.

Usage : python agent_newsletter.py
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

IDENTITE = """# AGENT NEWSLETTER — Caelum Partners

## IDENTITÉ
Tu gères la stratégie email marketing de Caelum Partners pour transformer les prospects en clients et les clients en ambassadeurs.

## LISTE EMAIL (objectif croissance)
- Prospects LinkedIn convertis en abonnés
- Clients passés (fidélisation + upsell)
- Partenaires potentiels (cabinets comptables, fiduciaires, etc.)

## STRATÉGIE EMAIL (règle des 80/20)
- 80% valeur (insight IA, conseil, cas concret, tendance)
- 20% commercial (offre, disponibilité, rappel de prix)

## TYPES D'EMAILS
1. NEWSLETTER HEBDO : 1 insight IA actionnable pour PME belges (tous les mardis)
2. BIENVENUE : séquence 5 emails sur 14 jours (nouveau abonné)
3. NURTURING : séquence 30 jours pour prospect pas encore prêt à acheter
4. RELANCE INACTIFS : réactiver les abonnés silencieux (> 60 jours sans ouverture)
5. ANNONCE OFFRE : email commercial ciblé (max 1 fois/mois)

## RÈGLES RÉDACTION
- Objet : 40 caractères max, curiosité ou bénéfice direct
- Corps : 200-400 mots max (lu en < 2 minutes)
- 1 seul CTA par email
- Désabonnement facile (confiance + RGPD Belgique)
- Personnalisation : prénom si disponible"""


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
    os.makedirs("fichiers/newsletter", exist_ok=True)
    fichier = f"fichiers/newsletter/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def newsletter_hebdo():
    print("\n  Sujet de cette semaine (ex: 'comment les PME perdent 5h/semaine sur leurs emails') :")
    sujet = input("  Sujet → ").strip()
    if not sujet:
        return
    r = streamer(
        f"""Écris la NEWSLETTER HEBDOMADAIRE de Caelum Partners sur : {sujet}

Format :
OBJET : (40 caractères max, accrocheur)
PREVIEW TEXT : (90 caractères, complète l'objet)

Bonjour [Prénom],

[Hook — 1 phrase qui donne envie de lire la suite]

[Corps : 200-300 mots — insight concret, exemples PME belges, chiffres]

[Conseil actionnable — ce que le lecteur peut faire AUJOURD'HUI en 15 min]

[Segue naturel vers Caelum Partners — 2-3 phrases, pas de pression]

À bientôt,
Chaima — Caelum Partners

P.S. : [post-scriptum qui intrigue sur la prochaine newsletter]

[Lien désabonnement]""",
        f"NEWSLETTER — {sujet[:40]}"
    )
    sauvegarder(f"newsletter_{sujet[:20].replace(' ', '_')}", r)


def sequence_bienvenue():
    r = streamer(
        """Crée la SÉQUENCE DE BIENVENUE complète pour les nouveaux abonnés Caelum Partners.

5 emails sur 14 jours :

EMAIL 1 (J+0 — immédiat) :
Objet + Corps : bienvenue, qui est Chaima, ce qu'ils vont recevoir, cadeau immédiat (conseil IA gratuit)

EMAIL 2 (J+2) :
Objet + Corps : "la vraie raison pour laquelle la plupart des PME ratent l'IA" — éducation

EMAIL 3 (J+5) :
Objet + Corps : cas concret (PME anonyme qui a économisé X heures/semaine) — preuve sociale

EMAIL 4 (J+9) :
Objet + Corps : "les 3 automatisations que toute PME devrait avoir en 2026" — valeur max

EMAIL 5 (J+14) :
Objet + Corps : offre douce (audit gratuit 30 min, sans engagement)

Chaque email : objet + prévisualisation + corps complet (200-300 mots) + CTA unique.""",
        "SÉQUENCE BIENVENUE — 5 emails"
    )
    sauvegarder("sequence_bienvenue", r)


def sequence_nurturing():
    print("\n  Secteur du prospect à nurture (ex: cabinet comptable, restaurant) :")
    secteur = input("  Secteur → ").strip() or "PME belge"
    r = streamer(
        f"""Crée une SÉQUENCE NURTURING 30 JOURS pour des prospects {secteur} qui ne sont pas encore prêts à acheter.

8 emails sur 30 jours (espacés) :

Structure de la séquence :
Semaine 1 : Éducation (problèmes sectoriels spécifiques à {secteur})
Semaine 2 : Solutions concrètes (comment l'IA résout ces problèmes)
Semaine 3 : Preuves (témoignages, chiffres, avant/après)
Semaine 4 : Offre (pourquoi maintenant, pourquoi Caelum)

Pour chaque email : numéro, jour d'envoi, objet, corps (150-250 mots), CTA.""",
        f"SÉQUENCE NURTURING — {secteur}"
    )
    sauvegarder(f"nurturing_{secteur.replace(' ', '_')}", r)


def campagne_relance():
    r = streamer(
        """Crée une CAMPAGNE DE RELANCE pour les abonnés inactifs depuis 60+ jours.

3 emails espacés de 3 jours :

EMAIL 1 — "Tu nous manques" (doux)
: Reconnaître l'absence, offrir de la valeur immédiate, ne pas reprocher

EMAIL 2 — "Dernière chance valeur" (milieu)
: Partager le meilleur contenu des 60 derniers jours en 1 résumé

EMAIL 3 — "On va se dire au revoir ?" (scarcity)
: Si pas d'ouverture, proposer de changer la fréquence ou se désabonner proprement

Chaque email : objet percutant + corps 100-150 mots + 1 CTA clair.""",
        "CAMPAGNE RELANCE INACTIFS"
    )
    sauvegarder("campagne_relance_inactifs", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  NEWSLETTER — Caelum Partners")
    print("  Nurturing · Fidélisation · Email marketing")
    print("═"*65)

    while True:
        print("\n  1. Newsletter hebdomadaire")
        print("  2. Séquence de bienvenue (5 emails / 14 jours)")
        print("  3. Séquence nurturing secteur (8 emails / 30 jours)")
        print("  4. Campagne relance inactifs")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            newsletter_hebdo()
        elif choix == "2":
            sequence_bienvenue()
        elif choix == "3":
            sequence_nurturing()
        elif choix == "4":
            campagne_relance()
        else:
            print("  Choix invalide.")
