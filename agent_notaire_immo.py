"""
AGENT NOTAIRE & IMMOBILIER BELGE — Automatisation documentaire pour notaires et agences immobilières
Usage : python agent_notaire_immo.py
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
Tu es un assistant IA spécialisé pour les notaires et agents immobiliers belges, développé par Caelum Partners (Bruxelles).
La Belgique compte environ 10 000 agences immobilières et plus de 1 500 études notariales, toutes noyées sous la paperasse administrative.
Tu maîtrises parfaitement le droit immobilier belge : la Loi Breyne pour les constructions neuves, le Code wallon du logement et le Code bruxellois du logement.
Tu connais les obligations bilingues FR/NL dans la Région de Bruxelles-Capitale et les exigences légales propres à chaque région.
Tu sais rédiger des annonces immobilières professionnelles conformes aux obligations légales : mention du PEB, informations urbanistiques, zone inondable, documents de copropriété.
Tu maîtrises les honoraires notariaux (1 à 2 % de la valeur du bien) et les commissions des agences immobilières (3 % du prix de vente).
Tu génères des correspondances clients professionnelles avec les références légales exactes du droit belge en vigueur.
Tu produis des résumés d'actes notariaux clairs avec checklists de documents manquants et timelines réalistes.
Tu rédiges des contrats de bail conformes à la législation belge : bail 3-6-9 ans, clause d'indexation, état des lieux, garantie locative.
Tu comprends les enjeux de la copropriété belge : syndic, assemblée générale, fonds de réserve, quote-part dans les charges.
Tu connais les spécificités fiscales de l'immobilier belge : droits d'enregistrement (12,5 % en Wallonie et Bruxelles, 3 % en Flandre), TVA 21 % sur neuf.
Tu aides Caelum Partners à démontrer que l'automatisation IA permet d'économiser 100+ heures/mois dans une étude notariale.
Le package Caelum à 1 500 € fait économiser plus de 10 000 €/an en temps administratif aux professionnels de l'immobilier.
Tu rédiges toujours en français professionnel, avec les équivalents néerlandais lorsque cela est demandé explicitement.
Tu inclus systématiquement toutes les mentions légales obligatoires dans chaque document immobilier produit.
Tu es factuel, précis et orienté vers la création de valeur commerciale pour Caelum Partners et ses clients.
Tes documents sont directement utilisables par des professionnels de l'immobilier belge sans retouche majeure.
Tu ne fournis jamais de conseil juridique personnalisé : chaque document doit être validé par un professionnel qualifié avant usage.
"""

def sanitize(text: str, max_chars: int = 3000) -> str:
    if not isinstance(text, str):
        text = str(text)
    return text.strip()[:max_chars]

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
    os.makedirs("fichiers/notaire_immo", exist_ok=True)
    fichier = f"fichiers/notaire_immo/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_annonce_immobiliere():
    print("\n  — Générer une annonce immobilière FR + NL —")
    type_bien = sanitize(input("  Type de bien (maison / appartement / terrain / commerce) : "))
    surface = sanitize(input("  Surface (m²) : "))
    chambres = sanitize(input("  Nombre de chambres : "))
    localisation = sanitize(input("  Localisation (commune, quartier) : "))
    prix = sanitize(input("  Prix demandé (€) : "))
    caracteristiques = sanitize(input("  Caractéristiques principales (jardin, garage, PEB, année, etc.) : "))

    prompt = f"""Génère une annonce immobilière professionnelle complète pour la vente d'un bien en Belgique.

DONNÉES DU BIEN :
- Type : {type_bien}
- Surface : {surface} m²
- Chambres : {chambres}
- Localisation : {localisation}
- Prix : {prix} €
- Caractéristiques : {caracteristiques}

LIVRABLES ATTENDUS :

1. ANNONCE IMMOBILIÈRE EN FRANÇAIS (300-400 mots)
   - Titre accrocheur et vendeur
   - Description valorisante et professionnelle avec les points forts du bien
   - Mentions légales obligatoires : PEB, informations urbanistiques, zone inondable si pertinent
   - Prix, modalités de visite et coordonnées (fictives, à remplacer)
   - Appel à l'action clair

2. VERSIE IN HET NEDERLANDS (résumé 150 mots)
   - Titre en néerlandais accrocheur
   - Description synthétique et professionnelle
   - Mentions légales obligatoires en NL

3. POST LINKEDIN (150 mots)
   - Ton professionnel et engageant pour attirer acheteurs et investisseurs
   - Hashtags pertinents (#immobilierbelge #vastgoed #bruxelles #belgique etc.)

4. EMAIL AU VENDEUR/CLIENT
   - Communication professionnelle informant le client de la mise en ligne de son annonce
   - Prochaines étapes et conseils pour optimiser la vente

Respecte scrupuleusement toutes les obligations légales belges en matière d'annonces immobilières."""

    resultat = streamer(prompt, "ANNONCE IMMOBILIÈRE FR + NL")
    sauvegarder("annonce_immo", resultat)

