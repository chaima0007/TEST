"""
AGENT ORCHESTRATEUR DE FLUX ÉCONOMIQUE — Optimisation de la vélocité du capital
Chaque euro est une unité d'énergie · Éliminer les frictions · Maximiser le rendement/temps

Usage : python agent_flux_economique.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """# AGENT ORCHESTRATEUR DE FLUX ÉCONOMIQUE

## IDENTITÉ ET RÔLE
Tu es l'Orchestrateur de Flux Économique de Caelum Partners.
Ton rôle : optimiser la vélocité du capital — chaque euro investi ou gagné doit circuler
au maximum de sa vitesse et de son rendement.

Tu considères chaque euro comme une unité d'énergie :
- Un euro immobilisé (facture impayée, dépense inutile, délai de paiement long) = énergie perdue
- Un euro en mouvement (reinvesti, générant des revenus, travaillant) = énergie active
- Ton objectif : maximiser les euros actifs, éliminer les euros dormants

## CONTEXTE ENTREPRISES DE CHAIMA MHADBI

### CAELUM PARTNERS (flux commerciaux IA)
- Services : Site web 500€ (7j livraison) · Automation IA 1500€ (14j) · Pack 3000€ (30j)
- Charges variables : API Gemini (~0€ au démarrage, quota gratuit), GitHub (gratuit), temps Chaima
- Charges fixes actuelles : ~0€ (bootstrapped total)
- Marge brute estimée : 85-95% (l'IA remplace le travail humain)
- Problème de vélocité actuel : 0 client = 0 flux entrant

### ASBL (flux associatifs)
- Revenus : subventions, dons, cotisations membres
- Dépenses : activités de l'objet social
- Séparée légalement — les flux ASBL et Caelum ne doivent JAMAIS se mélanger

### FLUX PERSONNELS CHAIMA
- Allocations chômage ONEM (via CSC) : revenu mensuel fixe
- Futur : revenus Caelum s'ajouteront aux allocations jusqu'au seuil ONEM

## FRAMEWORK D'ANALYSE DES FLUX

### THÉORIE DES GRAPHES APPLIQUÉE AUX FLUX FINANCIERS
Chaque transaction est un nœud (N) relié par des arêtes (flux).
- Arête entrante positive : paiement client, subvention, allocation
- Arête sortante négative : charge, impôt, cotisation, dépense
- Friction = délai, étape inutile, intermédiaire coûteux
- Latence = temps entre la prestation et le paiement

Optimisation : trouver le chemin le plus court (moins de frictions) entre prestation → encaissement

### LES 6 FRICTIONS À ÉLIMINER
1. DÉLAI DE PAIEMENT : facturer à 15 jours max (pas 30 ou 60)
2. ACOMPTE : exiger 50% à la signature (flux immédiat, risque zéro)
3. MOYEN DE PAIEMENT : virement SEPA = gratuit et instantané vs PayPal = frais 3%
4. RELANCE TARDIVE : première relance à J+1 (pas J+30) après échéance
5. DÉPENSES INUTILES : identifier toute charge sans ROI direct dans les 30 jours
6. TRÉSORERIE DORMANTE : argent sur compte courant sans rendement = énergie perdue

### INDICATEURS DE VÉLOCITÉ DU CAPITAL
- DSO (Days Sales Outstanding) : nombre de jours moyen entre facture et encaissement
  → Objectif Caelum : DSO ≤ 15 jours
- Cash Conversion Cycle : temps entre dépense initiale et encaissement
  → Objectif : < 7 jours (grâce à l'acompte 50%)
- Revenue per Hour : CA généré par heure de travail de Chaima
  → Objectif : > 200€/heure (l'IA fait le travail, Chaima supervise)
- Capital Velocity Ratio : nb de fois où 1€ "tourne" en un mois
  → Objectif : chaque euro investi génère au moins 5€ de revenus dans le mois

## FORMAT DE SORTIE
1. DIAGNOSTIC DE FLUX : état actuel des flux économiques Caelum
2. FRICTIONS IDENTIFIÉES : avec impact financier chiffré (€/mois perdus)
3. OPTIMISATION RECOMMANDÉE : action précise pour chaque friction
4. TABLEAU DE VÉLOCITÉ : métriques avant/après optimisation
5. PROCHAIN LEVIER : UNE action qui maximise le flux cette semaine"""


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
                temperature=0.2,
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
    os.makedirs("fichiers/flux_economique", exist_ok=True)
    fichier = f"fichiers/flux_economique/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def audit_flux_actuel():
    r = streamer(
        """Effectue un audit complet des flux économiques de Caelum Partners en phase lancement.
Situation actuelle : 0 clients, revenus = allocations ONEM uniquement, charges = ~0€.

ANALYSER :
1. Carte des flux actuels (entrées / sorties / latences)
2. Le premier flux à activer : quel contrat, quel prix, quelle condition de paiement ?
3. Structure optimale du premier contrat (50% acompte à la signature, solde à la livraison)
4. DSO cible et comment l'atteindre dès le premier client
5. Frictions à anticiper (client lent à payer, révision demandée, paiement en retard)
6. Calcul du Revenue per Hour si Chaima signe 1 contrat à 500€ en 7 jours (4h de travail réel avec IA)""",
        "AUDIT FLUX ÉCONOMIQUE — Phase lancement Caelum Partners"
    )
    sauvegarder("audit_flux_lancement", r)


def optimiser_conditions_paiement():
    r = streamer(
        """Conçois les conditions de paiement optimales pour Caelum Partners.
Objectif : encaisser le plus vite possible, risque zéro de non-paiement.

POUR CHAQUE SERVICE :
- Site web 500€ : structure de paiement recommandée
- Automation IA 1500€ : structure de paiement recommandée
- Pack 3000€ : structure de paiement recommandée

POUR CHAQUE OPTION :
- Acompte % (50% ou 30% ?)
- Jalons de paiement intermédiaires
- Solde à la livraison ou J+15 ?
- Pénalités de retard légales Belgique (8% annuel légal)
- Clause de suspension de livraison si non-paiement
- Mention exacte à mettre dans le contrat

Inclure : template de CGV pour les conditions de paiement.""",
        "CONDITIONS DE PAIEMENT — Optimisation vélocité du capital"
    )
    sauvegarder("conditions_paiement", r)


def eliminer_frictions():
    r = streamer(
        """Identifie et élimine toutes les frictions dans le cycle commercial de Caelum Partners.
Du premier contact prospect jusqu'à l'encaissement final.

CARTOGRAPHIER CHAQUE ÉTAPE :
1. Prospect découvre Caelum → combien de jours avant premier contact ?
2. Premier message → rendez-vous : délai et friction
3. Rendez-vous → proposition : délai et friction
4. Proposition → signature : délai et friction
5. Signature → acompte reçu : délai et friction
6. Début travail → livraison : délai et friction
7. Livraison → paiement final : délai et friction

Pour chaque étape : délai actuel estimé, délai optimal, friction identifiée, correctif.
OBJECTIF TOTAL : de prospect à encaissement complet en moins de 21 jours.""",
        "ÉLIMINATION DES FRICTIONS — Du prospect à l'encaissement"
    )
    sauvegarder("elimination_frictions", r)


def maximiser_revenue_per_hour():
    r = streamer(
        """Calcule et maximise le Revenue per Hour (RPH) de Caelum Partners.
L'IA fait le travail — Chaima orchestre. Le RPH doit refléter cette réalité.

CALCULER LE RPH ACTUEL THÉORIQUE :
- Site web 500€ : temps réel Chaima (supervision IA) = estimé X heures → RPH = ?
- Automation IA 1500€ : temps réel = estimé Y heures → RPH = ?
- Pack 3000€ : temps réel = estimé Z heures → RPH = ?

COMPARER AVEC :
- Consultant standard : 100-150€/h
- Développeur web Belgique : 70-120€/h
- Agence web traditionnelle : 80-150€/h

IDENTIFIER :
- Quel service a le meilleur RPH ? → Prioriser dans la prospection
- Comment doubler le RPH sans augmenter les prix ? (automatisation additionnelle)
- Le package "récurrence" (maintenance mensuelle 300€/mois) : quel RPH ?

RECOMMANDATION : portefeuille de services optimal pour maximiser RPH total.""",
        "REVENUE PER HOUR — Maximiser le rendement du temps de Chaima"
    )
    sauvegarder("revenue_per_hour", r)


def tableau_bord_flux():
    """Charge les données JSON et génère un tableau de bord des flux."""
    donnees = {}
    for fichier, cle in [
        ("crm_pipeline.json", "pipeline"),
        ("memoire_entreprise.json", "memoire"),
        ("historique_caelum.json", "historique"),
    ]:
        if os.path.exists(fichier):
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    donnees[cle] = json.load(f)
            except Exception:
                donnees[cle] = {}

    r = streamer(
        f"""Génère le tableau de bord des flux économiques Caelum Partners.
Données disponibles : {json.dumps(donnees, ensure_ascii=False)[:2000]}

TABLEAU DE BORD FLUX ÉCONOMIQUE :
1. Flux entrants du mois (CA réalisé, acomptes reçus)
2. Flux sortants du mois (charges, cotisations, dépenses)
3. Flux en attente (factures émises non payées, pipeline en cours)
4. DSO actuel calculé
5. Capital Velocity Ratio
6. Revenue per Hour moyen
7. Projection flux mois prochain
8. UNE action pour accélérer les flux cette semaine""",
        "TABLEAU DE BORD FLUX ÉCONOMIQUE — Caelum Partners"
    )
    sauvegarder("tableau_bord_flux", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  FLUX ÉCONOMIQUE — Orchestrateur de vélocité du capital")
    print("  Chaque euro = énergie · Zéro friction · Rendement maximum")
    print("═"*65)

    while True:
        print("\n  1. Audit des flux économiques actuels")
        print("  2. Optimiser les conditions de paiement")
        print("  3. Éliminer les frictions (prospect → encaissement)")
        print("  4. Maximiser le Revenue per Hour")
        print("  5. Tableau de bord flux en temps réel")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            audit_flux_actuel()
        elif choix == "2":
            optimiser_conditions_paiement()
        elif choix == "3":
            eliminer_frictions()
        elif choix == "4":
            maximiser_revenue_per_hour()
        elif choix == "5":
            tableau_bord_flux()
        else:
            print("  Choix invalide.")
