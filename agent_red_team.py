"""
AGENT RED TEAM ARCHITECT — Simulateur de stress et résilience système
Scénarios Black Swan · Détection de failles · Correctifs immédiats
Mission : rendre le système Caelum Partners INVINCIBLE

Usage : python agent_red_team.py
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

IDENTITE = """# AGENT RED TEAM ARCHITECT — SIMULATEUR DE STRESS

## IDENTITÉ ET RÔLE
Tu es le Red Team Architect de Caelum Partners.
Ton rôle est de tester la résilience de chaque stratégie, décision ou système
par des scénarios de crise extrêmes ("Black Swan") pour renforcer la structure
SANS jamais bloquer l'innovation.

Ta mission : trouver les failles AVANT que la réalité ne les trouve.
Ta directive : ton objectif n'est PAS de freiner — c'est de rendre le système INVINCIBLE.

## CONTEXTE DES ENTREPRISES DE CHAIMA MHADBI
1. CAELUM PARTNERS (activité commerciale IA)
   - Services : Site web 500€ / Automation IA 1500€ / Pack 3000€
   - Phase : lancement, 0 clients, Bruxelles
   - Dépendances critiques : API Gemini (Google), GEMINI_API_KEY, un seul laptop, Chaima seule

2. ASBL (association sans but lucratif)
   - Chaima en est présidente
   - Séparée légalement de Caelum Partners
   - Risque : confusion de patrimoines si mélangées

## FRAMEWORK RED TEAM QUE TU APPLIQUES

### NIVEAUX DE SCÉNARIOS
- NIVEAU 1 — Friction courante : client qui ne paie pas, prospect fantôme, bug technique
- NIVEAU 2 — Crise sectorielle : concurrence agressive, baisse de prix du marché, RGPD audit
- NIVEAU 3 — Black Swan : Google coupe l'API Gemini sans préavis, Chaima tombe malade 3 semaines,
  ONEM suspend les allocations, cyberattaque sur le système, catastrophe financière client
- NIVEAU 4 — Scénario catastrophe : faillite, poursuite judiciaire, violation de données massif

### PROCESSUS D'ANALYSE RED TEAM (pour chaque scénario)
1. DÉCLENCHEUR : qu'est-ce qui déclenche exactement ce scénario ?
2. PROPAGATION : comment ça se propage dans le système Caelum Partners ?
3. IMPACT CHIFFRÉ : perte financière estimée, délai de récupération, probabilité (%)
4. FAILLE IDENTIFIÉE : quelle faiblesse structurelle a permis ce scénario ?
5. CORRECTIF IMMÉDIAT : action à prendre dans les 24h
6. CORRECTIF STRUCTUREL : modification permanente du système pour éviter la récurrence

### SINGLE POINTS OF FAILURE À SURVEILLER (Caelum Partners)
- Dépendance unique : une seule API IA (Gemini) → Plan B : Claude, OpenAI, Mistral
- Dépendance unique : une seule personne (Chaima) → Plan B : documentation, agents autonomes
- Dépendance unique : zéro client → Plan B : avoir 3 prospects qualifiés en pipeline permanent
- Dépendance unique : revenus non diversifiés → Plan B : abonnements récurrents dès client 3
- Conformité légale : ONEM/INASTI non déclarés → risque remboursement allocations
- Sécurité : clé API Gemini unique exposée → rotation trimestrielle obligatoire

## FORMAT DE SORTIE OBLIGATOIRE
1. SCÉNARIO TESTÉ : description précise du Black Swan simulé
2. SIMULATION D'IMPACT :
   | Paramètre | Impact |
   | Probabilité | X% |
   | Délai avant effet | X jours/semaines |
   | Perte financière estimée | X€ |
   | Délai de récupération | X semaines |
3. FAILLES DÉTECTÉES : liste des vulnérabilités exposées par ce scénario
4. PLAN DE RÉSILIENCE : correctif immédiat (24h) + correctif structurel (30 jours)
5. SCORE DE RÉSILIENCE : note /100 du système AVANT et APRÈS correctifs"""


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
    os.makedirs("fichiers/red_team", exist_ok=True)
    fichier = f"fichiers/red_team/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def stress_test_strategie():
    strategie = input("\n  Décris la stratégie ou décision à tester → ").strip()
    if not strategie:
        return
    r = streamer(
        f"""STRESS TEST — Soumettre cette stratégie à 5 scénarios de crise :
Stratégie : {strategie}

Tester avec :
1. Scénario NIVEAU 1 : le cas probable (client problématique, retard)
2. Scénario NIVEAU 2 : la crise sectorielle (concurrent IA moins cher, RGPD)
3. Scénario NIVEAU 3 : le Black Swan (API coupée, Chaima malade, ONEM bloque)
4. Scénario NIVEAU 4 : le pire cas absolu
5. Scénario POSITIF inversé : et si ça marche 10x mieux que prévu — le système tient ?

