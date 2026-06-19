"""
AGENT EXPORT & COMMERCE INTERNATIONAL BELGE — Propositions multilingues, documentation export, prospection internationale
Usage : python agent_export_bilingue.py
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

IDENTITE = """
Tu es un assistant IA spécialisé pour les entreprises belges actives dans le commerce international et l'export.
La Belgique est l'économie la plus exportatrice d'Europe rapportée à son PIB : les exportations représentent 85% du PIB belge.
Tu connais parfaitement les organismes de soutien à l'export belge : Awex (Agence wallonne à l'Exportation et aux Investissements étrangers), Flanders Investment & Trade, et Brussels Invest & Export.
Tu maîtrises la documentation export belge et européenne : certificat EUR1 pour l'origine préférentielle, Carnet ATA pour l'exportation temporaire, déclarations douanières HS codes, SOFINEX pour les garanties financières, lettres de crédit documentaire.
Tu comprends les Incoterms 2020 (EXW, FCA, FOB, CIF, DDP) et leur impact sur les contrats commerciaux belges.
Tu produis des communications commerciales professionnelles en français, anglais, néerlandais et allemand adaptées aux cultures cibles.
Tu connais les différences culturelles business essentielles : directness britannique/néerlandaise vs formalisme français/belge, hiérarchie allemande, pragmatisme américain.
Tu sais adapter les propositions belges aux marchés cibles : France, Pays-Bas, Allemagne, Luxembourg, Royaume-Uni, États-Unis.
Tu intègres les spécificités contractuelles : droit applicable (CISG pour les ventes internationales), devises, TVA intracommunautaire (numéro de TVA EU), régime MOSS.
Tu comprends les barrières à l'export pour les PME belges : la langue et la documentation administrative sont citées par 40% des PME comme principal frein.
Tu génères des pitchs commerciaux adaptés culturellement, des factures proforma, des listes de colisage, des descriptions techniques de produits pour douanes étrangères.
Tu connais les accords commerciaux UE signés (CETA avec Canada, EPA avec Japon, accord UE-Corée) et leur impact sur les exportateurs belges.
Tu aides les PME belges manufacturières et distributrices à développer 3 à 5 nouveaux marchés sans embaucher un export manager supplémentaire.
Un forfait Caelum Partners à 3 000€ remplace l'équivalent de 40 heures de travail de traduction et adaptation commerciale professionnelle.
Ton ton est international, professionnel, adapté à chaque culture cible, avec une précision technique irréprochable.
Tu rédiges toujours des documents prêts à envoyer, sans placeholders génériques, avec des contenus concrets et convaincants.
Tu signales systématiquement les risques douaniers, les erreurs de classification HS ou les clauses contractuelles à risque pour l'exportateur belge.
"""

def sanitize(texte: str) -> str:
    return texte.strip()[:3000]

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/export_bilingue", exist_ok=True)
    fichier = f"fichiers/export_bilingue/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def traduire_proposition_commerciale():
    print("\n  — Traduction et adaptation de proposition commerciale —")
    print("  Collez votre proposition commerciale en français (terminez par une ligne vide + ENTER) :")
    lignes = []
    while True:
        ligne = input()
        if ligne == "":
            break
        lignes.append(ligne)
    texte_fr = sanitize("\n".join(lignes))
    marche_cible = sanitize(input("  Marché cible principal (UK/USA / Pays-Bas / Allemagne / France) : "))
    secteur = sanitize(input("  Secteur d'activité et type de produit/service : "))

    prompt = f"""Traduis et adapte culturellement cette proposition commerciale belge pour le marché cible indiqué.

PROPOSITION ORIGINALE EN FRANÇAIS :
{texte_fr}

MARCHÉ CIBLE : {marche_cible}
SECTEUR : {secteur}

Génère DEUX versions adaptées :

VERSION ANGLAISE (UK/USA selon marché cible) :
- Traduction professionnelle avec terminologie sectorielle correcte
- Adaptation culturelle : si UK → ton plus formel et réservé ; si USA → ton plus direct, ROI-centré, "can-do"
- Adaptation des références (réglementations locales, exemples pertinents pour le marché)
- Conversion des unités si nécessaire (m² → sq ft pour USA)
- Mention de la conformité aux normes locales si applicable

VERSION NÉERLANDAISE (si marché Pays-Bas ou Belgique néerlandophone) :
- Traduction professionnelle en néerlandais d'affaires (pas trop flamand pour les Pays-Bas)
- Ton direct et pragmatique (culture néerlandaise : "doe maar gewoon")
- Adaptation des références de prix et conditions de paiement (préférence NL pour délais courts)

Pour chaque version :
- Maintien de la précision technique absolue
- Optimisation de l'accroche pour la culture cible
- Formules de politesse appropriées à chaque culture
- Note de l'adaptateur : points culturels importants à retenir

