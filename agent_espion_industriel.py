"""
AGENT ESPION INDUSTRIEL [93] — Veille concurrentielle avancée, intelligence stratégique
Analyse mouvements de capital, recrutements, brevets pour anticiper les attaques concurrentes.

Usage : python agent_espion_industriel.py
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

IDENTITE = """# AGENT ESPION INDUSTRIEL — Caelum Partners

## IDENTITÉ
Tu es l'agent de renseignement concurrentiel de Caelum Partners.
Mission : anticiper les mouvements des concurrents avant qu'ils n'impactent le marché.

## SOURCES D'INTELLIGENCE (LÉGALES UNIQUEMENT)
- LinkedIn : changements de postes, recrutements, publications stratégiques
- Crossroads Data / Pappers.fr / BCE.be : modifications juridiques, capitaux
- Google Patents / BOIP : dépôts de brevets et marques
- Presse économique : La Libre Éco, L'Echo, Le Vif, Trends
- Offres d'emploi : révèlent les technologies et marchés ciblés
- Sites web et landing pages : nouvelles offres, pricing, positionnement

## PROFIL CONCURRENTS CAELUM (Belgique)
Concurrents directs : agences IA belges, freelances automation, ESN (SSII)
Substituts : consultants RPA, agences digitales ajoutant de l'IA
Concurrents indirects : formations IA en ligne, outils no-code (Zapier, Make)

## MÉTHODE D'ANALYSE (PORTER + INTEL)
1. SIGNAL FAIBLE : changement anodin en surface (recrutement DevOps → expansion tech)
2. CORRÉLATION : relier 3 signaux disparates pour révéler une intention cachée
3. TEMPORALITÉ : quand agir ? Avant l'annonce publique ou après ?
4. IMPACT CAELUM : opportunité ou menace directe ?
5. CONTRE-MESURE : que faire dans les 72h pour protéger notre position

## ÉTHIQUE
Toutes les sources sont publiques et légales. Jamais de hacking, d'espionnage illégal ou d'accès non autorisé."""


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
    os.makedirs("fichiers/espion", exist_ok=True)
    fichier = f"fichiers/espion/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def analyser_concurrent():
    print("\n  Nom de l'entreprise concurrente à analyser :")
    concurrent = input("  Concurrent → ").strip()
    print("  Secteur ou spécialité (ex: automation RPA, agence IA, SSII) :")
    secteur = input("  Secteur → ").strip() or "agence IA Belgique"
    if not concurrent:
        return
    r = streamer(
        f"""ANALYSE INTELLIGENCE CONCURRENTIELLE — {concurrent}
Secteur : {secteur}

Effectue une analyse complète de ce concurrent pour Caelum Partners :

1. PROFIL STRATÉGIQUE
   - Positionnement actuel (offres, prix, marché cible)
   - Taille estimée (CA, équipe, clients)
   - Forces et faiblesses apparentes

2. SIGNAUX D'ALERTE À SURVEILLER
   - Quels changements sur LinkedIn indiqueraient une expansion ?
   - Quels types de recrutements révèlent une nouvelle direction ?
   - Quels brevets ou marques déposeraient-ils s'ils attaquaient notre marché ?

3. SCÉNARIOS D'ATTAQUE POTENTIELS
   - Comment pourraient-ils attaquer la position de Caelum ?
   - Avec quelle probabilité et dans quel délai ?

4. CONTRE-MESURES IMMÉDIATES
   - Que faire maintenant pour blinder notre position ?
   - Quel avantage concurrentiel est difficile à copier ?

5. OPPORTUNITÉS DANS LEURS ANGLES MORTS
   - Où sont-ils faibles et où Caelum peut s'imposer ?""",
        f"ANALYSE CONCURRENT — {concurrent}"
    )
    sauvegarder(f"concurrent_{concurrent.replace(' ', '_')}", r)


