"""
AGENT INNOVATION DE RUPTURE [97] — R&D, technologies émergentes, avance 5-10 ans
Identifie les Deep Tech, IA, biotech, énergie pour acquérir ou développer en interne.

Usage : python agent_innovation_rupture.py
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

IDENTITE = """# AGENT INNOVATION DE RUPTURE — Caelum Partners

## IDENTITÉ
Tu es le directeur R&D et veille technologique de Caelum Partners.
Tu identifies les technologies émergentes qui créeront les marchés de demain.
Objectif : maintenir une avance de 5 à 10 ans sur les concurrents.

## TECHNOLOGIES SURVEILLÉES
- IA GÉNÉRATIVE : évolution LLM, multimodal, raisonnement, agents autonomes
- EDGE AI : IA locale sans cloud (Ollama, Apple Neural Engine, Qualcomm NPU)
- IA SPÉCIALISÉE : modèles verticaux (IA légale, IA médicale, IA financière)
- RAG & KNOWLEDGE GRAPHS : mémoire d'entreprise intelligente
- AUTOMATION : orchestrateurs agents (LangGraph, CrewAI, AutoGen, n8n AI)
- COMPUTER VISION : analyse documents, OCR intelligent, reconnaissance
- VOICE & AUDIO : interfaces vocales business, transcription, synthèse
- LOW-CODE IA : Bubble IA, Webflow IA, Glide, outils no-code augmentés

## GRILLE D'ÉVALUATION TECHNOLOGIE
1. MATURITÉ (TRL 1-9) : où en est la technologie ?
2. DÉLAI D'ADOPTION PME : dans combien de temps les PME belges en auront besoin ?
3. COMPLEXITÉ D'INTÉGRATION : combien de temps pour l'intégrer dans Caelum ?
4. BARRIÈRE À LA CONCURRENCE : est-ce difficile à copier ?
5. ROI POTENTIEL : quel CA additionnel cela génère-t-il ?

## STRATÉGIE D'INNOVATION CAELUM (réaliste)
Phase 1 (maintenant) : maîtriser ce qui existe (Gemini, n8n, RAG)
Phase 2 (6-18 mois) : intégrer les nouveaux outils AI Agent
Phase 3 (18-36 mois) : développer des offres propriétaires verticales
Phase 4 (3-5 ans) : IP, partenariats technologiques, label Caelum"""


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
                temperature=0.25,
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
    os.makedirs("fichiers/innovation", exist_ok=True)
    fichier = f"fichiers/innovation/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def radar_technologies():
    r = streamer(
        f"""RADAR TECHNOLOGIQUE — Caelum Partners
Date : {datetime.now().strftime('%B %Y')}

Génère le radar des technologies émergentes prioritaires pour Caelum Partners :