def rediger_correspondance_client():
    print("\n  — Rédiger une correspondance client —")
    situation = sanitize(input("  Situation (ex: offre acceptée / acte planifié / document manquant / compromis signé) : "))
    nom_client = sanitize(input("  Nom du client (optionnel, laisser vide si inconnu) : "))
    details = sanitize(input("  Détails supplémentaires sur le dossier : "))

    client_ref = nom_client if nom_client else "Monsieur/Madame [Nom]"

    prompt = f"""Rédige une correspondance professionnelle pour un notaire ou agent immobilier belge.

SITUATION : {situation}
CLIENT : {client_ref}
DÉTAILS DU DOSSIER : {details}

LIVRABLES :

1. LETTRE OFFICIELLE
   - En-tête professionnel au format étude notariale ou agence immobilière belge
   - Corps de lettre clair, professionnel et bienveillant adapté à la situation
   - Références légales belges exactes si pertinentes (acte authentique, compromis de vente, délai de réflexion, etc.)
   - Prochaines étapes concrètes et actionables pour le client
   - Formule de politesse professionnelle adaptée

2. VERSION EMAIL (même contenu, format court et direct)
   - Objet de l'email percutant
   - Corps adapté à la communication électronique

3. RAPPEL DES POINTS LÉGAUX IMPORTANTS
   - Délais légaux applicables à cette situation
   - Documents requis par le client et par le professionnel
   - Références aux textes de loi belges pertinents (Code civil belge, lois régionales, etc.)

Style global : professionnel, rassurant et précis. Éviter tout jargon inutile pour le client."""

    resultat = streamer(prompt, "CORRESPONDANCE CLIENT NOTAIRE/IMMO")
    sauvegarder("correspondance_client", resultat)

def resumer_acte_notarial():
    print("\n  — Résumer un acte notarial —")
    description = sanitize(input("  Décris la transaction / l'acte (type, parties, bien, montant, particularités) : "))

    prompt = f"""Analyse et résume l'acte notarial ou la transaction immobilière belge suivante pour constituer une note interne de dossier.

DESCRIPTION DE LA TRANSACTION : {description}

LIVRABLES :

1. RÉSUMÉ EXÉCUTIF DU DOSSIER
   - Parties impliquées et leurs rôles respectifs (vendeur, acheteur, notaire instrumentant, etc.)
   - Objet précis de la transaction (bien immobilier, nature, localisation estimée)
   - Montants, prix, droits d'enregistrement estimés et conditions financières
   - Points juridiques clés à surveiller
   - Risques identifiés et points d'attention particuliers

2. CHECKLIST DES DOCUMENTS MANQUANTS / À OBTENIR
   □ Documents urbanistiques (permis, certificat d'urbanisme, destination cadastrale)
   □ Certificat PEB valide
   □ Documents de copropriété si applicable (PV AG, décompte charges, fonds de réserve)
   □ Documents identitaires des parties (CIN, composition de ménage)
   □ Documents financiers (offre de prêt, état hypothécaire)
   □ Autres pièces spécifiques à ce type de transaction

3. TIMELINE RECOMMANDÉE
   - Étapes chronologiques avec délais indicatifs selon le droit belge
   - Dates butoirs importantes (délai de réflexion, signature compromis, acte authentique)
   - Actions à entreprendre par chaque partie à chaque étape

4. POINTS D'ATTENTION LÉGAUX
   - Références aux textes applicables (Loi Breyne si VEFA, Code civil belge, lois régionales)
   - Clauses particulières à insérer ou à vérifier

Format : note interne professionnelle, directement classable dans le dossier."""

    resultat = streamer(prompt, "RÉSUMÉ ACTE NOTARIAL")
    sauvegarder("resume_acte", resultat)

