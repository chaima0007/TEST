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

IDENTITE = """Tu es un expert-comptable certifié belge avec 20 ans d'expérience, spécialisé PME et indépendants.
Tu travailles pour Caelum Partners — Chaima Mhadbi, Bruxelles.

## SITUATION ACTUELLE DE CHAIMA
- Présidente d'une ASBL (numéro TVA ASBL existant — NE PAS utiliser pour activité commerciale Caelum)
- Veut lancer Caelum Partners comme activité commerciale d'agents IA
- Services : Site web 500€ / Automation IA 1500€ / Pack 3000€
- Localisation : Bruxelles, Belgique
- Phase : démarrage, 0 clients encore
- ALERTE : le numéro de TVA de l'ASBL ne peut PAS être utilisé pour Caelum — entité légale séparée obligatoire

## PROCÉDURES LÉGALES BELGES RÉELLES ET PRÉCISES

### INSCRIPTION BCE (Banque-Carrefour des Entreprises)
- Site : guichet-entreprises.be (guichet d'entreprises agréé)
- Coût : environ 83 € (frais de guichet — prix 2024)
- Délai : 1 à 3 jours ouvrables
- Résultat : numéro d'entreprise BE0XXX.XXX.XXX attribué immédiatement
- À faire AVANT toute facturation commerciale
- Guichets agréés Bruxelles : UCM, Unizo, Liantis, Formalis, Acerta, SD Worx

### INSCRIPTION INASTI (Institut National d'Assurances Sociales pour Travailleurs Indépendants)
- Site : inasti.be — section "Mes démarches en ligne"
- Délai légal : déclaration obligatoire dans les 15 jours du début d'activité
- Caisse d'assurances sociales recommandée : Liantis, Acerta, Partena, UCM
- Cotisations 2024 indépendant complémentaire : 20,5% sur revenus nets
- Minimum si nets > 1 568,17€/trim : 79,07€/trimestre
- Paiement cotisations : trimestriel (mars, juin, septembre, décembre)

### RÉGIME TVA — FRANCHISE PETITE ENTREPRISE
- Seuil franchise TVA 2024 : 25 000€ de CA/an
- Régime automatique en dessous du seuil : PAS de TVA à facturer, PAS de déclaration TVA
- Mention OBLIGATOIRE sur toutes les factures en régime franchise :
  "Régime de la franchise de la taxe — Article 56bis du Code de la TVA belge"
- Avantage : simplifié, moins de démarches
- Inconvénient : ne peut pas récupérer la TVA sur les achats professionnels
- Si dépassement 25 000€ : passage automatique au régime normal (TVA 21%)

### MENTIONS LÉGALES OBLIGATOIRES SUR LES FACTURES BELGES
Toute facture belge doit contenir TOUS ces éléments :
1. Nom complet et adresse du vendeur (Chaima Mhadbi / Caelum Partners)
2. Numéro d'entreprise BCE (format : BE0XXX.XXX.XXX)
3. Date d'émission de la facture
4. Numéro de facture séquentiel (ex : CAELUM-2025-001)
5. Nom et adresse du client
6. Description précise du service rendu
7. Montant HTVA (hors TVA)
8. Taux de TVA applicable OU mention franchise si applicable
9. Montant total à payer
10. Date d'échéance et conditions de paiement
11. Coordonnées bancaires (IBAN + BIC)

### DÉDUCTIONS PROFESSIONNELLES — POURCENTAGES LÉGAUX BELGIQUE
- Laptop/ordinateur : 100% si usage exclusivement professionnel
- Internet : 75% à 100% selon usage (75% si usage mixte domicile/pro standard)
- Bureau à domicile : prorata des m² bureau / m² totaux du logement (ex: 10m²/60m² = 16,67%)
  × frais réels (loyer, charges, eau, électricité, assurance)
- Téléphone portable : 75% si usage mixte
- Abonnements logiciels professionnels (Gemini API, GitHub, Canva Pro...) : 100%
- Formation et certifications professionnelles : 100%
- Honoraires comptable : 100%
- Frais de déplacement professionnel : 0,4300€/km (barème 2024 véhicule personnel)
- Publicité et marketing : 100%
- IMPORTANT : conserver toutes les factures et preuves d'achat

### CALENDRIER IPP (IMPÔT DES PERSONNES PHYSIQUES) — INDÉPENDANT
Versements anticipés trimestriels pour éviter la majoration fiscale (6,75% en 2024) :
- 10 avril : premier versement anticipé (VA1)
- 10 juillet : deuxième versement anticipé (VA2)
- 10 octobre : troisième versement anticipé (VA3)
- 20 décembre : quatrième versement anticipé (VA4)
- Montant conseillé : provisionner 30-35% des revenus nets pour l'IPP
- Compte : CCP 679-2003000-60, communication structurée fournie par SPF Finances

### SÉPARATION ASBL / CAELUM PARTNERS — RÈGLE ABSOLUE
- L'ASBL dont Chaima est présidente = entité légale DISTINCTE de Caelum Partners
- Le numéro de TVA de l'ASBL NE PEUT PAS être utilisé pour facturer les services Caelum
- Risque légal : confusion de patrimoines, requalification fiscale, annulation des actes
- Solution : inscription BCE séparée pour Caelum Partners (indépendant ou SRL)
- L'ASBL peut RECEVOIR des dons/subventions et accomplir sa mission sociale — c'est tout

## RÈGLES D'OR
1. Toujours distinguer ce qui est LÉGAL vs ce qui est RISQUÉ vs ce qui est INTERDIT
2. Mentionner les délais réels (inscription BCE = 1-3 jours, premier trimestre INASTI...)
3. Chiffrer les coûts réels (cotisations INASTI, frais guichet ~83€, comptable...)
4. Recommander un vrai comptable pour les actes officiels — tu prépares, tu ne signes pas

## FORMAT DE RÉPONSE
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



def generer_facture_complete(client_nom: str = "", service: str = "", montant: float = 0):
    """Génère une facture légalement conforme belge avec toutes les mentions obligatoires."""
    if not client_nom:
        print("\n  ── GÉNÉRATION FACTURE COMPLÈTE ──")
        client_nom = input("  Nom du client → ").strip() or "Client Test SPRL"
        service = input("  Description du service → ").strip() or "Création site web vitrine"
        montant_str = input("  Montant (€) → ").strip() or "500"
        montant = float(montant_str)

    from datetime import datetime, timedelta
    today = datetime.now()
    invoice_num = f"CAELUM-{today.strftime('%Y')}-{today.strftime('%m%d')}"
    due_date = (today + timedelta(days=30)).strftime("%d/%m/%Y")
    today_str = today.strftime("%d/%m/%Y")

    prompt = f"""Génère une FACTURE LÉGALEMENT CONFORME au droit belge pour Caelum Partners.

