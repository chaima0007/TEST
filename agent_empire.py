"""
AGENT EMPIRE — Vision et construction de l'empire Caelum Partners
Stratégie long terme : expansion, nouveaux marchés, levée de fonds,
acquisitions, licences, franchise IA — penser grand dès le début.

Usage : python agent_empire.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

VISION = {
    "entreprise": "Caelum Partners",
    "fondatrice": "Chaima Mhadbi",
    "base": "Bruxelles, Belgique",
    "phase_actuelle": "Lancement — recherche premiers clients",
    "services_actuels": ["Site web 500€", "Automation IA 1500€", "Pack complet 3000€"],
    "vision": "Devenir la référence européenne en agents IA pour PME",
    "horizon": "5 ans",
}


def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def streamer(instructions, prompt, label=""):
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=3000),
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
    os.makedirs("fichiers/empire", exist_ok=True)
    fichier = f"fichiers/empire/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def vision_empire():
    r = streamer(
        """Tu es le conseiller stratégique des plus grandes entreprises tech.
Tu construis la vision empire de Caelum Partners sur 5 ans.
Pense comme Elon Musk, Jeff Bezos, mais pour une entreprise IA belge.

FORMAT :
## EMPIRE CAELUM PARTNERS — Vision 5 ans

### ANNÉE 1 (2026) — FONDATION
Objectif CA : X€
Clients : X
Équipe : X personnes
Nouveaux services : ...
Milestones clés : ...

### ANNÉE 2 (2027) — CROISSANCE
...

### ANNÉE 3 (2028) — EXPANSION EUROPE
...

### ANNÉE 4 (2029) — DOMINATION
...

### ANNÉE 5 (2030) — EMPIRE
CA cible : X M€
Pays : ...
Produits : ...
Équipe : X personnes
Exit possible : IPO/Acquisition/Scale

### MOAT (Avantage défensif)
[Ce qui rend Caelum Partners impossible à copier]

### RISQUES MAJEURS & PLANS B
[Top 5 risques + mitigation]""",
        json.dumps(VISION, ensure_ascii=False),
        "VISION EMPIRE — Caelum Partners 2026-2030"
    )
    sauvegarder("vision_empire", r)


def nouveaux_services():
    r = streamer(
        """Tu es Chief Product Officer d'une scale-up IA.
Tu identifies les 10 prochains services que Caelum Partners peut lancer
pour multiplier son CA par 10 en 18 mois.

