"""
AGENT TARIFICATION — Expert en pricing et stratégie de prix
Value-based pricing · Packages · Augmenter les prix sans perdre des clients

Usage : python agent_tarification.py
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

IDENTITE = """Tu es un expert en pricing strategy avec 15 ans d'expérience en SaaS et agences B2B.
Tu as aidé des centaines d'agences à doubler leurs prix sans perdre de clients.

CONTEXTE CAELUM PARTNERS :
- Fondatrice : Chaima Mhadbi, Bruxelles
- Services actuels : Site web 500€ / Automation IA 1500€ / Pack 3000€
- Cible : PME belges et Europe francophone
- Phase : lancement, 0 clients — prix à valider sur le marché
- Concurrent : agences web traditionnelles (sites web 2000-8000€), agences IA (rares)

PHILOSOPHIE PRICING QUE TU DÉFENDS :
1. Value-based pricing — prix basé sur la valeur créée, pas sur le temps passé
2. L'IA permet de livrer PLUS vite → marges plus élevées, pas prix plus bas
3. Les prix trop bas signalent une mauvaise qualité — danger pour Caelum
4. Chaque package doit avoir une "ancre" (le plus cher fait paraître le milieu raisonnable)
5. La vraie concurrence n'est pas les autres agences IA — c'est l'inaction du client

OUTILS DE PRICING QUE TU UTILISES :
- ROI calculator (combien Caelum fait économiser au client)
- Good-Better-Best packaging (3 niveaux)
- Price anchoring et decoy pricing
- Value ladder (entrée → upsell → premium)
- Price increase strategy (augmenter sans perdre de clients)"""


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
                temperature=0.3,
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
    os.makedirs("fichiers/tarification", exist_ok=True)
    fichier = f"fichiers/tarification/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def audit_prix_actuels():
    r = streamer(
        """Analyse les prix actuels de Caelum Partners (500€ / 1500€ / 3000€) :
1. Ces prix sont-ils trop bas, justes ou trop élevés pour le marché belge ?
2. Que perd Chaima en chiffrant à 500€ un site web livré en 7 jours avec IA ?
3. Comparaison avec la concurrence (agences web belges, freelancers, agences IA)
4. Quel est le vrai ROI pour un client qui achète le site à 500€ ?
5. Recommandation : garder ces prix ou les ajuster ?
6. Si ajustement : nouveau prix recommandé avec justification""",
        "AUDIT PRIX ACTUELS — Les 500€/1500€/3000€ sont-ils bons ?"
    )
    sauvegarder("audit_prix", r)


def calculateur_roi_client():
    r = streamer(
        """Crée un calculateur de ROI pour que Chaima puisse montrer à ses prospects la valeur réelle.
Pour le site web à 500€ :
- Combien de clients supplémentaires le site peut apporter par mois ?
- Si 1 client vaut 500€ pour eux, le site est rentabilisé dès le 1er client
Pour l'automation IA à 1500€ :
- Combien d'heures économisées par semaine ?
- Si 10h/semaine économisées × salaire moyen → ROI en semaines
Pour le pack à 3000€ :
- ROI cumulé sur 12 mois
Donne des exemples chiffrés pour 3 profils types de PME belges.
Format : tableau utilisable en pitch commercial.""",
        "CALCULATEUR ROI — Outil de vente pour les prospects"
    )
    sauvegarder("calculateur_roi", r)


def nouveaux_packages():
    r = streamer(
        """Redesigne les packages de Caelum Partners pour maximiser le CA.
Utilise la technique Good-Better-Best et le price anchoring.
Contraintes :
- Entrée de gamme : reste accessible (500-800€)
- Milieu : valeur optimale (1500-2500€)
- Premium : prix ancre qui fait paraître le milieu raisonnable (5000€+)
- Récurrence possible ? (abonnement mensuel de maintenance/suivi)
Pour chaque package :
- Nom accrocheur
- Prix exact recommandé
- Contenu précis (livrables)
- Argument de vente principal
- Pour qui c'est fait
- Marge estimée (temps IA + temps Chaima)""",
        "NOUVEAUX PACKAGES — Maximiser le CA avec le bon pricing"
    )
    sauvegarder("nouveaux_packages", r)


def strategie_upsell():
    r = streamer(
        """Crée une stratégie d'upsell et de récurrence pour Caelum Partners.
Chaima livre un site web à 500€ → comment aller jusqu'à 3000€/an par client ?
1. Timing parfait pour proposer l'upsell (pas trop tôt, pas trop tard)
2. Les services de maintenance/suivi mensuels possibles (abonnement 200-500€/mois)
3. L'upsell naturel : site → automation → pack empire
4. Les services additionnels non encore dans l'offre (formation équipe, audit SEO...)
5. Script exact pour proposer l'upsell sans paraître cupide
6. Objectif : chaque client vaut 3x plus sur 12 mois""",
        "STRATÉGIE UPSELL — De 500€ à 3000€/an par client"
    )
    sauvegarder("strategie_upsell", r)


def augmenter_les_prix():
    r = streamer(
        """Chaima veut augmenter ses prix après les 10 premiers clients.
Comment augmenter les prix sans perdre de clients et sans nuire à la réputation ?
1. Quand augmenter (après combien de clients / quelle durée ?)
2. De combien augmenter (% recommandé)
3. Comment annoncer la hausse aux prospects (pas aux clients existants)
4. Argument : "nos prix augmentent parce que notre valeur augmente"
5. Protection des clients existants (tarif bloqué / clause de fidélité)
6. Script email/LinkedIn pour annoncer la hausse de prix positivement""",
        "AUGMENTER LES PRIX — Stratégie après les premiers clients"
    )
    sauvegarder("augmenter_prix", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT TARIFICATION — Pricing expert pour Caelum Partners")
    print("  Value-based pricing · Packages · Upsell · ROI")
    print("═"*65)

    while True:
        print("\n  1. Audit des prix actuels (500€/1500€/3000€)")
        print("  2. Calculateur ROI client — outil de vente")
        print("  3. Nouveaux packages — Good-Better-Best")
        print("  4. Stratégie upsell — de 500€ à 3000€/an par client")
        print("  5. Augmenter les prix — stratégie et script")
        print("  7. Question libre sur la tarification")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            audit_prix_actuels()
        elif choix == "2":
            calculateur_roi_client()
        elif choix == "3":
            nouveaux_packages()
        elif choix == "4":
            strategie_upsell()
        elif choix == "5":
            augmenter_les_prix()
        elif choix == "7":
            q = input("\n  Ta question → ").strip()
            if q:
                streamer(q, "QUESTION TARIFICATION")
        else:
            print("  Choix invalide.")
