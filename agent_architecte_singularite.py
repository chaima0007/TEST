"""
ARCHITECTE DE LA SINGULARITÉ — Concevoir l'avantage concurrentiel imbattable de Caelum
Mission : rendre Caelum Partners impossible à copier · Moats · Positionnement premium

Usage : python agent_architecte_singularite.py
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

IDENTITE = """# ARCHITECTE DE LA SINGULARITÉ — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es l'Architecte de la Singularité de Caelum Partners.
Ta mission : identifier, concevoir et cristalliser l'avantage concurrentiel imbattable —
le moat (fossé défensif) que AUCUN concurrent ne peut copier, acheter ou contourner.

## THÉORIE DES MOATS (Warren Buffett / Pat Dorsey)
Les 4 types de moats structurels :
1. EFFETS DE RÉSEAU : chaque nouveau client augmente la valeur pour tous (ex: LinkedIn)
2. COÛTS DE CHANGEMENT (Switching Costs) : quitter Caelum coûte plus cher que rester
3. ACTIFS INTANGIBLES : marque, réputation, données propriétaires, expertise rare
4. AVANTAGES DE COÛT : livrer moins cher que tout concurrent grâce à l'IA

## COMMENT L'IA CRÉE DES MOATS STRUCTURELS
- Les 50+ agents IA constituent un système propriétaire — aucun concurrent ne peut dupliquer
  l'écosystème entier sans des années de développement
- Chaque client intégré dans le système crée des données propriétaires non transférables
- L'automatisation permet des marges 85-95% que les agences traditionnelles ne peuvent atteindre
- La vitesse de livraison (7 jours vs 3 mois agence) crée une expérience client inégalable

## ACTIFS UNIQUES DE CHAIMA MHADBI
- Bilingue FR/NL : accès à 100% du marché belge (Wallonie + Bruxelles + Flandre)
- Bruxelles : capitale de l'UE, hub économique, accès aux institutions européennes
- Crédibilité ASBL : signal de confiance et d'engagement social fort
- Écosystème 50+ agents : impossible à répliquer en moins de 12 mois
- Profil atypique : femme, jeune, multilingue dans un secteur majoritairement masculin

## POSITIONNEMENT PREMIUM — ARCHITECTURE DE LA RARETÉ
- Prix premium justifié par la rareté (pas par le coût)
- La singularité rend la comparaison de prix impossible
- Objectif : être si unique que le client ne cherche plus d'alternative
- Un moat puissant = pricing power illimité sur le long terme

## FORMAT DE SORTIE OBLIGATOIRE
1. AUDIT DU MOAT ACTUEL : forces et faiblesses de la position défensive actuelle
2. CONCEPTION DU MOAT ULTIME : le fossé impossible à franchir pour tout concurrent
3. PLAN DE CONSTRUCTION : étapes concrètes pour construire ce moat en 12 mois
4. MÉTRIQUES DE SOLIDITÉ : comment mesurer la robustesse du moat
5. STRATÉGIE PREMIUM : justification du prix premium par l'architecture de rareté"""


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
    os.makedirs("fichiers/singularite", exist_ok=True)
    fichier = f"fichiers/singularite/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def analyser_avantage_concurrentiel():
    r = streamer(
        """Analyse l'avantage concurrentiel actuel de Caelum Partners face au marché belge de l'IA.

CARTOGRAPHIER LES MOATS ACTUELS :
1. Effet de réseau : existe-t-il ? À quel stade ? Comment l'activer ?
2. Coûts de changement : qu'est-ce qui retient un client chez Caelum vs un concurrent ?
3. Actifs intangibles : marque, réputation, données, expertise de Chaima (bilingue, ASBL, Brussels)
4. Avantage de coût : structure 85-95% de marge vs agences traditionnelles — comment l'utiliser ?

COMPARAISON CONCURRENTS BELGES :
- Agences web traditionnelles (Bruxelles) : forces et faiblesses vs Caelum
- Freelances IA : forces et faiblesses vs Caelum
- Grands cabinets conseil (Accenture, Deloitte) : forces et faiblesses vs Caelum

SCORE DE CHAQUE MOAT /10 avec justification chiffrée.
CONCLUSION : quel est le moat le plus solide aujourd'hui et lequel construire en priorité ?""",
        "ANALYSE AVANTAGE CONCURRENTIEL — Caelum Partners vs marché belge"
    )
    sauvegarder("avantage_concurrentiel", r)


def concevoir_moat_unique():
    r = streamer(
        """Conçois le moat ULTIME de Caelum Partners — l'avantage qu'aucun concurrent ne peut copier.

PROCESSUS DE CONCEPTION :
1. Identifier les ressources uniques de Chaima (bilingue, ASBL, 50 agents, Brussels)
2. Identifier les capacités que ces ressources créent (accès 100% marché belge, vitesse livraison, crédibilité)
3. Identifier les avantages concurrentiels que ces capacités génèrent
4. Identifier le moat structurel qui découle de ces avantages

CONCEVOIR LE MOAT EN 3 COUCHES :
- Couche 1 — Moat de VITESSE : livraison 10x plus rapide → switching cost psychologique
- Couche 2 — Moat de DONNÉES : chaque client crée des données propriétaires Caelum
- Couche 3 — Moat d'ÉCOSYSTÈME : 50 agents interconnectés = système que personne ne peut dupliquer

PLAN DE CONSTRUCTION DU MOAT :
- Actions des 30 premiers jours pour commencer à construire ce moat
- Actions mois 3, 6, 12 avec métriques de progression
- Comment transformer chaque client en ambassadeur du moat (référence, cas d'usage, données)

CONCLUSION : la formulation en 1 phrase du moat ultime de Caelum Partners.""",
        "CONCEPTION DU MOAT ULTIME — Caelum Partners"
    )
    sauvegarder("moat_unique", r)


