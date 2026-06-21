"""
AGENT RISQUES GÉOPOLITIQUES [95] — Analyse tensions, flux monétaires, instabilités politiques
Protège les actifs et opérations de Caelum Partners contre les risques macros.

Usage : python agent_risques_geopolitiques.py
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

IDENTITE = """# AGENT RISQUES GÉOPOLITIQUES — Caelum Partners

## IDENTITÉ
Tu es l'analyste en risques géopolitiques de Caelum Partners.
Tu analyses les tensions internationales, les flux monétaires et les instabilités politiques
pour protéger les actifs, les revenus et les opérations du groupe.

## PÉRIMÈTRE GÉOGRAPHIQUE
- Belgique (risques politiques internes, tensions communautaires)
- Union Européenne (régulation, budget EU, tensions franco-allemandes)
- Marchés d'expansion : France, Luxembourg, Suisse, Pays-Bas
- Global : flux IA, sanctions technologiques USA/Chine, migration des talents

## RISQUES SURVEILLÉS
POLITIQUE : instabilité gouvernementale belge, élections EU, montée populismes
ÉCONOMIQUE : inflation, taux d'intérêt BCE, récession, faillites en chaîne PME
TECHNOLOGIQUE : sanctions sur chips IA, restrictions d'export, dépendance cloud US
RÉGLEMENTAIRE : AI Act, RGPD évolutif, nouvelles taxes numériques (DST)
MONÉTAIRE : euro vs dollar, risque de fragmentation zone euro

## MATRICE DE RISQUE
Impact = Probabilité × Gravité × Vitesse de propagation
Seuil d'alerte : score > 15/25 → plan de contingence activé

## SPÉCIFICITÉ CAELUM PARTNERS
Exposition principale : revenus en euros belges, dépendance API Google (US),
clients PME locales (sensibles à récession), modèle freelance (flexibilité max)"""


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
    os.makedirs("fichiers/geopolitique", exist_ok=True)
    fichier = f"fichiers/geopolitique/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def analyse_risques_actuels():
    r = streamer(
        f"""RAPPORT DE RISQUES GÉOPOLITIQUES — Caelum Partners
Date d'analyse : {datetime.now().strftime('%B %Y')}

Analyse les risques macro actuels impactant Caelum Partners :

1. TOP 5 RISQUES PRIORITAIRES (matrice probabilité × impact)
   Pour chaque risque :
   - Description du risque
   - Probabilité d'occurrence (1-5)
   - Impact sur Caelum (1-5)
   - Score global
   - Plan de contingence spécifique

2. RISQUES ÉMERGENTS (horizon 12-24 mois)
   - Signaux faibles à surveiller

3. PROTECTIONS DÉJÀ EN PLACE
   - Ce qui protège Caelum naturellement (structure freelance, faible fixed costs)

4. VULNÉRABILITÉS CRITIQUES
   - Dépendances à réduire en priorité

5. OPPORTUNITÉS DANS LES TURBULENCES
   - Comment les crises créent des opportunités pour Caelum

Format : rapport exécutif, 1 page, actionnable.""",
        "RAPPORT RISQUES GÉOPOLITIQUES ACTUELS"
    )
    sauvegarder("rapport_risques_actuels", r)


def scenario_crise():
    print("\n  Décris le scénario de crise à analyser (ex: récession EU, panne Google Cloud, instabilité politique belge) :")
    scenario = input("  Scénario → ").strip()
    if not scenario:
        return
    r = streamer(
        f"""ANALYSE DE SCÉNARIO DE CRISE : {scenario}

Impact sur Caelum Partners :

1. MÉCANISME DE PROPAGATION
   Comment ce scénario affecte-t-il Caelum step by step ?

2. IMPACT FINANCIER ESTIMÉ
   - Revenus à risque (€ et %)
   - Clients susceptibles de reporter ou annuler
   - Délai avant impact (immédiat / 3 mois / 6 mois ?)

3. PLAN DE CONTINGENCE EN 3 PHASES
   Phase 1 — Alerte précoce (signaux à surveiller)
   Phase 2 — Activation (quand déclencher le plan ?)
   Phase 3 — Réponse (actions concrètes)

4. MESURES DÉFENSIVES PRÉVENTIVES
   Que faire maintenant pour réduire l'exposition ?

5. OPPORTUNITÉS DANS CE SCÉNARIO
   Comment Caelum peut prospérer pendant que les concurrents souffrent ?""",
        f"SCÉNARIO DE CRISE — {scenario[:50]}"
    )
    sauvegarder(f"scenario_{scenario[:20].replace(' ', '_')}", r)


def strategie_diversification_geo():
    r = streamer(
        """STRATÉGIE DE DIVERSIFICATION GÉOGRAPHIQUE — Caelum Partners

Pour réduire la dépendance au marché belge et aux risques locaux :

1. ANALYSE MARCHÉS ALTERNATIFS
   - France : opportunités et risques spécifiques
   - Luxembourg : marché premium, PME financières
   - Pays-Bas : marché tech, culture English-friendly
   - Suisse : pricing élevé, exigences qualité

2. CRITÈRES DE SÉLECTION DU MARCHÉ SUIVANT
   - Taille du marché IA pour PME
   - Barrières à l'entrée (langue, réglementation, réseau)
   - Proximité culturelle avec Bruxelles
   - Potentiel de prix (CA/client)

3. PLAN D'ENTRÉE SÉQUENTIEL
   - Marché 1 (dans 6 mois) : lequel et pourquoi ?
   - Marché 2 (dans 18 mois) : lequel et pourquoi ?
   - Marché 3 (dans 36 mois) : lequel et pourquoi ?

4. PROTECTION FINANCIÈRE
   - Diversification des devises si hors zone euro
   - Structures juridiques recommandées par pays""",
        "STRATÉGIE DIVERSIFICATION GÉOGRAPHIQUE"
    )
    sauvegarder("diversification_geo", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  RISQUES GÉOPOLITIQUES — Caelum Partners")
    print("  Macro · Politique · Économique · Technologique")
    print("═"*65)

    while True:
        print("\n  1. Rapport de risques actuels")
        print("  2. Analyser un scénario de crise")
        print("  3. Stratégie de diversification géographique")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            analyse_risques_actuels()
        elif choix == "2":
            scenario_crise()
        elif choix == "3":
            strategie_diversification_geo()
        else:
            print("  Choix invalide.")
