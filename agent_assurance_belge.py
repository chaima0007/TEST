"""
AGENT COURTIER EN ASSURANCES BELGIQUE — Devoir de conseil, comparatifs, sinistres, prospection
Usage : python agent_assurance_belge.py
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
Tu es un assistant IA spécialisé pour les courtiers et agents en assurances belges, avec une maîtrise complète du cadre réglementaire FSMA.
La Belgique compte plus de 7 000 intermédiaires d'assurances enregistrés auprès de la FSMA (Financial Services and Markets Authority).
Tu connais les obligations légales fondamentales du courtier belge : l'obligation d'inscription FSMA (numéro d'agrément obligatoire), le devoir de conseil documenté par écrit avant toute souscription, et les exigences IDD (Insurance Distribution Directive — Directive (UE) 2016/97 transposée en droit belge).
Tu maîtrises les produits d'assurance spécifiques au marché belge : RC familiale (très répandue en Belgique — quasi universelle), assurance incendie (obligatoire pour les locataires depuis 2019 en Wallonie), RC auto (obligatoire par loi du 21 novembre 1989), assurance vie branches 21 (taux garanti) et 23 (fonds d'investissement).
Tu connais l'assurance groupe (pension complémentaire d'entreprise, LOI du 28 avril 2003 sur les pensions complémentaires) et les exigences du plan de pension sectoriel.
Tu intègres les documents obligatoires : DIP (Document d'Information Produit — IPID en anglais), fiche d'information standardisée, et le document de conseil formalisé.
Tu connais les assureurs principaux actifs en Belgique : KBC, AXA, Allianz Benelux, Ethias, AG Insurance (BNP Paribas Fortis), Belfius Insurance.
Tu maîtrises la Loi du 25 juin 1992 sur le contrat d'assurance terrestre et ses délais : résiliation à l'échéance annuelle (préavis de 3 mois), résiliation après sinistre, résiliation pour non-paiement de prime.
Tu sais calculer les primes indicatives et expliquer les franchises, les plafonds de garantie, les exclusions standard du marché belge.
Un courtier belge gère en moyenne 500 à 2 000 dossiers clients. La charge administrative représente 40% de son temps : devoir de conseil, correspondances sinistres, lettres de résiliation, renouvellements.
Le forfait Caelum Partners à 1 500€ permet d'économiser 20 heures par mois d'administration pure, avec un ROI très clair pour un cabinet de courtage.
Tu génères des documents conformes aux exigences FSMA, prêts à intégrer dans les dossiers clients et à archiver selon les obligations légales.
Ton ton est précis, juridiquement rigoureux, professionnel, et adapté aux relations client en assurance (empathie lors des sinistres, clarté sur les garanties).
Tu ne donnes jamais de conseil financier ou juridique définitif : tu génères des documents d'aide à la décision que le courtier valide et personnalise.
Tu mentionnes systématiquement les numéros d'articles de loi belge applicables et les délais légaux précis.
Tu distingues clairement les produits MiFID (assurance-vie branche 23) des produits non-MiFID et les obligations de conseil différenciées.
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
                system_instruction=IDENTITE, temperature=0.15, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/assurance_belge", exist_ok=True)
    fichier = f"fichiers/assurance_belge/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def rediger_conseil_assurance(situation: str = ""):
    print("\n  — Rédaction du devoir de conseil (document FSMA) —")
    profil_client = sanitize(input("  Profil client (âge, situation familiale, profession, revenus approximatifs) : "))
    besoins = sanitize(input("  Besoins exprimés par le client : "))
    couvertures_existantes = sanitize(input("  Couvertures d'assurance déjà en place : "))
    produits_recommandes = sanitize(input("  Produit(s) que vous souhaitez recommander : "))
    if not situation:
        situation = sanitize(input("  Contexte / situation déclenchante (achat maison, naissance enfant, création entreprise...) : "))

    prompt = f"""Génère un document de devoir de conseil conforme FSMA pour un courtier en assurances belge.

DOSSIER CLIENT :
- Profil : {profil_client}
- Besoins exprimés : {besoins}
- Couvertures existantes : {couvertures_existantes}
- Produit(s) recommandé(s) : {produits_recommandes}
- Situation déclenchante : {situation}

