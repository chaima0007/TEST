"""
AGENT FINANCEMENT — Expert subventions et aides pour startups belges
Innoviris · Hub Brussels · Digital Wallonia · 1819 · Aides régionales Bruxelles

Usage : python agent_financement.py
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

IDENTITE = """Tu es un expert en financement de startups et PME belges avec 15 ans d'expérience.
Tu as aidé 200+ entrepreneurs belges à obtenir des subventions et aides publiques.

CONTEXTE CAELUM PARTNERS :
- Fondatrice : Chaima Mhadbi, Bruxelles
- Secteur : IA et automatisation pour PME
- Phase : lancement (0 clients)
- Services : Site web 500€ / Automation IA 1500€ / Pack 3000€
- Budget : bootstrapped (0€ extérieur)
- Atout : femme fondatrice, technologie IA, Bruxelles

AIDES ET ORGANISMES QUE TU MAITRISES :
🏛️ BRUXELLES :
- Innoviris (R&D bruxellois) — subventions innovation jusqu'à 500K€
- Hub.Brussels — accompagnement et financement startups
- Bruxelles Économie et Emploi — aides à l'emploi, primes installation
- Finance.Brussels — prêts et garanties
- 1819 (guichet info) — orientation toutes aides disponibles
- Starters Brussels — aide aux primo-entrepreneurs

🌍 FÉDÉRAL :
- VLAIO (si activités en Flandre)
- Agence pour l'Entreprise et l'Innovation
- Aide à la transition numérique (chèques numériques)

💰 INVESTISSEURS :
- Fonds de co-investissement bruxellois
- BAN Flanders / Be Angels (business angels)
- Crowd funding belge (MyMicroInvest, etc.)

🇪🇺 EUROPE :
- Horizon Europe (R&D IA)
- ERDF Bruxelles
- EIC Accelerator (jusqu'à 2,5M€)

STYLE : Pratique, chiffré, avec délais réels. Mentionner les critères d'éligibilité exacts."""


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
    os.makedirs("fichiers/financement", exist_ok=True)
    fichier = f"fichiers/financement/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def audit_aides_disponibles():
    r = streamer(
        """Fais un audit complet des aides auxquelles Caelum Partners est éligible MAINTENANT.
Pour chaque aide :
- Nom exact et organisme
- Montant ou avantage (en €)
- Critères d'éligibilité (Caelum les remplit-elle ?)
- Délai de traitement
- Lien ou contact direct
- Priorité (URGENT à demander / À planifier / Pour plus tard)
Classe les aides par impact financier décroissant.""",
        "AUDIT AIDES DISPONIBLES — Caelum Partners dès maintenant"
    )
    sauvegarder("audit_aides", r)


def dossier_innoviris():
    r = streamer(
        """Prépare un dossier de demande pour Innoviris (R&D bruxellois) pour Caelum Partners.
Inclure :
- Quel programme Innoviris est le plus adapté (Attract, Anticipate, Co-create...)
- Les sections obligatoires du dossier
- Comment présenter les agents IA comme innovation R&D
- Les arguments pour maximiser le score d'évaluation
- Les erreurs classiques qui font rejeter les dossiers
- Un draft de la section "Description du projet innovant"
- Montant réaliste à demander pour une startup IA en phase lancement""",
        "DOSSIER INNOVIRIS — Caelum Partners"
    )
    sauvegarder("dossier_innoviris", r)


def cheques_numeriques():
    r = streamer(
        """Les chèques numériques et aides à la digitalisation pour Caelum Partners :
1. Quels chèques numériques existent en Belgique (fédéral + régional) ?
2. Caelum Partners peut-elle les vendre à ses clients PME ? (revente de services numériques)
3. Comment intégrer les chèques numériques dans l'offre commerciale de Caelum ?
4. Les conditions et limites de ces programmes
5. Comment devenir prestataire agréé pour recevoir des chèques numériques clients
Cela pourrait DOUBLER le chiffre d'affaires si bien utilisé.""",
        "CHÈQUES NUMÉRIQUES — Opportunité commerciale Caelum Partners"
    )
    sauvegarder("cheques_numeriques", r)


def pitch_investisseur():
    r = streamer(
        """Prépare un pitch de 3 minutes pour un investisseur belge (business angel ou fonds).
Caelum Partners — startup IA bruxelloise, fondatrice Chaima Mhadbi.
Structure du pitch :
- Hook (10 secondes) : le problème que résout Caelum
- Solution (30 secondes) : les agents IA, comment ça marche
- Marché (30 secondes) : taille du marché PME belge + europe
- Traction (20 secondes) : état actuel (honnête mais positif)
- Business model (20 secondes) : 500€/1500€/3000€ + marges
- Équipe (10 secondes) : Chaima + agents IA
- Ask (20 secondes) : combien, pour quoi faire
Rédige le script exact, mot pour mot.""",
        "PITCH INVESTISSEUR — Script 3 minutes"
    )
    sauvegarder("pitch_investisseur", r)


def plan_financement_18_mois():
    r = streamer(
        """Crée un plan de financement sur 18 mois pour Caelum Partners.
Phase 0 (maintenant) : 0€ externe
Phase 1 (M1-M6) : subventions et aides publiques
Phase 2 (M6-M12) : love money / business angels
Phase 3 (M12-M18) : seed round si croissance prouvée

Pour chaque phase :
- Sources de financement à activer
- Montants réalistes
- Démarches concrètes
- Métriques à atteindre pour passer à la phase suivante
- Plan B si le financement n'arrive pas""",
        "PLAN FINANCEMENT 18 MOIS — De 0€ au seed round"
    )
    sauvegarder("plan_financement_18m", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT FINANCEMENT — Subventions et aides belges")
    print("  Innoviris · Hub Brussels · Chèques numériques · Angels")
    print("═"*65)

    while True:
        print("\n  1. Audit des aides disponibles maintenant")
        print("  2. Dossier Innoviris — R&D bruxellois")
        print("  3. Chèques numériques — opportunité client + revente")
        print("  4. Pitch investisseur — script 3 minutes")
        print("  5. Plan financement 18 mois")
        print("  7. Question libre sur les financements belges")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            audit_aides_disponibles()
        elif choix == "2":
            dossier_innoviris()
        elif choix == "3":
            cheques_numeriques()
        elif choix == "4":
            pitch_investisseur()
        elif choix == "5":
            plan_financement_18_mois()
        elif choix == "7":
            q = input("\n  Ta question → ").strip()
            if q:
                streamer(q, "QUESTION FINANCEMENT")
        else:
            print("  Choix invalide.")
