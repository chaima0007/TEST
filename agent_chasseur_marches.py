"""
CHASSEUR DE MARCHÉS ÉMERGENTS — Détecter les opportunités avant les concurrents
Blue Ocean Strategy · Jobs-to-be-Done · Belgique d'abord · Expansion EU

Usage : python agent_chasseur_marches.py
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

IDENTITE = """# CHASSEUR DE MARCHÉS ÉMERGENTS — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es le Chasseur de Marchés Émergents de Caelum Partners.
Ta mission : détecter les nouvelles opportunités de marché AVANT que les concurrents
ne les voient. Scanner les signaux faibles, identifier les segments sous-servis,
cartographier les océans bleus. Belgique d'abord, puis expansion EU systématique.

## THÉORIE DES JOBS-TO-BE-DONE (Clayton Christensen)
Les clients n'achètent pas des produits — ils "engagent" un produit pour accomplir un "job".
Exemple : les PME n'achètent pas "de l'IA" — elles engagent l'IA pour "avoir plus de clients",
"gagner du temps", "réduire les coûts", "prendre de meilleures décisions".
Identifier le "job" réel = identifier le vrai marché = trouver les segments sous-servis.

Jobs non réalisés = opportunités de marché = marchés émergents.

## BLUE OCEAN STRATEGY (Kim & Mauborgne)
- OCÉAN ROUGE : marché existant, concurrence intense, prix sous pression (agences web classiques)
- OCÉAN BLEU : espace de marché non contesté, concurrence non pertinente, croissance rentable

Outil de base : CANEVAS STRATÉGIQUE
- Facteurs sur lesquels les concurrents se battent (prix, délai, équipe, bureaux)
- Facteurs à ÉLIMINER de cette bataille (coûts inutiles)
- Facteurs à RÉDUIRE en dessous du standard (prix des concurrents)
- Facteurs à AUGMENTER au-dessus du standard (vitesse, qualité IA)
- Facteurs à CRÉER que personne ne propose encore

## MARCHÉS ÉMERGENTS EN BELGIQUE (signaux détectés)
- PME belges cherchent à automatiser la gestion RH (paie, contrats, onboarding)
- Cabinets comptables belges cherchent à automatiser les rapports fiscaux
- PME du secteur médical cherchent à automatiser la prise de rendez-vous et le suivi patient
- Associations (ASBL) cherchent à automatiser les demandes de subventions
- PME logistiques cherchent à optimiser les routes et la gestion des stocks en temps réel
- Retailers belges cherchent à personnaliser l'expérience client (comme Amazon, mais accessible)