QUADRANT 1 — ADOPTER MAINTENANT (maturité haute, impact fort)
[3-5 technologies avec plan d'action 30 jours]

QUADRANT 2 — EXPÉRIMENTER (maturité moyenne, potentiel élevé)
[3-5 technologies avec timeline 6 mois]

QUADRANT 3 — SURVEILLER (maturité faible, potentiel disruptif)
[3-5 technologies avec signaux à observer]

QUADRANT 4 — IGNORER POUR L'INSTANT (hype > réalité pour PME belges)
[3-5 technologies surévaluées à ne pas suivre maintenant]

Pour chaque technologie : nom + maturité + délai PME + opportunité Caelum.""",
        "RADAR TECHNOLOGIQUE CAELUM"
    )
    sauvegarder("radar_technologique", r)


def analyser_technologie():
    print("\n  Technologie à analyser (ex: AI agents autonomes, RAG d'entreprise, voice AI) :")
    tech = input("  Technologie → ").strip()
    if not tech:
        return
    r = streamer(
        f"""ANALYSE TECHNOLOGIQUE APPROFONDIE : {tech}

Pour Caelum Partners (PME IA, Bruxelles) :

1. ÉTAT DE L'ART
   - Maturité actuelle (TRL 1-9)
   - Principaux acteurs et outils disponibles maintenant
   - Coût d'accès réel

2. OPPORTUNITÉ POUR CAELUM
   - Quels services créer avec cette technologie ?
   - Quels secteurs de clients peuvent payer pour ça ?
   - Prix de marché estimé

3. DÉLAI D'ADOPTION MARCHÉ BELGE PME
   - Dans combien de mois les PME belges en auront besoin ?
   - Signaux précurseurs à surveiller

4. PLAN D'ACQUISITION DE COMPÉTENCE
   - Formation nécessaire (jours/semaines)
   - Ressources recommandées (cours, projets pilotes)
   - Coût d'apprentissage

5. AVANTAGE CONCURRENTIEL
   - Combien de temps avant que les concurrents belges maîtrisent aussi ?
   - Comment créer une barrière durable ?

6. DÉCISION RECOMMANDÉE : ADOPTER / EXPÉRIMENTER / SURVEILLER / IGNORER""",
        f"ANALYSE TECH — {tech}"
    )
    sauvegarder(f"analyse_tech_{tech.replace(' ', '_')}", r)


def roadmap_innovation():
    r = streamer(
        """ROADMAP D'INNOVATION CAELUM PARTNERS — 36 mois

Génère la roadmap technologique et produit sur 3 ans :

MAINTENANT → 6 MOIS
Objectif : consolider et monétiser les compétences actuelles
[Technologies à maîtriser + Nouvelles offres à lancer]

6 → 18 MOIS
Objectif : différenciation par l'innovation
[Technologies émergentes à intégrer + Offres premium à créer]

18 → 36 MOIS
Objectif : propriété intellectuelle et partenariats
[Développements propriétaires + Partenariats tech + Label Caelum]

Pour chaque phase :
- Investissement en temps formation
- Investissement financier (formation, outils, certifications)
- Revenus additionnels générés
- Risque si on ne le fait pas""",
        "ROADMAP INNOVATION 36 MOIS"
    )
    sauvegarder("roadmap_innovation_36mois", r)


def veille_startups():
    print("\n  Domaine à surveiller (ex: AI agents, no-code IA, sécurité IA) :")
    domaine = input("  Domaine → ").strip() or "AI agents entreprise"
    r = streamer(
        f"""VEILLE STARTUPS & ACQUISITIONS — {domaine}

Pour Caelum Partners, identifie :

1. STARTUPS À SURVEILLER (financement Series A/B, traction visible)
   [5-8 startups avec leur proposition de valeur et ce qu'elles révèlent sur le marché]

2. ACQUISITIONS RÉCENTES SIGNIFICATIVES
   [Ce que les grandes entreprises achètent = ce qui va devenir mainstream]

3. TECHNOLOGIES QUI VONT TUER CERTAINES OFFRES ACTUELLES
   [Ce que Caelum doit anticiper pour ne pas être dépassé]

4. PARTENARIATS TECHNOLOGIQUES POSSIBLES POUR CAELUM
   [Startups ou outils avec lesquels s'associer pour accélérer]

5. OPPORTUNITÉ D'INVESTISSEMENT OU D'ACQUISITION MICRO
   [Y a-t-il des micro-outils à acheter ou des compétences à recruter ?]""",
        f"VEILLE STARTUPS — {domaine}"
    )
    sauvegarder(f"veille_startups_{domaine.replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  INNOVATION DE RUPTURE — Caelum Partners")
    print("  R&D · Technologies émergentes · Avance 5-10 ans")
    print("═"*65)

    while True:
        print("\n  1. Radar technologique (quadrant complet)")
        print("  2. Analyser une technologie spécifique")
        print("  3. Roadmap innovation 36 mois")
        print("  4. Veille startups et acquisitions")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            radar_technologies()
        elif choix == "2":
            analyser_technologie()
        elif choix == "3":
            roadmap_innovation()
        elif choix == "4":
            veille_startups()
        else:
            print("  Choix invalide.")
