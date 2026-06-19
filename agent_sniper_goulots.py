"""
SNIPER DES GOULOTS D'ÉTRANGLEMENT — Éliminer tous les blocages opérationnels avec précision chirurgicale
Théorie des Contraintes (TOC) · Débit maximal · Throughput engineering

Usage : python agent_sniper_goulots.py
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

IDENTITE = """# SNIPER DES GOULOTS D'ÉTRANGLEMENT — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Sniper des Goulots d'Étranglement de Caelum Partners.
Ta mission : identifier et éliminer TOUS les blocages opérationnels avec une précision chirurgicale.
Un goulot d'étranglement est toute étape qui limite le débit total du système.
Ton objectif : maximiser le throughput (CA généré par unité de temps).

## THÉORIE DES CONTRAINTES (TOC) — ELIYAHU GOLDRATT
Les 5 étapes fondamentales du TOC :
1. IDENTIFIER la contrainte (le goulot qui limite tout le système)
2. EXPLOITER la contrainte (maximiser son débit sans investissement additionnel)
3. SUBORDONNER tout le reste à la contrainte (aligner toutes les étapes sur le goulot)
4. ÉLEVER la contrainte (investir pour augmenter sa capacité si nécessaire)
5. RECOMMENCER (identifier la nouvelle contrainte après correction)

## GOULOTS TYPIQUES DU CONSULTANT IA SOLO
- PROSPECTION : trouver des prospects qualifiés (goulot le plus fréquent au lancement)
- QUALIFICATION : identifier rapidement si un prospect peut devenir client
- CLOSING : convertir un prospect qualifié en client payant
- LIVRAISON : produire la prestation dans les délais promis
- FACTURATION & ENCAISSEMENT : transformer la livraison en cash réel
- APPRENTISSAGE : rester à jour sur les nouvelles fonctionnalités IA

## MESURER LE THROUGHPUT PAR ÉTAPE
Pour chaque étape du workflow Caelum :
- Débit entrant (inputs par semaine)
- Débit sortant (outputs par semaine)
- Ratio : si sortant < entrant → GOULOT IDENTIFIÉ
- Exemple : 10 prospects contactés → 2 rendez-vous → 1 proposition → 0 client = goulot au closing

## MÉTRIQUES DE DÉTECTION DES GOULOTS
- Temps d'attente entre étapes (idle time) : une file d'attente = goulot en amont
- WIP (Work In Progress) : trop de projets en cours = goulot en livraison
- Taux de conversion par étape : < 20% sur une étape = goulot potentiel
- Temps de cycle complet : de prospect à encaissement > 30 jours = goulot non résolu

## FORMAT DE SORTIE OBLIGATOIRE
1. CARTOGRAPHIE DES GOULOTS : tous les goulots identifiés avec débit mesuré
2. GOULOT PRIORITAIRE #1 : le seul à traiter cette semaine (Goldratt : une contrainte à la fois)
3. PLAN D'ÉLIMINATION : actions concrètes en 24h, 72h, 7 jours
4. WORKFLOW OPTIMAL : le flux parfait sans aucun goulot
5. INDICATEURS DE SUIVI : métriques pour confirmer l'élimination du goulot"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/goulots", exist_ok=True)
    fichier = f"fichiers/goulots/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def identifier_goulots():
    r = streamer(
        """Cartographie TOUS les goulots d'étranglement actuels dans le workflow Caelum Partners.

WORKFLOW COMPLET À ANALYSER (phase lancement, 0 clients actuellement) :

ÉTAPE 1 — GÉNÉRATION DE LEADS :
- Sources actuelles : réseau personnel, LinkedIn, bouche-à-oreille, ASBL contacts
- Débit estimé : X prospects identifiés par semaine
- Goulot probable : visibilité insuffisante → actions pour débloquer

ÉTAPE 2 — QUALIFICATION DES PROSPECTS :
- Critères de qualification pour Caelum (budget, besoin IA, décideur accessible)
- Débit : X prospects → Y qualifiés
- Goulot probable : pas de processus de qualification structuré

ÉTAPE 3 — PRISE DE RENDEZ-VOUS :
- Canaux de contact (LinkedIn, email, téléphone, événements)
- Taux de réponse estimé
- Goulot probable : message de prospection non optimisé

ÉTAPE 4 — CLOSING :
- Processus de proposition et négociation
- Taux de conversion estimé (industry standard : 20-30%)
- Goulot probable : absence de social proof au lancement

ÉTAPE 5 — LIVRAISON :
- Temps de production avec les 50 agents IA
- Goulot probable : supervision et révisions client

ÉTAPE 6 — ENCAISSEMENT :
- Délai paiement / acompte / solde
- Goulot probable : client lent à payer

Pour chaque étape : débit mesuré, goulot identifié, impact sur le CA mensuel, correctif immédiat.""",
        "CARTOGRAPHIE DES GOULOTS — Workflow complet Caelum Partners"
    )
    sauvegarder("cartographie_goulots", r)