## PRINCIPES DE MARKET TIMING
- Trop tôt = évangélisation coûteuse (le marché n'est pas prêt)
- Au bon moment = croissance explosive (le marché cherche une solution)
- Trop tard = compétition acharnée en océan rouge
Signal du bon moment : les prospects cherchent activement une solution mais n'en trouvent pas.

## STRATÉGIE D'EXPANSION GÉOGRAPHIQUE CAELUM
Phase 1 : Bruxelles (0-12 mois) — marché test, bilinguisme, réseau ASBL
Phase 2 : Wallonie (mois 6-18) — extension naturelle francophone
Phase 3 : Luxembourg (mois 12-24) — high-value, anglophone, EU institutions
Phase 4 : France Nord (mois 18-36) — Lille, Dunkerque, Nord-Pas-de-Calais
Phase 5 : EU institutions Bruxelles (mois 24-48) — commandes publiques UE

## FORMAT DE SORTIE OBLIGATOIRE
1. SIGNAUX DE MARCHÉ : 5-10 signaux faibles détectés avec niveau de maturité
2. ANALYSE DU SEGMENT : taille, accessibilité, concurrence, fit Caelum
3. SCORE D'OPPORTUNITÉ : timing × taille × accessibilité × marge potentielle
4. CARTE GÉOGRAPHIQUE : prochaine ville/pays et justification
5. PREMIER PAS : action cette semaine pour tester l'opportunité identifiée"""


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
    os.makedirs("fichiers/marches_emergents", exist_ok=True)
    fichier = f"fichiers/marches_emergents/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def scanner_signaux_marche():
    r = streamer(
        """Identifie les signaux faibles de demande émergente dans le marché belge de l'IA pour les PME.

SCANNER 5 CATÉGORIES DE SIGNAUX :

1. SIGNAUX TECHNOLOGIQUES :
   - Quelles technologies IA commencent à être adoptées par les PME belges en 2024-2025 ?
   - Quels outils SaaS IA ont le plus de croissance en Belgique ?
   - Quelles intégrations IA cherchent les PME (avec leur ERP, CRM, comptabilité) ?

2. SIGNAUX DE COMPORTEMENT D'ACHAT :
   - Quelles questions les dirigeants de PME belges posent-ils sur LinkedIn sur l'IA ?
   - Quels événements IA à Bruxelles ont le plus de participants PME ?
   - Quelles recherches Google sont en forte croissance en Belgique (mots-clés IA PME) ?

3. SIGNAUX RÉGLEMENTAIRES :
   - Comment l'EU AI Act (2024) crée-t-il de nouveaux besoins pour les PME belges ?
   - Quelles obligations de conformité IA s'approchent (calendrier 2025-2026) ?
   - Subventions disponibles pour la digitalisation des PME en Belgique en 2025 ?

4. SIGNAUX SECTORIELS (secteurs en forte demande) :
   - Comptabilité et fiscalité : automatisation de tâches répétitives
   - RH et recrutement : screening CV, onboarding, formation
   - Marketing et vente : personnalisation, content creation, lead scoring
   - Logistique : optimisation des routes, gestion des stocks
   - Médical / paramédical : prise de rendez-vous, suivi patient, documentation

5. SIGNAUX CONCURRENTIELS :
   - Quels nouveaux entrants proposent de l'IA aux PME belges ?
   - Quels marchés sont encore vides de tout prestataire IA spécialisé PME ?

POUR CHAQUE SIGNAL : niveau de maturité (précoce / en croissance / mature), taille estimée du marché adressable, fenêtre d'opportunité (mois avant saturation).""",
        "SCANNER SIGNAUX MARCHÉ — Belgique IA pour PME"
    )
    sauvegarder("signaux_marche", r)


def analyser_segment_sous_servi():
    secteur = input("\n  Nomme le secteur à analyser (ex: 'comptabilité', 'RH', 'logistique') → ").strip()
    if not secteur:
        return
    r = streamer(
        f"""Analyse approfondie du segment sous-servi : {secteur} en Belgique.

JOBS-TO-BE-DONE DANS CE SECTEUR :
1. Quels sont les "jobs" fonctionnels que les professionnels du {secteur} cherchent à accomplir ?
2. Quels sont leurs "jobs" émotionnels (réduire le stress, paraître professionnel, sécuriser leur poste) ?
3. Quels sont leurs "jobs" sociaux (impressionner leurs clients, être reconnu comme expert) ?

ANALYSE DU SOUS-SERVICE :
- Quelles tâches dans le {secteur} prennent trop de temps et pourraient être automatisées ?
- Pourquoi les solutions actuelles ne conviennent-elles pas aux PME du {secteur} ?
- Quel est le coût annuel de ces inefficacités pour une PME type du {secteur} en Belgique ?

OPPORTUNITÉ CAELUM :
- Quel service spécifique Caelum pourrait créer pour le {secteur} ?
- Prix justifié par la valeur créée (temps économisé × taux horaire du secteur)
- Nombre de PME dans ce secteur en Belgique (taille du marché)
- Canal d'accès préférentiel (fédérations professionnelles, LinkedIn, événements)

CANEVAS BLUE OCEAN POUR LE {secteur.upper()} :
- Facteurs à éliminer : quels coûts des solutions actuelles sont inutiles pour le {secteur} ?
- Facteurs à réduire : qu'est-ce qui est surdimensionné pour les besoins réels ?
- Facteurs à augmenter : qu'est-ce qui manque cruellement aux solutions actuelles ?
- Facteurs à créer : quelle fonctionnalité n'existe nulle part pour le {secteur} ?

PLAN D'ENTRÉE SUR CE SEGMENT :
- 1 client test pour valider l'hypothèse : comment le trouver cette semaine ?
- Prix de test recommandé
- Indicateurs de validation (comment savoir si ce marché est porteur ?)""",
        f"ANALYSE SEGMENT SOUS-SERVI — {secteur.title()} Belgique"
    )
    sauvegarder(f"segment_{secteur.replace(' ', '_')}", r)


def evaluer_opportunite():
    opportunite = input("\n  Décris l'opportunité de marché à évaluer → ").strip()
    if not opportunite:
        return
    r = streamer(
        f"""Évalue cette opportunité de marché pour Caelum Partners avec un score structuré.
Opportunité : {opportunite}

SCORE D'OPPORTUNITÉ — 6 DIMENSIONS (note /10 chacune) :

1. TIMING (0-10) :
   - Le marché est-il prêt ? (trop tôt = 0, parfait = 10, trop tard = 3)
   - Signaux de maturité du marché
   - Fenêtre d'opportunité (combien de mois avant que ce marché soit saturé ?)

2. TAILLE DU MARCHÉ (0-10) :
   - Nombre de clients potentiels en Belgique
   - Valeur annuelle moyenne par client (€)
   - Marché total adressable (TAM) pour Caelum

3. CONCURRENCE (0-10) :
   - Nombre de concurrents directs actuels
   - Qualité et financement des concurrents
   - Barrières à l'entrée (10 = aucune concurrence)

4. FIT AVEC CAELUM (0-10) :
   - Caelum peut-elle servir ce marché avec ses agents IA actuels ?
   - Chaima a-t-elle les compétences et le réseau dans ce secteur ?
   - Délai pour créer l'offre (10 = offre existante, 0 = 12 mois de développement)

5. MARGE POTENTIELLE (0-10) :
   - Prix que le marché peut payer
   - Coût de service pour Caelum (temps + IA)
   - Marge nette estimée (10 = > 80%)

6. SCALABILITÉ (0-10) :
   - Cette opportunité peut-elle se répliquer dans d'autres villes/pays ?
   - Peut-elle devenir récurrente (abonnement) ?
   - Peut-elle être automatisée à > 80% ?

SCORE TOTAL /60 avec interprétation :
- 50-60 : opportunité exceptionnelle → foncer immédiatement
- 40-50 : bonne opportunité → tester dans les 30 jours
- 30-40 : opportunité moyenne → mettre en liste d'attente
- < 30 : passer

PLAN D'ACTION SI SCORE > 40 :
Actions des 7 prochains jours pour saisir cette opportunité.""",
        f"ÉVALUATION OPPORTUNITÉ — {opportunite[:40]}"
    )
    sauvegarder(f"evaluation_{opportunite[:25].replace(' ', '_')}", r)


def cartographier_expansion_geo():
    r = streamer(
        """Cartographie l'expansion géographique optimale de Caelum Partners — quelle ville/pays ensuite et quand.

ANALYSE DE L'EXPANSION GÉOGRAPHIQUE :

PHASE 1 — BRUXELLES (base actuelle) :
- Taille du marché PME (nombre d'entreprises 1-50 employés)
- Avantages de Bruxelles pour Caelum (capital EU, bilinguisme, réseau ASBL, densité)
- Objectifs à atteindre avant de s'étendre : CA minimum, nb clients, réputation
- Délai estimé : 6-12 mois

PHASE 2 — WALLONIE (expansion naturelle) :
- Marchés prioritaires : Liège, Namur, Charleroi, Mons
- Avantages : francophone, mêmes réglementations, accessibilité depuis Bruxelles
- Adaptation nécessaire : aucune (même langue, même loi)
- Délai estimé : mois 9-18
- Méthode d'entrée : événements entrepreneuriat wallon, réseau CCI

PHASE 3 — GRAND-DUCHÉ DE LUXEMBOURG (premium) :
- Taille du marché : PME luxembourgeoises (secteurs finance, consulting, EU institutions)
- Avantages : revenus 3-5x plus élevés qu'en Belgique, faible concurrence IA PME
- Adaptation nécessaire : anglais + luxembourgeois, facturation en différentes devises
- Délai estimé : mois 15-24

PHASE 4 — NORD DE LA FRANCE (Hauts-de-France) :
- Marchés : Lille, Roubaix, Dunkerque, Valenciennes
- Avantages : francophone, densité industrielle, PME cherchant à se digitaliser
- Adaptation nécessaire : TVA française, réglementation française, entité légale française
- Délai estimé : mois 18-30

PHASE 5 — INSTITUTIONS EUROPÉENNES BRUXELLES :
- Marchés : contractants UE, agences EU (EMA, EASA, etc.), lobbying firms
- Avantages : marchés publics importants, prix élevés acceptés
- Adaptation nécessaire : anglais, procédures appels d'offres EU, certifications

INDICATEURS DE PASSAGE À LA PHASE SUIVANTE :
Pour chaque transition : métriques précises (CA, clients, réputation) qui autorisent l'expansion.""",
        "CARTOGRAPHIE EXPANSION GÉOGRAPHIQUE — Caelum Partners EU"
    )
    sauvegarder("expansion_geographique", r)


def veille_concurrence_emergente():
    r = streamer(
        """Identifie les nouveaux entrants dans le marché de l'IA pour PME en Belgique avant qu'ils ne deviennent des menaces.

SURVEILLANCE DES NOUVEAUX ENTRANTS :

TYPES DE CONCURRENTS ÉMERGENTS À SURVEILLER :

1. STARTUPS IA BELGES EN PHASE PRÉ-LANCEMENT :
   - Comment les détecter : Crunchbase, LinkedIn, communautés startup Bruxelles, Hub.Brussels
   - Signaux d'alerte : levée de fonds, recrutement actif, présence à des événements
   - Délai moyen avant qu'une startup devienne une menace réelle : 12-24 mois
   - Stratégie de Caelum si concurrent identifié : accélérer, différencier, ou coopérer ?

2. AGENCES WEB TRADITIONNELLES QUI PIVOTENT VERS L'IA :
   - Comment les détecter : pages "Services IA" sur leur site web, offres d'emploi IA
   - Force : réseau client existant, réputation établie
   - Faiblesse : mindset traditionnel, coûts fixes élevés, transformation lente
   - Stratégie de Caelum : signer les clients avant leur pivot

3. GRANDS GROUPES CONSEIL (Accenture, Deloitte, PwC) QUI DESCENDENT VERS LES PME :
   - Signaux : lancement d'offres "SME AI" à prix plus accessibles
   - Délai probable avant qu'ils atteignent le marché PME belge : 18-36 mois
   - Stratégie de Caelum : construire une marque indestructible avant leur arrivée

4. OUTILS IA EN SELF-SERVICE QUI ÉLIMINENT LE BESOIN D'UN CONSULTANT :
   - Exemples : si ChatGPT Enterprise devient si simple que les PME n'ont plus besoin d'aide
   - Stratégie de Caelum : remonter dans la chaîne de valeur (stratégie, pas exécution)

TABLEAU DE VEILLE MENSUEL :
- Sources à consulter chaque mois (LinkedIn, Crunchbase, Trends.be, Startups.be)
- Questions à se poser chaque mois
- Seuil d'alerte qui déclenche une révision stratégique

OPPORTUNITÉS CRÉÉES PAR LES NOUVEAUX ENTRANTS :
- Éducation du marché faite par eux → Caelum bénéficie de leur travail
- Partenariats possibles avec certains concurrents émergents
- Acquisition ou rachat de clients d'un concurrent qui échoue""",
        "VEILLE CONCURRENCE ÉMERGENTE — Nouveaux entrants IA Belgique"
    )
    sauvegarder("veille_concurrence_emergente", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  CHASSEUR DE MARCHÉS ÉMERGENTS — Caelum Partners")
    print("  Blue Ocean · Jobs-to-be-Done · Belgique → EU")
    print("═"*65)

    while True:
        print("\n  1. Scanner les signaux du marché belge IA")
        print("  2. Analyser un segment sous-servi")
        print("  3. Évaluer une opportunité de marché")
        print("  4. Cartographier l'expansion géographique EU")
        print("  5. Veille sur la concurrence émergente")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            scanner_signaux_marche()
        elif choix == "2":
            analyser_segment_sous_servi()
        elif choix == "3":
            evaluer_opportunite()
        elif choix == "4":
            cartographier_expansion_geo()
        elif choix == "5":
            veille_concurrence_emergente()
        else:
            print("  Choix invalide.")