def signal_faible():
    print("\n  Décris un signal observé (ex: 'X a recruté 3 devs Python sur LinkedIn cette semaine') :")
    signal = input("  Signal → ").strip()
    if not signal:
        return
    r = streamer(
        f"""ANALYSE DE SIGNAL FAIBLE :
Signal observé : {signal}

Décrypte ce signal pour Caelum Partners :
1. SIGNIFICATION CACHÉE : qu'est-ce que ce signal révèle vraiment ?
2. INTENTION PROBABLE : quelle décision stratégique est en cours chez le concurrent ?
3. TIMELINE : dans combien de temps cela deviendra-t-il visible sur le marché ?
4. IMPACT SUR CAELUM : menace directe, indirecte, ou opportunité ?
5. ACTION DANS 72H : que faire immédiatement pour prendre l'avantage ?
6. AUTRES SIGNAUX À SURVEILLER pour confirmer ou infirmer cette hypothèse""",
        f"SIGNAL FAIBLE — {signal[:50]}"
    )
    sauvegarder("signal_faible", r)


def carte_ecosysteme():
    print("\n  Marché ou secteur à cartographier (ex: automation IA PME Belgique) :")
    marche = input("  Marché → ").strip() or "automation IA PME Belgique"
    r = streamer(
        f"""CARTE DE L'ÉCOSYSTÈME CONCURRENTIEL — {marche}

Cartographie complète pour Caelum Partners :

1. ACTEURS CLÉS (catégorisés)
   - Concurrents directs (même offre, même marché)
   - Substituts (offre différente, même besoin)
   - Complémentaires (partenaires potentiels ou futurs concurrents)

2. DYNAMIQUES DE MARCHÉ
   - Qui gagne des parts ? Qui perd ?
   - Nouveaux entrants (startups, consultants indépendants)
   - Technologies qui vont disrupter dans 12-24 mois

3. BLANC SUR LA CARTE
   - Segments non servis ou mal servis
   - Niches où Caelum peut s'imposer sans résistance

4. BARRIÈRES À L'ENTRÉE
   - Qu'est-ce qui protège notre position une fois établie ?
   - Comment créer des barrières que les concurrents ne pourront pas franchir ?

5. RECOMMANDATION POSITIONNEMENT
   - Où se battre et où éviter le combat frontal""",
        f"CARTE ÉCOSYSTÈME — {marche}"
    )
    sauvegarder(f"ecosysteme_{marche.replace(' ', '_')}", r)


def rapport_hebdomadaire():
    r = streamer(
        """Génère le TEMPLATE DE RAPPORT HEBDOMADAIRE DE VEILLE CONCURRENTIELLE pour Caelum Partners.

Format :
SEMAINE DU [DATE]

📡 SIGNAUX PRIORITAIRES
1. [signal + source + interprétation + action recommandée]
2. [...]

🔴 ALERTES (action requise sous 72h)
[liste]

🟡 SURVEILLANCE (surveiller, pas encore d'action)
[liste]

🟢 OPPORTUNITÉS IDENTIFIÉES
[liste avec plan d'action]

📊 THERMOMÈTRE CONCURRENTIEL (score 1-10 pour chaque concurrent clé)
[tableau]

DÉCISION DE LA SEMAINE :
[1 décision stratégique à prendre basée sur la veille]

Format : dense, actionnable, max 1 page.""",
        "TEMPLATE RAPPORT VEILLE HEBDOMADAIRE"
    )
    sauvegarder("template_rapport_hebdo", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  ESPION INDUSTRIEL — Caelum Partners")
    print("  Intelligence concurrentielle · Sources légales uniquement")
    print("═"*65)

    while True:
        print("\n  1. Analyser un concurrent spécifique")
        print("  2. Décrypter un signal faible")
        print("  3. Cartographier l'écosystème concurrentiel")
        print("  4. Générer le template rapport hebdomadaire")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            analyser_concurrent()
        elif choix == "2":
            signal_faible()
        elif choix == "3":
            carte_ecosysteme()
        elif choix == "4":
            rapport_hebdomadaire()
        else:
            print("  Choix invalide.")
