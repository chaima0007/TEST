"""
AGENT AUTOMATISATION N8N [81] — Blueprints n8n / Make / Zapier / Power Automate
Conçoit des workflows d'automatisation clés en main pour les clients de Caelum.

Usage : python agent_automatisation_n8n.py
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

IDENTITE = """# AGENT AUTOMATISATION N8N — Caelum Partners

## IDENTITÉ
Tu es l'architecte d'automatisation de Caelum Partners.
Tu conçois des workflows d'automatisation pour n8n, Make (ex-Integromat), Zapier et Power Automate.
Tu identifies les processus manuels à automatiser, calcules le ROI, et produis des blueprints détaillés.

## EXPERTISE
- n8n : open-source, self-hosted, idéal pour données sensibles et coût maîtrisé
- Make (Integromat) : visuel, puissant, idéal pour connecter apps SaaS
- Zapier : simple, coûteux, pour clients non-techniques
- Power Automate : intégré Microsoft 365, idéal pour PME avec Teams/Outlook
- Gemini API : peut être intégrée dans n'importe quel workflow via HTTP Request

## PROCESSUS AUTOMATISABLES TYPIQUES (PME belge)
- Facturation automatique après signature contrat
- Relances impayées (J+30, J+45, J+60)
- Onboarding client (email séquence + CRM update)
- Monitoring concurrents (scraping hebdo + rapport email)
- Reporting financier mensuel (Excel → PDF → email)
- Traitement emails entrants (triage, réponse auto, ticket)
- Synchronisation agenda + CRM + facturation
- Publication réseaux sociaux (content calendar automatisé)

## FORMAT BLUEPRINT
Pour chaque workflow :
- Nom et objectif
- Déclencheur (Trigger)
- Étapes numérotées avec l'outil utilisé
- Données échangées
- Gestion des erreurs
- Estimation temps économisé/mois
- ROI calculé (temps × coût horaire client)"""


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
    os.makedirs("fichiers/automatisation", exist_ok=True)
    fichier = f"fichiers/automatisation/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def analyser_processus():
    print("\n  Décris le processus manuel du client (ex: 'il envoie les factures à la main chaque mois') :")
    processus = input("  Processus → ").strip()
    outils = input("  Outils actuels du client (ex: Gmail, Excel, WhatsApp) → ").strip() or "Gmail, Excel"
    if not processus:
        return
    r = streamer(
        f"""Analyse ce processus manuel et propose une solution d'automatisation :
Processus : {processus}
Outils actuels : {outils}

Fournis :
1. DIAGNOSTIC : identification des tâches répétitives et leur fréquence estimée
2. SOLUTION RECOMMANDÉE : quel outil d'automatisation (n8n/Make/Zapier/Power Automate) et pourquoi
3. BLUEPRINT : workflow étape par étape
4. ROI : temps économisé/mois × coût horaire moyen (40€/h)
5. COÛT D'IMPLÉMENTATION : estimation forfait Caelum (parmi 500/1500/3000€)""",
        f"ANALYSE PROCESSUS"
    )
    sauvegarder("analyse_processus", r)


def blueprint_facturation():
    r = streamer(
        """Crée un blueprint d'automatisation FACTURATION COMPLÈTE pour une PME belge.

Workflow à créer dans n8n :
1. Déclencheur : nouveau contrat signé (webhook ou Google Form)
2. Génération facture PDF (numérotation belge conforme TVA)
3. Envoi email au client (avec PDF joint)
4. Création rappel dans CRM (J+30 pour relance si impayé)
5. Archivage dans Google Drive ou dossier client
6. Notification WhatsApp/Telegram au comptable

Inclure : gestion erreurs, log des factures, conformité TVA belge.""",
        "BLUEPRINT FACTURATION AUTOMATIQUE"
    )
    sauvegarder("blueprint_facturation", r)


def blueprint_onboarding():
    r = streamer(
        """Crée un blueprint d'automatisation ONBOARDING CLIENT pour Caelum Partners.

Workflow n8n / Make déclenché quand nouveau client signe :
1. Email de bienvenue personnalisé (J+0)
2. Invitation réunion kick-off (Calendly/Cal.com)
3. Création espace client (Google Drive ou Notion)
4. Questionnaire de démarrage (Google Form)
5. Séquence email J+3, J+7, J+14 (check-in)
6. Mise à jour CRM (statut = "En cours")
7. Rappel à J+30 pour bilan mi-parcours

Chaque étape avec : outil, données échangées, délai.""",
        "BLUEPRINT ONBOARDING CLIENT"
    )
    sauvegarder("blueprint_onboarding", r)


def blueprint_prospection():
    r = streamer(
        """Crée un blueprint d'automatisation PROSPECTION LINKEDIN pour Caelum Partners.

Workflow hebdomadaire :
1. Liste de prospects ciblés (secteur + Bruxelles) depuis LinkedIn Sales Navigator ou Google Maps
2. Enrichissement contact (email via Hunter.io ou Apollo)
3. Séquence email/LinkedIn J+0, J+3, J+7, J+14
4. Si réponse → notification immédiate + mise à jour CRM
5. Si pas de réponse après 14j → archiver + nouvelle liste

Inclure : taux d'envoi sécurisé (max 20 mails/jour pour éviter spam).""",
        "BLUEPRINT PROSPECTION AUTOMATISÉE"
    )
    sauvegarder("blueprint_prospection", r)


def calculer_roi():
    print("\n  Quel processus automatiser ?")
    processus = input("  Processus → ").strip()
    print("  Combien d'heures par semaine ce processus prend-il actuellement ?")
    heures = input("  Heures/semaine → ").strip() or "5"
    print("  Coût horaire du client ou de son employé (€/h, défaut 35€) :")
    taux = input("  Taux horaire → ").strip() or "35"
    if not processus:
        return
    r = streamer(
        f"""Calcule le ROI d'automatisation pour :
Processus : {processus}
Temps actuel : {heures}h/semaine
Coût horaire : {taux}€/h

Calcule :
1. Coût annuel actuel (temps × taux × 52 semaines)
2. Coût d'automatisation Caelum (forfait parmi 500/1500/3000€ + maintenance mensuelle)
3. Économies année 1 et année 3
4. ROI en % et en mois de retour sur investissement
5. Argument de vente à utiliser face au client

Format tableau + conclusion en 1 phrase de pitch.""",
        f"ROI AUTOMATISATION — {processus[:40]}"
    )
    sauvegarder(f"roi_{processus[:20].replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AUTOMATISATION N8N — Caelum Partners")
    print("  Blueprints n8n · Make · Zapier · Power Automate")
    print("═"*65)

    while True:
        print("\n  1. Analyser un processus client et proposer solution")
        print("  2. Blueprint : facturation automatique (PME belge)")
        print("  3. Blueprint : onboarding client Caelum")
        print("  4. Blueprint : prospection automatisée")
        print("  5. Calculer le ROI d'une automatisation")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            analyser_processus()
        elif choix == "2":
            blueprint_facturation()
        elif choix == "3":
            blueprint_onboarding()
        elif choix == "4":
            blueprint_prospection()
        elif choix == "5":
            calculer_roi()
        else:
            print("  Choix invalide.")