Qualité : niveau traducteur professionnel certifié, prêt à envoyer."""

    resultat = streamer(prompt, "PROPOSITION COMMERCIALE — ADAPTATION MULTILINGUE")
    sauvegarder("proposition_traduite", resultat)

def generer_documentation_export(produit: str = ""):
    print("\n  — Génération de documentation export —")
    if not produit:
        produit = sanitize(input("  Description du produit (nature, HS code si connu, valeur unitaire) : "))
    destination = sanitize(input("  Pays de destination : "))
    incoterm = sanitize(input("  Incoterm utilisé (EXW / FCA / FOB / CIF / DDP) : "))
    quantite = sanitize(input("  Quantité et conditionnement : "))
    valeur = sanitize(input("  Valeur totale de l'expédition (€) : "))

    prompt = f"""Génère un pack complet de documentation export pour une expédition belge.

EXPÉDITION :
- Produit : {produit}
- Destination : {destination}
- Incoterm : {incoterm}
- Quantité / Conditionnement : {quantite}
- Valeur totale : {valeur} €

Génère les documents suivants :

1. CHECKLIST DOCUMENTAIRE EXPORT
   - Documents obligatoires selon destination et type de produit
   - Certificats spéciaux nécessaires (CE, conformité, sanitaire, phytosanitaire)
   - Délais d'obtention estimés

2. FACTURE PROFORMA (draft complet)
   - En-tête exportateur belge fictif (TVA BE, BCE, EORI)
   - Données importateur destination
   - Description produit avec code HS (suggestion basée sur la description)
   - Incoterm {incoterm}, lieu de livraison, délai
   - Conditions de paiement recommandées pour ce marché
   - Mentions légales obligatoires

3. LISTE DE COLISAGE (Packing List)
   - Structure standard douanière
   - Dimensions / poids brut / poids net
   - Marquages obligatoires

4. TEXTE CERTIFICAT D'ORIGINE (EUR1 ou CO standard)
   - Déclaration de conformité origine préférentielle UE si applicable
   - Mentions légales

5. ALERTES DOUANIÈRES
   - Droits de douane approximatifs à destination
   - Restrictions / licences éventuelles pour ce type de produit
   - Numéro EORI obligatoire rappel

Format : professionnel, prêt à transmettre au transitaire et à l'importateur."""

    resultat = streamer(prompt, "DOCUMENTATION EXPORT COMPLÈTE")
    sauvegarder("documentation_export", resultat)

def adapter_pitch_marche_cible(marche: str = ""):
    print("\n  — Adaptation du pitch pour un marché cible —")
    offre_core = sanitize(input("  Décrivez votre offre principale (produit/service, avantages clés) : "))
    if not marche:
        marche = sanitize(input("  Marché cible (France / Pays-Bas / Allemagne / UK / USA / Luxembourg) : "))
    budget_cible = sanitize(input("  Budget / fourchette de prix cible : "))
    type_acheteur = sanitize(input("  Type d'acheteur visé (distributeur / acheteur direct / revendeur) : "))

    prompt = f"""Adapte ce pitch commercial belge pour le marché cible spécifié.

OFFRE CORE : {offre_core}
MARCHÉ CIBLE : {marche}
BUDGET / PRIX : {budget_cible}
TYPE D'ACHETEUR : {type_acheteur}

Génère une analyse + pitch adapté en 4 parties :

PARTIE 1 — ANALYSE CULTURELLE BUSINESS ({marche})
- Code de communication : direct vs indirect, formel vs informel
- Critères d'achat prioritaires dans ce marché (prix / qualité / relation / références / rapidité)
- Erreurs typiques des exportateurs belges sur ce marché
- Salutation et formules d'entrée en matière appropriées

PARTIE 2 — PITCH ADAPTÉ (dans la langue du marché cible si FR/NL/DE/EN)
- Accroche culturellement calibrée (max 2 phrases)
- Valeur ajoutée reformulée selon les priorités locales
- Références et preuves sociales adaptées au marché
- Appel à l'action adapté à la culture

PARTIE 3 — SUGGESTIONS PRICING LOCALES
- Adaptation de la structure tarifaire (ex: prix nets en Allemagne, remises en France)
- Conditions de paiement préférées localement
- Positionnement prix recommandé vs concurrence locale

PARTIE 4 — RÉFÉRENCES ET ARGUMENTS LOCAUX
- Types de certifications ou labels valorisés dans ce marché
- Arguments "made in Belgium" / "EU origin" à utiliser ou éviter
- Associations professionnelles locales à mentionner

Ton : expert en commerce international, pratique et immédiatement actionnable."""

    resultat = streamer(prompt, f"PITCH ADAPTÉ — MARCHÉ {marche.upper()}")
    sauvegarder(f"pitch_{marche.lower().replace(' ', '_')}", resultat)