def analyser_throughput():
    etape = input("\n  Nomme l'étape à analyser (ex: 'closing', 'prospection', 'livraison') → ").strip()
    if not etape:
        return
    r = streamer(
        f"""Analyse de throughput pour l'étape : {etape}

MESURE DU THROUGHPUT :
1. Définir précisément ce que produit cette étape (output)
2. Mesurer la capacité maximale théorique (unités par semaine)
3. Mesurer la capacité réelle actuelle (compte tenu des frictions)
4. Calculer le ratio d'efficacité (réel / théorique × 100)

IDENTIFIER LA CONTRAINTE INTERNE À CETTE ÉTAPE :
- Qu'est-ce qui limite le débit de cette étape spécifique ?
- Est-ce une contrainte de RESSOURCE (temps de Chaima) ?
- Est-ce une contrainte de MARCHÉ (pas assez de prospects) ?
- Est-ce une contrainte de POLITIQUE (processus trop rigide) ?

CALCULER L'IMPACT SUR LE CA :
- Si cette étape est améliorée de 50% → impact sur le CA mensuel
- Si cette étape est améliorée de 100% → impact sur le CA mensuel
- ROI de l'investissement pour améliorer cette étape (temps × résultat)

PLAN D'OPTIMISATION EN 3 ACTIONS :
Action 1 (aujourd'hui) : quick win immédiat
Action 2 (cette semaine) : amélioration structurelle
Action 3 (ce mois) : automatisation ou délégation aux agents IA""",
        f"ANALYSE THROUGHPUT — Étape : {etape}"
    )
    sauvegarder(f"throughput_{etape.replace(' ', '_')}", r)


def eliminer_goulot_prioritaire():
    r = streamer(
        """Identifie le goulot #1 de Caelum Partners cette semaine et fournis le plan d'élimination.

PHASE LANCEMENT CAELUM : le goulot numéro 1 est probablement la GÉNÉRATION DE PREMIERS CLIENTS.

APPLIQUER LES 5 ÉTAPES TOC SUR CE GOULOT :

1. IDENTIFIER (confirmé) :
   - Le goulot est : aucun client = 0 revenue = 0 preuve sociale = difficulté à obtenir le suivant
   - Impact : CA = 0€, trésorerie = allocations ONEM uniquement

2. EXPLOITER le goulot (maximiser sans investissement) :
   - Actions gratuites et immédiates pour obtenir le premier client cette semaine
   - Utiliser le réseau de l'ASBL comme premier vivier de prospects
   - LinkedIn : 10 messages de prospection personnalisés par jour
   - Offre de lancement spéciale pour briser le cercle vicieux (premier client à prix réduit ou gratuit ?)

3. SUBORDONNER tout le reste au goulot :
   - Ne pas travailler sur le SEO, les agents, la compta si le goulot est la prospection
   - 80% du temps de Chaima cette semaine = activités qui génèrent des prospects

4. ÉLEVER le goulot si nécessaire :
   - Si le réseau personnel est épuisé : événements networking Bruxelles
   - Si LinkedIn ne convertit pas : optimiser le profil + automatiser avec un agent LinkedIn

5. PLAN D'ACTION CETTE SEMAINE (jour par jour) :
   - Lundi : X actions
   - Mardi : Y actions
   - Mercredi-Vendredi : Z actions
   - Objectif : 1 rendez-vous qualifié minimum d'ici vendredi""",
        "ÉLIMINATION GOULOT PRIORITAIRE #1 — Plan d'action cette semaine"
    )
    sauvegarder("elimination_goulot_prioritaire", r)


