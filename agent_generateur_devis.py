"""
AGENT GÉNÉRATEUR DE DEVIS [92] — Devis intelligents, comparaison packages, argumentaire prix
Génère des devis professionnels conformes droit belge en 2 minutes.

Usage : python agent_generateur_devis.py
"""

import os
import sys
from datetime import datetime, timedelta
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# Offres Caelum Partners
OFFRES = {
    "500": {
        "nom": "Site Web IA",
        "description": "Site web professionnel avec contenu IA optimisé SEO",
        "delai": "7 jours",
        "inclus": ["Design responsive", "3-5 pages", "SEO de base", "Formulaire de contact", "Hébergement Cloudflare 1 an"]
    },
    "1500": {
        "nom": "Automation IA",
        "description": "Automatisation d'un processus clé de l'entreprise",
        "delai": "14 jours",
        "inclus": ["Audit du processus", "Développement workflow", "Intégration outils existants", "Formation 1h", "Support 30 jours"]
    },
    "3000": {
        "nom": "Pack Complet",
        "description": "Site web + automation + stratégie IA complète",
        "delai": "30 jours",
        "inclus": ["Tout de l'offre Site Web", "Tout de l'offre Automation", "Audit IA complet", "Roadmap 6 mois", "Support 90 jours"]
    }
}

IDENTITE = f"""# AGENT GÉNÉRATEUR DE DEVIS — Caelum Partners

## IDENTITÉ
Tu génères des devis professionnels pour Caelum Partners selon le droit belge.
Chaque devis doit être conforme, clair et convaincant.

## OFFRES CAELUM
{str(OFFRES)}

## DROIT BELGE — MENTIONS OBLIGATOIRES DEVIS
- Nom/prénom ou dénomination sociale du prestataire
- Numéro de TVA (ou mention "TVA non applicable - Art. 56bis CIR" si franchise)
- Date du devis et date de validité
- Description détaillée des prestations
- Prix HTVA + TVA (21%) + Prix TVAC
- Conditions de paiement
- Délai de livraison
- Conditions d'annulation

## RÈGLES DE DEVIS
- Prix non négociables à la baisse
- Validité devis : 30 jours
- Acompte : 50% à la signature
- Solde : 50% à la livraison
- TVA : Article 56bis (franchise si CA < 25.000€/an) → "TVA non applicable"
- Paiement : virement bancaire (IBAN à indiquer)"""


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
    os.makedirs("fichiers/devis", exist_ok=True)
    fichier = f"fichiers/devis/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def generer_devis():
    print("\n  Nom complet du client :")
    client_nom = input("  Client → ").strip()
    print("  Entreprise du client :")
    client_entreprise = input("  Entreprise → ").strip()
    print("  Offre (500 / 1500 / 3000) :")
    offre_choix = input("  Offre → ").strip()
    print("  Précisions sur la mission (personnalisation) :")
    precisions = input("  Précisions → ").strip() or "selon discussion"

    if offre_choix not in OFFRES:
        print("  Offre invalide. Choisir 500, 1500 ou 3000.")
        return

    offre = OFFRES[offre_choix]
    date_devis = datetime.now()
    date_validite = date_devis + timedelta(days=30)
    date_livraison = date_devis + timedelta(days=int(offre["delai"].split()[0]))
    num_devis = f"CP-{date_devis.strftime('%Y%m')}-{str(int(offre_choix)//100).zfill(2)}"

    r = streamer(
        f"""Génère un DEVIS PROFESSIONNEL complet selon le droit belge :

NUMÉRO DE DEVIS : {num_devis}
DATE : {date_devis.strftime('%d/%m/%Y')}
VALIDITÉ : {date_validite.strftime('%d/%m/%Y')}

PRESTATAIRE :
Chaima Mhadbi — Caelum Partners
Bruxelles, Belgique
contact@caelumpartners.agency
caelumpartners.agency
TVA : non applicable — Art. 56bis CIR (franchise de taxe)

CLIENT :
Nom : {client_nom}
Entreprise : {client_entreprise}

MISSION : {offre['nom']}
Description : {offre['description']}
Précisions : {precisions}

PRESTATIONS INCLUSES :
{chr(10).join(['- ' + item for item in offre['inclus']])}

TARIFICATION :
Montant HT : {offre_choix}€
TVA : non applicable (Art. 56bis CIR)
MONTANT TOTAL : {offre_choix}€

CONDITIONS :
- Acompte : {int(offre_choix)//2}€ à la signature
- Solde : {int(offre_choix)//2}€ à la livraison
- Délai de livraison : {offre['delai']} après réception de l'acompte
- Paiement par virement bancaire
- Date de livraison estimée : {date_livraison.strftime('%d/%m/%Y')}

Formate ce devis de manière professionnelle et lisible.
Ajouter une ligne de signature : "Bon pour accord — Date — Signature client".""",
        f"DEVIS {num_devis} — {client_nom}"
    )
    sauvegarder(f"devis_{num_devis}_{client_nom.replace(' ', '_')}", r)


def comparaison_packages():
    print("\n  Secteur du client (pour adapter l'argumentaire) :")
    secteur = input("  Secteur → ").strip() or "PME"
    r = streamer(
        f"""Génère un TABLEAU COMPARATIF des 3 offres Caelum Partners pour un client {secteur}.

Format tableau :
| Critère | Site Web 500€ | Automation 1500€ | Pack Complet 3000€ |

Lignes du tableau :
- Prix
- Délai de livraison
- Inclus (livrables principaux)
- ROI estimé (6 mois)
- Idéal pour (profil client)
- Garanties

Sous le tableau : RECOMMANDATION pour {secteur} avec justification ROI.""",
        f"COMPARAISON PACKAGES — {secteur}"
    )
    sauvegarder(f"comparaison_{secteur.replace(' ', '_')}", r)


def devis_sur_mesure():
    print("\n  Décris la mission sur mesure (hors packages standards) :")
    mission = input("  Mission → ").strip()
    print("  Budget estimé du client :")
    budget = input("  Budget → ").strip() or "non défini"
    print("  Délai souhaité :")
    delai = input("  Délai → ").strip() or "à définir"
    if not mission:
        return
    r = streamer(
        f"""Génère un DEVIS SUR MESURE pour cette mission non-standard :
Mission : {mission}
Budget client : {budget}
Délai souhaité : {delai}

Inclure :
1. ANALYSE DE LA MISSION : ce qu'elle implique réellement
2. DÉCOMPOSITION DU PRIX : heures estimées × taux journalier, ou forfait
3. OPTIONS : version light / version complète / version premium
4. RISQUES ET CONDITIONS : ce qui est exclu, ce qui ferait augmenter le prix
5. DEVIS FORMEL : document complet prêt à envoyer

Taux journalier Caelum : 600€/jour (75€/h)""",
        "DEVIS SUR MESURE"
    )
    sauvegarder("devis_sur_mesure", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  GÉNÉRATEUR DE DEVIS — Caelum Partners")
    print("  Devis conformes droit belge · Professionnels · En 2 minutes")
    print("═"*65)

    while True:
        print("\n  1. Générer un devis (500€ / 1500€ / 3000€)")
        print("  2. Tableau comparatif des 3 packages")
        print("  3. Devis sur mesure (mission spéciale)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            generer_devis()
        elif choix == "2":
            comparaison_packages()
        elif choix == "3":
            devis_sur_mesure()
        else:
            print("  Choix invalide.")