def contrat_bail_standard():
    print("\n  — Contrat de bail standard belge —")
    type_bail = sanitize(input("  Type de bail (habitation / commercial / bail de courte durée / étudiant) : "))
    region = sanitize(input("  Région (Bruxelles / Wallonie / Flandre) : "))

    prompt = f"""Génère un modèle complet de contrat de bail belge avec toutes les clauses légalement obligatoires.

TYPE DE BAIL : {type_bail}
RÉGION : {region}

LIVRABLES :

1. MODÈLE DE CONTRAT DE BAIL COMPLET
   - Article 1 : Identification complète des parties (bailleur et preneur)
   - Article 2 : Description précise du bien loué et de ses annexes
   - Article 3 : Durée du bail (régime 3-6-9 ans pour bail d'habitation ou durée spécifique)
   - Article 4 : Loyer de base, date et modalités de paiement
   - Article 5 : CLAUSE D'INDEXATION (formule légale belge exacte : loyer indexé = loyer base × index santé nouveau / index santé de base)
   - Article 6 : Garantie locative (2 mois max en Wallonie et Bruxelles, 3 mois en Flandre)
   - Article 7 : État des lieux d'entrée contradictoire et état des lieux de sortie
   - Article 8 : Charges et provisions pour charges (détail des charges récupérables)
   - Article 9 : Entretien courant (preneur) et grosses réparations (bailleur)
   - Article 10 : Sous-location (interdite sauf autorisation écrite du bailleur)
   - Article 11 : Assurance incendie obligatoire du preneur
   - Article 12 : Droit de visite du bailleur avec préavis raisonnable
   - Article 13 : Résiliation anticipée et préavis légaux applicables
   - Article 14 : Enregistrement du bail (obligation légale, délai 2 mois, gratuit pour habitation)
   - Article 15 : Élection de domicile et juridiction compétente (Justice de Paix)

2. CHECKLIST PRÉ-SIGNATURE
   □ Documents identitaires des deux parties
   □ Preuve de revenus du locataire (3 dernières fiches de salaire)
   □ Attestation d'assurance incendie locataire
   □ Constitution de la garantie locative
   □ Inventaire et état des lieux d'entrée signés
   □ Remise des clés et compteurs relevés

3. NOTE LÉGISLATIVE RÉGIONALE
   - Spécificités légales applicables en {region}
   - Références aux décrets et ordonnances régionaux en vigueur

AVERTISSEMENT À INCLURE : "Ce modèle est fourni à titre indicatif par Caelum Partners et doit être validé par un notaire ou avocat qualifié avant tout usage contractuel." """

    resultat = streamer(prompt, "CONTRAT DE BAIL STANDARD BELGE")
    sauvegarder("contrat_bail", resultat)

def kit_prospection_agence():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les agences immobilières et études notariales belges.

CONTEXTE CAELUM PARTNERS :
- Cabinet d'automatisation IA basé à Bruxelles, fondé par Chaima Mhadbi
- Services : 500 € (starter), 1 500 € (standard), 3 000 € (premium)
- Cible : agences immobilières (~10 000 en Belgique) et études notariales (~1 500)
- Offre phare pour ce secteur : package 1 500 € standard

LIVRABLES :

1. EMAIL DE PROSPECTION (objet accrocheur + corps complet)
   - Objet : percutant, taux d'ouverture maximisé
   - Accroche personnalisée pour directeur d'agence immobilière ou notaire associé
   - Argument ROI chiffré : une agence immobilière gagne 80-100h/mois sur annonces et correspondances
   - Proposition de valeur : package 1 500 € = économie de 10 000 €+/an en temps administratif
   - Preuve sociale ou exemple concret de gain de temps
   - Call to action : démo gratuite de 30 minutes sans engagement
   - Ton professionnel, direct et non agressif

2. MESSAGE LINKEDIN (300 caractères max)
   - Accroche ultra-percutante sur la douleur administrative
   - Proposition de valeur en 2 phrases maximum
   - Call to action clair

3. CALCUL ROI DÉTAILLÉ POUR CE SECTEUR
   Avant IA :
   - Rédaction annonce FR+NL : 2h par bien
   - Correspondances clients : 1h/jour
   - Résumés et checklists dossiers : 2h/semaine
   Après IA Caelum :
   - Rédaction annonce FR+NL : 15 min
   - Correspondances : 10 min/email
   - Résumés dossiers : 20 min
   → Calcul économie mensuelle en heures et en euros (coût horaire 50-80 €)
   → ROI du package 1 500 € sur 12 mois

4. RÉPONSES AUX 3 OBJECTIONS PRINCIPALES
   - "L'IA ne peut pas capturer l'expertise terrain d'un agent immobilier"
   - "Nous avons déjà des modèles de documents internes"
   - "1 500 € c'est un budget que nous n'avons pas prévu"

5. SCRIPT D'APPEL DE DÉCOUVERTE (2 minutes, format dialogué)
   - Introduction et crédibilisation rapide de Caelum Partners
   - 3 questions de qualification du prospect
   - Transition naturelle vers la démonstration produit"""

    resultat = streamer(prompt, "KIT PROSPECTION AGENCES IMMOBILIÈRES & NOTAIRES")
    sauvegarder("kit_prospection_immo", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT NOTAIRE & IMMOBILIER BELGE")
    print("  Automatisation documentaire — Caelum Partners")
    print("═"*65)
    while True:
        print("\n  [menu]")
        print("  1. Générer une annonce immobilière FR+NL")
        print("  2. Rédiger correspondance client")
        print("  3. Résumer un acte notarial")
        print("  4. Contrat bail standard belge")
        print("  5. Kit prospection agences")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_annonce_immobiliere()
        elif choix == "2":
            rediger_correspondance_client()
        elif choix == "3":
            resumer_acte_notarial()
        elif choix == "4":
            contrat_bail_standard()
        elif choix == "5":
            kit_prospection_agence()
        else:
            print("  Choix invalide.")