def email_prospection_international(pays: str = ""):
    print("\n  — Email de prospection internationale —")
    produit_service = sanitize(input("  Produit / service proposé : "))
    if not pays:
        pays = sanitize(input("  Pays cible et langue souhaitée (ex: Allemagne / DE) : "))
    type_entreprise = sanitize(input("  Type d'entreprise cible (distributeur / fabricant / chaîne de retail / etc.) : "))
    avantage_cle = sanitize(input("  Avantage concurrentiel principal de votre offre : "))

    prompt = f"""Génère un email de prospection internationale professionnel pour une PME belge exportatrice.

PARAMÈTRES :
- Produit / Service : {produit_service}
- Pays cible : {pays}
- Type d'entreprise cible : {type_entreprise}
- Avantage concurrentiel : {avantage_cle}

Génère DEUX emails :

EMAIL 1 — DANS LA LANGUE CIBLE (adapté culturellement pour {pays})
- Objet : accrocheur, personnalisé, max 60 caractères
- Corps : 150-200 mots, structuré
- Ouverture culturellement appropriée
- Valeur ajoutée claire et différenciante
- Preuve crédibilité (origine belge, certifications, références EU)
- Call-to-action précis avec délai suggéré
- Signature professionnelle avec coordonnées complètes

EMAIL 2 — VERSION FRANÇAISE DE RÉFÉRENCE
- Traduction fidèle pour archivage et suivi interne

NOTES D'ENVOI :
- Meilleur jour/heure d'envoi pour ce pays
- Sujet de relance à J+7
- Points de personnalisation à adapter selon le destinataire
- Erreurs à éviter (cultural faux-pas spécifiques à ce pays)

Qualité : niveau directeur export senior, prêt à envoyer immédiatement."""

    resultat = streamer(prompt, f"EMAIL PROSPECTION INTERNATIONALE — {pays.upper()}")
    sauvegarder(f"email_prospection_{pays.lower().replace(' ', '_')}", resultat)

def kit_prospection_exportateurs():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les responsables export et CFO de PME belges exportatrices.

Le kit doit contenir :

1. EMAIL DE PROSPECTION CIBLÉ CFO/DIRECTEUR EXPORT (objet + corps, 250 mots max)
   - Accroche sur la douleur : "40% des PME belges ratent des marchés export faute de documentation multilingue"
   - Cas concret : PME wallonne perd contrat allemand faute de traduction technique professionnelle
   - Offre Caelum : forfait 3 000€ = équivalent 40h de traduction professionnelle
   - CTA : démo en direct "je traduis votre proposition commerciale en anglais ET néerlandais en 5 minutes"

2. MESSAGE LINKEDIN DIRECTEUR EXPORT (300 caractères, punch)
   - Ciblant : Export Manager / International Sales Director / CFO de PME belge manufacturière

3. CALCUL ROI EXPORTATEUR
   - Hypothèses : PME avec 2 traductions/mois, traducteur freelance 0,12€/mot, doc 2 000 mots = 240€/doc
   - 24 documents/an = 5 760€ en traductions
   - Caelum Partners 3 000€/an = économie de 2 760€ + gains délais (48h → 5 minutes)
   - Valeur additionnelle : adaptation culturelle = +15% taux de conversion estimé

4. SCRIPT DÉMO EN DIRECT (90 secondes)
   - "Donnez-moi votre dernière proposition commerciale FR"
   - → Génération EN + NL en direct
   - → Résultat : "Vous auriez payé 480€ et attendu 4 jours"

5. OBJECTIONS & RÉPONSES
   - "On a Google Translate" → "Voici la différence entre Google Translate et adaptation culturelle business"
   - "Notre traducteur est bon" → "ROI : 0,12€/mot vs 3 000€/an illimité"
   - "On n'exporte pas assez" → "Précisément — voici pourquoi"

Ton : senior, chiffré, Bruxelles. Signé Chaima Mhadbi — Caelum Partners."""

    resultat = streamer(prompt, "KIT PROSPECTION EXPORTATEURS BELGES")
    sauvegarder("kit_prospection_exportateurs", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT EXPORT & COMMERCE INTERNATIONAL BELGE")
    print("  Multilingual · Documentation · Adaptation culturelle")
    print("  Caelum Partners — Chaima Mhadbi, Bruxelles")
    print("═"*65)

    while True:
        print("\n  [MENU]")
        print("  1. Traduire une proposition commerciale (FR → EN + NL)")
        print("  2. Documentation export (proforma, packing list, EUR1)")
        print("  3. Adapter le pitch pour un marché cible")
        print("  4. Email de prospection internationale")
        print("  5. Kit prospection exportateurs belges")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            traduire_proposition_commerciale()
        elif choix == "2":
            generer_documentation_export()
        elif choix == "3":
            adapter_pitch_marche_cible()
        elif choix == "4":
            email_prospection_international()
        elif choix == "5":
            kit_prospection_exportateurs()
        else:
            print("  Choix invalide. Entrez 0 à 5.")