def audit_copiabilite():
    strategie = input("\n  Décris la stratégie ou l'offre à auditer → ").strip()
    if not strategie:
        return
    r = streamer(
        f"""Audit de copiabilité — analyser ce qui peut être copié dans cette stratégie :
Stratégie : {strategie}

ANALYSE EN 3 DIMENSIONS :

1. CE QUI PEUT ÊTRE COPIÉ EN < 30 JOURS :
   - Éléments facilement copiables par un concurrent bien financé
   - Coût estimé pour un concurrent de copier chaque élément
   - Délai de copie réaliste

2. CE QUI PEUT ÊTRE COPIÉ EN 6-12 MOIS :
   - Éléments copiables mais coûteux en temps/argent
   - Barrières à la copie (technique, réseau, réputation)

3. CE QUI NE PEUT PAS ÊTRE COPIÉ :
   - Éléments structurellement non-copiables (données propriétaires, réseau personnel, ASBL, expérience accumulée)
   - Pourquoi c'est non-copiable (théorie)

PLAN DE PROTECTION :
Pour chaque élément copiable : comment le rendre non-copiable ?
Actions concrètes cette semaine pour renforcer les barrières à la copie.""",
        f"AUDIT COPIABILITÉ — {strategie[:40]}"
    )
    sauvegarder("audit_copiabilite", r)


def roadmap_singularite():
    r = streamer(
        """Génère la roadmap 12 mois pour rendre Caelum Partners structurellement unique et non-copiable.

ROADMAP MENSUELLE :

MOIS 1-2 — FONDATIONS DU MOAT :
- Actions pour activer les premiers coûts de changement chez les clients
- Documentation de l'écosystème 50 agents comme actif propriétaire
- Premières preuves sociales (références, cas d'usage)

MOIS 3-4 — CONSTRUCTION DES ACTIFS INTANGIBLES :
- Stratégie de contenu pour établir Chaima comme autorité IA belge
- Premiers partenariats (Hub.Brussels, ULB, accélérateurs)
- Données propriétaires clients : comment les capturer et valoriser

MOIS 5-6 — ACTIVATION DES EFFETS DE RÉSEAU :
- Programme de référencement client-à-client
- Communauté d'utilisateurs Caelum (forum, newsletter, événements)
- Partenariats qui créent des effets de réseau (intégrateurs, revendeurs)

MOIS 7-12 — SINGULARITÉ EUROPÉENNE :
- Expansion géographique : Bruxelles → Wallonie → France → Luxembourg
- Certifications et labels qui bloquent l'entrée de concurrents
- Écosystème de partenaires qui dépendent de Caelum

MÉTRIQUES DE SINGULARITÉ À SUIVRE CHAQUE MOIS :
- Taux de churn (objectif < 5%)
- Net Promoter Score (objectif > 70)
- Mentions dans la presse belge
- Nombre de partenaires actifs""",
        "ROADMAP SINGULARITÉ 12 MOIS — Rendre Caelum impossible à copier"
    )
    sauvegarder("roadmap_singularite", r)


def positionnement_premium():
    r = streamer(
        """Justifie le positionnement premium de Caelum Partners par l'analyse du moat.

ARCHITECTURE DU PRIX PREMIUM :

1. POURQUOI LE PREMIUM EST JUSTIFIÉ (argumentation par le moat) :
   - Site web 500€ vs agence traditionnelle 3000€ : Caelum est moins cher ET meilleur → sous-évalué
   - Automation IA 1500€ vs développeur traditionnel 15 000€ : économie de 90%
   - Pack 3000€ vs consultant senior 30 000€ : même résultat, 1/10 du coût

2. COMMENT VENDRE LE PREMIUM SANS JUSTIFIER LE PRIX :
   - Technique du "prix d'ancrage" : montrer le coût alternatif
   - Technique de la "valeur perçue" : résultat > prix
   - Technique du "prix de la singularité" : il n'y a pas d'équivalent → pas de comparaison possible

3. STRUCTURE DE PRIX PREMIUM POUR LES 12 PROCHAINS MOIS :
   - Quand augmenter les prix (après combien de clients, quels signaux)
   - Services à créer pour justifier des prix encore plus élevés (500€ → 1500€ → 5000€ → 15 000€)
   - Services récurrents pour créer de la prévisibilité premium

4. SCRIPT DE VENTE BASÉ SUR LE MOAT :
   - Comment expliquer la valeur unique de Caelum en 3 minutes
   - Réponse aux objections "c'est cher" ou "je peux trouver moins cher"
   - Closing basé sur la singularité (pas sur le prix)""",
        "POSITIONNEMENT PREMIUM — Justification par le moat Caelum Partners"
    )
    sauvegarder("positionnement_premium", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ARCHITECTE DE LA SINGULARITÉ — Caelum Partners")
    print("  Moats · Avantage imbattable · Positionnement premium")
    print("═"*65)

    while True:
        print("\n  1. Analyser l'avantage concurrentiel actuel")
        print("  2. Concevoir le moat unique imbattable")
        print("  3. Audit de copiabilité d'une stratégie")
        print("  4. Roadmap 12 mois vers la singularité")
        print("  5. Justifier le positionnement premium")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            analyser_avantage_concurrentiel()
        elif choix == "2":
            concevoir_moat_unique()
        elif choix == "3":
            audit_copiabilite()
        elif choix == "4":
            roadmap_singularite()
        elif choix == "5":
            positionnement_premium()
        else:
            print("  Choix invalide.")
