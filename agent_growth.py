"""
AGENT GROWTH — Growth hacking autonome pour Caelum Partners
Trouve les leviers de croissance, génère des expériences,
optimise les canaux, double le CA chaque trimestre.

Usage : python agent_growth.py
"""

import os
import sys
import json
from datetime import datetime
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

CONTEXTE = {
    "entreprise": "Caelum Partners",
    "fondatrice": "Chaima Mhadbi",
    "localisation": "Bruxelles, Belgique",
    "services": ["Site web 500€", "Automation IA 1500€", "Pack complet 3000€"],
    "cible": "PME, startups, indépendants — Belgique + Europe francophone",
    "canal_principal": "LinkedIn",
    "site": "caelumpartners.agency",
}


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.4, max_output_tokens=3000),
    )
    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom, contenu):
    os.makedirs("fichiers/growth", exist_ok=True)
    fichier = f"fichiers/growth/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


# ─────────────────────────────────────────────────────────────
# 1. MOTEUR DE CROISSANCE — Les 10 leviers à activer maintenant
# ─────────────────────────────────────────────────────────────

def moteur_croissance():
    r = streamer(
        """Tu es le meilleur Growth Hacker au monde, spécialisé en agences IA B2B.
Tu travailles pour Caelum Partners — startup belge d'agents IA.
Tu identifies les 10 leviers de croissance les plus puissants
adaptés au marché belge et européen francophone.

FORMAT :
🚀 LEVIER [N] — [Nom du levier]
   Canal : [LinkedIn/Email/SEO/Partenariats/...]
   Effort : [Faible/Moyen/Élevé]
   Impact : [Faible/Moyen/Élevé]
   Délai résultat : [X jours/semaines]
   Action concrète : [Ce qu'on fait demain matin]
   Métrique de succès : [Comment mesurer]
   Coût : [0€/faible/moyen]""",
        f"""Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}
Objectif : 10 clients dans 90 jours
Budget marketing : 0€ (bootstrapped)
Avantage concurrentiel : IA + rapidité + prix accessible""",
        "MOTEUR DE CROISSANCE — 10 leviers à activer"
    )
    sauvegarder("moteur_croissance", r)


# ─────────────────────────────────────────────────────────────
# 2. EXPÉRIENCES GROWTH — 30 tests A/B à lancer cette semaine
# ─────────────────────────────────────────────────────────────

def experiences_growth():
    r = streamer(
        """Tu es un expert en growth experiments.
Tu génères 30 micro-expériences à tester cette semaine pour accélérer la croissance.
Chaque expérience prend moins de 2 heures à mettre en place.

FORMAT :
EXP[N] — [Nom]
   Hypothèse : Si je [action], alors [résultat attendu]
   Durée test : [X jours]
   Effort : [X heures]
   Mesure : [métrique clé]
   Succès = [seuil chiffré]
   Canal : [LinkedIn/Email/Site/...]""",
        f"Entreprise : {CONTEXTE['entreprise']} | Services : {CONTEXTE['services']} | Cible : {CONTEXTE['cible']}",
        "30 EXPÉRIENCES GROWTH — Cette semaine"
    )
    sauvegarder("experiences_growth", r)


# ─────────────────────────────────────────────────────────────
# 3. MACHINE À LEADS — Système automatique d'acquisition
# ─────────────────────────────────────────────────────────────

