"""
AGENT COMPTABLE BELGE — Expert-comptable spécialisé PME et indépendants belges
TVA · BCE · INASTI · IPP · ISOC · Déclarations · Optimisation fiscale légale

Usage : python agent_comptable_belge.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """Tu es un expert-comptable certifié belge avec 20 ans d'expérience.
Tu travailles pour Caelum Partners — Chaima Mhadbi, Bruxelles.

SITUATION ACTUELLE DE CHAIMA :
- Présidente d'une ASBL (numéro TVA ASBL existant — NE PAS utiliser pour activité commerciale)
- Veut lancer Caelum Partners comme activité commerciale d'agents IA
- Services : Site web 500€ / Automation IA 1500€ / Pack 3000€
- Localisation : Bruxelles, Belgique
- Phase : démarrage, 0 clients encore

TES CONNAISSANCES EXPERTES :
- BCE (Banque-Carrefour des Entreprises) — inscription entreprise
- INASTI (Institut national d'assurances sociales) — cotisations sociales
- TVA belge : taux 21%, seuil franchise 25 000€/an (petite entreprise)
- IPP (Impôt des Personnes Physiques) — déclaration revenus indépendant
- ISOC (Impôt des Sociétés) — si SRL créée
- Déductions professionnelles autorisées (matériel, logiciels, formation, bureau domicile)
- Différence indépendant complémentaire vs principal
- Séparation stricte ASBL / activité commerciale (crucial pour Chaima)

RÈGLES D'OR QUE TU RESPECTES :
1. Toujours distinguer ce qui est LÉGAL vs ce qui est RISQUÉ vs ce qui est INTERDIT
2. Mentionner les délais réels (inscription BCE = 1-2 semaines, premier trimestre INASTI...)
3. Chiffrer les coûts réels (cotisations INASTI, frais guichet, comptable...)
4. Recommander un vrai comptable pour les actes officiels — tu prépares, tu ne signes pas

FORMAT DE RÉPONSE :
1. RÉSUMÉ — situation légale actuelle en 2 phrases
2. OPTIONS DISPONIBLES — avec avantages, inconvénients et coûts chiffrés
3. ÉTAPES CONCRÈTES — checklist avec délais réels
4. ATTENTION LÉGALE — ce qu'il ne faut absolument pas faire"""


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
    os.makedirs("fichiers/comptabilite", exist_ok=True)
    fichier = f"fichiers/comptabilite/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def inscription_independant():
    r = streamer(
        """Chaima veut s'inscrire comme indépendante pour Caelum Partners.
Elle est déjà présidente d'une ASBL.
Explique-lui EXACTEMENT comment faire :
- Quelle structure choisir (indépendant complémentaire ou principal ou SRL ?)
- Les étapes précises avec noms des organismes belges
- Les coûts réels en euros
- Les délais réels en jours
- Les documents à préparer
- Les erreurs à éviter absolument avec l'ASBL en parallèle""",
        "INSCRIPTION INDÉPENDANTE — Guide complet Belgique"
    )
    sauvegarder("inscription_independant", r)


def tva_et_franchise():
    r = streamer(
        """Explique à Chaima tout ce qu'elle doit savoir sur la TVA pour Caelum Partners :
- Le régime de franchise TVA (sous 25 000€/an) — avantages et inconvénients
- Quand s'inscrire à la TVA volontairement vs obligatoirement
- Comment facturer sans TVA au début
- Que mettre sur les factures (mentions obligatoires en Belgique)
- La différence TVA belge vs clients étrangers (France, Luxembourg, Canada)
- Le numéro de TVA de l'ASBL : peut-elle l'utiliser pour Caelum Partners ?""",
        "TVA BELGE — Tout ce que Caelum Partners doit savoir"
    )
    sauvegarder("tva_franchise", r)


def deductions_professionnelles():
    r = streamer(
        """Liste toutes les déductions professionnelles que Chaima peut faire en tant qu'indépendante IA belge :
- Matériel informatique (laptop, écrans, etc.)
- Abonnements logiciels (Gemini API, Claude, GitHub, Canva, etc.)
- Bureau à domicile (% du loyer/propriété)
- Téléphone et internet
- Formation et certifications
- Déplacements professionnels (Bruxelles et partout en Belgique)
- Marketing et publicité
- Comptable et conseils juridiques
- Assurances professionnelles
Pour chaque catégorie : % déductible légal + limite annuelle éventuelle + justificatif requis""",
        "DÉDUCTIONS PROFESSIONNELLES — Maximiser légalement"
    )
    sauvegarder("deductions_pro", r)


def plan_fiscal_annuel():
    r = streamer(
        """Crée un plan fiscal annuel pour Chaima — objectif : déclarer correctement ET minimiser l'impôt légalement.
Basé sur CA estimé : 0-30 000€ la première année.
Inclure :
- Calendrier des obligations fiscales (dates limites déclarations, paiements INASTI...)
- Provision mensuelle à mettre de côté pour les impôts (en %)
- Seuils importants à connaître (TVA, ISOC, IPP...)
- Structure optimale (indépendant vs SRL) selon CA cible
- Ce qu'un comptable coûte et si ça vaut la peine dès le début""",
        "PLAN FISCAL ANNUEL — Caelum Partners"
    )
    sauvegarder("plan_fiscal", r)


def facture_conforme():
    r = streamer(
        """Génère un exemple de facture conforme au droit belge pour Caelum Partners.
Service fictif : Site web premium pour un client belge.
Inclure TOUTES les mentions légales obligatoires :
- Informations vendeur (Chaima Mhadbi / Caelum Partners)
- Informations acheteur
- Numéro de facture
- Date d'émission et date d'échéance
- Description du service
- Prix HT / TVA (ou mention franchise TVA si applicable)
- Modes de paiement
- Conditions de paiement
- Mentions légales obligatoires Belgique
Donner ensuite le template réutilisable en texte.""",
        "FACTURE CONFORME — Template légal belge"
    )
    sauvegarder("template_facture", r)


def asbl_vs_commerciale():
    r = streamer(
        """Chaima est présidente d'une ASBL ET veut lancer Caelum Partners (activité commerciale).
Explique clairement :
1. Ce qu'une ASBL peut et ne peut PAS faire commercialement en Belgique
2. Les risques légaux de mélanger ASBL et activité commerciale
3. Comment séparer complètement les deux structures
4. Si l'ASBL peut devenir un outil pour Caelum Partners (partenariat, sous-traitance ?)
5. Les avantages et inconvénients de transformer l'ASBL en SRL
6. La recommandation concrète pour Chaima en 2025""",
        "ASBL vs ACTIVITÉ COMMERCIALE — Séparation légale"
    )
    sauvegarder("asbl_vs_commerciale", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT COMPTABLE BELGE — Expert TVA, BCE, INASTI, IPP")
    print("  Spécialisé : PME et indépendants Bruxelles")
    print("═"*65)

    while True:
        print("\n  1. S'inscrire comme indépendante — guide complet")
        print("  2. TVA belge et régime franchise — tout comprendre")
        print("  3. Déductions professionnelles — maximiser légalement")
        print("  4. Plan fiscal annuel — provisions et calendrier")
        print("  5. Générer une facture conforme au droit belge")
        print("  6. ASBL vs activité commerciale — séparer les deux")
        print("  7. Question libre à l'expert-comptable")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            inscription_independant()
        elif choix == "2":
            tva_et_franchise()
        elif choix == "3":
            deductions_professionnelles()
        elif choix == "4":
            plan_fiscal_annuel()
        elif choix == "5":
            facture_conforme()
        elif choix == "6":
            asbl_vs_commerciale()
        elif choix == "7":
            question = input("\n  Ta question → ").strip()
            if question:
                streamer(question, "QUESTION LIBRE — Expert-Comptable Belge")
        else:
            print("  Choix invalide.")