Pour chaque scénario : impact chiffré + faille exposée + correctif.""",
        f"STRESS TEST — {strategie[:50]}"
    )
    sauvegarder("stress_test", r)


def audit_resilience_complet():
    r = streamer(
        """Effectue un audit de résilience complet du système Caelum Partners.

ANALYSER TOUS LES SINGLE POINTS OF FAILURE :
1. Dépendance technologique (Gemini API seule)
2. Dépendance humaine (Chaima seule)
3. Dépendance financière (0 client = 0 revenu)
4. Dépendance légale (ONEM non déclaré, ASBL mal séparée)
5. Dépendance sécurité (une seule clé API, données non sauvegardées)
6. Dépendance réputation (0 avis client, 0 référence)

Pour chaque point : probabilité de défaillance (%), impact (€), délai de récupération,
correctif immédiat et correctif structurel.

Conclure avec le SCORE DE RÉSILIENCE GLOBAL /100 et le plan de renforcement prioritaire.""",
        "AUDIT RÉSILIENCE COMPLET — Caelum Partners"
    )
    sauvegarder("audit_resilience", r)


def simuler_black_swan():
    print("\n  SCÉNARIOS BLACK SWAN DISPONIBLES :")
    print("  [A] Google coupe l'API Gemini sans préavis (24h)")
    print("  [B] Chaima tombe gravement malade 3 semaines")
    print("  [C] ONEM réclame un remboursement de 6 mois d'allocations")
    print("  [D] Un client attaque en justice pour mauvaise livraison")
    print("  [E] Cyberattaque — données clients compromises")
    print("  [F] Concurrent IA propose les mêmes services à 100€")
    print("  [G] Saisir un scénario personnalisé")

    choix = input("\n  Choix → ").strip().upper()
    scenarios = {
        "A": "Google coupe l'accès à l'API Gemini sans préavis dans 24 heures",
        "B": "Chaima tombe gravement malade et ne peut pas travailler pendant 3 semaines",
        "C": "L'ONEM réclame le remboursement de 6 mois d'allocations versées indûment",
        "D": "Un client attaque Caelum Partners en justice pour non-livraison ou mauvaise qualité",
        "E": "Cyberattaque : données de tous les clients compromises et publiées en ligne",
        "F": "Un concurrent IA bien financé propose les mêmes services à 100€ en ciblant les mêmes clients",
    }

    scenario = scenarios.get(choix)
    if choix == "G" or not scenario:
        scenario = input("  Décris le scénario → ").strip()
    if not scenario:
        return

    r = streamer(
        f"""BLACK SWAN SIMULATION — Scénario : {scenario}

Analyse complète :
1. Déclencheur exact et timeline (heure par heure les premières 48h)
2. Propagation dans le système Caelum Partners
3. Impact financier chiffré (perte immédiate + perte indirecte sur 3 mois)
4. Failles structurelles exposées par ce scénario
5. Plan de survie immédiat (premières 24h)
6. Reconstruction (semaines 1 à 4)
7. Mesures préventives pour que ce scénario ne puisse plus jamais se produire""",
        f"BLACK SWAN — {scenario[:50]}"
    )
    sauvegarder("black_swan", r)


def plan_continuite():
    r = streamer(
        """Crée le Plan de Continuité d'Activité (PCA) complet pour Caelum Partners.
Un PCA pour une solopreneuse avec des agents IA comme seuls collaborateurs.

COUVRIR :
1. Si Chaima est indisponible 1 semaine : quels agents tournent en autonome ?
2. Si l'API Gemini tombe : plan de basculement vers une autre IA (Claude, OpenAI)
3. Si un client annule le paiement : procédure légale et impact sur trésorerie
4. Si les données sont perdues : stratégie de sauvegarde et récupération
5. Si le laptop tombe en panne : accès aux données depuis n'importe où
6. Contacts d'urgence à avoir dans son téléphone (CSC, comptable, avocat, hébergeur)

FORMAT : document opérationnel que Chaima peut suivre dans le stress, pas une théorie.""",
        "PLAN DE CONTINUITÉ D'ACTIVITÉ — Caelum Partners"
    )
    sauvegarder("plan_continuite", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  RED TEAM ARCHITECT — Simulateur de stress Caelum Partners")
    print("  Scénarios Black Swan · Failles · Résilience · Invincibilité")
    print("═"*65)

    while True:
        print("\n  1. Stress test d'une stratégie ou décision")
        print("  2. Audit de résilience complet du système")
        print("  3. Simulation Black Swan (scénarios catastrophe)")
        print("  4. Plan de continuité d'activité (PCA)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            stress_test_strategie()
        elif choix == "2":
            audit_resilience_complet()
        elif choix == "3":
            simuler_black_swan()
        elif choix == "4":
            plan_continuite()
        else:
            print("  Choix invalide.")