def concevoir_workflow_optimal():
    r = streamer(
        """Conçois le workflow PARFAIT de Caelum Partners — zéro goulot, débit maximum.

WORKFLOW CIBLE (à atteindre dans 90 jours) :

SYSTÈME DE GÉNÉRATION DE LEADS AUTOMATIQUE :
- Sources passives : contenu LinkedIn, SEO, ASBL réseau, partenariats
- Sources actives : prospection automatisée par agent IA, événements mensuels
- Débit cible : 20 prospects qualifiés par semaine minimum

QUALIFICATION AUTOMATIQUE :
- Agent IA de pré-qualification (email ou LinkedIn bot)
- Critères binaires : budget OK ? Besoin IA confirmé ? Décideur accessible ?
- Débit cible : 5 rendez-vous qualifiés par semaine

CLOSING SYSTEMATISÉ :
- Proposition générée par agent IA en 2h max
- Signature électronique (DocuSign ou Docusign-like gratuit)
- Débit cible : 1-2 clients signés par semaine

LIVRAISON INDUSTRIALISÉE :
- Site web 500€ : livré en 72h avec agents IA (pas 7 jours)
- Automation 1500€ : livré en 7 jours (pas 14 jours)
- Pack 3000€ : livré en 15 jours (pas 30 jours)
- Débit cible : 3-5 projets simultanés sans goulot

ENCAISSEMENT ZERO-FRICTION :
- Acompte 50% avant démarrage (automatique)
- Solde à la livraison (automatique via lien de paiement)
- Débit cible : DSO ≤ 7 jours

MÉTRIQUES DU WORKFLOW OPTIMAL :
- CA mensuel cible : 15 000€ (5 projets × 3 000€ moyen)
- Temps Chaima par projet : 4h max (IA fait le reste)
- Revenue per Hour : > 750€/h""",
        "WORKFLOW OPTIMAL — Caelum Partners zéro goulot"
    )
    sauvegarder("workflow_optimal", r)


def mesures_preventives():
    r = streamer(
        """Conçois les mesures préventives pour éviter l'apparition de nouveaux goulots dans Caelum Partners.

PRÉVENTION PAR CONCEPTION (Design for Flow) :

1. RÈGLE DES 20% DE CAPACITÉ :
   - Ne jamais utiliser plus de 80% de la capacité de chaque étape
   - Le 20% restant est le buffer contre les imprévus
   - Comment appliquer cette règle à Caelum (charge de travail de Chaima)

2. INDICATEURS D'ALERTE PRÉCOCE :
   - Signal d'alerte 1 : pipeline < 3 prospects qualifiés → action immédiate
   - Signal d'alerte 2 : WIP > 3 projets simultanés → arrêter la prospection
   - Signal d'alerte 3 : DSO > 15 jours → relance immédiate
   - Signal d'alerte 4 : temps de livraison > 50% du délai promis → appel client

3. MÉCANISMES D'AUTO-RÉGULATION :
   - Liste d'attente clients : créer la perception de rareté ET gérer le débit
   - Tarification dynamique : prix plus élevé si carnet de commandes plein
   - Délégation aux agents IA dès que Chaima dépasse 30h/semaine

4. REVUE HEBDOMADAIRE DES GOULOTS (15 minutes le lundi) :
   - Checklist des 6 étapes du workflow
   - Identifier la nouvelle contrainte émergente
   - Une action corrective par semaine

5. ARCHITECTURE ANTI-GOULOT LONG TERME :
   - Quand recruter un premier collaborateur (et lequel) pour éviter le goulot humain
   - Quels outils/automatisations déployer à 10K€/mois, 30K€/mois, 100K€/mois""",
        "MESURES PRÉVENTIVES — Architecture anti-goulot Caelum Partners"
    )
    sauvegarder("mesures_preventives", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  SNIPER DES GOULOTS D'ÉTRANGLEMENT — Caelum Partners")
    print("  TOC · Throughput · Élimination chirurgicale des blocages")
    print("═"*65)

    while True:
        print("\n  1. Identifier tous les goulots du workflow")
        print("  2. Analyser le throughput d'une étape spécifique")
        print("  3. Éliminer le goulot prioritaire #1 (plan cette semaine)")
        print("  4. Concevoir le workflow optimal zéro goulot")
        print("  5. Mesures préventives anti-goulot")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            identifier_goulots()
        elif choix == "2":
            analyser_throughput()
        elif choix == "3":
            eliminer_goulot_prioritaire()
        elif choix == "4":
            concevoir_workflow_optimal()
        elif choix == "5":
            mesures_preventives()
        else:
            print("  Choix invalide.")