def machine_leads():
    r = streamer(
        """Tu es expert en acquisition B2B.
Tu conçois une machine à leads complète et automatisée pour une agence IA.
Le système doit générer des leads qualifiés SANS budget publicitaire.

FORMAT :
## MACHINE À LEADS — Caelum Partners

### CANAL 1 : LinkedIn (principal)
[Routine quotidienne, scripts, outils, KPIs]

### CANAL 2 : SEO / Contenu
[Stratégie, mots-clés, fréquence, types de contenu]

### CANAL 3 : Partenariats
[Types de partenaires, approche, deal structure]

### CANAL 4 : Référencement (bouche à oreille)
[Programme référral, incentives, scripts]

### CANAL 5 : Communautés
[Quelles communautés, comment y apporter de la valeur]

### AUTOMATISATION
[Ce qui peut être automatisé avec les agents IA]

### OBJECTIF : 10 leads qualifiés/semaine""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}",
        "MACHINE À LEADS — Acquisition automatique"
    )
    sauvegarder("machine_leads", r)


# ─────────────────────────────────────────────────────────────
# 4. FUNNEL DE CONVERSION — De inconnu à client payant
# ─────────────────────────────────────────────────────────────

def funnel_conversion():
    r = streamer(
        """Tu es expert en conversion B2B.
Tu conçois le funnel de conversion parfait pour une agence IA.
Chaque étape doit maximiser la conversion à l'étape suivante.

FORMAT :
## FUNNEL CAELUM PARTNERS

ÉTAPE 1 — DÉCOUVERTE
  Déclencheur : [comment ils trouvent Caelum]
  Message : [ce qu'ils voient en premier]
  Conversion → : [action à faire]
  Taux cible : X%

ÉTAPE 2 — INTÉRÊT
...jusqu'à...

ÉTAPE 6 — CLIENT FIDÈLE (upsell/référence)

## SCRIPTS & TEMPLATES
[Messages prêts pour chaque transition]

## AUTOMATISATION PAR AGENT IA
[Quel agent gère chaque étape]""",
        f"Services : {CONTEXTE['services']} | Prix : 500€/1500€/3000€ | Cible : PME Belgique",
        "FUNNEL DE CONVERSION — De prospect à client fidèle"
    )
    sauvegarder("funnel_conversion", r)


# ─────────────────────────────────────────────────────────────
# 5. VIRAL LOOP — Faire grandir l'empire par effet viral
# ─────────────────────────────────────────────────────────────

def viral_loop():
    r = streamer(
        """Tu es expert en growth viral et effets de réseau.
Tu conçois un système de croissance virale pour Caelum Partners.
Chaque client doit amener naturellement d'autres clients.

FORMAT :
## VIRAL LOOP — Caelum Partners

### MÉCANISME VIRAL PRINCIPAL
[Description du loop central]

### INCITATIONS (pourquoi partager ?)
- Client : [bénéfice]
- Référé : [bénéfice]

### PROGRAMME RÉFÉRRAL
[Structure, commission, processus]

### CONTENU VIRAL
[Types de contenu que les clients partagent naturellement]

### SOCIAL PROOF MACHINE
[Avis, témoignages, cas clients — comment les collecter et diffuser]

### PARTENARIATS MULTIPLICATEURS
[Qui peut recommander Caelum à 100 clients d'un coup ?]

### OBJECTIF : coefficient viral k > 0.3""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}",
        "VIRAL LOOP — Croissance exponentielle"
    )
    sauvegarder("viral_loop", r)


# ─────────────────────────────────────────────────────────────
# 6. PLAN CROISSANCE 90 JOURS — De 0 à 10 clients
# ─────────────────────────────────────────────────────────────

def plan_90_jours():
    r = streamer(
        """Tu es le Growth Director d'une startup IA qui scale de 0 à 10 clients en 90 jours.
Tu crées le plan d'exécution jour par jour pour les 30 premiers jours,
puis semaine par semaine pour les 60 jours suivants.

FORMAT :
## OBJECTIF : 10 clients payants en 90 jours (15 000€+ CA)

### MOIS 1 — FONDATIONS & PREMIERS CLIENTS
Semaine 1 (J1-J7) :
  Lundi : ...
  Mardi : ...
  ...
  Objectif : [X leads qualifiés]
  Agent à utiliser : [agent.py]

Semaine 2 ...
Semaine 3 ...
Semaine 4 ...

### MOIS 2 — ACCÉLÉRATION
[Plan hebdomadaire]

### MOIS 3 — SCALE
[Plan hebdomadaire]

### KPIs HEBDOMADAIRES
[Tableau de bord de suivi]

### AGENTS IA À UTILISER
[Quel agent pour quelle tâche]""",
        f"Contexte : {json.dumps(CONTEXTE, ensure_ascii=False)}\nBudget : 0€\nÉquipe : 1 personne + agents IA",
        "PLAN 90 JOURS — De 0 à 10 clients"
    )
    sauvegarder("plan_90_jours", r)


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT GROWTH — Growth hacking Caelum Partners")
    print("  Objectif : 10 clients en 90 jours")
    print("═"*65)

    while True:
        print("\n  1. Moteur de croissance — 10 leviers à activer")
        print("  2. 30 expériences growth — tests cette semaine")
        print("  3. Machine à leads — acquisition automatique")
        print("  4. Funnel de conversion — prospect → client fidèle")
        print("  5. Viral loop — croissance exponentielle")
        print("  6. Plan 90 jours — de 0 à 10 clients")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            moteur_croissance()
        elif choix == "2":
            experiences_growth()
        elif choix == "3":
            machine_leads()
        elif choix == "4":
            funnel_conversion()
        elif choix == "5":
            viral_loop()
        elif choix == "6":
            plan_90_jours()
        else:
            print("  Choix invalide.")