Le document doit respecter strictement les exigences IDD (Directive sur la Distribution d'Assurances — loi belge du 6 décembre 2018) et inclure :

1. EN-TÊTE OFFICIEL
   - Identification du courtier (nom, numéro FSMA fictif, numéro BCE, adresse)
   - Identification du client
   - Date et référence dossier

2. ANALYSE DES BESOINS CLIENT (section obligatoire IDD)
   - Situation personnelle et familiale
   - Objectifs et besoins déclarés par le client
   - Horizon temporel et appétit au risque (si produit financier branche 23)
   - Couvertures déjà détenues : lacunes identifiées

3. RECOMMANDATION ET JUSTIFICATION
   - Produit(s) recommandé(s) avec justification précise
   - Pourquoi ce(s) produit(s) correspond(ent) aux besoins identifiés
   - Alternatives considérées et raisons de non-recommandation
   - Exclusions importantes à signaler au client

4. INFORMATIONS SUR LE PRODUIT
   - Référence au Document d'Information Produit (DIP/IPID) remis
   - Garanties principales, franchises et plafonds indicatifs
   - Durée du contrat, modalités de résiliation (Loi 25 juin 1992)

5. DÉCLARATIONS ET SIGNATURES
   - Déclaration client : informations fournies exactes et complètes
   - Déclaration courtier : conseil fourni en toute indépendance
   - Lieu, date, signatures (courtier + client)

6. MENTIONS LÉGALES
   - Numéro FSMA du courtier
   - Procédure de réclamation (Ombudsman des assurances)
   - Loi applicable et juridiction compétente

Format : document officiel, sobre, prêt à archiver au dossier client. Niveau juridique élevé."""

    resultat = streamer(prompt, "DEVOIR DE CONSEIL — DOCUMENT FSMA")
    sauvegarder("devoir_de_conseil", resultat)

def comparatif_polices(type_assurance: str = ""):
    print("\n  — Comparatif de polices d'assurance —")
    if not type_assurance:
        type_assurance = sanitize(input("  Type d'assurance (RC familiale / incendie / auto / vie branche 21 / assurance groupe) : "))
    besoins_client = sanitize(input("  Besoins spécifiques du client : "))
    budget_mensuel = sanitize(input("  Budget mensuel ou annuel du client : "))
    profil_risque = sanitize(input("  Profil de risque particulier (propriétaire / locataire / famille / senior / jeune conducteur) : "))

    prompt = f"""Génère un comparatif structuré de polices d'assurance pour un courtier belge.

TYPE D'ASSURANCE : {type_assurance}
BESOINS CLIENT : {besoins_client}
BUDGET : {budget_mensuel}
PROFIL : {profil_risque}

Génère un tableau comparatif professionnel avec 3 à 4 options :

COLONNE PAR OPTION :
1. Nom de la formule (ex: Essentiel / Standard / Prestige / Sur mesure)
2. Assureur de référence sur le marché belge (KBC / AXA / AG Insurance / Ethias / Allianz)
3. Garanties principales incluses (liste à puces)
4. Exclusions importantes à signaler
5. Franchise standard (montant ou %)
6. Plafond de couverture
7. Prime indicative mensuelle / annuelle
8. Profil client idéal pour cette formule
9. Points forts / Points faibles
10. Note globale courtier : ⭐⭐⭐ à ⭐⭐⭐⭐⭐

SYNTHÈSE ET RECOMMANDATION :
- Formule recommandée pour ce profil client et pourquoi
- Mise en garde : exclusions critiques pour ce profil
- Documents à demander au client avant souscription
- Référence DIP/IPID disponible pour chaque option

TABLEAU EN FORMAT MARKDOWN lisible, prêt à présenter au client ou à intégrer dans le dossier conseil.

Mention obligatoire : "Ce comparatif est fourni à titre indicatif. Les primes définitives sont fournies par l'assureur après analyse du risque complet." """

    resultat = streamer(prompt, f"COMPARATIF POLICES — {type_assurance.upper()}")
    sauvegarder(f"comparatif_{type_assurance.lower().replace(' ', '_')}", resultat)

def lettre_resiliation_renouvellement():
    print("\n  — Lettre de résiliation ou renouvellement d'assurance —")
    print("  Type de courrier :")
    print("  a) Résiliation à l'échéance annuelle (client → assureur)")
    print("  b) Résiliation après sinistre (courtier pour client)")
    print("  c) Refus de renouvellement (assureur → client — lettre réponse courtier)")
    print("  d) Demande de renouvellement avec modification des garanties")
    type_courrier = input("  Choix (a/b/c/d) : ").strip().lower()
    police_details = sanitize(input("  Numéro de police / type de contrat / assureur : "))
    date_echeance = sanitize(input("  Date d'échéance du contrat : "))
    motif = sanitize(input("  Motif de la résiliation ou contexte du renouvellement : "))
    nom_client = sanitize(input("  Nom et adresse du preneur d'assurance : "))

    types_courrier = {
        "a": "résiliation à l'échéance annuelle (préavis 3 mois — Loi du 25 juin 1992, art. 30)",
        "b": "résiliation après sinistre (délai 30 jours après sinistre déclaré — art. 34 Loi 1992)",
        "c": "réponse au refus de renouvellement par l'assureur avec recherche alternative",
        "d": "demande de renouvellement avec avenant de modification des garanties"
    }
    contexte = types_courrier.get(type_courrier, motif)

    prompt = f"""Génère une lettre formelle d'assurance pour un courtier belge.

TYPE : {contexte}
POLICE : {police_details}
DATE D'ÉCHÉANCE : {date_echeance}
PRENEUR D'ASSURANCE : {nom_client}
MOTIF : {motif}

La lettre doit inclure :

1. EN-TÊTE (expéditeur courtier + destinataire assureur ou client selon le cas)
2. OBJET PRÉCIS avec numéro de police
3. CORPS DE LA LETTRE :
   - Rappel du contrat : référence, date de souscription, type de garantie
   - Motif clairement exposé
   - Référence légale précise (Loi du 25 juin 1992 sur le contrat d'assurance terrestre — article applicable)
   - Délai de préavis respecté ou demande de confirmation
   - Demande de confirmation écrite de prise en compte (accusé de réception)
4. CONSÉQUENCES ET PROCHAINES ÉTAPES :
   - Si résiliation : couverture maintenue jusqu'à la date d'échéance
   - Remboursement de prime prorata si applicable
   - Nouvelle couverture proposée (si le courtier a trouvé un nouvel assureur)
5. FORMULE DE POLITESSE PROFESSIONNELLE
6. SIGNATURE : courtier + cachet
7. MODE D'ENVOI RECOMMANDÉ : lettre recommandée avec accusé de réception (obligatoire pour résiliation)

Format : lettre officielle, ton formel et précis. Référence légale exacte pour chaque délai mentionné."""

    resultat = streamer(prompt, f"LETTRE ASSURANCE — {contexte.upper()[:50]}")
    sauvegarder("lettre_assurance", resultat)

def rapport_sinistre_client(sinistre: str = ""):
    print("\n  — Rapport de sinistre et communication client —")
    if not sinistre:
        sinistre = sanitize(input("  Décrivez le sinistre (type, date, circonstances, dommages) : "))
    police_ref = sanitize(input("  Référence police et type d'assurance : "))
    nom_client = sanitize(input("  Nom du client sinistré : "))
    assureur = sanitize(input("  Nom de l'assureur concerné : "))
    urgence = input("  Niveau d'urgence (1=normal / 2=urgent / 3=critique) : ").strip()

    prompt = f"""Génère un rapport de sinistre professionnel bipartite pour un courtier en assurances belge.

SINISTRE :
- Description : {sinistre}
- Police concernée : {police_ref}
- Client sinistré : {nom_client}
- Assureur : {assureur}
- Niveau d'urgence : {urgence}/3

Génère DEUX documents :

DOCUMENT 1 — RAPPORT DE SINISTRE POUR L'ASSUREUR (format officiel)
1. En-tête : courtier, assureur, référence police, date de déclaration
2. Identification du sinistré : nom, adresse, numéro de police
3. Description factuelle du sinistre :
   - Date, heure, lieu exact du sinistre
   - Circonstances détaillées
   - Nature et étendue des dommages (provisoire)
   - Tiers impliqués (noms, coordonnées, assureurs si applicables)
4. Mesures conservatoires prises (prévention aggravation)
5. Pièces jointes : liste des documents transmis (PV police, photos, devis, factures)
6. Demandes au gestionnaire sinistres : expertise requise, délai souhaité
7. Références légales : délai de déclaration respecté (en général 8 jours en Belgique)
8. Signature courtier avec numéro FSMA

DOCUMENT 2 — COMMUNICATION CLIENT (ton empathique et rassurant)
1. Accusé de réception de la déclaration du sinistre
2. Explication du processus en langage clair (4 étapes simples)
3. Délais indicatifs attendus
4. Ce que le client doit faire / ne pas faire (conserver preuves, ne pas faire de réparations avant expertise)
5. Coordonnées du gestionnaire sinistre désigné
6. Formule rassurante et professionnelle

Ton document 1 : technique, factuel, juridique. Document 2 : empathique, clair, rassurant."""

    resultat = streamer(prompt, "RAPPORT SINISTRE + COMMUNICATION CLIENT")
    sauvegarder("rapport_sinistre", resultat)

def kit_prospection_courtiers():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les cabinets de courtage en assurances belges.

Le kit doit contenir :

1. EMAIL DE PROSPECTION DIRIGÉ VERS DIRECTEUR DE CABINET (objet + corps, 250 mots max)
   - Accroche spécifique : "40% de votre temps sur l'administration — 60% pour vos clients. Et si on inversait ça ?"
   - Douleur réelle : devoir de conseil mal documenté = risque FSMA + perte de temps
   - Preuve : un dossier de conseil complet conforme IDD = 45 minutes manuellement / Caelum = 3 minutes
   - Offre : forfait 1 500€ Caelum Partners
   - CTA : "Je vous génère un devoir de conseil complet maintenant, en direct, gratuitement"

2. MESSAGE LINKEDIN DIRECTEUR CABINET (300 caractères, impactant)
   - Cible : Gérant cabinet / Directeur courtage / Compliance Officer assurances

3. SCRIPT DÉMONSTRATION EN DIRECT (2 minutes)
   - "Donnez-moi un profil client type — famille, propriétaire, 2 enfants"
   - Génération du devoir de conseil FSMA complet en direct
   - Impact immédiat : "Vous auriez passé 45 minutes sur ce document"
   - "Avec 500 clients actifs, c'est 375 heures par an. Juste sur les devoirs de conseil."

4. CALCUL ROI CABINET DE COURTAGE
   - Hypothèses : cabinet 1 000 clients, 2 nouvelles souscriptions/semaine
   - Temps devoir de conseil : 45 min x 2 x 52 = 78h/an
   - Lettres résiliation/renouvellement : 30 min x 20/mois x 12 = 120h/an
   - Rapports sinistres : 1h x 5/mois x 12 = 60h/an
   - TOTAL : 258h/an économisées
   - Valorisation à 50€/h (collaborateur) : 12 900€/an économisés
   - Forfait Caelum 1 500€ : ROI 760% — payback en 7 semaines

5. ARGUMENT CONFORMITÉ FSMA
   - Risque actuel : devoir de conseil mal documenté = amende FSMA (jusqu'à 2,5M€)
   - Caelum génère des documents déjà structurés selon IDD belge
   - "La conformité n'est plus une charge — c'est un bouton"

6. OBJECTIONS & RÉPONSES
   - "On a déjà un logiciel CRM" → "Caelum génère le contenu, votre CRM le stocke"
   - "Notre secrétaire fait ça" → ROI démontré + libérer la secrétaire pour les clients
   - "La FSMA n'a jamais contrôlé" → "Depuis IDD 2019, les contrôles ont augmenté de 40%"

Ton : rigoureux, chiffré, compliance-aware. Signé Chaima Mhadbi — Caelum Partners, Bruxelles."""

    resultat = streamer(prompt, "KIT PROSPECTION COURTIERS EN ASSURANCES")
    sauvegarder("kit_prospection_courtiers", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT COURTIER EN ASSURANCES BELGIQUE")
    print("  Conseil FSMA · Comparatifs · Sinistres · Prospection")
    print("  Caelum Partners — Chaima Mhadbi, Bruxelles")
    print("═"*65)

    while True:
        print("\n  [MENU]")
        print("  1. Rédiger un devoir de conseil (FSMA)")
        print("  2. Comparatif de polices")
        print("  3. Lettre résiliation / renouvellement")
        print("  4. Rapport de sinistre + communication client")
        print("  5. Kit prospection courtiers en assurances")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            rediger_conseil_assurance()
        elif choix == "2":
            comparatif_polices()
        elif choix == "3":
            lettre_resiliation_renouvellement()
        elif choix == "4":
            rapport_sinistre_client()
        elif choix == "5":
            kit_prospection_courtiers()
        else:
            print("  Choix invalide. Entrez 0 à 5.")