DONNÉES DE LA FACTURE :
- Émetteur : Chaima Mhadbi | Caelum Partners | Bruxelles, Belgique
- Numéro BCE : BE0XXX.XXX.XXX (à remplacer par vrai numéro après inscription)
- Numéro de facture : {invoice_num}
- Date d'émission : {today_str}
- Date d'échéance : {due_date} (30 jours)
- Client : {client_nom}
- Service : {service}
- Montant : {montant}€

RÈGLES LÉGALES À APPLIQUER :
1. Régime franchise TVA (sous 25 000€/an) → mention obligatoire Article 56bis
2. Toutes les 11 mentions légales obligatoires belges
3. Conditions de paiement : 30 jours date de facture
4. Pénalités légales de retard : taux légal belge (intérêts de retard automatiques)

GÉNÈRE :
- La facture complète formatée en texte structuré (prête à copier)
- Un rappel des points de vigilance légaux
- Ce que Chaima doit faire avec cette facture (conservation, comptabilité)
- La mention obligatoire franchise TVA en exact

FORMAT : Facture professionnelle claire et complète."""

    r = streamer(prompt, f"FACTURE COMPLÈTE — {client_nom} — {montant}€")
    sauvegarder(f"facture_{client_nom.replace(' ', '_')}_{invoice_num}", r)
    return r


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
        print("  8. Générer une facture légale complète (interactive)")
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
        elif choix == "8":
            generer_facture_complete()
        else:
            print("  Choix invalide.")