FORMAT :
SERVICE [N] — [Nom]
  Prix : X€
  Cible : [qui l'achète]
  Temps de création : [X jours avec les agents IA]
  Récurrence : [one-shot/mensuel/annuel]
  Marge : [%]
  Prérequis : [ce qui doit exister d'abord]
  CA potentiel/mois : X€
  Lancer quand : [après X clients / X mois]""",
        f"Base : {VISION['services_actuels']}\nMarchés : PME Belgique + Europe francophone\nOutils : 40+ agents IA déjà construits",
        "NOUVEAUX SERVICES — Multiplier le CA par 10"
    )
    sauvegarder("nouveaux_services", r)


def expansion_geographique():
    r = streamer(
        """Tu es expert en expansion internationale de startups tech.
Tu planifies l'expansion géographique de Caelum Partners en Europe.

FORMAT :
## EXPANSION GÉOGRAPHIQUE

### PHASE 1 — Belgique (J1-J180)
[Consolider la base, références, témoignages]

### PHASE 2 — France (M6-M12)
Marché : taille, opportunité, concurrence
Approche : comment entrer
Canal d'acquisition : ...
Adaptation needed : ...
CA potentiel : X€/mois

### PHASE 3 — Luxembourg + Suisse (M12-M18)
...

### PHASE 4 — Canada francophone (M18-M24)
...

### PHASE 5 — Europe anglophone (M24+)
...

### ADAPTATION LOCALE
[Ce qui change par pays : langue, culture, réglementation]

### PARTENAIRES LOCAUX
[Type de partenaires à trouver dans chaque pays]""",
        json.dumps(VISION, ensure_ascii=False),
        "EXPANSION GÉOGRAPHIQUE — Europe et au-delà"
    )
    sauvegarder("expansion_geographique", r)


def levee_de_fonds():
    r = streamer(
        """Tu es expert en financement de startups et tu as aidé 50+ startups à lever des fonds.
Tu prépares la stratégie de financement de Caelum Partners.

FORMAT :
## STRATÉGIE FINANCEMENT — Caelum Partners

### PHASE 0 — BOOTSTRAPPED (maintenant)
[Comment survivre et grandir sans argent externe]

### PHASE 1 — SUBVENTIONS & AIDES (M3-M6)
Aides disponibles en Belgique :
- [Nom aide] : montant, conditions, démarches
Hub Brussels, Innoviris, Digital Wallonia, etc.

### PHASE 2 — LOVE MONEY / ANGELS (M6-M12)
[Comment approcher, pitch, terms]

### PHASE 3 — SEED ROUND (M12-M24)
Montant cible : X€
Valorisation : X€
Investisseurs cibles : [noms de fonds belges/européens]
Use of funds : ...

### PITCH DECK STRUCTURE
[Les 10 slides essentielles avec le contenu]

### MÉTRIQUES POUR LEVER
[Ce que les investisseurs veulent voir]""",
        json.dumps(VISION, ensure_ascii=False),
        "LEVÉE DE FONDS — Stratégie financement"
    )
    sauvegarder("levee_de_fonds", r)


def modele_franchise():
    r = streamer(
        """Tu es expert en franchise et modèles de licence pour les entreprises tech.
Tu conçois le modèle de franchise/licence de Caelum Partners.
L'idée : vendre la suite d'agents IA à d'autres agences/consultants.

FORMAT :
## MODÈLE FRANCHISE / LICENCE — Caelum Partners

### CONCEPT
[Comment ça marche : licence de la suite d'agents IA]

### OFFRE FRANCHISÉ
- Ce qu'ils reçoivent : [liste des 40+ agents + formation + support]
- Prix de la licence : X€/an
- Revenue share : X%
- Territory : [exclusivité par région/pays]

### PROFIL FRANCHISÉ IDÉAL
[Qui achète cette licence]

### ONBOARDING FRANCHISÉ
[Comment on les forme avec les agents IA]

### PROJECTIONS
- 10 franchisés → CA additionnel : X€/an
- 50 franchisés → CA additionnel : X€/an
- 100 franchisés → CA additionnel : X€/an

### PROTECTION IP
[Comment protéger le code et les agents]

### LANCER QUAND
[À partir de X clients / X mois / X€ CA]""",
        json.dumps(VISION, ensure_ascii=False),
        "MODÈLE FRANCHISE — Multiplier par 100"
    )
    sauvegarder("modele_franchise", r)


def plan_empire_complet():
    """Lance tous les modules en séquence."""
    print(f"\n{'═'*65}")
    print(f"  CONSTRUCTION EMPIRE COMPLET")
    print(f"  5 modules — vision totale Caelum Partners")
    print(f"{'═'*65}")

    vision_empire()
    nouveaux_services()
    expansion_geographique()
    levee_de_fonds()
    modele_franchise()

    print(f"\n{'═'*65}")
    print(f"  Empire complet généré → fichiers/empire/")
    print(f"{'═'*65}\n")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT EMPIRE — Vision long terme Caelum Partners")
    print("  Penser grand dès le premier jour")
    print("═"*65)

    while True:
        print("\n  1. Vision empire 5 ans (2026-2030)")
        print("  2. Nouveaux services — multiplier le CA par 10")
        print("  3. Expansion géographique — Europe et au-delà")
        print("  4. Levée de fonds — subventions, angels, seed")
        print("  5. Modèle franchise — vendre la suite d'agents")
        print("  6. GÉNÉRER L'EMPIRE COMPLET (tous les modules)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            vision_empire()
        elif choix == "2":
            nouveaux_services()
        elif choix == "3":
            expansion_geographique()
        elif choix == "4":
            levee_de_fonds()
        elif choix == "5":
            modele_franchise()
        elif choix == "6":
            plan_empire_complet()
        else:
            print("  Choix invalide.")
